# websocket

> _**WebSocket是HTML5开始提供的一种在单个 TCP 连接上进行全双工通讯的协议**_

## WebSocket是基于HTTP的功能追加协议

在WebSocket API中，浏览器和服务器只需要做一个握手的动作，然后，浏览器和服务器之间就形成了一条快速通道。两者之间就直接可以数据互相传送。

浏览器通过 JavaScript 向服务器发出建立 WebSocket 连接的请求，连接建立以后，客户端和服务器端就可以通过 TCP 连接直接交换数据。

当你获取 Web Socket 连接后，你可以通过 send\(\) 方法来向服务器发送数据，并通过 onmessage 事件来接收服务器返回的数据。

浏览器通过 JavaScript 向服务器发出建立 WebSocket 连接的请求，连接建立以后，客户端和服务器端就可以通过 TCP 连接直接交换数据。因为 WebSocket 连接本质上就是一个 TCP 连接，所以在数据传输的稳定性和数据传输量的大小方面，和轮询以及 Comet 技术比较，具有很大的性能优势。

首先，Websocket是一个持久化的协议，相对于HTTP这种非持久的协议来说。

* HTTP的生命周期通过Request来界定，也就是一个Request 一个Response，那么在HTTP1.0中，这次HTTP请求就结束了。

  在HTTP1.1中进行了改进，使得有一个keep-alive，也就是说，在一个HTTP连接中，可以发送多个Request，接收多个Response。但是请记住 Request = Response ， 在HTTP中永远是这样，也就是说一个request只能有一个response。而且这个response也是被动的，不能主动发起。

* ajax轮询 ，ajax轮询 的原理非常简单，让浏览器隔个几秒就发送一次请求，询问服务器是否有新信息。
* long poll 其实原理跟 ajax轮询 差不多，都是采用轮询的方式，不过采取的是阻塞模型，也就是说，客户端发起连接后，如果没消息，就一直不返回Response给客户端。直到有消息才返回，返回完之后，客户端再次建立连接，周而复始

从上面可以看出其实这两种方式，都是在不断地建立HTTP连接，然后等待服务端处理，可以体现HTTP协议的另外一个特点，被动性。

![Ajax](http://upload-images.jianshu.io/upload_images/7662633-3fe35ff5434a3165.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

!\[Sequence diagram\]\([http://upload-images.jianshu.io/upload\_images/7662633-ffd83fd06a78fb65.png?imageMogr2/auto-orient/strip\|imageView2/2/w/1240](http://upload-images.jianshu.io/upload_images/7662633-ffd83fd06a78fb65.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

## WebSocket 规范

WebSocket 协议本质上是一个基于 TCP 的协议。为了建立一个 WebSocket 连接，客户端浏览器首先要向服务器发起一个 HTTP 请求，这个请求和通常的 HTTP 请求不同，包含了一些附加头信息，其中附加头信息”Upgrade: WebSocket”表明这是一个申请协议升级的 HTTP 请求，服务器端解析这些附加的头信息然后产生应答信息返回给客户端，客户端和服务器端的 WebSocket 连接就建立起来了，双方就可以通过这个连接通道自由的传递信息，并且这个连接会持续存在直到客户端或者服务器端的某一方主动的关闭连接。 一个典型的 WebSocket 发起请求和得到响应的例子看起来如下：

清单 1. WebSocket 握手协议

```text
客户端到服务端： 
GET /demo HTTP/1.1 
Host: example.com 
Connection: Upgrade 
Sec-WebSocket-Key2: 12998 5 Y3 1 .P00 
Upgrade: WebSocket 
Sec-WebSocket-Key1: 4@1 46546xW%0l 1 5 
Origin: http://example.com 
[8-byte security key] 

服务端到客户端：
HTTP/1.1 101 WebSocket Protocol Handshake 
Upgrade: WebSocket 
Connection: Upgrade 
WebSocket-Origin: http://example.com 
WebSocket-Location: ws://example.com/demo 
[16-byte hash response]
```

服务端收到报文后返回的数据格式类似：

```text
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: K7DJLdLooIwIG/MOpvWFB3y3FE8=
```

* 相比于正常的http请求多了 Upgrade和connection:grade
* 需要所有的浏览器升级以支持新的HTTP协议.
* Sec-WebSocket-Accept的值是服务端采用与客户端一致的密钥计算出来后返回客户端的
* Switching Protocols表示服务端接受WebSocket协议的客户端连接，经过这样的请求-响应处理后，两端的WebSocket连接握手成功, 后续就可以进行TCP通讯了。

WebSocket模式客户端与服务器请求响应模式如下图： ![websocket](http://upload-images.jianshu.io/upload_images/7662633-154d3f211e2f40b2.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

这些请求和通常的 HTTP 请求很相似，但是其中有些内容是和 WebSocket 协议密切相关的。我们需要简单介绍一下这些请求和应答信息，”Upgrade:WebSocket”表示这是一个特殊的 HTTP 请求，请求的目的就是要将客户端和服务器端的通讯协议从 HTTP 协议升级到 WebSocket 协议。从客户端到服务器端请求的信息里包含有”Sec-WebSocket-Key1”、“Sec-WebSocket-Key2”和”\[8-byte securitykey\]”这样的头信息。这是客户端浏览器需要向服务器端提供的握手信息，服务器端解析这些头信息，并在握手的过程中依据这些信息生成一个 16 位的安全密钥并返回给客户端，以表明服务器端获取了客户端的请求，同意创建 WebSocket 连接。一旦连接建立，客户端和服务器端就可以通过这个通道双向传输数据了。

相对于传统HTTP每次请求-应答都需要客户端与服务端建立连接的模式，WebSocket是类似Socket的TCP长连接通讯模式。一旦WebSocket连接建立后，后续数据都以帧序列的形式传输。在客户端断开WebSocket连接或Server端中断连接前，不需要客户端和服务端重新发起连接请求。在海量并发及客户端与服务器交互负载流量大的情况下，极大的节省了网络带宽资源的消耗，有明显的性能优势，且客户端发送和接受消息是在同一个持久连接上发起，实时性优势明显。

相比HTTP长连接，WebSocket有以下特点：

* 是真正的全双工方式，建立连接后客户端与服务器端是完全平等的，可以互相主动请求。而HTTP长连接基于HTTP，是传统的客户端对服务器发起请求的模式。
* HTTP长连接中，每次数据交换除了真正的数据部分外，服务器和客户端还要大量交换HTTP header，信息交换效率很低。
* Websocket协议通过第一个request建立了TCP连接之后，之后交换的数据都不需要发送 HTTP header就能交换数据，这显然和原有的HTTP协议有区别所以它需要对服务器和客户端都进行升级才能实现（主流浏览器都已支持HTML5）。此外还有 multiplexing、不同的URL可以复用同一个WebSocket连接等功能。这些都是HTTP长连接不能做到的。

