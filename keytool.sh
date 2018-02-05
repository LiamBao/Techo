#!/bin/sh

#  keytool.sh
#  
#
#  Created by LIamBao
#  
# Retrieve the Fingerprint of CA certificate
if [ -z "${path}" ] || [ -z "${file}" ]; then
    print "$cmd_fail - missing CA certificate path to retrieve fingerprint"
    exit 0
else
    result="$($keytool -printcert -file "${0}"/"${1}" | egrep SHA1 | cut -d ':' -f 2- -s)"
    if [ -z "$result" ]; then
        printf "$cmd_fail - unable to retrieve CA certificate SHA1 fingerprint."
        exit 0
    fi
fi
finger="$(echo $result | sed 's/://g')"



##查看单个证书
#Keytool 是一个数据证书的管理工具 ,Keytool将密钥（key）和证书（certificates）存在一个称为keystore的文件中在keystore里，
#包含两种数据:密钥实体（Key entity）-密钥（secret key）或者是私钥和配对公钥（采用非对称加密）可信任的证书实体（trusted certificate entries）-只包含公钥.

ca_issuer="$(keytool -printcert -file $path/ca_cert.cer | sed -n 's/Issuer:.*CN=\([^,\ ]*\).*/\1/p' | tr -d '\b\n\r')"

