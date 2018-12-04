#!/usr/bin/env bash
mkdir -p $logdir > /dev/null 2>&1
bash -x ./build.sh $CONFIGFILE $2 > $logdir/build-heb-vms-$ts.log 2>&1


sudo nohup node server.js &
netstat -tunlp | greo 80



# Remove cached SSH keys for the vm, new RSA keypair will be used.
egrep -v "$6" /root/.ssh/known_hosts > /root/.ssh/known_hosts.new
mv /root/.ssh/known_hosts.new /root/.ssh/known_hosts
exp_cmd="set timeout 20
spawn ssh root\@$6;
expect {
\"yes/no\"   { send \"yes\r\" ; exp_continue }
\"Password:\" { send \"$root_pwd\r\" }
\"password:\" { send \"$root_pwd\r\" }
timeout       { exit }
}
expect \"Router#\"
send \"show ip int brief\r\"
expect \"Router#\"
send \"exit\r\"
interact"
result="$(expect -c "$exp_cmd")"
echo "$result" >> $setuplog
var="$(echo $result | grep "show ip int")"
if [ -z "$var" ]; then
    printf "$cmd_fail - failed to set initial config to vm"
else
    printf "$cmd_succ"
fi


##   REGX

pid="$(sed -n -e 's/^\*[0-9]\s*\(\S*\).*/\1/p' $router_prov | head -n 1)”
serial_number="$(sed -n -e 's/^\*[0-9]\s*\S*\s*\([0-9A-Z]*\)\s*.*/\1/p' $router_prov | head -n 1)


string = "\
CGR1000_JAD1908022Y#show version | inc \*1\
*1    CGR1120/K9            JAD1908022Y\
CGR1000_JAD1908022Y#show version | inc \*2"


a = sed -n -e 's/^\*[0-9]\s*\S*\s*\([0-9A-Z]*\)\s*.*/\1/p' $string  | head -n 1
output = JAD1908022Y


grep ER_CONSOLE_IP $3 | cut -d '=' -f 2
sed -n 's/ER_CONSOLE_PORT=\(\S*\).*/\1/p' $3
grep CISCO-IOK-FND /root/.install | cut -d ' ' -f 3 | tr -d '\b\r'
grep -v   'strRegx'   file > newfile
Tail -n I path | head -n j
Wc -l xx.log | cut -d’ ‘ -f1


if [ -s $File ]; then
    echo "OK"
fi

#####################


ssh -o TCPKeepAlive=yes -o ConnectTimeout=30 -o StrictHostKeyChecking=no -i /root/.ssh/orch_rsa 192.168.234.2 "vim-cmd vmsvc/power.on vmid”


csr_ip="$1"
if [ -z "$csr_ip" ]; then
    csr_ip="$(grep "-HER\s" $orch_install| cut -d' ' -f3 -s | tr -d '\b\r')"
fi

if [ "${csr_ip:0:13}" = "CISCO-IOK-HER" ]; then
    new_csr_ip=""
    for f in $orch_home/CSR1000V-config-*; do
        csr_vmname="$(fnGetProperty "$f" "VMNAME")"
        if [ "$csr_vmname" = "$csr_ip" ]; then
            new_csr_ip="$(fnGetProperty "$f" "CSR-INTERNAL-IP")"
            break
        fi
    done

    csr_ip=$new_csr_ip
fi

if [ -z "$csr_ip" ]; then
    printf "$cmd_fail - Cannot find CSR1000V $csr_ip Internal IP address"
    exit 1
fi




####  验证上条语句是否执行成功
# vm-orch-cmd  line 2676
### dhcp Dynamic Host Configuration Protocol Client

res="$(ipcalc -c -6 $mesh_addr 2>/dev/null)"
if [ $? -ne 0 ]; then
    # Mesh prefix is invalid; try with mesh prefix delegation
    if [ -f "/var/run/dhclient6.pid" ]; then
    #dhclient -6 -r eth0
    killall dhclient 2>/dev/null
    fi

    rm -f /tmp/${serial_number}.lease
    echo "default-duid \"${pid}:${serial_number}\";" > /tmp/${serial_number}.lease
    res="$(dhclient -6 -P -sf /usr/sbin/dhclientpd-script -lf /tmp/${serial_number}.lease eth0)"
    if [ -n "$res" ]; then
        mesh_prefix=$res

        mesh_prefix_length="$(echo $mesh_prefix | cut -d'/' -f2)"
        mesh_prefix_addr="$(echo $mesh_prefix|cut -d'/' -f1)"
        if [[ "$mesh_prefix_addr" == *:: ]]; then
            mesh_addr="${mesh_prefix_addr}1/${mesh_prefix_length}"
        elif [[ "$mesh_prefix_addr" == *:0 ]]; then
            mesh_addr="${mesh_prefix_addr%:*}:1/${mesh_prefix_length}"
        else
            mesh_addr=$mesh_prefix
        fi

     rm -f /tmp/${serial_number}.lease
    else
        printf "$cmd_fail - failed to fetch dhclient prefix6 from dhcp server"
         rm -f /tmp/${serial_number}.lease
        exit 1
    fi
fi
#-6     Use the DHCPv6 protocol to obtain whatever IPv6 addresses are available along  with  configuration
#parameters.   It  cannot  be combined with -4.  The -S -T -P and -N arguments provide more control
#over aspects of the DHCPv6 processing.  Note: it is not recommended to mix  queries  of  different
#types together or even to share the lease file between them.

#-P     Enable IPv6 prefix delegation.  This implies -6 and also disables the normal address  query.   See
#-N to restore it.  Note only one requested interface is allowed.

#-sf script-file
#Path to the  network  configuration  script  invoked  by  dhclient  when  it  gets  a  lease.   If
#unspecified,  the  default  CLIENTBINDIR/dhclient-script  is  used.   See dhclient-script(8) for a
#description of this file.
#-lf lease-file
#Path  to the lease database file.  If unspecified, the default DBDIR/dhclient.leases is used.  See
#dhclient.leases(5) for a descriptionof this file.




##Suppress  lines  with no delimiter characters, when used with
#the �−f option. Unless specified,  lines  with  no  delimiters
#shall be passed through untouched.



###
#secure copy (remote file copy program)
    #-i
    #Selects the file from which the identity (private key) for public key authentication is read.  This
    #option is directly passed to ssh(1).

result = "$(scp -i /root/.ssh/orch_rsa $orch_home/cgr_admin_pwd root@${nms_ip_inner}:/root/cgr_admin.pwd)"
