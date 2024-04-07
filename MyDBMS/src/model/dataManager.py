import mysql.connector
import os
import pandas as pd
import sys
sys.path.append('C:/Users/VASILIADIS/MyDBMS/src')
from model.queryMaker import DBQueyrMaker


class DataManager:
    
    def __init__(self):
        self.qrMaker = DBQueyrMaker()

    #Returns a dataframe with values each country and each indicator for a year 
    def get_data_for_timelines_and_bar(self, countries, indicators, startYear, endYear, period):
        df = pd.DataFrame()
        #Fill dataframe with values from desired data
        for country in countries:
            for indicator in indicators:
                columnName = country + ' - ' + indicator 
                df[columnName] = self.qrMaker.get_stats_for_years_INRANGE(country, indicator, startYear, endYear)

        if(period != 1):
             df = df.groupby(df.index//period).mean()
        #Add to df years by period 
        years = self.organize_years_by_period(startYear, endYear, period)
        df['Years'] = years

        #Remove rows with all NaN values (dont count 'Years' column)
        columnsToCheck = [n for n in df if n != 'Years']
        df.dropna(how='all', subset=columnsToCheck, inplace=True)
        return df
    
    #Returns a dataframe with 2 indicator columns for a specific year for a country
    def get_data_for_scatter(self, country, indicators, startYear, endYear):
        df = pd.DataFrame()
        #Get specific years 
        years = self.qrMaker.get_years_INRANGE(startYear, endYear)
        for indicator in indicators:
            indicator_stats = [self.qrMaker.get_stats_for_specific_year(country, indicator, year) for year in years]
            #Convert list to dataframe
            df[indicator] = pd.DataFrame(indicator_stats)
        return df
    
    def organize_years_by_period(self, startYear, endYear, period):
        #List that includes the years by period 
        organized_years = []
        current_year = startYear

        while current_year <= endYear:
                organized_years.append(current_year)
                current_year +=period
        return organized_years
