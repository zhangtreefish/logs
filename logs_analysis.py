#!/usr/bin/env python3

import psycopg2


def find_popular_articles(cur):
    try:
        popular_article_query = '''
        SELECT articles.title, articles.id AS art_id, count(*) AS num
        FROM log, articles
        WHERE log.path = ('/article/' || articles.slug)
        GROUP BY art_id
        ORDER BY num DESC
        LIMIT 3;
        '''
        cur.execute(popular_article_query)
        rows = cur.fetchall()
        print("Top 3 most popular articles!")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))

    except BaseException:
        print("I am unable to find_popular_articles")


def find_popular_authors(cur):
    try:
        popular_author_query = '''
        SELECT authors.name, authors.id AS aid, count(*) AS num
        FROM articles, authors, log
        WHERE articles.author=authors.id
            AND log.path = ('/article/' || articles.slug)
        GROUP BY aid
        ORDER BY num DESC;
        '''
        cur.execute(popular_author_query)
        rows = cur.fetchall()
        print("\nAuthors ranked by popularity:")
        for row in rows:
            print('{} -- {} views'.format(row[0], row[2]))
    except BaseException:
        print("I am unable to find_popular_authors")


def find_high_error_dates(cur):
    try:
        greater_error_dates_query = '''
        WITH bad_vie AS (
            SELECT date_trunc('day', time) AS date, count(*) AS bad_count
            FROM log
            WHERE status LIKE '404 NOT FOUND'
            GROUP BY date
        ), total_vie AS (
            SELECT date_trunc('day', time) AS date, count(*) AS total_count
            FROM log
            GROUP BY date
        )
        SELECT to_char(b.date, 'FMMonth dd, yyyy'), 1.0 * b.bad_count/t.total_count
        FROM bad_vie b, total_vie t
        WHERE b.date = t.date AND 1.0 * b.bad_count/t.total_count > 0.01;
        '''
        cur.execute(greater_error_dates_query)
        rows = cur.fetchall()
        print("\nDates with access error rates greater than 1.00%:")
        for row in rows:
            print('{} -- {:.2%} errors'.format(row[0], row[1]))
    except BaseException:
        print("I am unable to find_high_error_dates")


if __name__ == '__main__':
    conn = psycopg2.connect("dbname='news'")
    cur = conn.cursor()
    find_popular_articles(cur)
    find_popular_authors(cur)
    find_high_error_dates(cur)
    cur.close()
