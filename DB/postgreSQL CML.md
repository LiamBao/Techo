### login


`sudo -u matrix psql -c "select count(*) from event;"`

-----
#### psql
```bash
matrix@matrix-virtual-machine:~$ sudo -u postgres psql
[sudo] password for matrix:
psql (9.5.14)
Type "help" for help.
postgres=# \l
                                  List of databases
   Name    |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
-----------+----------+----------+-------------+-------------+-----------------------
 matrix    | matrix   | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres  | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres          +
           |          |          |             |             | postgres=CTc/postgres
(4 rows)
postgres=# \c matrix
You are now connected to database "matrix" as user "postgres".
matrix=# \dt event
        List of relations
 Schema | Name  | Type  | Owner
--------+-------+-------+--------
 public | event | table | matrix
(1 row)
```
### Initial Postgresql
```bash
create_database() {
    CMD=$1
    # Create user and database
    sudo -u postgres createuser matrix --no-superuser --no-createdb --no-createrole
    sudo -u postgres createdb matrix --owner=matrix
    sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'cisco123';"
    sudo -u postgres psql -c "ALTER USER matrix WITH PASSWORD 'cisco123';"
    sleep 1
    ver_num="$(ls /etc/postgresql/)"
    if [ -z "$ver_num" ]; then
        printf "failed to get postgresql version path"
        return
    fi
    printf "postgreSQL version : $ver_num "
    #Accept connection from any IP address
    sudo -u postgres echo "listen_addresses = '*'" >> /etc/postgresql/"$ver_num"/main/postgresql.conf
    #To allow connections from absolutely any address with password authentication
    sudo -u postgres echo "host  all  all 0.0.0.0/0 md5" >> /etc/postgresql/"$ver_num"/main/pg_hba.conf
    sleep 1
    sudo /etc/init.d/postgresql restart
    sleep 1
    # Initialize the DB, create and migrate tables.
    cd $SERVER_DIR
    # If directory migrations  exists, remove it. We should regenerate a new one.
    if [ -d "$MIGRATIONS_DIR" ]; then
        rm -rf $MIGRATIONS_DIR
        printf "Remove dir $MIGRATIONS_DIR and postgesql tables to create new"
        run_command "python3 ./db_manage.py db init"
        run_command "python3 ./db_manage.py db migrate"
    fi
    run_command "python3 ./db_manage.py db upgrade"
}
```

---------

### 常用cml

|函数ming|返回类型|描述|
| ----- | ----- |-----|
|pg_column_size(any)|int|存储一个指定的数值需要的字节数（可能压缩过）|
|pg_database_size(oid)|bigint|指定OID的数据库使用的磁盘空间|
|pg_database_size(name)|bigint|指定名称的数据库使用的磁盘空间|
|pg_indexes_size(regclass)|bigint|关联指定表OID或表名的表索引的使用总磁盘空间|
|pg_relation_size(relation regclass, fork text)|bigint|指定OID或名的表或索引，通过指定fork('main', 'fsm' 或'vm')所使用的磁盘空间|
|pg_relation_size(relation regclass)|bigint|pg_relation_size(..., 'main')的缩写|
|pg_size_pretty(bigint)|text|Converts a size in bytes expressed as a 64-bit integer into a human-readable format with size units|
|pg_size_pretty(numeric)|text|把以字节计算的数值转换成一个人类易读的尺寸单位|
|pg_table_size(regclass)|bigint|指定表OID或表名的表使用的磁盘空间，除去索引（但是包含TOAST，自由空间映射和可视映射|
|pg_tablespace_size(oid)|bigint|指定OID的表空间使用的磁盘空间|
|pg_tablespace_size(name)|bigint|指定名称的表空间使用的磁盘空间|
|pg_total_relation_size(regclass)|bigint|指定表OID或表名使用的总磁盘空间，包括所有索引和TOAST数据|

-------


### DB CML

- 查看存储一个指定的数值需要的字节数
`select pg_column_size(1);`
`select pg_column_size(10000);`
`select pg_column_size('david');`
- 查看原始数据
`\d test`
- 数据库大小
`select pg_database_size('matrix');`
- 查看所有数据库大小
`select pg_database.datname, pg_database_size(pg_database.datname) AS size from pg_database; `
`select pg_size_pretty(pg_database_size('matrix'));`
- 查看单索引大小
`select pg_relation_size('idx_matrix');`
`select pg_size_pretty(pg_relation_size('idx_matrix'));`
`select pg_size_pretty(pg_relation_size('idx_join_date_matrix'));`
- 查看指定表中所有索引大小
`select pg_indexes_size('matrix');`
- 查看指定schema 里所有的索引大小，按从大到小的顺序排列。
`select * from pg_namespace;`
`select indexrelname, pg_size_pretty(pg_relation_size(relid)) from pg_stat_user_indexes where schemaname='public' order by pg_relation_size(relid) desc;`
- 查看指定表大小
`select pg_size_pretty(pg_relation_size('event'));`
`select pg_size_pretty(pg_table_size('event'));  `
- 查看指定表的总大小
`select pg_total_relation_size('event');`
`select pg_size_pretty(pg_total_relation_size('event'));`
- 查看指定schema 里所有的表大小，按从大到小的顺序排列。
`select relname, pg_size_pretty(pg_relation_size(relid)) from pg_stat_user_tables where schemaname='public' order by pg_relation_size(relid) desc;`
- 查看表空间大小
`select spcname from pg_tablespace;`
`select pg_size_pretty(pg_tablespace_size('pg_default'));`
`select pg_tablespace_size('pg_default')/1024/1024 as "SIZE M";`
`select pg_tablespace_size('pg_default')/1024/1024/1024 as "SIZE G"; `

### PostgreSQL的性能监控工具pgCluu
[pgCluu](https://github.com/darold/pgcluu)
link: https://github.com/darold/pgcluu
##### Installation
` tar xzf pgcluu-2.x.tar.gz`
`cd pgcluu-2.x/`
`perl Makefile.PL`
`make && sudo make install`
##### pgcluu和pgcluu_collectd这两个程序安装在/usr/local/bin目录下，两个程序都是用perl写的.
`mkdir /tmp/stat_db1/` 代码写死路径,不能修改
`pgcluu_collectd -D -i 60 /tmp/stat_db1/`
`LOG: Detach from terminal with pid: 11323`
-  or
`pgcluu_collectd -D -i 20 /tmp/stat_db1/ -h localhost -U postgres -d matrix`
- 终止:
`pgcluu_collectd -k`
`LOG: Received terminating signal.`
- 生成报告:
`mkdir /tmp/report_db1/`
`pgcluu -o /tmp/report_db1/ /tmp/stat_db1/`
            
上述参数中，`-D`表示后台运行；`-i` 30表示30秒收集一次数据；`/tmp/stat_db1/`是收集数据保存的目录；其他参数表示数据库的地址，用户名和数据库名。由于程序在后台运行，如果需要结束程序需要使用`-k`参数，表示kill掉后台的`pgcluu_collectd`。本文采用的方式是另一种自动退出的方法，即`-E 200`表示程序运行200秒之后自动退出，如下，
`pgcluu_collectd -E 200 -i 30 /tmp/stat_db1/ -h localhost -U postgres -d matrix`
`pgcluu_collectd -i 30 /tmp/stat_db1/ -h localhost -U postgres -d matrix`

-  as postgres user to monitor locally a full PostgreSQL
cluster:
`mkdir /tmp/stat_db1/`
`pgcluu_collectd -D -i 60 /tmp/stat_db1/`

- to collect statistics from pgbouncer too, and limit database statistics to a single database:

`pgcluu_collectd -D -i 60 /tmp/stat_db1/ -h 10.10.1.1 -U postgres -d mydb  --pgbouncer-args='-p 5342'`

- to disable statistics collect between 22:30 and 06:30 the next day:

`pgcluu_collectd -D -i 60 /tmp/stat_db1/ --exclude-time "22:30-06:30" `

- to collect statistics from a remote server:

`pgcluu_collectd -D -i 60 /tmp/stat_db1/ -h 10.0.0.1 -U postgres --disable-sar`

- the same but collecting system statistics using remote sar calls:

`pgcluu_collectd -D -i 60 /tmp/stat_db1/ -h 10.0.0.1 -U postgres --enable-ssh `
 ` --ssh-user postgres --ssh-identity /var/lib/postgresql/.ssh/id_rsa.pub`