# RemoteLoginPostgresql

1. 修改postgresql.conf

   postgresql.conf存放位置在/etc/postgresql/9.x/main下，这里的x取决于你安装PostgreSQL的版本号，编辑或添加下面一行，使PostgreSQL可以接受来自任意IP的连接请求。

   listen\_addresses = '\*'

2. 修改pg\_hba.conf

   pg\_hba.conf，位置与postgresql.conf相同，虽然上面配置允许任意地址连接PostgreSQL，但是这在pg中还不够，我们还需在pg\_hba.conf中配置服务端允许的认证方式。任意编辑器打开该文件，编辑或添加下面一行。

   **TYPE  DATABASE  USER  CIDR-ADDRESS  METHOD**

   host  all  all 0.0.0.0/0 md5

   默认pg只允许本机通过密码认证登录，修改为上面内容后即可以对任意IP访问进行密码验证。对照上面的注释可以很容易搞明白每列的含义，具体的支持项可以查阅文末参考引用。

   完成上两项配置后执行

   sudo service postgresql restart

psql -h 10.124.12.24 -p 5432 -U postgres -d mydb

sudo chown -R matrix:matrix /opt/1. 修改postgresql.conf postgresql.conf存放位置在/etc/postgresql/9.x/main下，这里的x取决于你安装PostgreSQL的版本号，编辑或添加下面一行，使PostgreSQL可以接受来自任意IP的连接请求。 listen\_addresses = '\*' 2. 修改pg\_hba.conf pg\_hba.conf，位置与postgresql.conf相同，虽然上面配置允许任意地址连接PostgreSQL，但是这在pg中还不够，我们还需在pg\_hba.conf中配置服务端允许的认证方式。任意编辑器打开该文件，编辑或添加下面一行。

## TYPE  DATABASE  USER  CIDR-ADDRESS  METHOD

host all all 0.0.0.0/0 md5 默认pg只允许本机通过密码认证登录，修改为上面内容后即可以对任意IP访问进行密码验证。对照上面的注释可以很容易搞明白每列的含义，具体的支持项可以查阅文末参考引用。 完成上两项配置后执行 sudo service postgresql restart

psql -h 10.124.12.24 -p 5432 -U postgres -d mydb

sudo chown -R matrix:matrix /opt/

