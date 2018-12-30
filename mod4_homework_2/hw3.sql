-- 操作表 11-20题
-- source ~/Codes/mysql/hw3.sql
use mydata;

-- 11、查询班级信息，包括班级id、班级名称、年级、年级级别(12为低年级，34为中年级，56为高年级)，示例结果
-- 如下；
-- 				班级id，	班级名称，	年级，		年级级别
-- 				1，			一年一班，	一年级 ， 	低
select cid,caption,class_grade.gname,
		(case
			when grade_id in (1,2) then '低'
			when grade_id in (3,4) then '中'
			when grade_id in (5,6) then '高'
		end
		) as grade_level
	from class,class_grade
	where class.grade_id = class_grade.gid;

-- 12、查询学过“张三”老师2门课以上的同学的学号、姓名；
set @tid = (select tid from teacher where tname='张三');
select * from student where sid in 
	(select student_id from
		(select * from score where 
			course_id in (select cid from course where teacher_id = @tid)
			and
			score >=60) as s
		group by student_id
		having count(course_id)>=2);
-- 13、查询教授课程超过2门的老师的id和姓名；
select * from teacher where tid in
	(select teacher_id from course group by teacher_id having count(cid) >=2);
-- 14、查询学过编号“1”课程和编号“2”课程的同学的学号、姓名；
select * from student where sid in
	(select distinct student_id from score where course_id in (1,2));
-- 15、查询没有带过高年级的老师id和姓名；
select * from teacher where tid not in  -- 非高年级老师
	(select tid from teach2cls where cid in  -- 高年级老师
		(select cid from class where grade_id >=5)); -- 高年级班
-- 16、查询学过“张三”老师所教的所有课的同学的学号、姓名；
set @tid = (select tid from teacher where tname='张三');
select * from student where sid in 
	(select student_id from score where course_id in 
		(select cid from course where teacher_id=@tid));
-- 17、查询带过超过2个班级的老师的id和姓名；
select * from teacher where tid in
	(select tid from teach2cls group by tid having count(cid) >=2);
-- 18、查询课程编号“2”的成绩比课程编号“1”课程低的所有同学的学号、姓名；
select * from student where sid in
	(select sid from
		(select a.sid,a.s_1,b.s_2 from
			(select student_id as sid,score as s_1 from score where course_id=1) as a
			inner join
			(select student_id as sid,score as s_2 from score where course_id=2) as b
			on a.sid=b.sid) as c
	where s_1>s_2);
-- 19、查询所带班级数最多的老师id和姓名；
select * from teacher where tid in
	(select tid from teach2cls group by tid 
	having count(cid)=(
		select max(a.c_num) from( select count(cid) as c_num from teach2cls group by tid) as a));
-- 20、查询有课程成绩小于60分的同学的学号、姓名；
select * from student where sid in
(select distinct student_id from score where score <60);