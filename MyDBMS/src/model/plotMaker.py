import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
sys.path.append('C:/Users/VASILIADIS/MyDBMS/src')
from model.dataManager import DataManager

class PlotMaker:

    def __init__(self):
        self.dataManager = DataManager()

    def make_timeline_plot(self, countries, indicators, startYear, endYear, period):
        #Get data
        data = self.dataManager.get_data_for_timelines_and_bar(countries, indicators, startYear, endYear, period)
        #Plot data
        data.plot(x="Years", y=data.columns[:-1])
        plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        plt.show()

    def make_bar_plot(self, countries, indicators, startYear, endYear, period):
        #Get data
        data = self.dataManager.get_data_for_timelines_and_bar(countries, indicators, startYear, endYear, period)
        #Plot data
        data.plot(x="Years", y=data.columns[:-1], kind='bar')
        plt.gca().yaxis.set_major_formatter(ScalarFormatter(useOffset=False))
        plt.show()

    def make_scatter_plot(self, country, indicators, startYear, endYear):
        #Get data
        data = self.dataManager.get_data_for_scatter(country[0], indicators, startYear, endYear)
        #Plot data
        data.plot(x=data.columns[0], y=data.columns[1], kind='scatter')
        plt.title('Correlation of %s for specified years' % (country[0]))
        plt.ticklabel_format(useOffset=False, style='plain', axis='y')
        plt.show()
