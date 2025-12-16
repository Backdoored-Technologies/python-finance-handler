import json
from pathlib import Path
from datetime import datetime

import import_utils


#todo in near future:
#use dispatch tables instead of elif chain
#load json file only once then pull it from memory when changing it (use import_utils.methods for this)

class ExpenseCalculator:

    def __init__(self):
        #variable initialization
        self.expense_type = None
        self.expense_amount = None
        self.expense_description = None
        self.expense_ID = None
        self.expense_date = None

    def expense_stored_object(self):
        expense_obj = {
            "expense_type": self.expense_type,
            "expense_amount": self.expense_amount,
            "expense_description": self.expense_description,
            "expense_ID": self.expense_ID,
            "expense_date": self.expense_date,
        }
        return expense_obj

    def expense_type_function(self):
        while True:
            expense_type = input("Input Expense Type: ")
            confirm1 = input(f"Is {expense_type} correct? (y/n): ")

            if import_utils.is_yes_utils(confirm1):
                self.expense_type = expense_type
                print("Expense Type Initialized.")
                return self.expense_type
            else:
                print("Expense Type assumed to be incorrect. Reprompting...")
                continue
        
    def expense_amount_neg_function(self):
        while True:
            try:
                expense_amount = float((input("Input Expense Amount ($): ")).strip())
            except ValueError:
                print("Invalid input! Please enter a number for expense amount. Reprompting...")
                continue
            
            #expense amount
            confirm2 = input(f"Is {expense_amount} correct? (y/n): ")
            if import_utils.is_yes_utils(confirm2):
                self.expense_amount = expense_amount
                print("Amount Initialized.")
            else:
                print("Amount assumed to be incorrect. Reprompting...")
                continue
            
            #convert expense_amount to negative int (expenses will always be negative)
            self.expense_amount = -abs(self.expense_amount)
            return self.expense_amount
        
    def expense_description_function(self):
        while True:
            expense_description = input("Input Expense Description: ")
            confirm3 = input(f"Is {expense_description} correct? (y/n): ")

            if import_utils.is_yes_utils(confirm3):
                self.expense_description = expense_description
                return self.expense_description
            else:
                print("Expense Description assumed to be incorrect. Reprompting...")
                continue

    def expense_input(self):
            self.expense_type = self.expense_type_function()
            self.expense_amount = self.expense_amount_neg_function()
            self.expense_description = self.expense_description_function()
            self.expense_ID = self.expense_id_plusplus()
            self.expense_date = self.define_expense_date()

            self.store_expense_object()

            import_utils.npc_confirm()
            
            print("New Expense Stored.")
            return
    
    def define_expense_date(self):
        self.expense_date = datetime.now().strftime("%m-%d-%Y")
        return self.expense_date

    def store_expense_object(self):
        #write expense obj to .json
        expense_data = self.expense_stored_object()
         
        stored_expenses_1 = []
        
        if import_utils.STORED_EXPENSES_FILE.exists():
            try:
                with import_utils.STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                    stored_expenses_1 = json.load(f)
            except json.JSONDecodeError:
                raise RuntimeError("stored_expenses.json is corrupted (DEBUG: go to save_expense_object funct)")
        else:
            stored_expenses_1 = []

        stored_expenses_1.append(expense_data)

        # open "w" - will automatically create stored_expense.json if it does not exist
        with import_utils.STORED_EXPENSES_FILE.open("w", encoding="utf-8") as f:
            json.dump(stored_expenses_1, f, indent=2)

    def expense_id_plusplus(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            return 1

        try:
            with import_utils.STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                expenses_file = json.load(f)

            if not expenses_file:
                return 1
            
            last_listed_expense_id = expenses_file[-1]["expense_ID"]
            return last_listed_expense_id + 1
        
        except (json.JSONDecodeError, KeyError, IndexError):
            print("DEBUG: expense_id_plusplus funct error, error opening import_utils.STORED_EXPENSES_FILE. Returning 1 for order_ID.")
            return 1
    
    def request_expense_stats(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            print("stored_expenses.json does not exist. By extension no expense stats exist.")
            return

        while True:
            input2 = input("Choose what to display: expense total (et), display array (da), or exit (e): ")
            stripped = input2.strip().lower()
            
            if stripped in ["et", "expensetotal"]: 
                expense_total = self.calculate_total_expenses()
                print(f"Expense Total: {expense_total}")
                return expense_total
            
            elif stripped in ["da", "displayarray"]:
                dsea = self.display_stored_expenses_array()
                return dsea
            
            elif stripped in ["e", "exit"]:
                return
            
            else:
                print("Please respond with 'et', 'da', or 'e'. Reprompting...")
                continue

    def display_stored_expenses_array(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            print("DEBUG: display_stored_expenses_array, no valid stored_expenses.json file")
            return []

        try:
            with import_utils.STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                stored_expenses = json.load(f)
                print(stored_expenses)
                return stored_expenses
        except json.JSONDecodeError:
            print("stored_expenses.json is corrupted. Returning...")
            return

    def calculate_total_expenses(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            return 0
        
        with import_utils.STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
            expenses_file = json.load(f)
        return sum(ii["expense_amount"] for ii in expenses_file)


    def delete_expense(self):
        while True:
            print("Current array: ")
            stored_expenses_array = self.display_stored_expenses_array()
            
            max_index = len(stored_expenses_array) - 1
            while True:
                try:
                    index = int(input(f"Enter the index (0 to {max_index}), that you would like to delete: "))

                    if index < 0 or index > max_index:
                        print("Index out of bounds. Reprompting...")
                        continue
                    else:
                        break
                except ValueError:
                    print("Please enter a value number. Reprompting...")
                    continue
                
            value_confirmation = input(f"Is index {index} the desired value? (y/n): ")

            if import_utils.is_yes_utils(value_confirmation):
                print("Value confirmed!")
                popped = stored_expenses_array.pop(index)
                with import_utils.STORED_EXPENSES_FILE.open("w", encoding="utf-8") as f:
                    json.dump(stored_expenses_array, f, indent=2)
                print(f"Deleted: {popped}")
                return
            else:
                print("Not the desired value? Reprompting...")
                continue

    def DEBUG_expense_prompt_handler(self):
        #need to add dispatch table later, for profit and netProfit aswell
        while True:
            input_e = input("---\nInput expense (e), Request expense stats (res), Delete expense (d), or Exit (exit): ")
            stripped = input_e.strip().lower()

            if stripped in ["e", "exp", "input", "inputexpense"]:
                self.expense_input()

            elif stripped in ["r", "res", "request", "requestexpensestats"]:
                self.request_expense_stats()
                
            elif stripped in ["d","del", "delete", "deleteexpense"]:
                self.delete_expense()
            
            elif stripped in ["exit"]:
                print("Exited")
                return

            else:
                print("Error: Invalid Prompt Handler Input")


if __name__ == "__main__":
    ec = ExpenseCalculator()
    ec.DEBUG_expense_prompt_handler()
