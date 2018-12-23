-- 操作表 31-30题
-- source ~/Codes/mysql/hw3.sql
use mydata;

-- 31、查询各科成绩前三名的记录(不考虑成绩并列情况) ；
select course_id as cid,score, from score order by course_id,score desc;

select a.course_id,a.score,count(a.score)as xx from score a
left join score b
on a.course_id=b.course_id AND a.score<b.score
group by a.sid,a.course_id,a.score
having xx<3
order by a.course_id,a.score desc,xx;

-- 32、查询每门课程被选修的学生数；
select course_id,count(student_id) as s_num from score group by course_id;

-- 33、查询选修了2门以上课程的全部学生的学号和姓名；
select * from student where sid in(
select student_id as c_num from score group by student_id having c_num>=2);

-- 34、查询男生、女生的人数，按倒序排列；
select gender,count(*) as c from student group by gender order by c desc;
-- 35、查询姓“张”的学生名单；
select * from student where sname like '张%';
-- 36、查询同名同姓学生名单，并统计同名人数；
select sname,count(*) as c from student group by sname having c >1;
-- 37、查询每门课程的平均成绩，结果按平均成绩升序排列，平均成绩相同时，按课程号降序排列；
select course_id,avg(score) as avg_s from score group by course_id order by avg_s,course_id desc;
-- 38、查询课程名称为“数学”，且分数低于60的学生姓名和分数；
select @cid:=cid from course where cname='数学';
select a.student_id,b.sname,a.score from score as a,student as b where a.course_id=@cid and a.score<60 and a.student_id=b.sid;
-- 39、查询课程编号为“3”且课程成绩在80分以上的学生的学号和姓名；
select * from student where sid in
(select student_id from score where course_id=3 and score>80);
-- 40、求选修了课程的学生人数
select count(*) from (select distinct student_id from score) as a;


-- 41、查询选修“王五”老师所授课程的学生中，成绩最高和最低的学生姓名及其成绩；
select @tid:=tid from teacher where tname='王五';
select @s_max:=max(score),@s_min:=min(score) from 
	(select * from score where course_id in (select cid from course where teacher_id  = @tid)) as a
group by course_id;
select a.student_id,b.sname,a.score from 
(select * from score where course_id in (select cid from course where teacher_id  = @tid)) a,student b 
where a.student_id =b.sid and score = @s_max;
select a.student_id,b.sname,a.score from 
(select * from score where course_id in (select cid from course where teacher_id  = @tid)) a,student b 
where a.student_id =b.sid and score = @s_min;

-- 42、查询各个课程及相应的选修人数；
select a.course_id,b.cname,count(a.student_id) from score a,course b where a.course_id=b.cid 
group by (a.course_id);
-- 43、查询不同课程但成绩相同的学生的学号、课程号、学生成绩；
select a.student_id,a.course_id,b.student_id,b.course_id,a.score 
from score a,score b
where a.course_id!=b.course_id and a.score = b.score and a.student_id!= b.student_id;
-- 44、查询每门课程成绩最好的前两名学生id和姓名；

select a.course_id,a.student_id,a.score,b.sname from
(select * from score c
where (
    select count(*) from score
    where course_id=c.course_id and score>c.score )<2
  ) a,student b
where a.student_id=b.sid
order by course_id,score desc;

-- 45、检索至少选修两门课程的学生学号；

select student_id from score group by student_id having count(course_id) >=2;
-- 46、查询没有学生选修的课程的课程号和课程名；
select * from course where cid not in(
select distinct course_id from score);
-- 47、查询没带过任何班级的老师id和姓名；
select * from teacher where tid not in(
select distinct tid from teach2cls);
-- 48、查询有两门以上课程超过80分的学生id及其平均成绩；
select student_id,avg(score) from score where student_id in
	(select student_id from score where score>80 group by student_id having count(course_id) >=2)
group by student_id;
-- 49、检索“3”课程分数小于60，按分数降序排列的同学学号；
select student_id,score from score where course_id=3 and score<60 order by score desc;
-- 50、删除编号为“2”的同学的“1”课程的成绩；
delete from score where student_id =2 and course_id =1;
-- 51、查询同时选修了物理课和生物课的学生id和姓名；
select @phy:=cid from course where cname='物理';
select @bio:=cid from course where cname='生物';
select * from student where sid in(
select student_id from score where course_id in (@phy,@bio)
group by student_id
having count(course_id)>=2);