## Joins
use FSDS;
select * from customers;

create table customer_order(
             oid int primary key auto_increment,
			 cid int,
             pname varchar(50),
             row_total float);
insert into customer_order values (1,1,'Pen',10);  
insert into customer_order values (2,3,'Pen',10);   
insert into customer_order values (3,3,'Box',100);  
insert into customer_order values (4,6,'Pencil',5);   
insert into customer_order values (5,8,'Cookies',20);  
insert into customer_order values (6,7,'Chocolate',20); 

select * from customers;
select * from customer_order;	

## Inner Join  - Common records
select * from customers as c
			  inner join customer_order as co
              on c.id=co.cid;
              
select * from customer_order as co
			  inner join customers as c
              on co.cid=c.id;

## Left Join  - 1st table records            
select * from customers as c
			  left join customer_order as co
              on c.id=co.cid;
              
select * from customer_order as co
			  left join customers as c
              on co.cid=c.id;
              
## Right Join  - 2nd table records  
select * from customers as c
			  right join customer_order as co
              on c.id=co.cid;
              
select * from customer_order as co
			  right join customers as c
              on co.cid=c.id;

## Cross Join  
select * from customers as c
			  cross join customer_order as co
              on c.id=co.cid;

select * from customers as c
			  cross join customer_order;
              
