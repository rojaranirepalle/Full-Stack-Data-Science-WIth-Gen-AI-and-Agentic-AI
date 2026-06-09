##SQL Create Table:
use FSDS;    
create table customers ( ID int primary key,
						 NAME varchar(50),
                         AGE int,
                         ADDRESS varchar(50),
                         SALARY float);
Desc customers;
select ID, NAME, SALARY FROM customers;

##SQL Insert Rows:                         
select * from customers;                         
Insert into customers values(1,'Roja',32,'Hyderabad',10000);   
Insert into customers values(2,'Rani',50,'Hyderabad',5000);
Insert into customers values(3,'Teja',22,'Tenali',7000); 
Insert into customers values(4,'Teja',21,'Chennai',4000);   
Insert into customers values(5,'Prerna',31,'Kerala',9000);  
Insert into customers values(6,'Avinash',33,'Guntur',8000);  
Insert into customers values(7,'Charvik',21,'Delhi',13000);  
                    
##SQL Comparison Operators:
select * from customers where SALARY > 4000;
select * from customers where SALARY = 4000;
select * from customers where SALARY < 7000;
select * from customers where SALARY != 7000;
select * from customers where SALARY <> 7000;
select * from customers where SALARY >= 7000;
select * from customers where name = 'Roja';

##SQL Logical Operators:
select * from customers where SALARY > 4000 and SALARY <=10000;
select * from customers where AGE > 25 OR SALARY <=10000;
select * from customers where AGE IS NOT NULL;
select * from customers where NAME LIKE '%Te%';
select * from customers where SALARY IN(4000,8000);
select * from customers where SALARY BETWEEN 4000 AND 8000;

SELECT AGE FROM CUSTOMERS
WHERE EXISTS (SELECT AGE FROM CUSTOMERS WHERE SALARY > 9500);

SELECT * FROM CUSTOMERS
WHERE AGE > ALL (SELECT AGE FROM CUSTOMERS WHERE SALARY > 6500);

SELECT * FROM CUSTOMERS
WHERE AGE > ANY (SELECT AGE FROM CUSTOMERS WHERE SALARY > 6500);

## SQL Expressions
select * from customers where SALARY = 10000;
select 10+1 as addition;
select count(*) as total_rows from customers;
SELECT CURRENT_TIMESTAMP;
SELECT CURDATE();
SELECT NOW();

## SQL CREATE Database & Tables
create database testdata;
show databases;
use testdata;

CREATE TABLE SALARY AS SELECT ID, SALARY FROM FSDS.CUSTOMERS;
select * from SALARY;
drop table salary;
desc salary;

drop database testdata;
show databases;