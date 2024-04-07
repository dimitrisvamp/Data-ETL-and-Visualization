import mysql.connector
import os
import sys
import pandas as pd


class DBLoader:

    def __init__(self, path_countries, path_indicators, path_stats):
        #paths for merged csvs
        self.path_countries = path_countries
        self.path_indicators = path_indicators
        self.path_stats = path_stats

    def load_data_intoDB(self):
        #Load data into DBMS 
        self.connect_toDB()
        self.load_data_into_table(self.path_countries, 'Countries')
        self.load_data_into_table(self.path_indicators, 'Indicators')
        self.load_data_into_table(self.path_stats, 'Stats')

        self.conn.commit()
        self.conn.close()

    def connect_toDB(self):
        print("\nTo MySql Connection...\n")
        try:
            self.conn = mysql.connector.connect(
                host = '127.0.0.1',
                user = 'root',
                password = 'root',
                database = 'DBMS',
                allow_local_infile = True
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(e)
            sys.exit("An error has been occured during connection to MySql.")
        print("\nConnection has been established.\n") 

    def load_data_into_table(self, path_to_csv, table):
        #Give access to MySql to read files from your system
        self.cursor.execute('SET GLOBAL local_infile=\'ON\';')
        if(self.table_already_filled(table) == True):
            print("\nAlready filled table.")
            pass
        else:
            print("\nEmpty table is gonna filled.\n")
            self.load_data(path_to_csv, table)

    def load_data(self, path_to_csv, table):
        print("\nLoading data into DBMS...\n")
        loadData_query = '''
        LOAD DATA LOCAL INFILE '%s' INTO TABLE %s FIELDS TERMINATED BY ',' 
        OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
        ''' % (path_to_csv, table)
        self.cursor.execute(loadData_query)
        print("\nData has been loaded successfully.\n")

    def table_already_filled(self, table):
        check_for_data_existence_query = '''
        SELECT * FROM %s LIMIT 1
        ''' % (table)
        #Return none if no row exists in table
        self.cursor.execute(check_for_data_existence_query)
        existence = self.cursor.fetchone()
        #If None returns False otherwise True
        return bool(existence)
    