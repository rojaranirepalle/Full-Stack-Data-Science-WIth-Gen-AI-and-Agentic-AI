use FSDS;
SELECT * FROM student;

## Select Clause
select NAME from student;
select NAME,id from student;

## Where Clause
select * from student where id =4;

## Insert
insert into student values(4,'Roja','Hyd',87);

## Update
update student set address = "Tenali" where id =4;
SELECT * FROM student;

## Alter Tables / DDL 
alter table student add phone_num int;
desc student;

update student set phone_num=123;
update student set phone_num=456 where id=1;

alter table student modify name varchar(60);
desc student;

alter table student drop column phone_num;
desc student;

SELECT * FROM student;

## Delete Rows
delete from student where name="Roja";
SELECT * FROM student;

insert into student values('Roja',1,'Hyd',87);

## SQL Functions
select sum(marks) from student;
select avg(marks) from student;
select count(marks) from student;
select max(marks) from student;
select min(marks) from student;

select * from student order by marks;
select * from student order by marks desc;

## Wildcards % & _

## 2nd character as a in the name
select * from student where name like '_a%';
## Name starts with A
select * from student where name like 'a%';