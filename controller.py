# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 09:05:23 2022

@author: hendr
"""
from GUI.main_gui import Main_GUI
from GUI.result_gui import Result_GUI
import pandas as pd
import numpy as np

class Controller:
    def __init__(self):
        self.columns = ["Year", "Loan", "Interests", "Repayment", "Loan rest", "Special payment"]
        self.main_gui = Main_GUI(self)
        
    def new_calculation(self, values: dict):
        credit = float(values["credit"].replace(",", "."))
        interest = float(values["interest"].replace(",", ".")) / 100
        monthly_rate = float(values["monthly"].replace(",", "."))
        special_repayment = np.zeros(100)
        if values["special"]:
            for index in range(int(values["from"]) - 1, int(values["to"])):
                special_repayment[index] = values["amount"]
        
        df, result_year, initial_credit = self.calculate(credit, interest, monthly_rate, special_repayment)
        self.result_gui = Result_GUI(self, df.values)
        self.result_gui.show_results(df, monthly_rate, interest, result_year, initial_credit, values["excel"])
    
    def calculate(self, credit, interest, monthly_rate, special_repayment=None):
        year = 0
        initial_credit = credit
        df = pd.DataFrame(columns = self.columns)
        while credit > 0:
            annual_interest = 0
            annual_repayment = 0
            year += 1
            credit_before = credit
            for i in range(12):
                monthly_interest = credit * interest / 12
                annual_interest += monthly_interest
                monthly_repayment = monthly_rate - monthly_interest
                annual_repayment += monthly_repayment
                credit -= monthly_repayment
            if special_repayment[year-1]:
                    credit -= special_repayment[year-1]
            df = df.append({key:value for key, value in zip(df.keys(), [int(year), round(credit_before, 2), round(annual_interest,2), round(annual_repayment,2), round(credit, 2), special_repayment[year-1]])}, ignore_index=True)
        return df, year, initial_credit    