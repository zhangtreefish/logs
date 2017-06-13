# Logs Analysis Project of Udacity Full Stack Nanodegree Program

## How to run
1. git clone this repository
2. cd <to the directory where the Vagrantfile is>:
```sh
vagrant up (Vagrantfile not included)
vagrant ssh
```
4. inside vagrant:
```sh
cd /vagrant/logs_project/
psql -d news newsdata.sql (newsdata.sql file not included)
python logs_analysis.py
```
## Sources
1. udacity.com, Full Stack Nanodegree Program.
2. [Extract date (yyyy/mm/dd) from a timestamp in PostgreSQL](https://stackoverflow.com/questions/6133107/extract-date-yyyy-mm-dd-from-a-timestamp-in-postgresql)
3. [autopep8](https://github.com/hhatto/autopep8)