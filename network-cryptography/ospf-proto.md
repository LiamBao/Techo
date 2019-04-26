# ospf proto

### 开放式最短路径优先 [`wiki`](https://zh.wikipedia.org/wiki/开放式最短路径优先)

> Open Shortest Path First，缩写为 OSPF）是对链路状态路由协议的一种实现，隶属内部网关协议（IGP），故运作于自治系统内部。采用戴克斯特拉算法（Dijkstra's algorithm）被用来计算最短路径树。它使用“代价（Cost）”作为路由度量。链路状态数据库（LSDB）用来保存当前网络拓扑结构，路由器上属于同一区域的链路状态数据库是相同的（属于多个区域的路由器会为每个区域维护一份链路状态数据库）。OSPF分为OSPFv2和OSPFv3两个版本,其中OSPFv2用在IPv4网络，OSPFv3用在IPv6网络。OSPFv2是由RFC 2328定义的，OSPFv3是由RFC 5340定义的。

* OSPF协议是大中型网络上使用最为广泛的IGP（Interior Gateway Protocol）协议。节点在创建邻接，接受链路状态通告（Link-state Advertisement，LSA）时，可以通过MD5或者明文进行安全验证。
* OSPF提出了“区域（Area）”的概念，一个网络可以由单一区域或者多个区域组成。其中，一个特别的区域被称为骨干区域（Backbone Area），该区域是整个OSPF网络的核心区域，并且所有其他的区域都与之直接连接。所有的内部路由都通过骨干区域传递到其他非骨干区域。所有的区域都必须直接连接到骨干区域，如果不能创建直接连接，那么可以通过虚链路（virtual link）和骨干区域创建虚拟连接。
* 同一个广播域（Broadcast Domain）的路由器或者一个点对点（Point To Point）连接的两端的路由器，在发现彼此的时候，创建邻接（Adjacencies）\[注 1\]。多路访问网络以及非广播多路访问网络的路由器会选举指定路由器（Designated Router, DR）和备份指定路由器（Backup Designated Router, BDR），DR和BDR作为网络的中心负责路由器之间的信息交换从而降低了网络中的信息流量。OSPF协议同时使用单播（Unicast）和组播（Multicast）来发送Hello包和链路状态更新（Link State Updates），使用的组播地址为224.0.0.5和224.0.0.6。与RIP和BGP不同的是，OSPF协议不使用TCP或者UDP协议而是承载在IP协议之上，IP协议号为89，工作在OSI模型的传输层。

### OSPF:All you need to know for the CCNA/Configuring OSPF for IPv6 on Cisco routers

原文 : [https://www.ictshore.com/free-ccna-course/ospf-understanding/](https://www.ictshore.com/free-ccna-course/ospf-understanding/)

Any network engineer worth his salt can implement routing. In any Enterprise environment, static routes are simply not enough. They can’t scale, and are slow to converge. Instead, Open Short Path First – or simply OSPF – is a great Enterprise-level solution. With it, you can build a dynamic routing infrastructure that can scale. Being open standard, with convergence times and easy to implement \(and scale\) are all factors that make OSPF great for any environment, including yours. In this article, we are going to see all the theory behind it. We will explore the concepts of OSPF, and see how we can tune it. With this knowledge, you will then be able to implement it.

OSPF is a complex protocol, and we can talk about it for days. For this article, we will focus on the knowledge Cisco requires for the CCNA. Therefore, if you are a beginner, you will benefit from this article. It will give you a _beginner-to-intermediate_ knowledge of OSPF.

### Introducing OSPF

OSPF is a _Link-State Routing \(LSR\)_ protocol. This means that, unlike RIP, it doesn’t exchange routes. When using OSPF, routers won’t tell each other _“you can reach this subnet through me”_. Instead, **routers talk about links**: they tell each other which other routers are their neighbors. For example, if Router 1 is connected to Router 2, it will tell: _“Hey, I’ve a direct connection to R2”_. This process aims to give all routers an overall understanding of the topology. Each router must know the size and shape of the network. In a converged topology, all routers have _a map of the entire network_. Here’s a visualization of that. ![OSPF is a link-state routing protocol: routers propagate the current state of links. After convergence, each router knows the picture of the topology.](http://upload-images.jianshu.io/upload_images/7662633-efd280ab1c33f080.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

That map each router holds is the **OSPF Database**. However, once all routers have an updated database, we still don’t have routes. In fact, the router will take the database and look in it for the shortest path to any destination. Once found, it will add a route to the routing table. To do that, the router runs the [Dijkstra’s Algorithm](https://en.wikipedia.org/wiki/Dijkstra's_algorithm) over the database. This can eat a lot of CPU, proportionally to the number of routers and subnets in the database.

In RIP, a router just tells its neighbor what are the subnets it can reach. With OSPF, each router knows the topology. By knowing it, it can **autonomously select** the best next-hop for each destination.

### OSPF Adjacencies

#### How does communication happens?

Interestingly, OSPF implements its own transport layer. In fact, it doesn’t use TCP nor UDP, but directly IP. Router puts OSPF messages into IP packets, and set the **protocol number to 89.** OSPF will have to handle acknowledgements and retransmissions on his own. OSPF uses unicast to send some packets, and multicast for some others. To increase efficiency, we don’t use broadcast. Instead, we use two multicast addresses.

* `224.0.0.5`  is the multicast address for All OSPF routers on the same network
* `224.0.0.6`  is the multicast address for all Designated OSPF Routers on the same network. We will talk about Designated router later in the article

Generally speaking, all traffic that may interest multiple router goes in _multicast_ packets. Instead, specific exchanges between two routers will leverage _unicast_.

#### The Hello packet

Before two routers can start talking about links, they must form an **adjacency**. This simply means that two routers understand to be neighbor, and to have the same OSPF parameters.

OSPF routers periodically send out Hello packets using the multicast address _“All OSPF routers”_. With these messages, that don’t need to be acknowledged, they tell they exist.

![OSPF hello packets can verify neighbor availability and establish adjacencies.](http://upload-images.jianshu.io/upload_images/7662633-007b5b7534133b0a.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

Routers put basic information about themselves in the hello packet. The purpose of that is just the discovery of new neighbors. Once two routers sees \(with hello packets\) that are **neighbors**, they can start to create an adjacency. Only after that, they will start to exchange details about links. However, this process is not as simple as it might seem. Routers will go through multiple states, as we explain in the next section.

### OSPF States

#### Introducing OSPF Router states

Two routers will need to go through **7-8 states** in order to converge. Having a clear understanding of them allows you to troubleshoot OSPF issues. The 7 states you need to remember are: _Down_, _Init_, _2-Way_, _ExStart_, _Exchange_, _Loading_ and _Full_. For the pros, we can add the _Attempt_ state \(right after Down\).

The flow chart for these states is straightforward: each state can lead only to the next state. To that, we have just one exception if we need to consider the “Attempt” state. We consider that two routers have converged only when they reach the _Full_ state. Remember that states aren’t just about routers. They indicate the _state of a router toward another router_. As a result, the same router can be in a state for the relationship with a second router, and in a different state for the relationship with a third router. ![OSPF states diagram.](http://upload-images.jianshu.io/upload_images/7662633-52be5c9410876f4e.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

The states from Down to 2-Way have the major goal of forming an adjacency. Once that they form the adjacency, states from ExStart to Loading allow the two routers to talk about links. Once they agree on the topology, they move to the Full state that represents convergence.

#### Diving into OSPF states

To better understand how OSPF works, we need to look into its states.

* **Down** is the initial stage, the routers just don’t know about each other.
* For _Non-Broadcast Multi Access_ Networks, like Frame Relay, we have the **Attempt**  state. It is essentially means that the router is trying to establish a L2 connection with the possible neighbor.
* In the **Init**  state, the router has received a hello packet. Both routers must move to that state before continuing. This mean that each router has seen the hello packet of the other.
* Once both routers have heard of each other, they move to the **2-Way** state. In this state, they have established a bidirectional communication that can use to talk about links.
* **ExStart**  indicates that routers are starting to exchange links’ information
* In the **Exchange** State, routers send each other a summary of their OSPF database. This allow the other routers to have an idea about the links the neighbor knows about
* With the **Loading**  State, each router ask the neighbor for details about the new links. In fact, with the previous step the router can tell what are the links that he doesn’t knows \(but that the neighbor does\). With this step, the two routers will end up having the same OSPF database.
* **Full** state indicates that the two routers have the same OSPF database. They are known to be fully adjacent.

In normal conditions, all routers should be fully adjacent. The only exception to that is where we need Designated Routers, as we will explain later.

#### The Router ID

To identify each link , we need to identify the two routers that form the link. To do that, we don’t use the hostname. We don’t even use the IP address, as each router can have multiple of them. We need something unique. To have that, we created a new concept specifically for OSPF: the **Router ID**.

The Router ID is a _32-bit numeric identifier_ of the router. We represent that in dotted notation \(`X.X.X.X`\), just like an IP address. However, remember that **this is not an IP address**. When you first configure OSPF on your router, it will try to create a Router ID on his own. To do that, it will look for the following items \(in order of preference\): 1. The highest IP address among loopback interfaces \(if any\). _If no loopback interfaces are configured, move to the next point_ 2. The highest IP address among Ethernet \(including Fast and Giga\) interfaces

However, the best practice is to _configure the router ID manually_.

### The OSPF Database

#### The Link State Database \(LSDB\)

We know from the introduction the routers hold a map of the topology. This is the OSPF database, technically known as **Link State Database \(LSDB\)**. We call it LSDB because it simply contains all the links in the topology.

You can think about the LSDB like a set of tables. One of them stores all the links \(Link States, LS – technically\). Each **Link State** is a row containing the Router IDs of the two routers forming the links, and a cost. The cost indicates how much does it cost to take this path \(this link\). Obviously, the lower the cost, the better. We will come back to that in a minute.

In the _Exchange_ state, routers see a summary of the LSDB of the neighbor. That summary is known as **Database Description \(DBD\)**, and it is a specific OSPF packet to be unicasted. Based on that, they decide which Link States they need to know more information about. ![OSPF routers propagate their database summary in the exchange state.](http://upload-images.jianshu.io/upload_images/7662633-d83b08d455a52c36.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

After that, they use the _Loading_ state to retrieve such information. In that state, the router that doesn’t have a link ask for that with a **Link State Request \(LSR\)** message. The other router will reply with a **Link State Advertisement \(LSA\)** message. All of that happens using unicast.

Remember that OSPF is a _master-slave_ protocol. When exchanging data, a router asks and the other respond. They don’t do both things at the same time, but instead they exchange roles once the first finishes.

#### Calculating the OSPF Cost

From the previous section, we know each link has a cost. This cost exclusively rely on the bandwidth of the link: the higher the bandwidth, the lower the cost. Specifically, OSPF has the concept of **reference bandwidth**. This is the bandwidth for which you want to have a cost of 1, and by default it is _100Mbps_. Since the cost is an integer, if you have faster links \(such as 1Gbps\), they will still cost 1. However, Cisco allows you to change the reference bandwidth to fit your needs.

Calculating the cost of a link is simple, it is reference bandwidth over actual bandwidth. Calculating the cost of a path of multiple links \(the **metric**\) is aslo simple: it is the sum of the cost of all links in the path. When the OSPF produces two path to the same destination, the one with the lower cost will go in the routing table.

It might be handy to know what are the cost of different bandwidths according to OSPF. The following table shows the cost each link has, based on different reference bandwidths \(100Mbps, 1Gbps and 10Gbps\).

| Link | Speed | Reference 100Mbps | Reference 1Gbps | Reference 10Gbps |
| :--- | :--- | :--- | :--- | :--- |
| Ten Gigabit Ethernet | 10Gbps | 1 | 1 | 1 |
| Gigabit Ethernet | 1Gbps | 1 | 1 | 10 |
| FastEthernet | 100Mbps | 1 | 10 | 100 |
| T3 | 45Mbps | 2 | 22 | 223 |
| Token Ring | 16Mbps | 6 | 63 | 625 |
| Ethernet | 10Mbps | 10 | 100 | 1000 |
| Token Ring | 4Mbps | 25 | 250 | 2500 |
| E1 | 2.048Mbps | 49 | 488 | 4883 |
| T1 | 1.544Mbps | 65 | 648 | 6477 |
| 64kbps line | 64Kbps | 1562 | 15625 | 156250 |
| 56kbps line | 56Kbps | 1785 | 17857 | 178571 |
| 9.6kbpsline | 9.6Kbps | 10416 | 104167 | 141667 |

With this knowledge in mind, we are now ready to dive into two OSPF-specific topics.

### The good part of OSPF

#### Designated Router, Backup Designated Router

OSPF adjacencies are _peer-to-peer_. It means an adjacency **involves two routers**, and only two. Imagine we have a switch, and we connect three routers to it. If they were to talk OSPF, they will need to establish adjacencies between each other. So, R1 will have an adjacency with R2 and another with R3, and R3 will have an adjacency with R2 as well. This results in having 3 adjacencies, which is acceptable. If we add another routers, we have 6 adjacencies. If we have 10 routers, we would have 45 adjacencies! This is way not scalable.

To overcome that, OSPF engineers invented the concept of **Designated Router \(DR\)**, and its backup **\(BDR\)**. On a broadcast network, like _Ethernet_, OSPF routers will elect a designated router and a backup. Then, they will establish adjacencies only toward them. The DR will take updates from a neighbor, and sync the others. The BDR maintains the adjacencies already up to replace the DR in case it fails. If the DR fails, the BDR becomes the DR, and a new BDR is elected. ![On broadcast link, an adjacency reaches the full state only if it involves the BR or BDR on one end.](http://upload-images.jianshu.io/upload_images/7662633-54fe540cf073290f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

To elect the DR, we need to look at a specific field: **the priority**. This is an administratively chosen value, designed for DR election, which is included in all Hello packets. The router with the highest priority will become the DR, while the router with the second-highest priority will become the BDR. In case of ties on the priority, we consider the Router ID \(the higher the most likely to become DR\). Furthermore, if we manually set the priority to zero, that router will never be a DR.

#### OSPF Areas

For the whole article, we haven’t mentioned the concept of **area**. Believe it or not, this is a key concept for OSPF, but Cisco doesn’t require you to leverage it at the CCNA level.

The more routers you add to the OSPF topology, the more processing the LSDB becomes **CPU-intesive**. Because of that, you generally shouldn’t have more than _50 routers_ in the topology. However, many networks will have much more of them, but this doesn’t mean we can’t use OSPF.

You can group routers into areas, groups of contiguous routers. Then, routers will use their LSDB to map the topology only of routers in the same area. For routers in a different area, they don’t care anymore about the status of links. Instead, they care about routes, just like with RIP. Some router known as **Area Border Routers \(ABR\)** will have an interface in an area, and another interface in another. ABRs will take the LSDB from an area, and create inter-area routes to inject in the other area. Of course, this is true from both directions.

Grouping routers into areas bring many benefits. In fact, this isn’t simply a way to save CPU resources:

* Allows segmentation of the network
* Creates summarization points \(the ABRs\), potentially reducing the size of routing table
* Reduces convergence times and management traffic \(inter-area updates\)

In fact, with area, if a link goes down only routers in the same area will be notified. Other areas will be notified only if there is a change in routes.

#### The Backbone Area

OSPF identifies each area with a numeric ID. On top of that, it defines the concept of **backbone area**, an area with the role of connecting other areas. The backbone area must have the **ID set to 0**. As a requirement, all areas must have at least an ABR shared with area 0, making them directly connected to area 0. In CCNP, we learn how to circumvent that, but this is not recommended. By design, use area 0 at the center of your network.

As a result, your topology will look something like this.

![OSPF Areas allow network segmentation.](http://upload-images.jianshu.io/upload_images/7662633-bb48c42c6b8b0641.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

_Tip: for the CCNA, you are going to use OSPF single-area. This means you will configure all routers in the same area. If you do so, you must use area 0. A OSPF topology where no area 0 exists is simply a bad design. Remember that for the labs and for the exam too!_

### Conclusion

In this article, we discovered what is OSPF and how we can use it. With this knowledge, you are now able to understand a complex routing environment which leverages this protocol. To do that, there are some concepts you absolutely need to remember. Here’s a quick recap:

* OSPF is a Link-State protocol, it propagates changes to links to other routers. It identifies each router with a Router ID \(32-bit\)
* Updates are forwarded “as they are” by neighboring router, because the goal is to make all router know the entire topology
* Routers maintain a representation of the interconnection in the networks, the Link State Database \(LSDB\)
* In a broadcast \(or generic multi access\) network, routers elect a Designated Router to coordinate updates. As a result, we limit redundant updates on that segment
* OSPF groups router into areas: all remote areas must be connected to the backbone area \(ID 0\)
* Routers that are in at least two areas are known as Area Border Routers \(ABRs\)

Take a moment to truly understand these concepts, and read again the article if necessary. In the next article, you will try your knowledge by learning how to configure a full OSPF topology

## OSPFv6: Configuring OSPF for IPv6 on Cisco routers

OSPF is a stable routing protocol, and we know it from [this article](https://www.ictshore.com/free-ccna-course/ospf-understanding/). In fact, we have tons of reasons that motivate us to adopt it with IPv4. IPv6 makes no difference, we still want to use OSPF. While the configuration commands are slightly different, the concept is always the same. In this article, we are going to guide you through the new commands of this protocol. We are entering the world of what Cisco calls “OSPFv6”, or simply OSPF for IPv6.

This is a practice article, where we will see some configuration commands. The best way to remember is to try them on your own, this is why we created this lab. You can download it for free by using the link below.

Once you downloaded it, un-zip it and open it with Packet Tracer. You will be able to try the commands you learn in the lab, and this will help you mastering OSPFv6.

### OSPFv6 Lab Intro

#### The topology

Look at the picture below, do you recognize the topology? If you are coming from the Free CCNA course, you will. This arrow-like topology is the same we used for [traditional IPv4 OSPF](https://www.ictshore.com/free-ccna-course/ospf-configuration/). In this article, we are going to use it for OSPFv6.

![The topology for this lab.](http://upload-images.jianshu.io/upload_images/7662633-0d062d35ba20c7eb.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

As you can see, we have 8 routers in total, going from 0 to 7. We connected four of them to a central switch, operating only in VLAN 1. Then, we added some ring-like connections between the other routers. The physical and Layer 2 topology is still the same from the previous article. What changes, though, is the whole addressing plan. We have completely removed all IPv4 addresses, and replaced them with IPv6 ones.

This results in a cleaner and more predictable addressing plan. Each router has its interface ID set to its router number, except router 0. For example, router 1 will be `::1` on any network, router 2 `::2`and so on. Instead, Router 0 will be `::10`. The subnet we are going to use are reported below.

| Link | Subnet |
| :--- | :--- |
| R0-R1 | `2001:db8:0:1::/64` |
| R0-R2 | `2001:db8:0:2::/64` |
| R1-R2 | `2001:db8:1:2::/64` |
| Broadcast \(Switch\) | `2001:db8:cafe::/64` |
| R3-R7 | `2001:db8:3:7::/64` |
| R4-R5 | `2001:db8:4:5::/64` |
| R5-R6 | `2001:db8:5:6::/64` |
| R6-R7 | `2001:db8:6:7::/64` |

#### The Requirements

Even if we moved to the newer protocol, requirements haven’t changed. In fact, we still want to use OSPF to reach the convergence. We are still working at a CCNA-level, so all routers will go into Area 0 as they did for IPv4. And, we even want the same router IDs we had before. To refresh your mind, we want the router ID to be `1.0.0.0` plus the router number. Router 1 will be `1.0.0.1`, router 4 will be router `1.0.0.4` and so on.

### Configuring OSPFv6 \(OSPF for IPv6\)

#### Before we start…

Cisco offers two ways of configuring OSPF for IPv6. The simplest one is the one we are going to use in this article, the OSPFv6. In the CCNP certification, you will learn about a more sophisticated alternative: OSPFv3. Just know that both exists, and that based on needs you may use one instead of the others. Since we have simplicity in our mind, we will go for OSPFv6.

Article continues below the advertisement

Note that “OSPFv6” is not really the sixth version of OSPF. It doesn’t even exist such version. Instead, it is just an informal jargon we use, only for Cisco devices, to define the configuration done with `ipv6 router ospf` command. You’ll see in the next section what are we talking about.

#### The OSPFv6 Router

All routers comes pre-configured with IPv6 addresses and with `ipv6 unicast-routing enabled`. If you want to do a set up from scratch, don’t forget that. Since we have our routers ready we will just skip that part.

The first thing we want to do, is to turn on OSPFv6 on the router. To do that, we use the `ipv6 router ospf` command, followed by the process ID. Just like in IPv4, the process ID is a locally significant number that identifies the OSPF instance. Therefore, it doesn’t need to match between routers. However, for scoring purposes, always set the ID to 1 during this lab.

At this point, you will enter the `Router(config-rtr)#` prompt. This indicates you are configuring an IPv6 routing protocol \(`rtr` instead of `router` means just that\). And, most likely, you will see another interesting thing. When you enter the prompt, the router will send you this warning.

```text
%OSPFv3-4-NORTRID: OSPFv3 process 1 could not pick a router-id,please configure manually
```

This `NORTID` \(**No Router ID**\) warning indicates that the OSPFv6 process has no router ID. In fact, if we don’t define it manually, the router tries to create one from its IPv4 interfaces. The thing is, we have no IPv4 at all on this router, so it can’t automatically generate a router ID. So, until we configure a router ID manually, the OSPF process won’t start.

To configure the router ID, we just type `router-id` followed by the ID. If you are starting on router 0, then you will type `router-id 1.0.0.0`.

#### Adding networks

We remember from the previous article that having the OSPF process on doesn’t mean we are doing routing. In fact, we need to specify the networks for which we want to do routing. This is true also with IPv6 and OSPFv6, but the configuration paradigm is completely different. If you are still in the `config-rtr` prompt, type `?` to see all the available commands. You won’t see any `network`command, because we don’t use that anymore.

With OSPFv6, we associate networks to the routing instance at the **interface level**. As a result, in the router configuration prompt we will add only _protocol-specific_ settings, like the router ID. Instead, we need to enter the interface configuration and associate the interface to a process ID.

To do that, we type

`ipv6 ospf area` at interface configuration level. Just look at the interfaces that have an IPv6 address \(with `show ipv6 interface brief`\) and add them to the binding.

Below, an example of the whole configuration on Router 0.

```text
ipv6 router ospf 1
 router-id 1.0.0.0
 exit

interface Serial0/0/0
 ipv6 ospf 1 area 0
 exit

interface Serial0/0/1
 ipv6 ospf 1 area 0
 exit
```

#### The other routers

For other routers, we are going to apply the same principles and commands. The only things to change are the values \(interface name and Router IDs\). Because of that, you should be able to do all the configuration on your own. In case you struggle, we reported below all the remaining configuration.

This is for

**R1**…

\`\`\`ipv6 router ospf 1 router-id 1.0.0.1 exit

interface Serial0/0/0 ipv6 ospf 1 area 0 exit

interface Serial0/0/1 ipv6 ospf 1 area 0 exit

```text
Instead, this other is for **R2** (note that it has three interfaces).

```ipv6 router ospf 1
 router-id 1.0.0.2
 exit

interface Serial0/0/0
 ipv6 ospf 1 area 0
 exit

interface Serial0/0/1
 ipv6 ospf 1 area 0
 exit

interface GigabitEthernet0/0
 ipv6 ospf 1 area 0
 exit
```

Then we have **R3**…

```text
ipv6 router ospf 1
 router-id 1.0.0.3
 exit

interface Serial0/0/0
 ipv6 ospf 1 area 0
 exit

interface GigabitEthernet0/0
 ipv6 ospf 1 area 0
 exit
```

Then **R4**…

```text
ipv6 router ospf 1
 router-id 1.0.0.4
 exit

interface Serial0/0/0
 ipv6 ospf 1 area 0
 exit

interface GigabitEthernet0/0
 ipv6 ospf 1 area 0
 exit
```

**R5**…

\`\`\`ipv6 router ospf 1 router-id 1.0.0.5 exit

interface Serial0/0/0 ipv6 ospf 1 area 0 exit

interface GigabitEthernet0/1 ipv6 ospf 1 area 0 exit

```text
And this is the configuration of **R6**, which has three interfaces too…
```

ipv6 router ospf 1 router-id 1.0.0.6 exit

interface GigabitEthernet0/0 ipv6 ospf 1 area 0 exit

interface GigabitEthernet0/1 ipv6 ospf 1 area 0 exit

interface GigabitEthernet0/2 ipv6 ospf 1 area 0 exit

```text
And, in the end, we have **R7** which is a lot like R5.
```

ipv6 router ospf 1 router-id 1.0.0.7 exit

interface Serial0/0/0 ipv6 ospf 1 area 0 exit

interface GigabitEthernet0/0 ipv6 ospf 1 area 0 exit

\`\`\`

Congratulations, You have now mastered the configuration of OSPFv6!

### Troubleshooting OSPFv6

Even if useful, configuration alone is worthless. In fact, sometimes we just type the wrong letter or number, or we just forgot about a device or customization. In these cases, you need to find your way to the truth. If you know the right tools, troubleshooting will be easier than you might think. In this section, we will just give you these tools.

#### Verifying the LSDB

To verify the Link State Database with OSPFv6, we have our old but gold `show ipv6 ospf database`. This command is identical to our IPv4 counterpart, we only need to add _“v6”_ after _“ip”_.

![Example of OSPF database in IPv6.](http://upload-images.jianshu.io/upload_images/7662633-796fa81595950d11.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

Example of OSPF database in IPv6.

Just like we did for IPv4, we need to focus on the Router advertisements and on the Net advertisements. These two are the top two tables shown in the output. Since this command shows the entire LSDB, you can use it to see if a route that didn’t made it to the routing table is there. If you see a network with this command, but not in the routing table, maybe another protocol has a better route to it.

#### Troubleshooting Adjacencies

At the CCNA level, we use single-area OSPF. Furthermore, we are not working with complex concepts like redistribution or route filtering. So, once the routers join the OSPF domain, they are most likely to propagate routes. Where we can encounter problems, instead, are the adjacencies. It is a common problem to see two routers not talking with each other. To easily identify if we have that problem, we can use the `show ipv6 ospf neighbor` command.

![OSPFv6 neighbors.](http://upload-images.jianshu.io/upload_images/7662633-82ee3f8516b5ce64.png?imageMogr2/auto-orient/strip|imageView2/2/w/1240)

Even this command is identical to its IPv4 version. It shows the Router ID of the neighbor, the priority and the state. Then, exactly like in IPv4, it adds the dead time and the interface. **States** are exactly the same, and we want to see the `FULL` state with everyone except on broadcast segment. On them, instead, we expect to see a full adjacency with the DR, one with the BDR and many other 2-Way with the DROTHER routers. In case you don’t see the adjacency with the DR, check if the local router is the DR before panic. A router won’t have an adjacency with itself!

### Conclusion

With this article, we configured an entire topology with OSPF for IPv6. This concludes our CCNA journey in the world of OSPF: we started with theory, then faced the IPv4 and IPv6 configuration. Using the knowledge you gained from this article, you are now able to deploy a mid-size routing domain on your own. Since the commands are basically identical to the ones of IPv4, we can report the same key concepts.

* Use `ipv6 router ospf` to create a OSPFv6 instance
* Define the router ID with `router-id` under thhe `config-rtr` prompt, this is mandatory if the router has no IPv4 address at all
* To associate an interface to the OSPF instance, under the interface configuration type `ipv6 ospf area`
* Troubleshoot with `show ipv6 ospf database`  and `show ipv6 ospf neighbor`

With this very knowledge, you have now the tools to understand complex routing. In the following articles, we are going to introduce another routing masterpiece: EIGRP. You will be able to compare it to OSPF, and soon assess and select a routing protocol over another.

