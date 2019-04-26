# Postgresql Query

[http://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL\_GetStarted.html](http://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html)

[https://blog.csdn.net/zhwzju/article/details/49636817](https://blog.csdn.net/zhwzju/article/details/49636817) _\*_分片

* [\(递归）CTE 通用表表达式](http://www.jasongj.com/sql/cte/)
* [使用PostgreSQL进行复杂查询](http://zealscott.com/posts/6785/)
* [高级SQL特性](https://yq.aliyun.com/articles/626536)
* [从PostgreSQL json中提取数组](https://github.com/digoal/blog/blob/master/201609/20160910_01.md)
* * * * 
```text
ALTER TABLE assets
    ALTER COLUMN location TYPE VARCHAR,
    ALTER COLUMN description TYPE VARCHAR;
```

* Create a view

  \`\`\`sql

  CREATE VIEW myview AS

    SELECT city, temp\_lo, temp\_hi, prcp, date, location

  ```text
    FROM weather, cities
    WHERE city = name;
  ```

SELECT \* FROM myview;

```text
```sql
SELECT depname, empno, salary,
       rank() OVER (PARTITION BY depname ORDER BY salary DESC) FROM empsalary;
```

Output:

```text
depname  | empno | salary | rank
-----------+-------+--------+------
 develop   |     8 |   6000 |    1
 develop   |    10 |   5200 |    2
 develop   |    11 |   5200 |    2
 develop   |     9 |   4500 |    4
 develop   |     7 |   4200 |    5
 personnel |     2 |   3900 |    1
 personnel |     5 |   3500 |    2
 sales     |     1 |   5000 |    1
 sales     |     4 |   4800 |    2
 sales     |     3 |   4800 |    2
(10 rows)
```

* `ssh matrix@10.79.44.52`

```sql
SELECT * FROM event
WHERE eui64 IN (
    SELECT eui64 FROM (
        (SELECT eui64, count(etime_stamp) as stamp  FROM event
            WHERE eui64 IN (
                SELECT eui64 from (
                    SELECT eui64 ,COUNT(eui64) as count
                    FROM event GROUP BY eui64 ORDER BY count DESC LIMIT 10 OFFSET 0)a
            )
        GROUP BY eui64 ORDER BY stamp DESC LIMIT 1))b
         )  and event_id like '%DHCP%'


ORDER BY etime_stamp LIMIT 1000 OFFSET 0


select * from event
        where event_id like '%PANID%'
        limit 10000

SELECT event_id , count(*) as count FROM event
        WHERE eui64='00173b09010001a4'
        group by event_id order by count desc
```

## JSON vs JSONB Operation

```sql
select * from event
where  event_opts->0->'opt_data'->'sac_addr'
@> '"00173b0101000018"'::jsonb;

select * from event
where  event_opts->0->'opt_data'->'sac_addr'='"00173b0101000018"';

SELECT data->'title' FROM books WHERE data->'genres' @> '["Fiction"]'::jsonb;

select jsonb '{"a":1, "b": {"c":[1,2,3], "d":["k","y","z"]}, "d":"kbc"}' @> '{"b":{"c":[2]}}'
```

* 存在，JSON中是否存在某个KEY，某些KEY，某些KEY的任意一个
  * 存在某个KEY\(TOP LEVEL\) `'{"a":1, "b":2}'::jsonb ? 'b'`
  * 存在所有KEY `'{"a":1, "b":2, "c":3}'::jsonb ?& array['b', 'c']`
  * 存在任意KEY、元素 '\["a", "b"\]'::jsonb ?\| array\['a', 'b'\]
* 等值 JSON中是否存在指定的key:value对（支持嵌套JSON） `'{"a":1, "b":2}'::jsonb @> '{"b":2}'::jsonb`
* 包含，JSON中某个路径下的VALUE（数组）中，是否包含指定的所有元素 `select jsonb '{"a":1, "b": {"c":[1,2,3], "d":["k","y","z"]}, "d":"kbc"}' @> '{"b":{"c":[2,3]}}';`
* 相交，JSON中某个路径下的VALUE（数组）中，是否包含指定的任意元素

  ```text
    select jsonb '{"a":1, "b": {"c":[1,2,3], "d":["k","y","z"]}, "d":"kbc"}' @> '{"b":{"c":[2]}}'
    or
    jsonb '{"a":1, "b": {"c":[1,2,3], "d":["k","y","z"]}, "d":"kbc"}' @> '{"b":{"c":[3]}}'
    ;
  ```

  或\(注意1,2,3需要双引号，作为text类型存储，因为操作符?\| ?&暂时只支持了text\[\]，如果是numeric匹配不上\)

  ```text
    select jsonb '{"a":1, "b": {"c":["1","2","3"], "d":["k","y","z"]}, "d":"kbc"}' -> 'b' -> 'c' ?& array['2','3','4'] ;
    select jsonb '{"a":1, "b": {"c":["1","2","3"], "d":["k","y","z"]}, "d":"kbc"}' -> 'b' -> 'c' ?| array['2','3','4'] ;
  ```

* 范围查找，JSON中某个路径下的VALUE，是否落在某个范围内

  ```text
    (js ->> 'key1' )::numeric between xx and xx

    (js ->> 'key2' )::numeric between xx and xx
  ```

select \* from event where event\_opts-&gt;0-&gt;'opt\_data'-&gt;'sac\_addr' @&gt; '"00173b0101000018"'::jsonb;

select \* from event where event\_opts-&gt;0-&gt;'opt\_data'-&gt;'sac\_addr'='"00173b0101000018"';

SELECT data-&gt;'title' FROM books WHERE data-&gt;'genres' @&gt; '\["Fiction"\]'::jsonb;

select pg\_typeof\(col\), jsonb\_typeof\(col\),col from \(select event\_opts col from event\) t;

select json\_each\('{\[1,2,3,"d":{"f1":1,"f2":\[5,6\]},4\]}'\); select jsonb\_each\('{"a":"foo", "b":"bar"}'\);

select pg\_typeof\('{"a":\[1,2,3\],"b":\[4,5,6\]}'::json-&gt;&gt;'a'\), '{"a":\[1,2,3\],"b":\[4,5,6\]}'::json-&gt;&gt;'a';

select \* from event where json\_arr2int\_arr\( event\_opts-&gt;0-&gt;'opt\_data'-&gt;'sac\_addr'\) @&gt; array\['0xFFFF'\];

SELECT array\(select \(json\_array\_elements\_text\('{"a":"B","b":\[1,2,3,4,5,6\]}'::json-&gt;'b'\)\)::int \); SELECT array\(select json\_array\_elements\_text\('{"a":"B","b":\[1,2,3,4,5,6\]}'::json-&gt;'b'\)\);

create extension ltree;

select \* from pg\_extension ;

* 验证数据库设置类型及数据类型

   `select pg_typeof(col), jsonb_typeof(col),col from (select event_opts col from event) t;`

* **给出那些所有temp\_lo值曾都低于 40的城市。最后，如果我们只关心那些名字以“S”开头的城市，我们可以用：**

  ```sql
  SELECT city, max(temp_lo)
   FROM weather
   WHERE city LIKE 'S%'
   GROUP BY city
   HAVING max(temp_lo) < 40;
  ```

  理解聚集和SQL的WHERE以及HAVING子句之间的关系对我们非常重要。WHERE和HAVING的基本区别如下：WHERE在分组和聚集计算之前选取输入行（因此，它控制哪些行进入聚集计算）， 而HAVING在分组和聚集之后选取分组行。因此，WHERE子句不能包含聚集函数； 因为试图用聚集函数判断哪些行应输入给聚集运算是没有意义的。相反，HAVING子句总是包含聚集函数（严格说来，你可以写不使用聚集的HAVING子句， 但这样做很少有用。同样的条件用在WHERE阶段会更有效\)

  在前面的例子里，我们可以在WHERE里应用城市名称限制，因为它不需要聚集。这样比放在HAVING里更加高效，因为可以避免那些未通过 WHERE检查的行参与到分组和聚集计算中。

* **需要获取一个问题列表，这个问题列表的排序方式是分为两个部分，第一部分是一个已有的数组\[0,579489,579482,579453,561983,561990,562083\] 第二个部分是按照id进行排序，但是需要过滤掉前面已有的数组**

  ```sql
  select * from question q join (
   select * from unnest(
       array_cat( ARRAY[0,579489,579482,579453,561983,561990,562083]::integer[], (
           select array(
               select id from question where id not in (0,579489,579482,579453,561983,561990,562083) and status in (1, -1) and created_at > 1426131436 order by id desc offset 0 limit 10
           )
       )::integer[] )
   ) WITH ORDINALITY as ids(id, rn)
  ) as tmp on q.id = tmp.id order by tmp.rn
  ```

  一个是unnest函数，是将一个array变成一个多行的子查询结果。

  一个是WITH ORDINALITY，这个函数是只在pg9.4中才增加的函数，和unnest一起使用能返回对应的数组和在数组中的排序

* **有个字段是content，content 里面存储的是双层json，即**

{"title": "testtest", "content": "{"id":23,"qid":580585, "content":"\u8fd9\u4e2a\u662f\u8ffd\u95ee"}"}

现在我要获取按照解析后的qid进行排序分页的结构。

使用了json -&gt;&gt; 符号

语句实现如下：

```sql
select a.question_id, max(is_read) as is_read from (
    select id, is_read, (content::json->>'content')::json->>'qid' as question_id
    from inbox where receiver=1
) a group by a.question_id order by a.question_id desc offset 0 limit 10
```

这里的json-&gt;&gt;直接使用了两层解析结构

## PostgreSQL 树状数据存储与查询\(非递归\)

> [https://github.com/digoal/blog/blob/master/201105/20110527\_01.md](https://github.com/digoal/blog/blob/master/201105/20110527_01.md)

```sql
select * from tbl_music
order by song;

create table tbl_music(id serial4,song ltree not null);
insert into tbl_music (song) values ('GangTai.NanGeShou.LiuDeHua.AiNiYiWanNian');
insert into tbl_music (song) values ('GangTai.NanGeShou.LiuDeHua.JinTian');
insert into tbl_music (song) values ('GangTai.NanGeShou.LiuDeHua.WangQinShui');
insert into tbl_music (song) values ('GangTai.NanGeShou.ZhangXueYou.WenBie');
insert into tbl_music (song) values ('GangTai.NanGeShou.ZhangXueYou.QingShu');
insert into tbl_music (song) values ('GangTai.NvGeShou.ZhenXiuWen.MeiFeiSeWu');
insert into tbl_music (song) values ('GangTai.NvGeShou.ZhenXiuWen.ZhongShenMeiLi');
insert into tbl_music (song) values ('DaLu.NanGeShou.DaoLang.2002NianDeDiYiChangXue');
insert into tbl_music (song) values ('DaLu.NvGeShou.FanBinBin.FeiNiao');

select subltree(song,0,4) from tbl_music where subltree(song,2,3)='LiuDeHua';

select distinct subltree(song,2,3) from tbl_music where song <@
(select  subpath(song,0,2) from tbl_music where subltree(song,2,3)='LiuDeHua' limit 1);
```

-

```sql
create table tbl (
  uid int8 primary key,  -- 用户ID
  pid int8               -- 直接上游ID,如果一个用户是ROOT用户，则PID为 null
);

create index idx_tbl_1 on tbl (pid);

create or replace function gen_pid(int8) returns int8 as $$
  -- 生成它的上游ID，2w以内的ID为根ID。其他都取比它小2w对应的那个ID，形成一颗50级的树。
  select case when $1<=20000 then null else $1-20000 end;
$$ language sql strict;

-- 写入100w数据，形成深度为50的树。
insert into tbl select id, gen_pid(id) from generate_series(1,1000000) t(id) on conflict do nothing;

select count(0) from tbl;
select * from tbl order by uid desc limit 100 ;


with recursive tmp as (select * from tbl where uid=992999
union all
select tbl.* from tbl join tmp on (tmp.pid=tbl.uid))
select uid,pid from tmp where pid is null or uid=992999;


with recursive tmp as (select * from tbl where uid=992999
union all
select tbl.* from tbl join tmp on (tmp.pid=tbl.uid))
select uid,pid from tmp;

\set uid random(1,10000)
with recursive tmp as (select * from tbl where uid=:uid
union all
select tbl.* from tbl join tmp on (tmp.pid=tbl.uid))
select uid,pid from tmp where pid is null or uid=:uid;
```

```text
create table a(id int primary key, info text);

create table b(id int primary key, aid int, crt_time timestamp);
create index b_aid on b(aid);

-- a表插入1000条
insert into a select generate_series(1,1000), md5(random()::text);

-- b表插入500万条，只包含aid的500个id。
insert into b select generate_series(1,5000000), generate_series(1,500), clock_timestamp();


select * from b
limit 100

select a.id from a left join b on (a.id=b.aid) where b.* is null;

select * from a where id not in
(
with recursive skip as (
  (
    select min(aid) aid from b where aid is not null
  )
  union all
  (
    select (select min(aid) aid from b where b.aid > s.aid and b.aid is not null)
      from skip s where s.aid is not null
  )
)
select aid from skip where aid is not null
);
```

