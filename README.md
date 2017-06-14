# Logs Analysis Project of Udacity Full Stack Nanodegree Program
## A Description of the Program's Design
The purpose of this program is to query a PostgreSQL database called news using Python
adaptor psycopg2. The program outputs the most popular authors and articles and dates
when http error exceed certain limit.
## How to run
1. git clone this repository
2. cd (to the directory where the Vagrantfile is):
```sh
vagrant up (Vagrantfile not included)
vagrant ssh
```
4. inside vagrant:~$:
```sh
cd <to where logs_analysis and newsdata.sql files are>
psql -d news newsdata.sql (newsdata.sql file not included)
psql news
inside =>news:
	CREATE VIEW bad_view AS
	    SELECT date_trunc('day', time) AS date, count(*) AS bad_count
	    FROM log
	    WHERE status LIKE '404 NOT FOUND'
	    GROUP BY date;
	CREATE VIEW total_view AS
	    SELECT date_trunc('day', time) AS date, count(*) AS total_count
	    FROM log
	    GROUP BY date;
    <CtrlD to exit news psql>
python logs_analysis.py
```
## Sources
1. udacity.com, Full Stack Nanodegree Program.
2. [Extract date (yyyy/mm/dd) from a timestamp in PostgreSQL](https://stackoverflow.com/questions/6133107/extract-date-yyyy-mm-dd-from-a-timestamp-in-postgresql)
3. [autopep8](https://github.com/hhatto/autopep8)
4. [PostgreSQL Date Formatting](https://www.postgresql.org/docs/8.1/static/functions-formatting.html)