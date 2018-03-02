## Installation Guide for radius and openssl server in RHEL7 or centos

#version=RHEL7
# Install OS instead of upgrade
install
sshpw --username=root --iscrypted xxxxx
# Reboot after installation
reboot
# Use network installation
url --url="http://xx.xx.xx.xx/rhel-server-7.1"
# Use graphical install
graphical
# Firewall configuration
firewall --disabled
firstboot --disable
ignoredisk --only-use=sda
# Keyboard layouts
keyboard --vckeymap=us --xlayouts='us'
# System language
lang en_US.UTF-8

# Network information
network  --bootproto=static --device=eth0 --hostname=projectproname --ip=xx.xx.xx.xx --nameserver=xx.xx.xx.xx --netmask=255.255.255.0 --activate
network  --bootproto=static --device=eth1 --gateway= --ip=xx.xx.xx.xx --netmask=255.255.252.0 --activate
repo --name="Server-HighAvailability" --baseurl=http://xx.xx.xx.xx/rhel-server-7.1/addons/HighAvailability
repo --name="Server-ResilientStorage" --baseurl=http://xx.xx.xx.xx/rhel-server-7.1/addons/ResilientStorage
# Root password
rootpw --iscrypted L6uOYhxxxxUWM
# SELinux configuration
selinux --disabled
# System services
services --enabled="chronyd"
# System timezone
timezone America/Los_Angeles --isUtc
# X Window System configuration information
xconfig  --defaultdesktop=gnome --startxonboot
# System bootloader configuration
bootloader --append=" crashkernel=auto net.ifnames=0 biosdevname=0" --location=mbr --boot-drive=sda
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all --initlabel
# Disk partitioning information
autopart --type=thinp
#part /boot --fstype="ext3" --size=200
#part / --fstype="ext4" --size=192439
#part /var --fstype="ext4" --size=4095
#swap --recommended

%pre
# Pre commands.

%end

%post --nochroot --logfile /root/post-nochroot.log

# Post commands without chroot. This means we can grab install logs and
# place them in the future root home directory for later perusal.

# Save our ks.cfg in the future root home directory.
if [ -f /tmp/ks.cfg ]; then
     cp /tmp/ks.cfg /mnt/sysimage/root/.ks.cfg
elif [ -f /ks.cfg ]; then
    cp /ks.cfg /mnt/sysimage/root/.ks.cfg
fi

# Save memory configuration.
cat /proc/meminfo > /mnt/sysimage/root/.meminfo

# Save log files from /tmp.
FILES="/tmp/anaconda.log /tmp/syslog /tmp/netinfo /tmp/modules.conf /tmp/modprobe.conf /tmp/scsidisks /tmp/lvmout"
mkdir /mnt/sysimage/root/.kickstart
for FILE in $FILES; do
    if [ -f $FILE ]; then
        cp $FILE /mnt/sysimage/root/.kickstart/
    fi
done

# Save our grub config too.
cp /mnt/sysimage/boot/grub2/grub.cfg /mnt/sysimage/root/.kickstart/grub.cfg.before-post

%end

%post --logfile /root/post.log

set -x

installdir=/media/install
mkdir -p $installdir
mount /dev/cdrom $installdir


#
# Install nginx, redis, celery for pro
#
rpm -Uv $installdir/pro/*.rpm
mkdir -p /tmp/pro
cp $installdir/pro/*.rpm /tmp/pro

cp $installdir/proestration* /etc/nginx/
chmod 0400 /etc/nginx/proestration*

cp $installdir/config_path/nginx.conf /etc/nginx/

#mkdir -p /tmp/openssl-build
#tar xf $installdir/pro/openssl-1.0.1p.tar.gz -C /tmp/openssl-build
#cd /tmp/openssl-build/openssl-1.0.1p
#./config
#make
#make install

#echo "export PATH=/usr/local/ssl/bin:\$PATH" >> /etc/bashrc


cp $installdir/pro/freeradius-server*.tar.bz2 /tmp
cp $installdir/pro/openssl*.tar.gz /tmp

OPENSSL_SRCTAR="$(find /tmp -name "openssl*.tar.gz")"
FREERADIUS_SRCTAR="$(find /tmp -name "freeradius-server*.tar.bz2")"

if [ -z "$OPENSSL_SRCTAR" ]; then
    echo "Cannot find tarball for OpenSSL"
    exit 1
fi

if [ -z "$FREERADIUS_SRCTAR" ]; then
    echo "Cannot find tarball for FreeRADIUS"
    exit 1
fi

OPENSSL_SRCDIR="$(echo $OPENSSL_SRCTAR | sed 's/.tar.gz//')"
OPENSSL_DSTDIR=/opt/ssl

FREERADIUS_SRCDIR="$(echo $FREERADIUS_SRCTAR | sed 's/.tar.bz2//')"
FREERADIUS_DSTDIR=/opt/freeradius

# Build OpenSSL
rm -rf $OPENSSL_SRCDIR
rm -rf $OPENSSL_DSTDIR

mkdir $OPENSSL_SRCDIR
tar xf $OPENSSL_SRCTAR -C $OPENSSL_SRCDIR
cd $OPENSSL_SRCDIR/openssl*
./config shared --prefix=$OPENSSL_DSTDIR  && make depend && make && make install
if [ $? -ne 0 ]; then
    echo "ERROR: Build OpenSSL failed"
    rm -rf $OPENSSL_SRCDIR
    rm -f $OPENSSL_SRCTAR
    exit 1
fi

echo $OPENSSL_DSTDIR/lib >/etc/ld.so.conf.d/openssl-x86_64.conf
rm -rf $OPENSSL_SRCDIR

echo "export PATH=$OPENSSL_DSTDIR/bin:$PATH" >> /etc/bashrc
export PATH=$OPENSSL_DSTDIR/bin:$PATH

# Build FreeRADIUS
rm -rf $FREERADIUS_SRCDIR
rm -rf $FREERADIUS_DSTDIR

mkdir $FREERADIUS_SRCDIR
tar xf $FREERADIUS_SRCTAR -C $FREERADIUS_SRCDIR
cd $FREERADIUS_SRCDIR/freeradius-server*

./configure --prefix=$FREERADIUS_DSTDIR --with-openssl-include-dir=$OPENSSL_DSTDIR/include --with-openssl-lib-dir=$OPENSSL_DSTDIR/lib && make && make install
if [ $? -ne 0 ]; then
    echo "ERROR: Build FreeRADIUS failed"
    rm -rf $FREERADIUS_SRCDIR
    rm -f $FREERADIUS_SRCTAR
    exit 1
fi

cat >/usr/lib/systemd/system/radiusd.service <<EOF
[Unit]
Description=FreeRADIUS multi-protocol policy server
After=syslog.target network.target mariadb.target
Documentation=man:radiusd(8) man:radiusd.conf(5) http://wiki.freeradius.org/ http://networkradius.com/doc/

[Service]
EnvironmentFile=-$FREERADIUS_DSTDIR/etc/sysconfig/radiusd
ExecStartPre=$FREERADIUS_DSTDIR/sbin/radiusd $FREERADIUS_OPTIONS -Cxm -lstdout
ExecStart=$FREERADIUS_DSTDIR/sbin/radiusd $FREERADIUS_OPTIONS -fm
ExecReload=/usr/sbin/radiusd -C
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload

rm -rf $FREERADIUS_SRCDIR

rm -f $OPENSSL_SRCTAR
rm -f $FREERADIUS_SRCTAR


#
# Install  Provision Script
#
#cp $installdir/provision /etc/init.d
cp $installdir/sudoers /etc

mkdir -p /etc/project-installer

# setup firstboot service
cp $installdir/config_path/iot-firstbootproname /etc/project-installer/firstboot
chmod 0755 /etc/project-installer/firstboot

cp $installdir/config_path/iot-firstbootproname.service /usr/lib/systemd/system/project-firstboot.service
systemctl enable project-firstboot.service

# setup network provision service
cp $installdir/config_path/iot-provision /etc/project-installer/provision
chmod 0755 /etc/project-installer/provision

cp $installdir/config_path/iot-provision.service /usr/lib/systemd/system/project-provision.service
systemctl enable project-provision.service


# Setup timezone
timedatectl set-timezone UTC


# add default user project without password
# without the default user, rhel7 will prompt for new user add
# that's a security hole for rhel7
/usr/sbin/adduser project
/usr/bin/chfn -f "project" project

# avoid possible issue caused by random number generate too slow for web service
if [ -f /usr/lib/systemd/system/rngd.service ]; then
  sed -i -e 's#\s*ExecStart=.*#ExecStart=/sbin/rngd -f -r /dev/urandom -o /dev/random -W 2048#' /usr/lib/systemd/system/rngd.service
fi


%end

%packages
@^Server with GUI
@Compatibility Libraries
@Development Tools
@Graphical Administration Tools
@Legacy UNIX Compatibility
@Scientific Support
@Security Tools
@System Administration Tools
@System Management
@base
@core
@desktop-debugging
@dial-up
@fonts
@gnome-desktop
@guest-agents
@guest-desktop-agents
@input-methods
@internet-browser
@multimedia
@print-client
@x11
GeoIP
MySQL-python
chrony
compat-libcap1
dhcp
dhcp-common
dhcp-libs
dos2unix
emacs
expect
glibc
glibc-devel
kexec-tools
ksh
libaio
libaio-devel
librsvg2
librsvg2-devel
librsvg2-tools
libxml2-devel
libxslt
libxslt-devel
mariadb
mariadb-devel
mariadb-libs
mariadb-server
net-snmp
net-snmp-libs
net-snmp-utils
ntp
openssl-devel
pcre-devel
perl-CGI
pexpect
python-devel
python-mako
python-netaddr
python-pyasn1
screen
sysstat
tcl
tcl-devel
telnet
tigervnc-server
unixODBC
unixODBC-devel
wireshark
-NetworkManager
-NetworkManager-glib
-NetworkManager-gnome
-fprintd
-fprintd-pam
-krb5-auth-dialog
-logwatch
-pirut
-rhgb
-rhnsd
-smartmontools
-subscription-manager

%end

%addon com_redhat_kdump --enable --reserve-mb='auto'

%end
