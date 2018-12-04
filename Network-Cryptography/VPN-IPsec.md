###VPN

Virtual Private Network（虚拟专用网络），被定义为通过一个公用网络（通常是因特网）建立一个临时的、安全的连接，是一条穿过公用网络的安全、稳定的隧道。虚拟专用网是对企业内部网的扩展,它可以帮助异地用户、公司分支机构、商业伙伴及供应商同公司的内部网建立可信的安全连接，并保证数据的安全传输。


- IETF 组织对基于IP 的VPN 解释为：通过专门的隧道加密技术在公共数据网络上仿真一条点到点的专线技术。所谓虚拟，是指用户不再需要拥有实际的长途数据线路，而是使用Internet公众数据网络的长途数据线路。所谓专用网络，是指用户可以为自己制定一个最符合自己需求的网络。早期的专用网一般指的是电信运营商提供的Frame Relay或ATM 等虚拟固定线路（PVC）服务的网络，或通过运营商的DDN 专线网络构建用户自己的专用网。

- 现在的VPN 是在Internet 上临时建立的安全专用虚拟网络，用户节省了租用专线的费用，同时除了购买VPN 设备或VPN软件产品外，企业所付出的仅仅是向企业所在地的ISP 支付一定的上网费用，对于不同地区的客户联系也节省了长途电话费。这就是VPN 价格低廉的原因。

- 以OSI 模型参照标准，不同的VPN 技术可以在不同的OSI 协议层实现。
 如下表

| VPN在OSI中的层次 | VPN实现技术 |
| ------ | ------ |
| 应用层 | SSL VPN |
| 会话层 | Socks5 VPN |
| 网络层 | IPSec VPN |
| 数据链路层 | PPTP及L2TP |

#### 应用层VPN
SSL协议：
    安全套接字层（Secure Socket Layer,SSL）属于高层安全机制，广泛应用于Web 浏览程序和Web 服务器程序，提供对等的身份认证和应用数据的加密。在SSL中，身份认证是基于证书的。服务器方向客户方的认证是必须的，而SSL 版本3中客户方向服务方的认证只是可选项，但是并没有得到广泛的应用。SSL 会话中包含一个握手阶段，在这个阶段通信双方交换证书，生成会话密钥，协商以后通信使用的加密算法。完成了握手以后，对于B/S的应用，应用程序就可以安全地传输数据而无需做很大修改，除了在传输数据时要调用SSL API而不是传统的套接字API，但是对于C/S结构的应用软件，其解决方案与会话层的VPN异曲同工。
    SSL 是一个端到端协议，因而是在处于通信通路端点的机器上实现（通常是在客户机和服务器上），而不需要在通信通路的中间节点（如路由器或防火墙）上实现。虽然理论上SSL可以用于保护TCP/IP 通信，但事实上SSL的应用几乎只限于HTTP。在SSL通信中，服务器方使用443端口，而客户方的端口是任选的。 

#### 会话层VPN 
Socks4协议：
     Socks 处于OSI 模型的会话层，在Socks协议中，客户程序通过Socks客户端的1080端口透过防火墙发起连接，建立到Socks服务器的VPN隧道，然后代理应用程序的客户端与应用程序服务器进行通讯。在该框架中，协议能安全透明地穿过防火墙，并客户程序对目的主机是不可见的，从而很好地隐藏了目标主机。SOCKS 的关键技术是对客户端应用程序进行Socks化，加入对Socks协议的支持，然后服务器端再解析Socks化的结果。
     Socks4协议，它为TELNET、FTP、HTTP、WAIS和GOPHER等基于TCP协议（不包括UDP）的客户/服务器程序提供了一个无需认证的防火墙，建立了一个没有加密认证的VPN隧道。

Socks5协议：
     Socks5协议扩展了Socks4，以使其支持UDP、TCP框架规定的安全认证方案、地址解析方案中所规定的IPv4、域名解析和IPv6。为了实现这个Socks协议，通常需要重新编译或者重新链接基于TCP的客户端应用程序以使用Socks库中相应的加密函数，并且增加了对数据传输的完整性、数据包的压缩支持。

#### 网络层VPN 技术

- IPSec协议：
    IPSec 也是IETF 支持的标准之一，它和前两种不同之处在于它是第三层即IP层的加密。 IPSec 不是某种特殊的加密算法或认证算法，也没有在它的数据结构中指定某种特殊的加密算法或认证算法，它只是一个开放的结构，定义在IP数据包格式中，不同的加密算法都可以利用IPSec定义的体系结构在网络数据传输过程中实施。 
    IPSec协议可以设置成在两种模式下运行：一种是隧道（tunnel）模式，一种是传输(transport)模式。在隧道模式下，IPSec 把IPv4 数据包封装在安全的IP帧中。传输模式是为了保护端到端的安全性，即在这种模式下不会隐藏路由信息。隧道模式是最安全的，但会带来较大的系统开销。


#### 链路层VPN 技术 
- PTP协议：
   PPTP（点到点隧道协议）是由PPTP论坛开发的点到点的安全隧道协议，为使用电话上网的用户提供安全VPN业务，1996 年成为IETF草案。PPTP是PPP 协议的一种扩展，提供了在IP 网上建立多协议的安全VPN 的通信方式，远端用户能够通过任何支持PPTP 的ISP 访问企业的专用网络。
    PPTP 提供PPTP 客户机和PPTP服务器之间的保密通信。PPTP 客户机是指运行该协议的PC 机，PPTP 服务器是指运行该协议的服务器。通过PPTP，客户可以采用拨号方式接入公共的IP 网。拨号客户首先按常规方式拨号到ISP的接入服务器，建立PPP 连接；在此基础上，客户进行二次拨号建立到PPTP 服务器的连接，该连接称为PPTP隧道。PPTP隧道实质上是基于IP协议的另一个PPP连接，其中IP包可以封装多种协议数据，包括TCP／IP、IPX和NetBEUI。对于直接连接到IP网的客户则不需要第一次的PPP拨号连接，可以直接与PPTP服务器建立虚拟通路。
    PPTP 的最大优势是Microsoft 公司的支持，另外一个优势是它支持流量控制，可保证客户机与服务器间不拥塞，改善通信性能，最大限度地减少包丢失和重发现象。PPTP 把建立隧道的主动权交给了客户，但客户需要在其PC 机上配置PPTP，这样做既会增加用户的工作量，又会造成网络的安全隐患。另外，PPTP 仅工作于IP，不具有隧道终点的验证功能，需要依赖用户的验证。


- L2F/L2TP 协议：
   L2F（Layer 2 Forwarding）是由Cisco 公司提出的，可以在多种介质（如ATM、FR、IP）上建立多协议的安全VPN 的通信方式。它将链路层的协议（如HDLC、PPP、ASYNC等）封装起来传送，因此网络的链路层完全独立于用户的链路层协议。该协议1998 年提交给IETF，成为RFC2341。 
    L2F远端用户能够通过任何拨号方式接入公共IP网络。首先，按常规方式拨号到ISP 的接入服务器（NAS），建立PPP 连接；NAS 根据用户名等信息发起第二次连接，呼叫用户网络的服务器，这种方式下，隧道的配置和建立对用户是完全透明的。L2F允许拨号服务器发送PPP帧，并通过WAN 连接到L2F 服务器。L2F 服务器将包去封装后，把它们接入到企业自己的网络中。与PPTP 所不同的是，L2F 没有定义客户。
    L2F 的主要缺陷是没有把标准加密方法包括在内，因此它基本上已经成为一个过时的隧道协议。 


VPN，被定义为通过一个公用网络（通常是因特网）建立一个临时的、安全的连接，是一条穿过公用网络的安全、稳定的隧道。虚拟专用网是对企业内部网的扩展,它可以帮助异地用户、公司分支机构、商业伙伴及供应商同公司的内部网建立可信的安全连接，并保证数据的安全传输