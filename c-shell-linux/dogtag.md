# dogtag

## Guide for Dogtag Installation

> RHEL7.5/CentOS env

### steps

* sudo su
* yum udpate
* yum install 389-ds pki-ca

### Install DS

* dnf install -y 389-ds-base

### to install DS instance

edit /etc/hostname

```text
127.0.0.1 localhost localhost.localdomain
::1 localhost localhost.localdomain
10.124.22.60 ca.iokdomain.com ca
```

```text
setup-ds.pl --silent\
 General.FullMachineName=$HOSTNAME\
 General.SuiteSpotUserID=nobody\
 General.SuiteSpotGroup=nobody\
 slapd.ServerPort=389\
 slapd.ServerIdentifier=pki-tomcat\
 slapd.Suffix=dc=example,dc=com\
 slapd.RootDN="cn=Directory Manager"\
 slapd.RootDNPwd=Secret.123
```

### Installing CA

Prepare a deployment configuration file \(e.g. ca.cfg\):

```text
[CA]
pki_admin_email=caadmin@example.com
pki_admin_name=caadmin
pki_admin_nickname=caadmin
pki_admin_password=Secret.123
pki_admin_uid=caadmin

pki_client_database_password=Secret.123
pki_client_database_purge=False
pki_client_pkcs12_password=Secret.123

pki_ds_base_dn=dc=ca,dc=pki,dc=example,dc=com
pki_ds_database=ca
pki_ds_password=Secret.123

pki_security_domain_name=EXAMPLE
```

Optionally, the certificate nicknames can be specified in the following parameters:

```text
pki_ca_signing_nickname=ca_signing
pki_ocsp_signing_nickname=ca_ocsp_signing
pki_audit_signing_nickname=ca_audit_signing
pki_ssl_server_nickname=sslserver # Same nicknames must be specified manually for other subsystems
pki_subsystem_nickname=subsystem  # Same nicknames must be specified manually for other subsystems
```

_**pkispawn -v -f ca.cfg -s CA**_

## Verification

