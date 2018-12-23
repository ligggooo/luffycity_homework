-- 操作表 1-10题
-- source ~/Codes/mysql/hw2.sql
use mydata;
-- 1、自行创建测试数据；
--   在hw1.sql中完成
-- 2、查询学生总人数；
select count(*) from student;
-- 3、查询“生物”课程和“物理”课程成绩都及格的学生id和姓名；

set @phy = (select cid from course where cname = '物理');
set @bio = (select cid from course where cname = '生物');
select sid,sname from student where sid in
	(select bio_score.student_id from
		(select student_id,score from score where course_id = @bio and score >=60) as bio_score
			inner join
		(select student_id,score from score where course_id = @phy and score >=60) as phy_score
			on
		bio_score.student_id = phy_score.student_id
);
-- 4、查询每个年级的班级数，取出班级数最多的前三个年级；
select a.grade_id,b.gname,a.class_num 
from 
	(select grade_id,count(cid) as class_num from class group by grade_id) as a
		left join
	class_grade as b
		on
	a.grade_id= b.gid
order by class_num desc
limit 3;
-- 5、查询平均成绩最高和最低的学生的id和姓名以及平均成绩；
(select student_id,avg(score) as avs from score group by student_id order by avs desc limit 1)
union
(select student_id,avg(score) as avs from score group by student_id order by avs limit 1);
-- 6、查询每个年级的学生人数；
select c.gid,sum(c.class_cap) as cap from
	(select a.grade_id as gid,b.class_cap from 
		class as a,
		(select class_id,count(sid) as class_cap from student group by class_id) as b
		where a.cid=b.class_id
	) as c
group by gid;
-- 7、查询每位学生的学号，姓名，选课数，平均成绩；
select c.sid,c.sname,count(c.course_id)as course_num,avg(c.score) as avg_score from
	(select b.sid,b.sname,a.course_id,a.score from
		score as a,student as b
	where a.student_id=b.sid) as c
group by c.sid,c.sname;
-- 8、查询学生编号为“2”的学生的姓名、该学生成绩最高的课程名、成绩最低的课程名及分数；
set @no = 2;
set @course_max_score=(select max(a.score) from (select student_id,course_id,score from score 
					where student_id=@no) as a group by a.student_id);
set @course_min_score=(select min(a.score) from (select student_id,course_id,score from score 
					where student_id=@no) as a group by a.student_id);


select a.sid,a.sname,c.cname,b.score from
	(student as a
		join
	((select student_id,course_id,score from score where student_id=@no and score=@course_max_score)
	union all
	(select student_id,course_id,score from score where student_id=@no and score=@course_min_score)) as b
		on a.sid = b.student_id)
		join
	course as c
		on c.cid = b.course_id
	order by score desc;
-- 9、查询姓“李”的老师的个数和所带班级数；

select count(*) from teach2cls where tid in (select tid from teacher where tname like '李%');
-- 10、查询班级数小于5的年级id和年级名；
select a.grade_id,b.gname,a.class_num 
from 
	(select grade_id,count(cid) as class_num from class group by grade_id) as a
		left join
	class_grade as b
		on
	a.grade_id= b.gid
where class_num <5
order by class_num desc
limit 3;

