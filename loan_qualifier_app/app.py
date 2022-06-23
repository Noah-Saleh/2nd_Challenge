# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys                  #importing necessary libraries
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio      import (                 #importing self-made functions (because are code is modularized)
    load_csv ,
    save_csv ,                          )

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,      )


from qualifier.filters.max_loan_size  import filter_max_loan_size                
from qualifier.filters.credit_score   import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value  import filter_loan_to_value


def load_bank_data():
    
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():        
        sys.exit(f"Oops! Can't find this path: {csvpath}")                      #if the filepath is invalid, the program
                                                                                #quits to avoid exploits or the program breaking
    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?"                  ).ask()
    debt         = questionary.text("What's your current amount of monthly debt?").ask()
    income       = questionary.text("What's your total monthly income?"          ).ask()
    loan_amount  = questionary.text("What's your desired loan amount?"           ).ask()
    home_value   = questionary.text("What's your home value?"                    ).ask()

    credit_score = int  (credit_score)            #these variables are to make sure that the program doesn't break
    debt         = float(debt)                    #We need them because the program only accepts certain data types.
    income       = float(income)
    loan_amount  = float(loan_amount)
    home_value   = float(home_value)

    return (
             credit_score ,                 #This order is specific and important b/c it matches with the run() functions ordering.
             debt         ,
             income       ,
             loan_amount  ,
             home_value   ,
           )


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")  #"the .02f rounds the ratio to 2 decimal places

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size (loan, bank_data)                            #these 4 filters find the intersection of banks that the user meets requirements for         
    bank_data_filtered = filter_credit_score  (credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value (loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")                 #the len function counts the total number of items in the list

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    prompt = questionary.confirm("Save list of your qualifying loans?:").ask() #y/n response
    if prompt:
            csvpath = questionary.text("Enter save location:").ask()
            csvpath = Path(csvpath)
            if csvpath.exists():
                save_csv(qualifying_loans)
                print(f"Saved to '{csvpath}'!")
            else:
                sys.exit("Invalid filepath or filepath does not exist.")        #ensures that they enter a valid file path to not break the program
    else:
        sys.exit("List not saved. Have a nice day!")   #if they say no then quit the app

def run():                                               #calls all the functions
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":                               #calls the run() function, which transitively calls all the other important functions
    fire.Fire(run)
