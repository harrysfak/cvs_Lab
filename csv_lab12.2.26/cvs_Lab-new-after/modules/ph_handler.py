'''
This module collect all pH data and format them at the xeroxed file
'''
import pandas as pd 
import openpyxl

template = "pH.xlsx"
class pH_Handler:

    def __init__(self, dataframe : pd.DataFrame):
        
        self.df = dataframe
        self.pH_df = self.df["PH"]
        


    # method: open and write down the values of ph column
    def create_ph_file(self):
        


        wb = openpyxl.load_workbook(template)
        ws = wb.active
        print(ws[f"B15"].value)