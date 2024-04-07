import pandas as pd 
import os 
import glob 


class GatherToCsv:

    def __init__(self, path_countries, path_indicators, path_stats):
        #paths for original data
        self.path_countries = path_countries
        self.path_indicators = path_indicators
        self.path_stats = path_stats

    def create_merged_csvs(self):
        self.create_csvs_Dir()
        self.create_countries_csv()
        self.create_indicators_csv()
        self.create_stats_csv()

    def create_countries_csv(self):
        merged_csvs = pd.DataFrame()
        df = self.read_multiple_csvs(self.path_countries)
        #Merge all df to one 
        merged_csvs = pd.concat(df, ignore_index=True)
        
        #Drop unnamed columns
        merged_csvs = merged_csvs.drop(['Unnamed: 5', 'Unnamed: 4'], axis='columns')
        self.countries_codes = merged_csvs['Country Code']
        #Write to csv
        merged_csvs.to_csv(os.path.join(self.csvs_Dir, 'countries.csv'), index=False)

    def create_indicators_csv(self):
        merged_csvs = pd.DataFrame()
        df = self.read_multiple_csvs(self.path_indicators)
        #Merge all df to one 
        merged_csvs = pd.concat(df, ignore_index=True)
    
        #Drop unnamed columns
        merged_csvs = merged_csvs.drop(['Unnamed: 4'], axis='columns')
        #Select specific indicators
        merged_csvs = merged_csvs[merged_csvs['INDICATOR_CODE'].str.startswith('BM') |
                                    merged_csvs['INDICATOR_CODE'].str.startswith('EG') |
                                    merged_csvs['INDICATOR_CODE'].str.startswith('GC.TAX')]
        #Drop duplicated indicators
        merged_csvs= merged_csvs.drop_duplicates()
        #Write to csv file
        merged_csvs.to_csv(os.path.join(self.csvs_Dir, 'indicators.csv'), index=False)

    def create_stats_csv(self):
        merged_csvs = pd.DataFrame()
        df = self.read_multiple_csvs(self.path_stats)

        id= 1
        for dfc in df:
            #Drop unnamed and unnecessary columns and fill nan values with NULL
            dfc = dfc.drop(['Country Name', 'Indicator Name', 'Unnamed: 65'], axis='columns')
            dfc.fillna(value="NULL", inplace=True)
            #keep only stats about specific indicators 
            metrics = ('BM', 'EG', 'GC.TAX')
            dfc = dfc.drop(dfc[dfc['Indicator Code'].str.startswith(metrics) == False].index)

            #Replace each country code with its respective id
            dfc = dfc.rename(columns = {'Country Code' : 'Country ID'})
            #Rename Indicator Code column to Year
            dfc = dfc.rename(columns={'Indicator Code': 'Year'})
            
            #Transpose columns to rows 
            dfc = dfc.T
            #Name headers based on each 'Indicator Code'
            dfc = dfc.rename(columns=dfc.iloc[0]).drop(dfc.index[0])
            dfc = dfc.reset_index()
            dfc.columns = dfc.iloc[0]
            dfc = dfc.drop(dfc.index[0])
            #Insert as a column the respective ID of each country
            dfc.insert(0, 'Country ID', id)
            
            #Merge to one df
            merged_csvs = pd.concat([merged_csvs, dfc], ignore_index=True)
            #Prepare id for the next country
            id += 1
            
        #Write to csv
        merged_csvs.to_csv(os.path.join(self.csvs_Dir, 'stats.csv'), index=False)


    def read_multiple_csvs(self, path):
        #Read every csv file that exists into given path
        multiple_csvs = glob.glob(path + "/*.csv")
        if(path == self.path_stats):
            df = [pd.read_csv(csv, skiprows=4, index_col=False) for csv in multiple_csvs]
        else:   
            df = [pd.read_csv(csv, index_col=False) for csv in multiple_csvs]

        return df
    
    def create_csvs_Dir(self):
        #Create the csvs directory at my path
        self.csvs_Dir = os.path.join(r"C:\Users\VASILIADIS\MyDBMS", 'final')

        #create directory if doesn't exist
        if(os.path.exists(self.csvs_Dir) == False):
            os.mkdir(self.csvs_Dir)


