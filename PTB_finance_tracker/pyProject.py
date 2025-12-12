import json
from pathlib import Path

from datetime import datetime

#get program directory
PROGRAM_DIR = Path(__file__).parent

#creates data subfolder next to program directory
DATA_DIR = PROGRAM_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

#data file
STORED_ORDERS_FILE = DATA_DIR / "stored_orders.json"

class profitCalculator:
    order_ID_increment = 1
    
    def __init__(self, user):
        # maybe make a login system in the future.
        self.customer = None
        self.order_ID = None
        self.amount_paid = None
        self.timestamp = None
        self.total_profit = None

    #def customer, orderID, amount paid, datetime set, 
    def prompt_amount(self):
        while True:
            print(f"Hello User")   #make login system at some point after GUI development
            
            self.customer = self.define_customer()
         
            self.order_ID = self.obtain_next_order_id()

            self.amount_paid = self.amount_paid_input_function()

            self.timestamp = datetime.now().strftime("%m-%d-%Y")

            self.total_profit = self.total_profit_calculation()

            self.save_order_to_file()

            return

    def stored_order_data_function(self):
        stored_order_data = {
            "customer": self.customer,
            "order_ID": self.order_ID,
            "amount_paid": self.amount_paid,
            "timestamp": self.timestamp,
            "total_profit": self.total_profit,
        }
        return stored_order_data

    def read_and_display_order_file(self):
        if STORED_ORDERS_FILE.exists():
            try:
                with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
                    stored_orders_1 = json.load(f)
                    print(stored_orders_1)
            except json.JSONDecodeError:
                print("stored_orders.json exists but is not valid JSON")
                return 0
        else:
            print("Can not find STORED_ORDERS_FILE")
            return 0

    def save_order_to_file(self):
        #data = stored data array
        data = self.stored_order_data_function()
        
        stored_orders_2 = []
        
        if STORED_ORDERS_FILE.exists():
            try:
                with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
                    stored_orders_2 = json.load(f)
            except json.JSONDecodeError:
                print("stored_orders.json exists but is not valid JSON (DEBUG: save_order_to_file funct)")
                return 0
        else:
            stored_orders_2 = []

        stored_orders_2.append(data)

        # open "w" - will automatically create stored_expense.json if it does not exist
        with STORED_ORDERS_FILE.open("w", encoding="utf-8") as f:
            # indent=2 for easier reading if opened
            json.dump(stored_orders_2, f, indent=2)
        
    def display_order_confirmation(self):
        response = input("Do you want to display the order array? (y/n): ")
        while True:
            if response in ["yes", "y", "Yes", "Y", "YES"]:
                self.read_and_display_order_file()
                break
            elif response in ["no", "n", "No", "N", "NO"]:
                break
            else:
                print("Invalid input, is all caps on?")
                reprompt = input("Do you want to reprompt? (y/n): ")
                if reprompt in ["yes", "y", "Yes", "Y", "YES"]:
                    continue
                elif reprompt in ["no", "n", "No", "N", "NO"]:
                    break
                else:
                    print("Invalid input. Exiting...")
                    break
    
    def define_customer(self):
        while True:
            customer_name = input("Please input customer name: ")
            customer_check = input(f"Is '{customer_name}' correct? (y/n): ")
            if customer_check in ["T", "True", "TRUE", "true", "t", "yes", "y", "Yes", "Y", "YES"]:
                print("Confirmed.")
            else:
                print("Invalid Input. Reprompting...")
                continue
            self.customer = customer_name
            print(f"Customer name defined as: {self.customer}")
            return self.customer

   # def prompt_expense(self):
    #def total_profit_calc(self):
        #access amount_paid from each index and add them together, print result for all
    #def total_expenses_calc(self):
        #leave undefined/defined in other file
   # def net_profit_calc(self):
        #total profit - expenses, (import expenses file)
    
    def delete_customer_order(self):
        #delete a customer's order in stored_orders.json by index
        print("Current array: ")
        self.read_and_display_order_file()
        
        if not STORED_ORDERS_FILE.exists():
            print("No orders file found. DEBUG: read_and_display_order returned 0.")
            return
        
        with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
            orders_file1 = json.load(f)

        max_index = len(orders_file1) - 1
        while True:
            try:
                index = int(input(f"Enter the index (0 to {max_index}), that you would like to delete: "))
                #print the indexed file and confirm
                if index < 0 or index > max_index:
                    print("Index out of bounds. Reprompting...")
                    continue
            except ValueError:
                print("Please enter a value number. Reprompting...")
                continue
            index_confirmation = input(f"Is index {index} \n ({orders_file1[index]}) \n the desired value? (y/n): ")
            if index_confirmation in ["T", "True", "TRUE", "true", "t", "yes", "y", "Yes", "Y", "YES"]:
                break
            else:
                print("Reprompting...")
                continue
        
        #.pop is mad useful
        # as f: -> f = file
        deleted_index = orders_file1.pop(index)
        print(f"Deleted: {deleted_index}")
        with STORED_ORDERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(orders_file1, f, indent=2)

    def obtain_next_order_id(self):
        # I chose to obtain orderID to increment from the stored_orders file, but you could just store it in a seperate (.txt) to increment
        if not STORED_ORDERS_FILE.exists():
            return 1

        try:
            with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
                orders_file = json.load(f)

            #if orders_file is empty
            if not orders_file:
                return 1
            
            #coudl also use [len(orders_file) - 1]["order_ID"]
            last_listed_order_id = orders_file[-1]["order_ID"]
            return last_listed_order_id + 1
        
        except (json.JSONDecodeError, KeyError, IndexError):
            #Corrupted file, missing key, or empty file errors
            print("DEBUG: obtain_next_order_id funct error, error opening STORED_ORDERS_FILE. Returning 1 for order_ID.")
            return 1

    def amount_paid_input_function(self):
        while True:    
            
            
            try:
                self.amount_paid = int(input("Please input the amount paid: "))
            except ValueError:
                print("Invalid input! Please enter a number for amount paid. Reprompting...")
                continue
        
            verification1 = input(f"Intended Value: {self.amount_paid} - (y/n): ")
        
            #optimize entire codebase with .lower() function ASAP (coming soon^TM)
            if verification1 in ["T", "True", "TRUE", "true", "t", "yes", "y", "Yes", "Y", "YES"]:
                print("Amount Initialized.")
                return self.amount_paid
            elif verification1 in ["F", "False", "f", "FALSE", "false", "no", "n", "No", "N", "NO"]:
                print("Reprompting...")
                continue
            else:
                print("Did you mispell? Reprompting...")
                continue

    # def input_or_display(self):
    #     profit_input = input("Do you want to input a profit? (y/n): ")
    #     if profit_input in ["yes", "y", "Yes", "Y", "YES"]:
    #         self.prompt_amount()
    #         self.save_order_to_file()

    #     expense_input = input("Do you want to input an expense? (y/n): ")
    #     if expense_input in ["yes", "y", "Yes", "Y", "YES"]:
    #         self.prompt_expense()

    #     net_input = input("Do you want to display total profit/expense + net profit? (y/n): ")
    #     if net_input in ["yes", "y", "Yes", "Y", "YES"]:
    #         print("DEBUG: display profit/expenses/net here")
            
    def total_profit_calculation(self):

        if not STORED_ORDERS_FILE.exists():
            self.total_profit = self.amount_paid
            return self.total_profit
           
        with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
            orders_file = json.load(f)
        profit = 0
        for ii in range(len(orders_file)):
            profit += orders_file[ii]["amount_paid"]
        
        self.total_profit = profit + self.amount_paid

        if self.total_profit is None:
            self.total_profit = self.amount_paid

        return self.total_profit
    
    #stored_orders.json last index reliant
    def current_total_profit(self):
        if not STORED_ORDERS_FILE.exists():
            return print("stored_orders.json does not exist, by extension there is not profit to pull from. (DEBUG most_recent_total_profit_ripper funct)")

        with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        profit_total = data[-1]["total_profit"]

        return print(f"{profit_total}")



    def request_stats_function(self):
        while True:
            input1 = input("Display order array (d), Profit Total (t), or Exit (e): ")
            stripped = input1.strip().lower()

            if stripped in ["d", "da", "display", "displayorderarray"]:
                self.read_and_display_order_file()

            elif stripped in ["t", "total", "profittotal"]:
                # pull profit total from most recent index of stored_orders.json
                self.current_total_profit()

            elif stripped in ["e", "exit"]:
                return print("Exited Request Stats.")
            
            else:
                print("Invalid input. Reprompting...")

    def DEBUG_profit_prompt_handler(self):
            while True:
                input1 = input("---\nInput profit (p), Request stats (r), Delete customer (d), or Exit Program (exit): ")
                stripped = input1.strip().lower()    

                if stripped in ["p", "profit", "input", "inputprofit"]:
                    self.prompt_amount()

                elif stripped in ["r", "request", "requeststats"]:
                    self.request_stats_function()
                
                elif stripped in ["d", "delete", "deletecustomer"]:
                    self.delete_customer_order()

                elif stripped in ["e", "exit"]:
                    return print("Exited.")
                else:
                    print("Error: Invalid Prompt Handler Input. Reprompting...")



    
if __name__ == "__main__":
    pc = profitCalculator("Example User")

    # DEBUG
    print("Using orders file:", STORED_ORDERS_FILE)

    pc.DEBUG_profit_prompt_handler()

    print("Program complete.")

    # to do:
    # work on net profit handler

    # optionally add seperate .json file for running profit/expense/net total
    # for easier code maintainability and simplicity