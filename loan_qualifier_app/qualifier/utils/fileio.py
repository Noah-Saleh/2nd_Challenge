# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv
from pathlib import Path

def load_csv(csvpath):                                                  #reads the csv and turns the csv into a list of lists
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data


def save_csv(qualifying_loans):                 #writes to csv
   
    csvpath = Path("./qualifying_loans.csv")
    with open(csvpath, 'w' , newline='') as csvfile:
         csvwriter = csv.writer(csvfile)

         csvwriter.writerow(["Lender" , "Max Loan Amount" , "Max LTV" , "Max DTI" , "Min Credit Score" , "Interest Rate"])

         for row in qualifying_loans:
             csvwriter.writerow(row)
     