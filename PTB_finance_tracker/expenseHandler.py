import json
from pathlib import Path
from datetime import datetime

#finds directory, makes sure data file exists, creates new data file
PROGRAM_DIR = Path(__file__).parent
DATA_DIR = PROGRAM_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
STORED_EXPENSES_FILE = DATA_DIR / "stored_expenses.json"

#tried to make this a more polished version of the profitCalculator as I was writing it, so some things are declared differently
class expenseCalculator:
    
    def __init__(self, customer):
        #variable initialization
        self.expense_type = None
        self.expense_amount = None
        self.expense_description = None
        self.expense_ID = None
        self.expense_date = None
        self.total_expenses = None

    def expense_stored_object(self):
        expense_obj = {
            "expense_type": self.expense_type,
            "expense_amount": self.expense_amount,
            "expense_description": self.expense_description,
            "expense_ID": self.expense_ID,
            "expense_date": self.expense_date,
            "total_expenses": self.total_expenses,
        }
        return expense_obj

    def expense_type_function(self):
        while True:
            expense_type = input("Input Expense Type: ")
            confirm1 = input(f"Is {expense_type} correct? (y/n): ")
            #redo ALL of these with .strip().lower() like below
            stripped1 = confirm1.strip().lower()
            if stripped1 in ["true", "t", "yes", "y"]:
                self.expense_type = expense_type
                print("Expense Type Initialized.")
                return self.expense_type
            else:
                print("Expense Type assumed to be incorrect. Reprompting...")
                continue
        
    def expense_amount_neg_function(self):
        while True:
            try:
                expense_amount = int(input("Input Expense Amount ($): "))
            except ValueError:
                print("Invalid input! Please enter a number for expense amount. Reprompting...")
                continue
            
            #expense amount
            confirm2 = input(f"Is {expense_amount} correct? (y/n): ")
            if confirm2 in ["T", "True", "TRUE", "true", "t", "yes", "y", "Yes", "Y", "YES"]:
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
            if confirm3 in ["T", "True", "TRUE", "true", "t", "yes", "y", "Yes", "Y", "YES"]:
                self.expense_description = expense_description
                return self.expense_description
            else:
                print("Expense Description assumed to be incorrect. Reprompting...")
                continue

    def expense_input(self):
        while True:

            self.expense_type = self.expense_type_function()
            
            self.expense_amount = self.expense_amount_neg_function()
            
            self.expense_description = self.expense_description_function()
            
            self.expense_ID = self.expense_id_plusplus()
            
            self.expense_date = self.define_expense_date()
            
            self.total_expenses = self.total_expense_calculation()

            #store expense obj to new .json
            self.store_expense_object()
            
            print("New Expense Stored.")
            
            return
    
    def define_expense_date(self):
        self.expense_date = datetime.now().strftime("%m-%d-%Y")
        return self.expense_date

    def store_expense_object(self):
        #write expense obj to .json
        expense_data = self.expense_stored_object()
         
        stored_expenses_1 = []
        
        if STORED_EXPENSES_FILE.exists():
            try:
                with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                    stored_expenses_1 = json.load(f)
            except json.JSONDecodeError:
                print("stored_expenses.json exists but is not valid JSON or internal stored_expenses.json code is not valid (DEBUG: go to save_expense_object funct)")
                return 0
        else:
            stored_expenses_1 = []

        stored_expenses_1.append(expense_data)

        # open "w" - will automatically create stored_expense.json if it does not exist
        with STORED_EXPENSES_FILE.open("w", encoding="utf-8") as f:
            json.dump(stored_expenses_1, f, indent=2)

    def expense_id_plusplus(self):
        if not STORED_EXPENSES_FILE.exists():
            return 1

        if self.expense_ID == None:
            return 1

        try:
            with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                expenses_file = json.load(f)

            if not expenses_file:
                return 1
            
            last_listed_expense_id = expenses_file[-1]["expense_ID"]
            return last_listed_expense_id + 1
        
        except (json.JSONDecodeError, KeyError, IndexError):
            print("DEBUG: expense_id_plusplus funct error, error opening STORED_EXPENSES_FILE. Returning 1 for order_ID.")
            return 1


    def total_expense_calculation(self):
        
        if not STORED_EXPENSES_FILE.exists():
            self.total_expenses = self.expense_amount
            return self.total_expenses

        
        
        with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
            expenses_file = json.load(f)
        
        total_expenses = 0
        
        for ii in range(len(expenses_file)):
            total_expenses += expenses_file[ii]["expense_amount"]
        
        self.total_expenses = total_expenses + self.expense_amount

        if self.total_expenses is None:
            self.total_expenses == self.expense_amount

        return self.total_expenses
    
    def request_expense_stats(self):
        if not STORED_EXPENSES_FILE.exists():
            return print("stored_expenses.json does not exist. By extension no expense stats exist.")
        
        while True:
            input2 = input("Choose what to display: expense total (et), display array (da), or exit (e): ")
            stripped = input2.strip().lower()
            
            if stripped in ["et", "expensetotal"]: 
                try:
                    with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
                        expenses_file = json.load(f)
                except (json.JSONDecodeError, KeyError, IndexError):
                    print("DEBUG: JSON error at request_expense_stats")
                    return 1
                
                expense_total =  expenses_file[-1]["total_expenses"]
                print(expense_total)
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
        if not STORED_EXPENSES_FILE.exists():
            return print("DEBUG: display_stored_expenses_array, no valid stored_expenses.json file")
        
        with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
            stored_expenses = json.load(f)

            return print(stored_expenses)

    def delete_expense(self):
        print("Current array: ")
        stored_expenses_array = self.display_stored_expenses_array()
        
        max = len(stored_expenses_array) - 1
        while True:
            try:
                index = int(input(f"Enter the index (0 to {max}), that you would like to delete: "))

                if index < 0 or index > max:
                    print("Index out of bounds. Reprompting...")
                    continue
                else:
                    break
            except ValueError:
                print("Please enter a value number. Reprompting...")
                continue
                
        popped = stored_expenses_array.pop(index)
            
        value_confirmation = input(f"Is index {popped} the desired value? (y/n): ")
        stripped = value_confirmation.strip().lower()
        if stripped in ["true", "t", "yes", "y"]:
            print("Value confirmed!")
        else:
            #probably some way to reappend popped and resort array so we don't have to manually reprompt (put all this code in the while True loop), but this is easier
            print("Please Reprompt.")
            return
        
        #restore file
        with STORED_EXPENSES_FILE.open("w", encoding="utf-8") as f:
            json.dump(stored_expenses_array, f, indent=2)

            print(f"Deleted: {popped}")
            

    def DEBUG_expense_prompt_handler(self):
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
                return print("Exited")

            else:
                print("Error: Invalid Prompt Handler Input")


if __name__ == "__main__":
    ec = expenseCalculator("Example Expense") 

    ec.DEBUG_expense_prompt_handler()