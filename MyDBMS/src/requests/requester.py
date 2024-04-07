import sys
sys.path.append('C:/Users/VASILIADIS/MyDBMS/src')
from model.plotMaker import PlotMaker
from model.queryMaker import DBQueyrMaker

class Requester:

    def __init__(self):
        self.pltMaker = PlotMaker()
        self.qrMaker = DBQueyrMaker()

    def get_countries(self):
        return self.qrMaker.get_countries()
    
    def get_indicators(self):
        return self.qrMaker.get_indicators()
    
    def get_years(self):
        return self.qrMaker.get_years()
    
    def timeline_plot(self, countries, indicators, startYear, endYear, period):
        self.pltMaker.make_timeline_plot(countries, indicators, startYear, endYear, period)

    def bar_plot(self, countries, indicators, startYear, endYear, period):
        self.pltMaker.make_bar_plot(countries, indicators, startYear, endYear, period)

    def scatter_plot(self, country, indicators, startYear, endYear):
        self.pltMaker.make_scatter_plot(country, indicators, startYear, endYear)
