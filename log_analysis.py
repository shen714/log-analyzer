#!/usr/bin/env python
import psycopg2

DBNAME = "news"

'''
# views
views = [
    '''create or replace view popular_paths as select path, count(*) from log where 
    status = '200 OK' and path != '/' group by path order by count desc''',

    '''create or replace view popular_article_to_author as select author, count 
    from articles join popular_paths on popular_paths.path like '%' || articles.slug ''',

    '''create or replace view logs as select date(time), count(*) as views from log group by date;''',

    '''create or replace view errors as select date(time), count(*) as errors from log where status = '404 NOT FOUND' 
    group by date;''',

    '''create or replace view error_rate as select logs.date, round(((errors * 100.0) / views), 2) as
     percent from logs join errors on logs.date = errors.date;'''
]
'''

# queries
top_three_articles = '''select title, count from articles join 
popular_paths on popular_paths.path like '%' || articles.slug limit 3;'''

popular_authors = '''select name, sum(count) from authors join popular_article_to_author
                     on popular_article_to_author.author = authors.id group by name order
                     by sum DESC'''

date_error_greater_than_one_percent = '''select date, percent from error_rate where percent > 1;'''

'''
def create_views(views):
    '''create views to make following code more concise'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    for view in views:
        c.execute(view)
        db.commit()
    c.close()
'''

def get_result(query):
    '''connect to the database and get result based on input query'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    result = c.fetchall()
    db.close()
    return result

def get_top_three_articles():
    result = get_result(top_three_articles)
    print("The most popular three articles:")
    for title, count in result:
        print(title + ' -- ' + str(count) + 'views')

def get_popular_authors():
    result = get_result(popular_authors)
    print("The authors with the most popular in the top:")
    for name, sum in result:
        print(name + ' -- ' + str(sum) + 'views')

def get_most_error_date():
    result = get_result(date_error_greater_than_one_percent)
    print("The dates when errors rate greater than 1%:")
    for date, percent in result:
        print(str(date) + " -- " + str(percent) + "% " + "errors")

if __name__ == '__main__':
    # create_views(views)
    get_top_three_articles()
    print("--------------------------------------")
    get_popular_authors()
    print("--------------------------------------")
    get_most_error_date()
    