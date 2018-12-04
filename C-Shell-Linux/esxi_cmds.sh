#!/bin/sh +x

#  esxi_cmds.sh
#  
#
#  Created by LIamBao
#  
https://www.jianshu.com/p/f9c30b3732fb
#升级esxi

#进入维护模式：
vim-cmd hostsvc/maintenance_mode_enter

#升级ESXi操作系统:
esxcli software vib update -d "/vmfs/volumes/datastore55.19/ESXi550-201505002.zip"

#重启系统:
esxcli system shutdown reboot -r "reboot"


#To enter maintenance mode:
vim-cmd /hostsvc/maintenance_mode_enter

#To exit maintenance mode:
vim-cmd hostsvc/maintenance_mode_exit

#Find out which VMs are running on esxi host
esxcli vm process list

#reboot the host by entering the following command:
reboot


#使用以下命令查看当前 vSwitch 配置和 vmkernel 接口配置：
esxcli network vswitch standard list    # list current vswitch configuration

esxcli network vswitch dvs vmware list  # list Distributed Switch configuration

esxcli network ip interface list        # list vmkernel interfaces and their configuration

esxcli network nic list                 # display listing of physical adapters and their link state



#使用以下命令在 vNetwork Distributed Switch (vDS) 中添加或移除网卡（称为 vmnic）：

esxcfg-vswitch -Q vmnic -V dvPort_ID_of_vmnic dvSwitch # unlink/remove a vDS uplink

esxcfg-vswitch -P vmnic -V unused_dvPort_ID dvSwitch     # add a vDS uplink


