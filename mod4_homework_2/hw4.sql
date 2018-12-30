-- 操作表 21-30题
-- source ~/Codes/mysql/hw4.sql
use mydata;

-- 21、查询没有学全所有课的同学的学号、姓名；
select @c_num:=count(cid) from course;
select * from student where sid in
	(select student_id from score group by student_id having count(course_id)<@c_num);
-- 22、查询至少有一门课与学号为“1”的同学所学相同的同学的学号和姓名；
select * from student where sid in
(select distinct student_id from score where student_id!=1 and course_id in (
select course_id from score where student_id=1));
-- 23、查询至少学过学号为“1”同学所选课程中任意一门课的其他同学学号和姓名；
select * from student where sid in
(select distinct student_id from score where student_id!=1 and course_id in (
select course_id from score where student_id=1));
-- 24、查询和“2”号同学学习的课程完全相同的其他同学的学号和姓名；
--     先将选课数目不同的先剔除
--     再把score和2号的课程innner join
--     inner join之后还是课程数目相同的就是要找的
select @c_num:=count(course_id) from score where student_id=2;
select * from student where sid in
	(select distinct c.student_id from
		(select * from 
			(select * from score where student_id in 
				(select student_id from score where student_id!=2 group by student_id having count(course_id)=@c_num)) as b 
			inner join
				(select student_id as ref_sid,course_id as ref_cid from score where student_id =2) as a
			on
			b.course_id=a.ref_cid
		order by b.student_id,b.course_id) as c
	group by student_id
	having count(*)=@c_num);
	
-- 25、删除学习“张三”老师课的score表记录；
set @tid = (select tid from teacher where tname='张三');
drop from score where course_id in
(select cid from course where teacher_id=@tid);
-- 26、向score表中插入一些记录，这些记录要求符合以下条件：①没有上过编号“2”课程的同学学号；②插入“2”号课
-- 程的平均成绩；
delete from score where score=79;
delimiter //
drop procedure  if exists wk;  
create procedure wk(in c_id int)
begin
	declare i int;
	declare s_num int;
	declare avgs int;
	declare s_id_tmp int;
	
	set i = 0;

	set avgs = (select avg(score) from score where course_id=c_id group by course_id);
	
	drop table if exists tmp;
	create table tmp as (select * from student where sid not in
			(select distinct student_id from score where course_id=c_id));
			
	set s_num = (select count(*) from tmp);
	
	while i < s_num do
		set s_id_tmp= (select sid from tmp limit i,1);
		select s_id_tmp,c_id,avgs;
		insert into score(student_id,course_id,score) values(s_id_tmp,c_id,avgs);
		set i = i +1;
	end while;
	drop table tmp;
end//
delimiter ;
call wk(2);

-- 27、按平均成绩从低到高显示所有学生的“语文”、“数学”、“英语”三门的课程成绩，按如下形式显示： 学生ID,语文,
-- 数学,英语,课程数和平均分；
select a.sid,a.chn,b.math,c.eng,(a.chn+b.math+c.eng)/3 as avg from 
(select student_id as sid,course_id as cid,score as chn from score where course_id =1) as a
,
(select student_id as sid,course_id as cid,score as math from score where course_id =2) as b
,
(select student_id as sid,course_id as cid,score as eng from score where course_id =3) as c
where a.sid=b.sid and a.sid=c.sid
order by avg;
-- 28、查询各科成绩最高和最低的分：以如下形式显示：课程ID，最高分，最低分；
select course_id,max(score),min(score) from score group by course_id;
-- 29、按各科平均成绩从低到高和及格率的百分数从高到低顺序；
select course_id,avg(score) as avg_s from score group by course_id order by avg_s;

select a.course_id,a.num,b.pass_num,b.pass_num/a.num as pass_ratio from
(select course_id,count(score) as num from score group by course_id) as a
left join
(select course_id,count(score) as pass_num from score where score >=60 group by course_id) as b
on a.course_id = b.course_id
order by pass_ratio;
-- 30、课程平均分从高到低显示（现实任课老师）；
select c.tid,c.avg_s from
	(select a.course_id as cid,a.avg_s,b.teacher_id as tid from
		(select course_id,avg(score) as avg_s from score group by course_id order by avg_s) as a
		left join course as b
	on a.course_id = b.cid) as c
order by avg_s desc;
	
	