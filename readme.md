# The Scraper

These scripts perform data scrapping from URL http://feeds.reuters.com/reuters/topNews, saving it to PostgreSQL or Mongo database and exporting to CSV files (actually -- comma & tab separation).
Article links, titles, summaries, bodies and publishing dates are extracted.

## Requirements
- Python 3.X + packages, listed in *requirements.txt* (may be installed with `pip`)
- Installed and configured PostgreSQL server (+ user account) and MongoDB server;
- Linux;
- systemd (`systemctl` is used to run\stop the DB servers, but this can be overriden by editing commands in *postgresql_config.py* and *mongo_config.py*);
- super user privilegies (to run servers).

## Files
- shell.py -- user command-line interface;
- scraper.py -- provides functions to parse data from the site and put it to database;
- postgresql_database.py -- provides functions for interacting with PostgreSQL database;
- postgresql_config.py -- provides self-descriptive configurable data for 'postgresql_database' module;
- mongo_database.py -- provides functions for interacting with MongoDB database;
- mongo_config.py -- provides self-descriptive configurable data for 'mongo_database' module;
- requirements.txt -- list of required Python packages.
- readme.md -- this document.

## Usage
Running the script:
`$python3 shell.py`
Command line prompt displays:
`shell>`
The following commands are accepted (X | Y means either one or another to be chosen):
`runserver postgre | mongo`
> Runs the database server.
> Requires super user privilegies.

`stopserver postgre | mongo`
> Stops the database server.
> Requires super user privilegies.

`schema`
> Creates schema in the PostgreSQL database table.
> If schema already exists, it won't be changed.
> PostgreSQL server should be running.

`scrape postgre | mongo`
> Scrapes data from the source and puts it to the PostgreSQL or Mongo database; displays count of records added.
> PostgreSQL \ Mongo server is expected to be running.

`bydate postgre | mongo <date> [<path>]`
> Outputs entries for the given `<date>` to the `<path>` file or to the screen by default; displays count of records found.
> Recommended date format is YYYYMMDDZ (year, month, day, time zone).
> Existing file will be overwritten.
> Fields in the file are separated with comma & tab characters; special characters (line breaks and tabs) in titles, summaries and bodies are escaped.
> PostgreSQL | Mongo server is expected to be running.

`clear postgre | mongo`
> Removes all data from the specified database.
> PostgreSQL | Mongo server is expected to be running.

`help`
> Displays brief help.

`exit`
> Quits to the command line.

Any other command is reported as invalid.
After the command exectution display returns to `shell>`.

## Example
For PostgreSQL:

|Command|Display|Comment
|-|-|-
|`$python3 shell.py`|`shell>`|Displaying this also is implied below.
|`runserver postgre`|`Server is running at localhost:5432`|
|`schema`|`Done`|
|`bydate postgre 20181109-0500`|`0 entries are found`|2018.11.09, -05:00 time zone is used here. Use your current date & time zone for testing.
|`scrape postgre`|`20 entries are added`|
|`bydate postgre 20181109-0500 ./test.csv`|`20 entries are found`|Check test.csv for the scraped data.
|`stopserver postgre`|`Done`|
|`exit`|`$`|Returning to system command line

For MongoDB use example above, but specify `mongo` instead of `postgre`, and skip `schema` command.
Display will be the same (except the different default port in `runserver`).
