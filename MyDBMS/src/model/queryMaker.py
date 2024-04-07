import mysql.connector
import os
import sys
import pandas as pd

class DBQueyrMaker:

    def __init__(self):
        self.connect_toDB()
     
    def __del__(self):
        
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

    def get_countries(self):
        query = " SELECT country_name FROM Countries"
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]
    
    def get_indicators(self):
        query = " SELECT indicator_name FROM Indicators"
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]
    
    def get_years(self):
        query = " SELECT DISTINCT year FROM Stats"
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]
    
    def get_countryID(self, country):
        query = " SELECT country_id FROM Countries WHERE country_name = '%s' " % (country)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    def get_indicatorCode(self, indicator):
        query = "SELECT indicator_code FROM Indicators WHERE indicator_name = '%s'" % (indicator)
        self.cursor.execute(query)
        return self.cursor.fetchone()[0].replace('.', '_')
    
    def get_years_INRANGE(self, startYear, endYear):
        query = " SELECT DISTINCT year FROM Stats WHERE year BETWEEN %d AND %d " % (startYear, endYear)
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]
    
    def get_stats_for_specific_year(self, country, indicator, year):
        #Select stats from a country for a specific indiator and year 
        countryID = self.get_countryID(country)
        indicatorCode = self.get_indicatorCode(indicator)
        query = "SELECT %s FROM Stats WHERE country_id = %d AND year = %d "  % (indicatorCode, countryID, year)
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]
    
    def get_stats_for_years_INRANGE(self, country, indicator, startYear, endYear):
        #Select stats from a country for a specific indicator and multiple years 
        countryID = self.get_countryID(country)
        indicatorCode = self.get_indicatorCode(indicator)
        query = " SELECT %s FROM Stats WHERE country_id = %d AND year BETWEEN %d AND %d " % (indicatorCode, countryID, startYear, endYear)
        self.cursor.execute(query)
        return [ind[0] for ind in self.cursor.fetchall()]

        