import mysql.connector
import os
import sys
import pandas as pd


class DBCreator:
    
    def __init__(self, path_countries, path_indicators, path_stats):
        #paths for merged csvs
        self.path_countries = path_countries
        self.path_indicators = path_indicators
        self.path_stats = path_stats

    def createDB(self):
        #create database 
        self.connect_toDB()
        self.cursor.execute("SHOW DATABASES")
        databases = self.cursor.fetchall()
        #if DBMS exists skip from recreating it 
        if ('dbms',) in databases:
            print("\n EXISTS \n")
            pass
        else:
            print("\n NOT EXISTS \n")
            self.create_database()
            self.create_countries_table()
            self.create_indicators_table()
            self.create_stats_table()

        self.conn.commit()
        self.conn.close()

    def connect_toDB(self):
        print("\nTo MySql Connection...\n")
        try:
            self.conn = mysql.connector.connect(
                host = '127.0.0.1',
                user = 'root',
                password = 'root'
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(e)
            sys.exit("An error has been occured during connection to MySql.")
        print("\nConnection has been established.\n")   

    def create_database(self):
        print("\nCreating DBMS database...\n")
        self.cursor.execute("DROP DATABASE IF EXISTS DBMS")
        self.cursor.execute("CREATE DATABASE DBMS")
        self.cursor.execute('USE DBMS')
        print("\nDatabase has been created successfuly.\n")

    def create_countries_table(self):
        print("\nCreating Table for countries in DBMS...\n")
        createCountryTableQuery = '''
            CREATE TABLE Countries (
            country_code VARCHAR(3),
            region VARCHAR(64),
            income_group VARCHAR(64),
            country_name VARCHAR(64),
            special_notes TEXT,
            country_id INT NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (country_id)
            )ENGINE=InnoDB
        '''
        self.cursor.execute(createCountryTableQuery)
        print("\nTable for countries had been created successfuly.\n")
    
    def create_indicators_table(self):
        print("\nCreating Table for indicators in DBMS...\n")
        createIndicatorTableQuery = '''
        CREATE TABLE Indicators (
        indicator_code VARCHAR(64),
        indicator_name TEXT,
        source_not TEXT,
        source_organization TEXT,
        indicator_id INT NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (indicator_id)
        )ENGINE=InnoDB
        '''
        self.cursor.execute(createIndicatorTableQuery)
        print("\nTable for indicators had been created successfuly.\n")

    def create_stats_table(self):
        print("\nCreating Table for stats in DBMS...\n")
        createStatsTableQuery = '''
        CREATE TABLE Stats (
        country_id INT NOT NULL,
        year YEAR NOT NULL,
        PRIMARY KEY (country_id, year),
        FOREIGN KEY (country_id) REFERENCES Countries(country_id)
        '''
        #Select each Indicator Code 
        df = pd.read_csv(self.path_stats)
        headers = df.columns.tolist()[2:]
    
        #Add each Indicator Code into table 
        for header in headers:
            createStatsTableQuery += ',\n %s DOUBLE' % (header.replace('.', '_'))
        createStatsTableQuery += '\n)ENGINE=InnoDB'
        
        self.cursor.execute(createStatsTableQuery)
        print("\nTable for stats had been created successfuly.\n")

