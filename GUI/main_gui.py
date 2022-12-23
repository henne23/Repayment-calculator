# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 09:08:22 2022

@author: hendr
"""

import PySimpleGUI as sg

class Main_GUI:
    def __init__(self, controller):
        self.controller = controller
        self.size_text = (15,1)
        self.size_small_text = (6,1)
        self.size_input = (8,1)
        self.layout = [
            [sg.Text("loan:", size=self.size_text), sg.InputText(key="credit", size=self.size_input)],
            [sg.Text("interest [%]:", size=self.size_text), sg.InputText(key="interest", size=self.size_input)],
            [sg.Text("monthly rate:", size=self.size_text), sg.InputText(key="monthly", size=self.size_input)],
            [sg.Checkbox("special repayment", key="special", enable_events=True)],
            [sg.Text("from:", size=self.size_small_text, visible=False, key="from_text"), sg.InputText(key="from", size=self.size_input, visible=False), 
            sg.Text("to:", size=self.size_small_text, visible=False, key="to_text"), sg.InputText(key="to", size=self.size_input, visible=False), 
            sg.Text("amount:", size=self.size_small_text, visible=False, key="amount_text"), sg.InputText(key="amount", size=self.size_input, visible=False)],
            [sg.Checkbox("Excel-Output", key="excel", default=True)],
            [sg.Submit(), sg.Button("Update from Excel", key="update"), sg.Exit()]
        ]

        self.window = sg.Window("Repayment calculator", self.layout, finalize=True)
        self.window["Submit"].bind("<Return>", "_Enter")
        #window["Update"].bind("<u>", "u")

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            self.show_special_repayment_fields(values["special"])
            if event == "Submit":
                self.controller.new_calculation(values)
                break
            if event == "update":
                self.controller.update_results()
                break
        
        self.window.close()
        
    def show_special_repayment_fields(self, special=False):
        fields = ["from", "to", "amount"]
        for field in fields:
            self.window.find_element("%s_text" % field).update(visible=special)
            self.window.find_element(field).update(visible=special)