#!/usr/bin/env python

import io, sys

from dateutil import parser

import postgresql_config, postgresql_database, mongo_database, mongo_config, scraper
    

def get_by_date(select_by_date_function, date, output_path):
    output_file = io.open(output_path, 'w') if output_path is not None else sys.stdout
    records = select_by_date_function(date)
    for record in records:
        output_file.write(
            ',\t'.join([
                record['link'],
                repr(record['title']),
                repr(record['summary']),
                repr(record['content']),
                str(record['published'])
            ]) + '\n'
        )
    if output_path is not None:
        output_file.close()
    return len(records)

RUN_SERVER = 'runserver'
STOP_SERVER = 'stopserver'
CREATE_SCHEMA = 'schema'
RUN_SCRAPER = 'scrape'
DATA_BY_DATE = 'bydate'
CLEAR = 'clear'
HELP = 'help'
EXIT = 'exit'

POSTGRESQL = 'postgre'
MONGO = 'mongo'

def print_message(message):
    sys.stdout.write(message + '\n')

def print_error(message):
    sys.stderr.write("Error: {}\n".format(message))

def choose_database_specific(database_type, postgresql_variant, mongo_variant):
    if database_type == POSTGRESQL:
        return postgresql_variant
    if database_type == MONGO:
        return mongo_variant
    return None

while True:
    try:
        sys.stdout.write("shell>")
        argv = input().split(' ')
        argc = len(argv)
        command = argv[0]
        if command == RUN_SERVER:
            run_server = choose_database_specific(
                argv[1],
                postgresql_database.run_server,
                mongo_database.run_server
            )
            if run_server is None:
                print_error("invalid target database argument `{}`".format(argv[1]))
            else:
                run_server()
                print_message("Server is running at {}:{}\n".format(
                    *choose_database_specific(
                        argv[1],
                        [postgresql_config.URL, postgresql_config.PORT],
                        [mongo_config.URL, mongo_config.PORT]
                    )
                ))
        elif command == STOP_SERVER:
            stop_function = choose_database_specific(
                argv[1],
                postgresql_database.stop_server,
                mongo_database.stop_server
            )
            if stop_function is None:
                print_error("invalid target database argument `{}`".format(argv[1]))
            else:
                stop_function()
                print_message("Done")
        elif command == CREATE_SCHEMA:
            postgresql_database.create_schema()
            print_message("Done")
        elif command == RUN_SCRAPER:
            if argc < 2:
                print_error("target database argument ({} or {}) expected".format(POSTGRESQL, MONGO))
            else: 
                run_function = choose_database_specific(
                    argv[1],
                    scraper.run_postgresql,
                    scraper.run_mongo
                )
                if run_function is None:
                    print_error("invalid target database argument `{}`".format(argv[1]))
                else:
                    count = run_function()
                    print_message(
                        "{} entr{} added".format(
                            count,
                            "y is" if count == 1 else "ies are"
                        )
                    )
        elif command == DATA_BY_DATE:
            if argc < 3:
                print_error("too few arguments")
            else:
                select_by_date_function = choose_database_specific(
                    argv[1],
                    postgresql_database.select_by_date,
                    mongo_database.select_by_date
                )
                if select_by_date_function is None:
                    print_error("invalid target database argument `{}`".format(argv[1]))
                else:
                    count = get_by_date(
                        select_by_date_function,
                        parser.parse(argv[2]),
                        argv[3] if argc >= 4 else None
                    )
                    print_message(
                        "{} entr{} found".format(
                            count,
                            "y is" if count == 1 else "ies are"
                        )
                    )
        elif command == CLEAR:
            if argc < 2:
                print_error("target database argument ({} or {}) expected".format(POSTGRESQL, MONGO))
            else:
                clear_function = choose_database_specific(
                    argv[1],
                    postgresql_database.clear,
                    mongo_database.clear
                )
                if clear_function is None:
                    print_error("invalid target database argument `{}`".format(argv[1]))
                else:
                    clear_function()
                    print_message("Done")
        elif command == HELP:
            f = "\t{}\n\t\t{}\n"
            print_message("\nBrief:\n")
            POSTGRE_OR_MONGO = ' {} | {}'.format(POSTGRESQL, MONGO)
            print_message(f.format(RUN_SERVER + POSTGRE_OR_MONGO, "Runs the database server."))
            print_message(f.format(STOP_SERVER + POSTGRE_OR_MONGO, "Stops the database server."))
            print_message(f.format(CREATE_SCHEMA, "Creates schema in the PostgreSQL database table."))
            print_message(f.format(RUN_SCRAPER + POSTGRE_OR_MONGO, "Scrapes data from the source and puts it to the PostgreSQL or Mongo database; displays count of records added."))
            print_message(f.format(DATA_BY_DATE + "{} <date> [<path>]".format(POSTGRE_OR_MONGO), "Outputs entries for the given <date> to the <path> file or to the screen by default; displays count of records found."))
            print_message(f.format(CLEAR + POSTGRE_OR_MONGO, "Removes all data from the specified database."))
            print_message(f.format(HELP, "Displays this help."))
            print_message(f.format(EXIT, "Quit the shell."))
        elif command == EXIT:
            break
        else:
            print_error("unknown command `{}`".format(command))
    except Exception as exception:
        print_error("uncaught exception\n\n" + str(exception))
