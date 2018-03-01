### VPN Routing and Forwarding (VRF)-Lite Software Configuration Guide for Cisco CGR1000 (Cisco IOS)

[ 原文链接 ](https://www.cisco.com/c/en/us/td/docs/routers/connectedgrid/cgr1000/ios/software/15_4_1_cg/vrf_cgr1000.html#pgfId-1180836)

> Virtual Private Networks (VPNs) provide a secure way for customers to share bandwidth over an ISP backbone network. A VPN is a collection of sites sharing a common routing table. A customer site is connected to the service provider network by one or more interfaces, and the service provider associates each interface with a VPN routing table. A VPN routing table is called a VPN routing/forwarding (VRF) table.

#### Information About VRF-lite
VRF-lite provides traffic isolation by using input interfaces to distinguish routes for different VLANs and forms virtual packet-forwarding tables by associating one or more Layer 3 interfaces with each VRF. Interfaces in a VRF can be either physical, such as Ethernet ports, or logical, such as VLAN SVIs and loopback interfaces, but a Layer 3 interface cannot belong to more than one VRF at any time.

> Note	VRF-lite interfaces must be Layer 3 interfaces

Figure 1 shows an example of a VRF-lite implementation for the CGR 1000.

![VRF-lite Example](./img/vrflite.jpg)

In Figure 1, two CGR 1000 routers are connected to the head-end router in a FlexVPN hub-and-spoke configuration. VRF Green is mapped to VLAN1, and VRF Orange is mapped to VLAN2. Each router has a serial interface, associated with a local IP address, to transport raw socket traffic from Remote Terminal Units (RTUs). Ethernet ports in VLAN2 and the loopback interface used by raw socket on each CGR 1000 are configured in VRF Orange so that traffic from those interfaces can be isolated and routed to SCADA Server A according to the FlexVPN tunnel configuration.
在图1中，两个CGR 1000路由器通过FlexVPN轮辐式配置连接到头端路由器。VRF Green被映射到VLAN1, VRF Orange映射到VLAN2。每个路由器都有一个串行接口，与本地IP地址相关联，以传输来自远程终端单元(RTUs)的原始套接字流量。VLAN2中的以太网端口和每个CGR 1000上的raw socket使用的loopback接口配置在VRF橙色中，这样就可以根据FlexVPN隧道配置将这些接口的通信隔离并路由到SCADA服务器A
For more information about FlexVPN, see [FlexVPN Software Configuration Guide for Cisco 1000 Series Connected Grid Routers (Cisco IOS)](https://www.cisco.com/c/en/us/support/routers/1000-series-connected-grid-routers/products-installation-and-configuration-guides-list.html)

