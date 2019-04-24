# https://segmentfault.com/a/1190000010009295

import sys
import re
import unicodedata
import pickle
import warnings
import itertools
import functools
from collections import namedtuple
import asyncio

RE_WORD = re.compile('\w+')
RE_UNICODE_NAME = re.compile('^[A-Z0-9 -]+$')
RE_CODEPOINT = re.compile('U\+[0-9A-F]{4, 6}')

INDEX_NAME = 'charfinder_index.pickle'
MINIMUM_SAVE_LEN = 10000
CJK_UNI_PREFIX = 'CJK UNIFIED IDEOGRAPH'
CJK_CMP_PREFIX = 'CJK COMPATIBILITY IDEOGRAPH'

CRLF = b'\r\n'
PROMPT = b'?> '

sample_chars = [
    '$',  # DOLLAR SIGN
    'A',  # LATIN CAPITAL LETTER A
    'a',  # LATIN SMALL LETTER A
    '\u20a0',  # EURO-CURRENCY SIGN
    '\u20ac',  # EURO SIGN
]

CharDescription = namedtuple('CharDescription', 'code_str char name')

QueryResult = namedtuple('QueryResult', 'count items')


def tokenize(text):
    '''
    :param text:
    :return: return iterable of uppercased words
    '''
    for match in RE_WORD.finditer(text):
        yield match.group().upper()


def query_type(text):
    text_upper = text.upper()
    if 'U+' in text_upper:
        return 'CODEPOINT'
    elif RE_UNICODE_NAME.match(text_upper):
        return 'NAME'
    else:
        return 'CHARACTERS'


class UnicodeNameIndex:
    # unicode name 索引类
    def __init__(self, chars=None):
        self.load(chars)

    def load(self, chars=None):
        # 加载 unicode name
        self.index = None
        if chars is None:
            try:
                with open(INDEX_NAME, 'rb') as fp:
                    self.index = pickle.load(fp)
            except OSError:
                pass
        if self.index is None:
            self.build_index(chars)
        if len(self.index) > MINIMUM_SAVE_LEN:
            try:
                self.save()
            except OSError as exc:
                warnings.warn('Could not save {!r}: {}'
                              .format(INDEX_NAME, exc))

    def save(self):
        with open(INDEX_NAME, 'wb') as fp:
            pickle.dump(self.index, fp)

    def build_index(self, chars=None):
        if chars is None:
            chars = (chr(i) for i in range(32, sys.maxunicode))
        index = {}
        for char in chars:
            try:
                name = unicodedata.name(char)
            except ValueError:
                continue
            if name.startswith(CJK_UNI_PREFIX):
                name = CJK_UNI_PREFIX
            elif name.startswith(CJK_CMP_PREFIX):
                name = CJK_CMP_PREFIX

            for word in tokenize(name):
                index.setdefault(word, set()).add(char)

        self.index = index

    def word_rank(self, top=None):
        # (len(self.index[key], key) 是一个生成器，需要用list 转成列表，要不然下边排序会报错
        res = [list((len(self.index[key], key)) for key in self.index)]
        res.sort(key=lambda  item: (-item[0], item[1]))
        if top is not None:
            res = res[:top]
        return res

    def word_report(self, top=None):
        for postings, key in self.word_rank(top):
            print('{:5} {}'.format(postings, key))

    def find_chars(self, query, start=0, stop=None):
        stop = sys.maxsize if stop is None else stop
        result_sets = []
        for word in tokenize(query):
            # tokenize 是query 的生成器 a b 会是 ['a', 'b'] 的生成器
            chars = self.index.get(word)
            if chars is None:
                result_sets = []
                break
            result_sets.append(chars)

        if not result_sets:
            return QueryResult(0, ())

        result = functools.reduce(set.intersection, result_sets)
        result = sorted(result)  # must sort to support start, stop
        result_iter = itertools.islice(result, start, stop)
        return QueryResult(len(result),
                           (char for char in result_iter))

    def describe(self, char):
        code_str = 'U+{:04X}'.format(ord(char))
        name = unicodedata.name(char)
        return CharDescription(code_str, char, name)

    def find_descriptions(self, query, start=0, stop=None):
        for char in self.find_chars(query, start, stop).items:
            yield self.describe(char)

    def get_descriptions(self, chars):
        for char in chars:
            yield self.describe(char)

    def describe_str(self, char):
        return '{:7}\t{}\t{}'.format(*self.describe(char))

    def find_description_strs(self, query, start=0, stop=None):
        for char in self.find_chars(query, start, stop).items:
            yield self.describe_str(char)

    @staticmethod  # not an instance method due to concurrency
    def status(query, counter):
        if counter == 0:
            msg = 'No match'
        elif counter == 1:
            msg = '1 match'
        else:
            msg = '{} matches'.format(counter)
        return '{} for {!r}'.format(msg, query)

# 实例化UnicodeNameIndex 类，它会使用charfinder_index.pickle 文件
index = UnicodeNameIndex()

async def handle_queries(reader, writer):
    # 这个协程要传给asyncio.start_server 函数，接收的两个参数是asyncio.StreamReader 对象和 asyncio.StreamWriter 对象
    while True:  # 这个循环处理会话，直到从客户端收到控制字符后退出
        writer.write(PROMPT)  # can't await!  # 这个方法不是协程，只是普通函数；这一行发送 ?> 提示符
        await writer.drain()  # must await!  # 这个方法刷新writer 缓冲；因为它是协程，所以要用 await
        data = await reader.readline()  # 这个方法也是协程，返回一个bytes对象，也要用await
        try:
            query = data.decode().strip()
        except UnicodeDecodeError:
            # Telenet 客户端发送控制字符时，可能会抛出UnicodeDecodeError异常
            # 我们这里默认发送空字符
            query = '\x00'
        client = writer.get_extra_info('peername')  # 返回套接字连接的远程地址
        print('Received from {}: {!r}'.format(client, query))  # 在控制台打印查询记录
        if query:
            if ord(query[:1]) < 32:  # 如果收到控制字符或者空字符，退出循环
                break
            # 返回一个生成器，产出包含Unicode 码位、真正的字符和字符名称的字符串
            lines = list(index.find_description_strs(query))
            if lines:
                # 使用默认的UTF-8 编码把lines    转换成bytes 对象，并在每一行末添加回车符合换行符
                # 参数列表是一个生成器
                writer.writelines(line.encode() + CRLF for line in lines)
            writer.write(index.status(query, len(lines)).encode() + CRLF) # 输出状态

            await writer.drain()  # 刷新输出缓冲
            print('Sent {} results'.format(len(lines)))  # 在服务器控制台记录响应

    print('Close the client socket')  # 在控制台记录会话结束
    writer.close()  # 关闭StreamWriter流



def main(address='127.0.0.1', port=2323):  # 添加默认地址和端口，所以调用默认可以不加参数
    port = int(port)
    loop = asyncio.get_event_loop()
    # asyncio.start_server 协程运行结束后，
    # 返回的协程对象返回一个asyncio.Server 实例，即一个TCP套接字服务器
    server_coro = asyncio.start_server(handle_queries, address, port,
                                loop=loop)
    server = loop.run_until_complete(server_coro) # 驱动server_coro 协程，启动服务器

    host = server.sockets[0].getsockname()  # 获得这个服务器的第一个套接字的地址和端口
    print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # 在控制台中显示地址和端口
    try:
        loop.run_forever()  # 运行事件循环 main 函数在这里阻塞，直到服务器的控制台中按CTRL-C 键
    except KeyboardInterrupt:  # CTRL+C pressed
        pass

    print('Server shutting down.')
    server.close()
    # server.wait_closed返回一个 future
    # 调用loop.run_until_complete 方法，运行 future
    loop.run_until_complete(server.wait_closed())
    loop.close()  # 终止事件循环


if __name__ == '__main__':
    main(*sys.argv[1:])