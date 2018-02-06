#!/bin/sh +x

dhclient -6 -P -sf /usr/sbin/dhclientpd-script -lf /tmp/${serial_number}.lease eth0

#  -6 : Use the DHCPv6 protocol to obtain whatever IPv6 addresses are available along 
#       with configuration parameters.
#       It  cannot  be combined with -4.  The -S -T -P and -N arguments provide more control
#       over aspects of the DHCPv6 processing.  Note: it is not recommended to mix  queries  of  different
#       types together or even to share the lease file between them.


#  -P :Enable IPv6 prefix delegation.  This implies -6 and also disables the normal address  query.   See
#       -N to restore it.  Note only one requested interface is allowed.


# -sf :script-file
#       Path to the  network  configuration  script  invoked  by  dhclient  when  it  gets  a  lease.   If
#       unspecified,  the  default  CLIENTBINDIR/dhclient-script  is  used.   See dhclient-script for a
#       description of this file.


# -lf :lease-file
#       Path  to the lease database file.  If unspecified, the default DBDIR/dhclient.leases is used.  See
#       dhclient.leases(5) for a descriptionof this file.

