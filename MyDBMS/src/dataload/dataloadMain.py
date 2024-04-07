import sys
sys.path.append('C:/Users/VASILIADIS/MyDBMS/src')
from dataload.FinalCsvs import GatherToCsv
from dataload.databaseCreator import DBCreator
from dataload.databaseLoader import DBLoader
from dataload.__init__ import *


if __name__ == "__main__":
    GatherToCsv(origi_path_c, origi_path_i, origi_path_s).create_merged_csvs()
    DBCreator(path_c, path_i, path_s).createDB()
    DBLoader(path_csv_c, path_csv_i, path_csv_s).load_data_intoDB()