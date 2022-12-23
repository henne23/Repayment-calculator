# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 09:09:15 2022

@author: hendr
"""

import PySimpleGUI as sg
import numpy as np
import pandas as pd

class Result_GUI:
    def __init__(self, controller, results):
        self.controller = controller
        self.results = results
        self.layout = self.get_result_layout()
        
    def get_result_layout(self, results=None):
        if results is None:
            results = self.results
        result_size=(12,1)
        header = [
            sg.Text("Year:", size=result_size), sg.Text("Loan:", size=result_size), sg.Text("Interest:", size=result_size),
            sg.Text("Repayment:", size=result_size), sg.Text("Loan rest", size=result_size), sg.Text("Special payment", size=result_size)]
        result_fields = [[
            sg.Text(str(int(x[0])), size=result_size), sg.Text(str(x[1]), size=result_size), sg.Text(str(x[2]), size=result_size), 
            sg.Text(str(x[3]), size=result_size), sg.Text(str(x[4]), size=result_size), 
            sg.InputText(key="input%d" % index, size=result_size, default_text=str(x[5]))] for index, x in enumerate(results)]
        buttons = [
            sg.Button("OK", key="OK"), sg.Button("Update", key="update"), sg.Button("Print (no function)", key="print")]
        result_layout = [
            [buttons, header, sg.Column(result_fields, scrollable=True, vertical_scroll_only=True, element_justification="c")]]
        return result_layout
    
    def show_results(self, df, monthly_rate, interest, year, initial_credit, excel_output=True):    
        if excel_output:
            df.to_excel("results.xlsx", index=False)
            np.savetxt("rate_interest.txt", np.array((monthly_rate, interest)))
        #sg.Popup("Finished after %d years!" % year)
        results = df.values

        result_layout = self.get_result_layout(results)
    
        self.window = sg.Window("Repayment overview", result_layout, finalize=True)
        self.window["OK"].bind("<Return>", "_Enter")
    
        while True:
            event, values = self.window.read()
            if event == "update":
                special = [float(x) for x in values.values()]
                self.window.close()
                update = self.controller.calculate(initial_credit, interest, monthly_rate, special)
                self.show_results(df=update[0], monthly_rate=monthly_rate, interest=interest, year=update[1], initial_credit=update[2], excel_output=excel_output)
            if event == sg.WINDOW_CLOSED or event == "OK":
                break
            
    def update_results(self):
        try:
            df = pd.read_excel("results.xlsx")
            f = open("rate_interest.txt")
            monthly, interest = [float(x.replace("\n","")) for x in f.readlines()]
        except:
            sg.Popup("No file found")
            return
        if len(df) == 0:
            sg.Popup("No valid inputs")
            return
    
        credit = df["Credit"][0]
        special_payment = np.array(df["Special payment"].fillna(0))
        df, result_year, initial_credit = self.controller.calculate(credit, interest, monthly, special_payment)
        self.show_results(df, monthly, interest, result_year, initial_credit)