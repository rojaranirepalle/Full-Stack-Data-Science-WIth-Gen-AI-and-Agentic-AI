## SQL AND and OR Operators
use FSDS;
select * from customers where AGE > 32 and SALARY >5000;
select * from customers where AGE > 32 or SALARY >5000;

select name,age from customers where AGE > 32 or SALARY >5000;

## SQL UPDATE Query
update customers set age=24 where age=21;

## SQL Delete Query
delete from customers where age=18;

## Wildcards
select * from customers where name like '%Ro%';
select * from customers where ADDRESS like '%Hyd%';
select * from customers where ADDRESS like 'Hyd%';
select * from customers where ADDRESS like '_e%';
select * from customers where SALARY like '_0%';
## Finds any values that start with 2 and are at least 3 characters in length
select * from customers where SALARY like '2___%';

## SQL Limit Clause
select * from customers limit 3;
select * from customers limit 1,3;
select * from customers limit 3,3;

## SQL ORDER BY Clause
select * from customers order by name;
select * from customers order by salary;
select * from customers order by salary desc;

## SQL Group By
select sum(salary) from customers group by salary order by salary;
select address,sum(salary) from customers group by address order by address;

## SQL Distinct Keyword
select distinct address from customers;
select distinct address,name from customers;
select distinct address,name,salary from customers order by address;

## SQL SORTING Results
select * from customers order by name asc;
select * from customers order by name,salary asc;

## Custom ordering

SELECT * FROM CUSTOMERS
ORDER BY (CASE ADDRESS
WHEN 'Delhi' THEN 1
WHEN 'Guntur' THEN 20
WHEN 'Hyd' THEN 30
WHEN 'Kerala' THEN 4
WHEN 'Tenali' THEN 5
ELSE 100 END) ASC, ADDRESS DESC;