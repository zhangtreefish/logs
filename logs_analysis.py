#!/usr/bin/env python3

import psycopg2


conn = psycopg2.connect("dbname='news'")
cur = conn.cursor()

def find_popular_articles():
    try:
        popular_article_query = '''
        SELECT articles.title, articles.id AS art_id, count(*) AS num
        FROM log, articles
        WHERE log.path LIKE ('/article/' || articles.slug)
        GROUP BY art_id
        ORDER BY num DESC
        LIMIT 3;
        '''
        cur.execute(popular_article_query)
        rows = cur.fetchall()
        print("Top 3 most popular articles!")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))

    except:
        print "I am unable to find_popular_articles"

find_popular_articles()


def find_popular_authors():
    try:
        popular_author_query = '''
        SELECT authors.name, authors.id AS aid, count(*) AS num
        FROM articles, authors, log
        WHERE articles.author=authors.id AND log.path LIKE ('/article/' || articles.slug)
        GROUP BY aid
        ORDER BY num DESC
        LIMIT 3;
        '''
        cur.execute(popular_author_query)
        rows = cur.fetchall()
        print("Top 3 most popular authors!")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))
    except:
        print "I am unable to find_popular_authors"

find_popular_authors()


def find_high_error_dates():
    try:
        greater_error_day_query = '''
        CREATE VIEW day_view AS
            SELECT date_trunc('day',time) AS d, status, count(*) AS n
            FROM log
            GROUP BY d, status;
        CREATE VIEW bad_view AS
            SELECT d, n
            FROM day_view
            WHERE status LIKE '404 NOT FOUND';

        CREATE VIEW total_view AS
            SELECT d, sum(n) AS t
            FROM day_view
            GROUP BY d;

        SELECT b.d, b.n/t.t AS r
        FROM bad_view b, total_view t
        WHERE b.d = t.d AND b.n/t.t > 0.01;
        '''
        cur.execute(greater_error_day_query)
        rows = cur.fetchall()
        print("high_error_dates:")
        for row in rows:
            print('{} -- {:.0%} errors'.format(row[0], row[1]))
    except:
        print "I am unable to find_high_error_dates"

find_high_error_dates()


cur.close()