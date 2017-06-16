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


popular_articles_query = '''
    SELECT articles.title, articles.id AS art_id, count(*) AS num
    FROM log, articles
    WHERE log.path = ('/article/' || articles.slug)
    GROUP BY art_id
    ORDER BY num DESC
    LIMIT 3;
    '''
popular_articles_exception_msg = "I am unable to find_popular_articles"


popular_authors_query = '''
    SELECT authors.name, authors.id AS aid, count(*) AS num
    FROM articles, authors, log
    WHERE articles.author=authors.id
        AND log.path = ('/article/' || articles.slug)
    GROUP BY aid
    ORDER BY num DESC;
    '''
popular_authors_exception_msg = "I am unable to find_popular_authors"


greater_error_dates_query = '''
    SELECT to_char(b.date, 'FMMonth dd, yyyy'), 1.0 * b.bad_count/t.total_count
    FROM bad_view b, total_view t
    WHERE b.date = t.date AND 1.0 * b.bad_count/t.total_count > 0.01;
    '''
greater_error_dates_exception_msg = "I am unable to find_high_error_dates"


def do_query(query_string, exception_message_string):
    try:
        conn, cur = connect()
        cur.execute(query_string)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            if query_string == popular_articles_query:
                print('{} -- {} views'.format(row[0], row[2]))
            elif query_string == popular_authors_query:
                print('{} -- {} views'.format(row[0], row[2]))
            elif query_string == greater_error_dates_query:
                print('{} -- {:.2%} errors'.format(row[0], row[1]))

    except BaseException:
        print(exception_message_string)


if __name__ == '__main__':
    print("Top 3 most popular articles!")
    do_query(popular_articles_query, popular_articles_exception_msg)
    print("\nAuthors ranked by popularity:")
    do_query(popular_authors_query, popular_authors_exception_msg)
    print("\nDates with access error rates greater than 1.00%:")
    do_query(greater_error_dates_query, greater_error_dates_exception_msg)
