#!/bin/bash +x
# chkconfig:   235 04 99
# description: Updates the network configuration of ESXi vms.

# Source function library.
. /etc/init.d/functions

# Source networking configuration.
. /etc/sysconfig/network

sys_cfg_path="/etc/sysconfig"
net_cfg_path="/etc/sysconfig/network-scripts"
vm_cmd_path="/usr/bin"
host_cfg_path="/etc/hosts"

# Check if the input is a valid IPv4 type address
function is_valid_ipv4()
{
  addr=${1:-"INVALID_ADDR"}
  python -c "import sys; import netaddr; netaddr.valid_ipv4(\"$addr\") and sys.exit(0) or sys.exit(1)"
  return $?
}

function get_guestinfo()
{
  "$vm_cmd_path"/vmtoolsd --cmd "info-get guestinfo.$1" 2>/dev/null
}

function set_guestinfo()
{
  "$vm_cmd_path"/vmtoolsd --cmd "info-set guestinfo.$1 "$2"" 2>/dev/null
}

function get_nic_attr()
{
  get_guestinfo "${1}.${2}"
}

function set_nic_attr()
{
  set_guestinfo "${1}.${2}" "$3"
}

# replace "key = value" in config file
function replace_item()
{
  conf="$1"
  key="$2"
  value="$3"

  if [ -f "$conf" ]; then
    sed -i '/'$key'\s*=/Id' "$conf"
    sed -i '$a'$key'='$value'' "$conf"
  fi
}

function provision_hostname()
{
  local vm_cmd_daemon="vmtoolsd"
  local hostname="$(get_guestinfo hostname)"

  # Set hostname if provisioned
  if [ "$hostname" != "N/A" ] && [ -n "$hostname" ]; then
    #replace hostname in /etc/sysconfig/network
    replace_item "$sys_cfg_path/network" "HOSTNAME" "$hostname"

    # add hostname for 127.0.0.1
    egrep -v "127.0.0.1" "$host_cfg_path" > "$host_cfg_path".new
    echo "127.0.0.1"$'\t'"$hostname  localhost.localdomain  localhost" >> "$host_cfg_path".new
    rm "$host_cfg_path"
    mv "$host_cfg_path".new "$host_cfg_path"

    # update hostname for system
    hostname "$hostname"
    echo "$hostname" > /etc/hostname

    # unprovision hostname
    set_guestinfo hostname "N/A"

    return 1
  fi

  return 0
}

function provision_nic()
{
  local nic_name=$1
  local is_default_router=$2

  # Retrieve network information provisioned during installation for NIC
  ip="$(get_nic_attr "${nic_name}" "ipv4")"
  mask="$(get_nic_attr "${nic_name}" "mask")"
  gateway="$(get_nic_attr "${nic_name}" "gateway")"
  dns="$(get_nic_attr "${nic_name}" "dns")"
  ip6="$(get_nic_attr "${nic_name}" "ipv6")"
  ip6_gateway="$(get_nic_attr "${nic_name}" "ipv6_gateway")"

  # Set network information for ethernet0
  # If IP is provisioned as a valid ip, take it. Otherwise, ignore
  if is_valid_ipv4 "$ip"; then
    if !(is_valid_ipv4 "$mask"); then
        # Set mask to be default if not provisioned
        mask="255.255.255.0"
    fi

    replace_item "$net_cfg_path"/ifcfg-${nic_name} "BOOTPROTO" "no"
    replace_item "$net_cfg_path"/ifcfg-${nic_name} "IPADDR" "$ip"
    replace_item "$net_cfg_path"/ifcfg-${nic_name} "NETMASK" "$mask"

    if is_valid_ipv4 $gateway && [ -n "$is_default_router" ] && [ "$is_default_router" = "true" ]; then
      echo "GATEWAY=$gateway" >> "$net_cfg_path"/ifcfg-${nic_name}
      replace_item "$net_cfg_path"/ifcfg-${nic_name} "GATEWAY" "$gateway"
      replace_item "$sys_cfg_path"/network "GATEWAY" "$gateway"
      ip route add default via $gateway dev ${nic_name}
    else
      echo "IOK: invalid gateway $gateway for ${nic_name}"
    fi
    if is_valid_ipv4 $dns; then
      replace_item "$net_cfg_path"/ifcfg-${nic_name} "DNS" "$dns"
    else
      echo "IOK: invalid dns $dns for ${nic_name}"
    fi
    if [ -n "$ip6" ]; then
        replace_item "$net_cfg_path"/ifcfg-${nic_name} "IPV6INIT" "yes"
        replace_item "$net_cfg_path"/ifcfg-${nic_name} "IPV6ADDR" "$ip6"
        replace_item "$net_cfg_path"/ifcfg-${nic_name} "IPV6_DEFAULTGW" "$ip6_gateway"
        
        replace_item "$sys_cfg_path"/network "NETWORKING_IPV6" "yes"

        set_nic_attr "${nic_name}" "ipv6" "N/A"
        set_nic_attr "${nic_name}" "ipv6_gateway" "N/A"
    fi

    # Unprovision ethernet
    set_nic_attr "${nic_name}" "ipv4" "N/A"
    set_nic_attr "${nic_name}" "mask" "N/A"
    set_nic_attr "${nic_name}" "gateway" "N/A"
    set_nic_attr "${nic_name}" "dns" "N/A"

    # reload NIC config
    ifup ${nic_name}
    return 1
  fi

  return 0
}

prog=provision

start() {
  need_reload=0

  provision_nic "eth0" "true"
  let need_reload+=$?

  provision_nic "eth1" "false"
  let need_reload+=$?

  provision_nic "eth2" "false"
  let need_reload+=$?

  provision_hostname
  let need_reload+=$?

  # Set time synchorization and time zone default to be UTC.
  vmware-toolbox-cmd timesync enable
  timedatectl set-timezone UTC

  if [ $need_reload -ne 0 ]; then
      systemctl restart network
  fi

  exit 0
}

# See how we were called.
case "$1" in
    start)
    start
    ;;
    *)
    echo $"Usage: $0 {start}"
    exit 2
esac
