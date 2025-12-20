import json
from pathlib import Path
from datetime import datetime

import import_utils



class ExpenseCalculator:
    #EXIT = "EXIT"

    def __init__(self):
        self.expense_type = ""
        self.expense_amount = 0
        self.expense_description = ""
        self.expense_ID = 1
        self.expense_date = ""

    def expense_stored_object(self):
        expense_obj = {
            "expense_type": self.expense_type,
            "expense_amount": self.expense_amount,
            "expense_description": self.expense_description,
            "expense_ID": self.expense_ID,
            "expense_date": self.expense_date,
        }
        return expense_obj

#method titles binded to a user-inputted string
    def dt_expense_input(self):
        return {
            "e":  self.expense_input,
            "exp": self.expense_input,
            "input": self.expense_input,
            "inputexpense": self.expense_input,

            "r": self.request_expense_stats,
            "res": self.request_expense_stats,
            "request": self.request_expense_stats,
            "requestexpensestats": self.request_expense_stats,

            "d": self.delete_expense,
            "del": self.delete_expense,
            "delete": self.delete_expense,
            "deleteexpense": self.delete_expense,

            "exit": lambda: exit(),
        }


#bear witness to my verbose names
    def dt_request_expense_stats(self):
        return {
            "et": import_utils.npc_confirm,
            "expense": import_utils.npc_confirm,
            "expensetotal": import_utils.npc_confirm,
            "total": import_utils.npc_confirm,
            
            "da": self.display_stored_expenses_array,
            "displayarray": self.display_stored_expenses_array,
            "display": self.display_stored_expenses_array,

            "e": lambda: exit(),
            "exit": lambda: exit(),
                }


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
            self.expense_date = datetime.now().strftime("%m-%d-%Y")

            self.store_expense_object()

            import_utils.npc_confirm()
            return


    def store_expense_object(self):
        expense_data = self.expense_stored_object()
         
        stored_expenses_1 = import_utils.load_json_utils(import_utils.STORED_EXPENSES_FILE)

        stored_expenses_1.append(expense_data)
        
        import_utils.save_json_utils(import_utils.STORED_EXPENSES_FILE, stored_expenses_1)


#I gotta try to reuse this code somehow, it's duplicated in profitHandler. Probably need to make a function in import_utils
    def expense_id_plusplus(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            return 1

        try:
            expenses_file = import_utils.load_json_utils(import_utils.STORED_EXPENSES_FILE)

            if not expenses_file:
                return 1
            
            last_listed_expense_id = expenses_file[-1]["expense_ID"]
            return last_listed_expense_id + 1
        
        #dont raise any error here because you dont really need to
        except (json.JSONDecodeError, KeyError, IndexError):
            print("DEBUG: expense_id_plusplus funct error, error opening import_utils.STORED_EXPENSES_FILE. Returning 1 for order_ID.")
            return 1


    def display_stored_expenses_array(self):
        stored_expense = import_utils.load_json_utils(import_utils.STORED_EXPENSES_FILE)
        print(stored_expense)
        return stored_expense


    def delete_expense(self):
        while True:
            print("Current array: ")
            stored_expenses_array = self.display_stored_expenses_array()

            if not stored_expenses_array:
                print("No expenses to delete.")
                return
        
            max_index = len(stored_expenses_array) - 1
            while True:
                try:
                    index = int(input(f"Enter the index (0 to {max_index}), that you would like to delete: ").strip())

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
                popped = stored_expenses_array.pop(index)
                
                import_utils.save_json_utils(import_utils.STORED_EXPENSES_FILE, stored_expenses_array)

                print(f"Deleted: {popped}")
                return
            else:
                confirm_var = input("Not the desired value? Reprompt (r) or exit (e): ").strip().lower()
                if confirm_var in ["r", "reprompt"]:
                    continue
                else:
                    return


    def request_expense_stats(self):
        if not import_utils.STORED_EXPENSES_FILE.exists():
            print("stored_expenses.json does not exist. By extension no expense stats exist.")
            return

        dispatch_table = self.dt_request_expense_stats()

        while True:
            stripped = input("\nChoose what to display: expense total (et), display array (da), or exit (e): ").strip().lower()

            dispatch_funct = dispatch_table.get(stripped)

            if stripped in ("et", "expense", "total", "expensetotal"):
                dispatch_funct("total_expenses")
                continue

            if dispatch_funct is None:
                print("Invalid input. Reprompting...")
                continue
            
            #need a better way to exit than lambdas, implement in a later patch

            if callable(dispatch_funct):
                dispatch_funct()

            continue


    def DEBUG_expense_prompt_handler(self):
        dispatch_table = self.dt_expense_input()

        while True:
            stripped = input("\nExpense Handler:\nInput expense (e), Request expense stats (res), Delete expense (d), or Exit (exit): ").strip().lower()
            
            dispatch_caller = dispatch_table.get(stripped)

            if dispatch_caller is None:
                print("Invalid input. Reprompting...")
                continue

            #need a better way to exit than lambdas, implement in a later patch

            if callable(dispatch_caller):
                dispatch_caller()
            
            continue

if __name__ == "__main__":
    ec = ExpenseCalculator()
    ec.DEBUG_expense_prompt_handler()
