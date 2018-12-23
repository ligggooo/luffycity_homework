-- 建表和配置表
-- source ~/Codes/mysql/hw1.sql
drop database if exists mydata;
create database mydata;
use mydata;

-- 1, class
drop table if exists class;
CREATE TABLE class(
	cid int primary key,
	caption char(20) not null,
	grade_id int
);
-- insert into class values
	-- (1,'一年一班',1),
	-- (2,'二年一班',2),
	-- (3,'三年一班',3),
	-- (4,'四年一班',4),
	-- (5,'五年一班',5),
	-- (6,'六年一班',6),
	-- (7,'一年一班',1);
LOAD DATA INFILE '/home/goodwillie/data/data/class.csv' INTO TABLE class FIELDS TERMINATED BY ',';

-- 2, student
drop table if exists student;
CREATE TABLE student(
	sid int primary key,
	sname char(20) not null,
	gender enum('男','女') not null,
	class_id int
);
-- insert into student values
	-- (1,'乔丹','女',1),
	-- (2,'艾弗森','女',1),
	-- (3,'科比','男',2),
	-- (4,'叉叉','男',5);
LOAD DATA INFILE '/home/goodwillie/data/data/student.csv' INTO TABLE student FIELDS TERMINATED BY ',';

-- 3, teacher
drop table if exists teacher;
CREATE TABLE teacher(
	tid int primary key,
	tname varchar(20) not null
);
-- insert into teacher values
	-- (1,'张三'),
	-- (2,'李四'),
	-- (3,'王五');
LOAD DATA INFILE '/home/goodwillie/data/data/teacher.csv' INTO TABLE teacher FIELDS TERMINATED BY ',';
	
-- 4, course
drop table if exists course;
CREATE TABLE course(
	cid int primary key,
	cname char(20) not null,
	teacher_id int
);
-- insert into course values
	-- (1,'生物',1),
	-- (2,'体育',1),
	-- (3,'物理',2);
LOAD DATA INFILE '/home/goodwillie/data/data/course.csv' INTO TABLE course FIELDS TERMINATED BY ',';

-- 5, score
drop table if exists score;
CREATE TABLE score(
	sid int primary key auto_increment,
	student_id int,
	course_id int,
	score int
);
-- insert into score values
	-- (1,1,1,60),
	-- (2,1,2,59),
	-- (3,2,2,99),
	-- (4,1,3,61),
	-- (5,2,1,75);
LOAD DATA INFILE '/home/goodwillie/data/data/score.csv' INTO TABLE score FIELDS TERMINATED BY ',';
	
-- 6, class_grade
drop table if exists class_grade;
CREATE TABLE class_grade(
	gid int primary key,
	gname char(20) not null
);
-- insert into class_grade values
	-- (1,'一年级'),
	-- (2,'二年级'),
	-- (3,'三年级');
LOAD DATA INFILE '/home/goodwillie/data/data/class_grade.csv' INTO TABLE class_grade FIELDS TERMINATED BY ',';

-- 7, teach2cls
drop table if exists teach2cls;
CREATE TABLE teach2cls(
	tcid int primary key,
	tid int,
	cid int
);
-- insert into teach2cls values
	-- (1,1,1),
	-- (2,1,2),
	-- (3,2,1),
	-- (4,3,2);
LOAD DATA INFILE '/home/goodwillie/data/data/teach2cls.csv' INTO TABLE teach2cls FIELDS TERMINATED BY ',';
	
-- 8, 加外键
alter table class add constraint a foreign key(grade_id) references class_grade(gid) on delete cascade on update cascade; -- 班级表外键
alter table student add constraint b foreign key(class_id) references class(cid) on delete cascade on update cascade; -- 学生表外键
alter table course add constraint c foreign key(teacher_id) references teacher(tid) on delete cascade on update cascade; -- 课程表外键
alter table score add constraint d1 foreign key(student_id) references student(sid) on delete cascade on update cascade,
add constraint d2 foreign key(course_id) references course(cid) on delete cascade on update cascade; -- 成绩表外键
alter table teach2cls add constraint e1 foreign key(tid) references teacher(tid) on delete cascade on update cascade, 
add constraint e2 foreign key(cid) references class(cid) on delete cascade on update cascade; -- 任职表外键

-- alter table score modify sid int auto_increment;
