import customtkinter as ctk
import tkinter
import sys
sys.path.append('C:/Users/VASILIADIS/MyDBMS/src')
from requests.requester import Requester

class Viewer(ctk.CTk):

    def __init__(self):
        self.requester = Requester()

        # Array with user's desired data
        self.data_to_plot = []

        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Create application
        self.app = ctk.CTk()
        self.app.title('Statistic Visualization')
        self.app.geometry("600x450")
        self.label = ctk.CTkLabel(self.app, text="This is an application for statistic visualization")
        self.label.pack()
        self.create_buttons()
        self.app.mainloop()

    def create_buttons(self):
        plot_button = ctk.CTkButton(master=self.app, text='Plots',
                                     width=225, command=self.show_plots)
        plot_button.pack(anchor=tkinter.CENTER, pady=20)
        countries_button = ctk.CTkButton(master=self.app, text='Countries', 
                                width=225, command=self.show_countries)
        countries_button.pack(anchor=tkinter.CENTER, pady=10)
        indicators_butoon = ctk.CTkButton(master=self.app, text='Indicators', 
                                width=225, command=self.show_indicators)
        indicators_butoon.pack(anchor=tkinter.CENTER, pady=20)
        
        from_year_button = ctk.CTkButton(master=self.app, text='From Year',
                                     width=225, command=self.show_years)
        from_year_button.pack(anchor=tkinter.CENTER, pady=10) 
        
        to_year_button = ctk.CTkButton(master=self.app, text='To Year',
                                     width=225, command=self.show_years)
        to_year_button.pack(anchor=tkinter.CENTER, pady=20) 
        per_year_button = ctk.CTkButton(master=self.app, text='Per Years',
                                     width=225, command=self.show_per_years)
        per_year_button.pack(anchor=tkinter.CENTER, pady=10) 

        visualize_button = ctk.CTkButton(master=self.app, text='Visualize Statistics',
                                         width=225, command=self.visualize)
        visualize_button.pack(anchor=tkinter.CENTER, pady=20) 

    def show_plots(self):
        plots = ['Timeline Plot', 'Bar Plot', 'Scatter Plot'] 

        # Pop-up window with the available plots to select
        self.popup = ctk.CTk()
        self.popup.title("Available Plots")
        self.popup.geometry("300x300")

        # Add widgets to the pop-up window
        label = ctk.CTkLabel(self.popup, text="Select Plot")
        label.pack()
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(self.popup)
        frame.pack(anchor=tkinter.CENTER)
        
        # Format the pop-up window options according to plots
        self.format_options(plots, frame)

    def show_countries(self):
        countries = self.requester.get_countries()
        
        # Pop-up window with the available countries to select
        self.popup = ctk.CTk()
        self.popup.title("Available Countries")
        self.popup.geometry("300x300")
        
        # Add widgets to the pop-up window
        label = ctk.CTkLabel(self.popup, text="Select Countries")
        label.pack()
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(self.popup)
        frame.pack(anchor=tkinter.CENTER)
        
        # Format the pop-up window options according to countries
        self.format_options(countries, frame)
       
    def show_indicators(self):
        indicators = self.requester.get_indicators()

        # Pop-up window with the available indicators to select
        self.popup = ctk.CTk()
        self.popup.title("Available Indicators")
        self.popup.geometry("600x300")
        
        # Add widgets to the pop-up window
        label = ctk.CTkLabel(self.popup, text="Select indicators")
        label.pack()
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(self.popup, width=520)
        frame.pack(anchor=tkinter.CENTER)
        
        # Format the pop-up window options according to countries
        self.format_options(indicators, frame)
        
    def show_years(self):
        years = self.requester.get_years()

        # Pop-up window with the available years to select
        self.popup = ctk.CTk()
        self.popup.title("Available Years")
        self.popup.geometry("300x300")
        
        # Add widgets to the pop-up window
        label = ctk.CTkLabel(self.popup, text="Select Years")
        label.pack()
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(self.popup)
        frame.pack(anchor=tkinter.CENTER)
        
        # Format the pop-up window options according to countries
        self.format_options(years, frame)
        
    def show_per_years(self):
        perYears = [1, 5, 10, 20]

        # Pop-up window with the available years to select
        self.popup = ctk.CTk()
        self.popup.title("Available perYears")
        self.popup.geometry("300x300")
        
        # Add widgets to the pop-up window
        label = ctk.CTkLabel(self.popup, text="Select Year Period")
        label.pack()
        # Create scrollable frame
        frame = ctk.CTkScrollableFrame(self.popup)
        frame.pack(anchor=tkinter.CENTER)
        
        # Format the pop-up window options according to countries
        self.format_options(perYears, frame)

    def visualize(self):
        if(self.data_to_plot[0][0] == 'Timeline Plot'):
            self.requester.timeline_plot(self.data_to_plot[1], self.data_to_plot[2],
                                         self.data_to_plot[3][0], self.data_to_plot[4][0], self.data_to_plot[5][0])
        elif(self.data_to_plot[0][0] == 'Bar Plot'):
            self.requester.bar_plot(self.data_to_plot[1], self.data_to_plot[2],
                                         self.data_to_plot[3][0], self.data_to_plot[4][0], self.data_to_plot[5][0])

        else:
            self.requester.scatter_plot(self.data_to_plot[1], self.data_to_plot[2],
                                         self.data_to_plot[3][0], self.data_to_plot[4][0])
        # Clear data that have just been plotted
        self.data_to_plot.clear()

    def submit(self):
        self.checked_values = []
        for checkbox, value in self.checkboxes.items():
            if checkbox.get() == "on":
                self.checked_values.append(value)
        # Save users preferences
        self.data_to_plot.append(self.checked_values)
        # Close the pop-up window
        self.popup.destroy()

    def format_options(self, variables, frame):
        self.checkboxes = {}
        for variable in variables:
            check_var = ctk.StringVar(value='off')
            check_countries = ctk.CTkCheckBox(frame, text=variable, variable=check_var, 
                                              onvalue="on", offvalue="off")
            check_countries.pack(anchor='nw', padx=0, pady=5)
            self.checkboxes[check_countries] = variable
        submit_button = ctk.CTkButton(master=self.popup, text='Submit', command=self.submit)
        submit_button.pack(pady=20)
        self.popup.mainloop() 


if __name__ == "__main__":
    Viewer()