# Log Analyzer
This project is an internal reporting tool which analyze useful information about a newspaper site. It uses PostgreSQL and Python to query information from the database and print out the result.  Specifically, it answers the following questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Configurations
1. Linux Environment(with psql 9.5.8)
2. PostgresQL database system
3. python 2.7

### Create views
type the following commands in your terminal to creat view:
```
create or replace view popular_paths as select path, count(*) from log where status = '200 OK' and path != '/' group by path order by count desc;

create or replace view popular_article_to_author as select author, count 
from articles join popular_paths on popular_paths.path like '%' || articles.slug;

create or replace view logs as select date(time), count(*) as views from log group by date;

create or replace view errors as select date(time), count(*) as errors from log where status = '404 NOT FOUND' group by date;

create or replace view error_rate as select logs.date, round(((errors * 100.0) / views), 2) as percent from logs join errors on logs.date = errors.date;
```


### Database
The database contains newspaper articles, as well as the web server log for the site. You can [download it here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
Below are the snippets of the database:

Table "authors"

Column |  Type   
-------|---------
name   | text    
bio    | text    
id     | integer 

Table "articles"

 Column |           Type           
--------|--------------------------
 author | integer                  
 title  | text                     
 slug   | text                     
 lead   | text                     
 body   | text                     
 time   | timestamp with time zone 
 id     | integer                  

 Table "log"

 Column |           Type           
--------|--------------------------
 path   | text                      
 ip     | inet                      
 method | text                      
 status | text                      
 time   | timestamp with time zone 
 id     | integer                  