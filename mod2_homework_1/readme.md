# 员工信息增删改查程序

## 作业完成情况
在实现原本的四个需求的同时，增加以下功能：
+ DESC Table_name
+ 可以模板化配置新命令，同时不必变更命令解析函数
+ set部分支持同时修改多个字段
+ where部分支持更复杂的逻辑运算表达式

例如：
```
execute('desc staff_table')
execute('find name,age from staff_table where age > 22')
execute('find name,age from staff_table where (age >= 23 and dept=\'IT\') or name = \'Alex Li\'')
execute('UPDATE staff_table SET age=25,name=Ding Dong WHERE name = "Alex Li"')
execute('UPDATE staff_table SET age=25,dep=W.C. WHERE name = "Alex Li"')
execute('del from staff_table where staff_id=3')
execute('add staff_table with Alex Li,25,134435344,IT,2015‐10‐29')
```

## 需求如下
### 员工信息表

staff_id | name | age | phone |dept | eroll_date
---------|------|-----|-------|-----|-----------
1        | Alex | 22|  12345678|IT| 2013-12-03
2        | Tom  | 12|  12433278|Security| 2013-12-03
3        | Jerry | 5|  12345678|Supply| 2013-12-03
4        | Donald| 42|  12345678|Market| 2013-12-03

### 以这样的方式存储在文件里面
    
    1,Alex Li,22,13651054608,IT,2013‐04‐01
    2,Jack Wang,28,13451024608,HR,2015‐01‐07
    3,Rain Wang,21,13451054608,IT,2017‐04‐01
    4,Mack Qiao,44,15653354208,Sales,2016‐02‐01
    5,Rachel Chen,23,13351024606,IT,2013‐03‐16
    6,Eric Liu,19,18531054602,Marketing,2012‐12‐01
    7,Chao Zhang,21,13235324334,Administration,2011‐08‐08
    8,Kevin Chen,22,13151054603,Sales,2013‐04‐01
    9,Shit Wen,20,13351024602,IT,2017‐07‐03
    10,Shanshan Du,26,13698424612,Operation,2017‐07‐02
    



### 支持如下操作
1. 可进行模糊查询，语法至少支持下面3种查询语法:
    ```
    find name,age from staff_table where age > 22
    find * from staff_table where dept = "IT"
    find * from staff_table where enroll_date like "2013"
    ```
2. 可创建新员工纪录，以phone做唯一键(即不允许表里有手机号重复的情况)，staff_id需自增
    ```
    add staff_table Alex Li,25,134435344,IT,2015‐10‐29
    ```
3. 可删除指定员工信息纪录，输入员工id，即可删除
    ```
    del from staff where id=3
    ```
4. 可修改员工信息，语法如下:
    ```
    UPDATE staff_table SET dept="Market" WHERE dept = "IT" 把所有dept=IT的纪录的dept改成Market
    UPDATE staff_table SET age=25 WHERE name = "Alex Li" 把name=Alex Li的纪录的年龄改成25
    ```
5. 以上每条语名执行完毕后，要显示这条语句影响了多少条纪录。 比如查询语句 就显示 查询出了多少条、
修改语句就显示修改了多少条等。
* 注意：以上需求，要充分使用函数，请尽你的最大限度来减少重复代码！* 