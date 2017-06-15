#!/usr/bin/env python3

import psycopg2
import sys


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname={}".format(database_name))
        cur = conn.cursor()
        return conn, cur
    except psycopg2.Error as e:
        print "Unable to connect to database"
        sys.exit(1)


def find_popular_articles():
    try:
        popular_article_query = '''
        SELECT articles.title, articles.id AS art_id, count(*) AS num
        FROM log, articles
        WHERE log.path = ('/article/' || articles.slug)
        GROUP BY art_id
        ORDER BY num DESC
        LIMIT 3;
        '''
        conn, cur = connect()
        cur.execute(popular_article_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print("Top 3 most popular articles!")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))

    except BaseException:
        print("I am unable to find_popular_articles")


def find_popular_authors():
    try:
        popular_author_query = '''
        SELECT authors.name, authors.id AS aid, count(*) AS num
        FROM articles, authors, log
        WHERE articles.author=authors.id
            AND log.path = ('/article/' || articles.slug)
        GROUP BY aid
        ORDER BY num DESC;
        '''
        conn, cur = connect()
        cur.execute(popular_author_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print("\nAuthors ranked by popularity:")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))
    except BaseException:
        print("I am unable to find_popular_authors")


def find_high_error_dates():
    try:
        greater_error_dates_query = '''
        SELECT to_char(b.date, 'FMMonth dd, yyyy'), 1.0 * b.bad_count/t.total_count
        FROM bad_view b, total_view t
        WHERE b.date = t.date AND 1.0 * b.bad_count/t.total_count > 0.01;
        '''
        conn, cur = connect()
        cur.execute(greater_error_dates_query)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        print("\nDates with access error rates greater than 1.00%:")
        for row in rows:
            print('{} -- {:.2%} errors'.format(row[0], row[1]))
    except BaseException:
        print("I am unable to find_high_error_dates")


if __name__ == '__main__':
    find_popular_articles()
    find_popular_authors()
    find_high_error_dates()
