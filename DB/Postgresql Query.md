http://www.ntu.edu.sg/home/ehchua/programming/sql/PostgreSQL_GetStarted.html

https://blog.csdn.net/zhwzju/article/details/49636817 分片


ALTER TABLE assets 
    ALTER COLUMN location TYPE VARCHAR,
    ALTER COLUMN description TYPE VARCHAR;
    
    

- `ssh matrix@10.79.44.52`

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

----


> - **给出那些所有temp_lo值曾都低于 40的城市。最后，如果我们只关心那些名字以“S”开头的城市，我们可以用：**
```sql
SELECT city, max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'
    GROUP BY city
    HAVING max(temp_lo) < 40;
```
理解聚集和SQL的WHERE以及HAVING子句之间的关系对我们非常重要。WHERE和HAVING的基本区别如下：WHERE在分组和聚集计算之前选取输入行（因此，它控制哪些行进入聚集计算）， 而HAVING在分组和聚集之后选取分组行。因此，WHERE子句不能包含聚集函数； 因为试图用聚集函数判断哪些行应输入给聚集运算是没有意义的。相反，HAVING子句总是包含聚集函数（严格说来，你可以写不使用聚集的HAVING子句， 但这样做很少有用。同样的条件用在WHERE阶段会更有效)
在前面的例子里，我们可以在WHERE里应用城市名称限制，因为它不需要聚集。这样比放在HAVING里更加高效，因为可以避免那些未通过 WHERE检查的行参与到分组和聚集计算中。

----


> - **需要获取一个问题列表，这个问题列表的排序方式是分为两个部分，第一部分是一个已有的数组[0,579489,579482,579453,561983,561990,562083] 第二个部分是按照id进行排序，但是需要过滤掉前面已有的数组**
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


> - **有个字段是content，content 里面存储的是双层json，即**

{"title": "testtest", "content": "{"id":23,"qid":580585, "content":"\u8fd9\u4e2a\u662f\u8ffd\u95ee"}"}

现在我要获取按照解析后的qid进行排序分页的结构。

使用了json ->> 符号

语句实现如下：
```sql
select a.question_id, max(is_read) as is_read from (
    select id, is_read, (content::json->>'content')::json->>'qid' as question_id
    from inbox where receiver=1
) a group by a.question_id order by a.question_id desc offset 0 limit 10
```
这里的json->>直接使用了两层解析结构


#### 