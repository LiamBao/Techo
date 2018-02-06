
![](https://github.com/LiamBao/Techo/tree/master/Kubernets/images/docker-swarm-kubernetes-1024x504.png)

- [GCE 搭建环境](https://blog.gcp.expert/gke-k8s-pod-network/)
- [Microservices](https://martinfowler.com/articles/microservices.html)

Kubernetes 是自动化容器操作的开源平台，这些操作包括部署，调度和节点集群间扩展。如果你曾经用过Docker容器技术部署容器，那么可以将Docker看成Kubernetes内部使用的低级别组件。Kubernetes不仅仅支持Docker，还支持Rocket，这是另一种容器技术。
使用Kubernetes可以：

> 自动化容器的部署和复制
> 随时扩展或收缩容器规模
> 将容器组织成组，并且提供容器间的负载均衡
> 很容易地升级应用程序容器的新版本
> 提供容器弹性，如果容器失效就替换它

Kubernets 的特性有:
1. 每個Service包含著一個以上的pod
2. 每個Service有個獨立且固定的IP地址 – Cluster IP
3. 客戶端訪問Service時，會經由上述提過的proxy來達到負載平衡、與各pod連結的結果
4. 利用標籤選擇器(Label Selector)，聰明地選擇那些已貼上標籤的pod


实际上，使用Kubernetes只需一个部署文件，使用一条命令就可以部署多层容器（前端，后台等）的完整集群：

`kubectl create -f single-config-file.yaml`

kubectl是和Kubernetes API交互的命令行程序。现在介绍一些核心概念.


分布式系統，主要元件有：
1. Master – 大總管，可做為主節點
2. Node – 主要工作的節點，上面運行了許多容器。可想作一台虛擬機。K8S可操控高達1,000個nodes以上
3. masters和nodes組成叢集(Clusters),如图:

![基础架构](https://github.com/LiamBao/Techo/tree/master/Kubernets/images/k8s_arch-1024x437.png)

Master 包含了三個基本組件
*Etcd, API Server, Controller Manager Server*

Node 包含了四個基本組件
*Kubelet, Proxy, Pod, Container*

現在我們著重在K8S最重要的三個部分，即是：
• Pod
• Service
• Deployments (Replication Controller)


Pod
容器是位於pod內部，一個pod包覆著一個以上的容器，這造成K8S與一般容器不同的操作概念。在Docker裡，Docker container是最小單位，但在K8S可想作pod為最小單位。從以下pod的特性來看，就可以了解為什麼它是K8S裡面三巨頭之一了。

1. Pod 擁有不確定的生命週期，這意味著您不曉得任一pod是否會永久保留
2. Pod 內有一個讓所有container共用的Volume，這會與Docker不同
3. Pod 採取shared IP，內部所有的容器皆使用同一個Pod IP，這也與Docker不同
4. Pod 內的眾多容器都會和Pod同生共死，就像桃園三結義一樣！

Service
K8S的 Service 有它的獨特方法，我們看看它的特性
1. 每個Service包含著一個以上的pod
2. 每個Service有個獨立且固定的IP地址 – Cluster IP
3. 客戶端訪問Service時，會經由上述提過的proxy來達到負載平衡、與各pod連結的結果
4. 利用標籤選擇器(Label Selector)，聰明地選擇那些已貼上標籤的pod

Deployments
舊版的K8S使用了副本控制器(Replication Controller)的名詞，在新版已經改成 Deployments囉。Deployments顧名思義掌控了部署Kubernetes服務的一切。它主要掌管了Replica Set的個數，而Replica Set的組成就是一個以上的Pod

1. Deployments 的設定檔(底下以YAML格式為例)，可以指定replica，並保證在該replica的數量運作
2. Deployments 會檢查pod的狀態
3. Deployments 下可執行滾動更新或者回滾
