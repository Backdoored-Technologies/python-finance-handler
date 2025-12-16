import json
from pathlib import Path
from datetime import datetime

import import_utils


class ProfitCalculator:
    order_ID_increment = 1

    def __init__(self):
        # maybe make a login system in the distant future.
        self.customer = None
        self.order_ID = None
        self.amount_paid = None
        self.timestamp = None
        #self.total_profit = None

    def prompt_amount(self):
        while True:
            self.customer = self.define_customer()
            self.order_ID = self.obtain_next_order_id()
            self.amount_paid = self.amount_paid_input_function()
            self.timestamp = datetime.now().strftime("%m-%d-%Y")
            #self.total_profit = self.total_profit_calculation()

            import_utils.npc_confirm()

            self.save_order_to_file()

            return

    def stored_order_data_function(self):
        return {
            "customer": self.customer,
            "order_ID": self.order_ID,
            "amount_paid": self.amount_paid,
            "timestamp": self.timestamp,
            #"total_profit": self.total_profit,
        }


    def read_and_display_order_file(self):
        if import_utils.STORED_ORDERS_FILE.exists():
            try:
                with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
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
        
        if import_utils.STORED_ORDERS_FILE.exists():
            try:
                with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
                    stored_orders_2 = json.load(f)
            except json.JSONDecodeError:
                print("stored_orders.json exists but is not valid JSON (DEBUG: save_order_to_file funct)")
                return 0
        else:
            stored_orders_2 = []

        stored_orders_2.append(data)

        with import_utils.STORED_ORDERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(stored_orders_2, f, indent=2)
        
    def display_order_confirmation(self):
        reprompt1 = input("Do you want to display the order array? (y/n): ")
        while True:
            if import_utils.is_yes_utils(reprompt1):
                self.read_and_display_order_file()
                break
            elif import_utils.is_no_utils(reprompt1):
                break
            else:
                print("Invalid input, is all caps on?")
                reprompt2 = input("Do you want to reprompt? (y/n): ")
                if import_utils.is_no_utils(reprompt2): 
                    break
                elif import_utils.is_yes_utils(reprompt2):
                    continue
                else:
                    print("Invalid input. Exiting...")
                    break
    
    def define_customer(self):
        while True:
            customer_name = input("Please input customer name: ")
            customer_check = input(f"Is '{customer_name}' correct? (y/n): ")
            if not import_utils.is_yes_utils(customer_check):
                print("Invalid Input. Reprompting...")
                continue
            self.customer = customer_name
            print(f"Customer name defined as: {self.customer}")
            return 
    
    def delete_customer_order(self):
        #delete a customer's order in stored_orders.json by index
        print("Current array: ")
        self.read_and_display_order_file()
        
        if not import_utils.STORED_ORDERS_FILE.exists():
            print("No orders file found. DEBUG: read_and_display_order returned 0.")
            return
        
        with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
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
            if import_utils.is_yes_utils(index_confirmation):
                break
            else:
                print("Reprompting...")
                continue
        
        deleted_index = orders_file1.pop(index)
        print(f"Deleted: {deleted_index}")
        with import_utils.STORED_ORDERS_FILE.open("w", encoding="utf-8") as f:
            json.dump(orders_file1, f, indent=2)

    def obtain_next_order_id(self):
        # I chose to obtain orderID to increment from the stored_orders file, but you could just store it in a seperate (.txt) to increment
        if not import_utils.STORED_ORDERS_FILE.exists():
            return 1

        try:
            with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
                orders_file = json.load(f)

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
                input_1 = float(input("Please input the amount paid: $").strip())
                if input_1 < 0:
                    print("Profit amount cannot be negative. Reprompting...")
                    continue
            
            except ValueError:
                print("Invalid input! Please enter a number for amount paid. Reprompting...")
                continue
        
            verification1 = input(f"Intended Value: {input_1} - (y/n): ")
        
            if import_utils.is_yes_utils(verification1):
                self.amount_paid = input_1
                return self.amount_paid
            elif import_utils.is_no_utils(verification1):
                print("Reprompting...")
                continue
            else:
                print("Did you mispell? Reprompting...")
                continue

#I do this better later            
    # def total_profit_calculation(self):
    #     if not import_utils.STORED_ORDERS_FILE.exists():
    #         self.total_profit = self.amount_paid
    #         return self.total_profit
           
    #     with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
    #         orders_file = json.load(f)

    #     if not orders_file:
    #         #mutates value and returns value, but is necessary
    #         self.total_profit = 0
    #         return self.total_profit

    #     profit = 0
    #     for ii in range(len(orders_file)):
    #         profit += orders_file[ii]["amount_paid"]
        
    #     self.total_profit = profit + self.amount_paid

    #     if self.total_profit is None:
    #         self.total_profit = self.amount_paid

    #     return self.total_profit
    

    # #stored_orders.json last index reliant
    # def current_total_profit(self):
    #     if not import_utils.STORED_ORDERS_FILE.exists():
    #         return print("stored_orders.json does not exist, by extension there is not profit to pull from. (DEBUG most_recent_total_profit_ripper funct)")

    #     with import_utils.STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
    #         data = json.load(f)

    #     profit_total = data[-1]["total_profit"]
    #     print(f"{profit_total}")
    #     return

    def request_stats_function(self):
        while True:
            input1 = input("Display order array (d), Profit Total (t), or Exit (e): ")
            stripped = input1.strip().lower()

            if stripped in ["d", "da", "display", "displayorderarray"]:
                self.read_and_display_order_file()

            elif stripped in ["t", "total", "profittotal"]:
                #self.current_total_profit()
                import_utils.npc_confirm(show_prompt=True)

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
    pc = ProfitCalculator()
    pc.DEBUG_profit_prompt_handler()
    