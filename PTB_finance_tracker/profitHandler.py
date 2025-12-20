import json
from pathlib import Path
from datetime import datetime

import import_utils


class ProfitCalculator:
    order_ID_increment = 1

    def __init__(self):
        # maybe make a login system in the distant future.
        self.customer = ""
        self.order_ID = 1
        self.amount_paid = 0
        self.timestamp = ""


    def stored_order_data_function(self):
        return {
            "customer": self.customer,
            "order_ID": self.order_ID,
            "amount_paid": self.amount_paid,
            "timestamp": self.timestamp,
        }

    def dt_profit_prompt_handler(self):
        return {
            #profit input
            "p": self.prompt_amount,
            "profit": self.prompt_amount,
            "input": self.prompt_amount,
            "inputprofit": self.prompt_amount,
            
            #stats
            "r": self.request_stats_function,
            "request": self.request_stats_function,
            "requeststats": self.request_stats_function,

            #delete customer
            "d": self.delete_customer_order,
            "delete": self.delete_customer_order,
            "deletecustomer": self.delete_customer_order,

            #exit
            "e": lambda: exit(),
            "exit": lambda: exit(),

        }
    
    def dt_request_stats(self):
        return {
            "d": self.read_and_display_order_file,
            "da": self.read_and_display_order_file,
            "display": self.read_and_display_order_file,
            "displayorderarray": self.read_and_display_order_file,

            "t": import_utils.npc_confirm,
            "total": import_utils.npc_confirm,
            "profittotal": import_utils.npc_confirm,

            "e": lambda: exit(),
            "exit": lambda: exit(),
        }

    def prompt_amount(self):
    
        self.customer = self.define_customer()
        self.order_ID = self.obtain_next_order_id()

        while True:
            amount = self.amount_paid_input_function()  
            if amount is not None:
                break

        self.timestamp = datetime.now().strftime("%m-%d-%Y")
        self.save_order_to_file()

        import_utils.npc_confirm()
        return


    def read_and_display_order_file(self):
        data_read = import_utils.load_json_utils(import_utils.STORED_ORDERS_FILE)
        print(data_read)
        return data_read
    

    def save_order_to_file(self):
        data = self.stored_order_data_function()
        
        stored_orders_2 = import_utils.load_json_utils(import_utils.STORED_ORDERS_FILE)
        
        stored_orders_2.append(data)

        import_utils.save_json_utils(import_utils.STORED_ORDERS_FILE, stored_orders_2)
        return

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
            customer_name = input("\nPlease input customer name: ")
            customer_check = input(f"Is '{customer_name}' correct? (y/n): ")
            if not import_utils.is_yes_utils(customer_check):
                print("Invalid Input. Reprompting...")
                continue
            self.customer = customer_name
            print(f"Customer name defined as: {self.customer}")
            return self.customer
    
    def delete_customer_order(self):
        #neat bit of optimization here with the print + returned value all in one
        print("Current array: ")
        orders_file1 = self.read_and_display_order_file()

        if not orders_file1:
            print("No orders left to delete.")
            return
        
        # ADD SEARCH BY NAME, and then specify options with the date
        max_index = len(orders_file1) - 1
        while True:
            try:
                init_inp = input(f"\nEnter the index (0 to {max_index}), that you would like to delete or cancel (c): ").strip().lower()
                
                if init_inp in ("c", "cancel"):
                    return
                
                index = int(init_inp)
                if index < 0 or index > max_index:
                    print("Index out of bounds. Reprompting...")
                    continue
            except ValueError:
                print("Please enter a value number. Reprompting...")
                continue
            index_confirmation = input(f"\nIs index {index} \n ({orders_file1[index]}) \n the desired value? (y/n): ")
            if import_utils.is_yes_utils(index_confirmation):
                break
            else:
                print("Reprompting...")
                continue
        
        deleted_index = orders_file1.pop(index)
        print(f"Deleted: {deleted_index}")

        import_utils.save_json_utils(import_utils.STORED_ORDERS_FILE, orders_file1)
        return
    

    def obtain_next_order_id(self):
        if not import_utils.STORED_ORDERS_FILE.exists():
            return 1

        try:
            orders_file = import_utils.load_json_utils(import_utils.STORED_ORDERS_FILE)

            if not orders_file:
                return 1
            
            #figure out a different way to do this later, this could introduce inconsistencies when deleting orders
            last_listed_order_id = orders_file[-1]["order_ID"]
            return last_listed_order_id + 1
        
        except (json.JSONDecodeError, KeyError, IndexError):
            #Corrupted file, missing key, or empty file errors
            print("DEBUG: obtain_next_order_id funct error, error opening STORED_ORDERS_FILE. Returning 1 for order_ID.")
            return 1


    def amount_paid_input_function(self):
        while True:    
            try:
                input_1 = float(input("\nPlease input the amount paid: $").strip())
                if input_1 < 0:
                    print("Profit amount cannot be negative. Reprompting...")
                    continue
            
            except ValueError:
                print("Invalid input! Please enter a number for amount paid. Reprompting...")
                continue
        
            verification1 = input(f"\nIntended Value: {input_1} - (y/n): ")
        
            if import_utils.is_yes_utils(verification1):
                self.amount_paid = input_1
                return self.amount_paid
            elif import_utils.is_no_utils(verification1):
                print("Reprompting...")
                continue
            else:
                print("Did you misspell? Reprompting...")
                continue


    def request_stats_function(self):
        import_utils.ge_file_checker(import_utils.STORED_ORDERS_FILE)

        dt_rs = self.dt_request_stats()

        while True:
            stripped = input("\nDisplay order array (d), Profit Total (t), or Exit (e): ").strip().lower()

            handler = dt_rs.get(stripped)

            if stripped in ("t", "total", "profittotal"):
                #could cache this I bet
                result = handler("total_profits")
                return result

            if handler is None:
                print("Invalid command.")
                continue

            if callable(handler):
                handler()

            #need a better way to exit than lambdas, implement in a later patch

            continue


    def DEBUG_profit_prompt_handler(self):
        import_utils.ge_file_checker(import_utils.STORED_ORDERS_FILE)

        dt_pp = self.dt_profit_prompt_handler()
        
        while True:
            stripped = input("\nProfit Handler:\nInput profit (p), Request stats (r), Delete customer (d), or Exit Program (exit): ").strip().lower()

            handler = dt_pp.get(stripped)
            
            if handler is None:
                print("Invalid command.")
                continue
            
            if callable(handler):
                handler()

            #need a better way to exit than lambdas, implement in a later patch

            continue


    
if __name__ == "__main__":
    pc = ProfitCalculator()
    pc.DEBUG_profit_prompt_handler()

