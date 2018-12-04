# -*- coding: utf-8 -*-

import os
import math
from config import *
import codecs
import jieba
jieba.set_dictionary("./dict.txt")
jieba.initialize()
import jieba.posseg as pseg


def tokenization(filename):
    stopwords = codecs.open(STOP_WORDS, 'r', encoding='utf8').readlines()
    stopwords = [w.strip() for w in stopwords]
    stop_flag = ['x', 'c', 'u', 'd', 'p', 't', 'uj', 'm', 'f', 'r']
    result = []
    with open(filename, encoding="utf-8") as f:
        text = f.read()
        words = pseg.cut(text)
    for word, flag in words:
        if flag not in stop_flag and word not in stopwords:
            result.append(word)
    return result

# 统计关键词及个数
def CountKey(fileName):
    try:
        # 统计格式 格式<key:value> <属性:出现个数>
        table = {}
        corpus = tokenization(fileName)
        # print(len(corpus))

        for word in corpus:
            if word != '' and word in table:  # 如果存在次数加1
                num = table[word]
                table[word] = num + 1
            elif word != '':  # 否则初值为1
                table[word] = 1

        dic = sorted(table.items(), key=lambda x: x[1], reverse=True)
        return dic

    except Exception as e:
        print('Error:', e)
    finally:
        pass

''' ------------------------------------------------------- '''


# 统计关键词及个数 并计算相似度
def MergeKeys(dic1, dic2):
    # 合并关键词 采用三个数组实现
    arrayKey = []
    for i in range(len(dic1)):
        arrayKey.append(dic1[i][0])  # 向数组中添加元素
    for i in range(len(dic2)):
        if dic2[i][0] in arrayKey:
            pass
            # print('has_key', dic2[i][0])
        else:  # 合并
            arrayKey.append(dic2[i][0])

    # 计算词频 infobox可忽略TF-IDF
    arrayNum1 = [0] * len(arrayKey)
    arrayNum2 = [0] * len(arrayKey)

    # 赋值arrayNum1
    for i in range(len(dic1)):
        key = dic1[i][0]
        value = dic1[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum1[j] = value
                break
            else:
                j = j + 1

    # 赋值arrayNum2
    for i in range(len(dic2)):
        key = dic2[i][0]
        value = dic2[i][1]
        j = 0
        while j < len(arrayKey):
            if key == arrayKey[j]:
                arrayNum2[j] = value
                break
            else:
                j = j + 1

    # print(arrayNum1)
    # print(arrayNum2)
    # print(len(arrayNum1), len(arrayNum2), len(arrayKey))

    # 计算两个向量的点积
    x = 0
    i = 0
    while i < len(arrayKey):
        x = x + arrayNum1[i] * arrayNum2[i]
        i = i + 1
    # print(x)

    # 计算两个向量的模
    i = 0
    sq1 = 0
    while i < len(arrayKey):
        sq1 = sq1 + arrayNum1[i] * arrayNum1[i]  # pow(a,2)
        i = i + 1
    # print(sq1)

    i = 0
    sq2 = 0
    while i < len(arrayKey):
        sq2 = sq2 + arrayNum2[i] * arrayNum2[i]
        i = i + 1
    # print(sq2)

    result = float(x) / (math.sqrt(sq1) * math.sqrt(sq2))
    return result

''' ------------------------------------------------------- 
    基本步骤：
        1.分别统计两个文档的关键词
        2.两篇文章的关键词合并成一个集合,相同的合并,不同的添加
        3.计算每篇文章对于这个集合的词的词频 TF-IDF算法计算权重
        4.生成两篇文章各自的词频向量
        5.计算两个向量的余弦相似度,值越大表示越相似                             
    ------------------------------------------------------- '''


# 主函数
def main():

    data_path = os.listdir(os.getcwd() + '/{}/'.format(SOURCE_DIR_NAME))[0]
    data_file = os.getcwd() + '/{}/{}'.format(SOURCE_DIR_NAME, data_path)
    target_folder = os.listdir(os.getcwd() + '/{}/'.format(TARGET_DIR_NAME))
    print('Start to read source file')
    source_dic = CountKey(data_file)
    print('Source file key calculation completed.\n')
    similarities_result = []
    for filename in target_folder:
        suffix = os.path.splitext(filename)[-1]
        if suffix == '.txt':
            print('Start to read target file: ' + filename)
            target_file = os.getcwd() + '/{}/{}'.format(TARGET_DIR_NAME, filename)
            target_dic = CountKey(target_file)
            print('target file: ' + filename + ' key calculation completed')
            # 合并两篇文章的关键词及相似度计算
            print('Start to compare similarity for ' + filename)
            result = MergeKeys(source_dic, target_dic)
            print(filename + ' similarity value is: ' + str(result) + '\n')
            similarities_result.append([filename, result])

    print(similarities_result)

    sim_file = open(RESULT_FILE, 'w')
    for item in similarities_result:
        sim_file.write(str(item[1]) + '\t'*5 + item[0] + '\n')
    sim_file.close()
    

    print('Similarity comparision completed. Please find the details in result.txt.\n')

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
    input("Press Enter to continue...")
