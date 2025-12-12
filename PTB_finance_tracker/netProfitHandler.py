from pathlib import Path
import json
from datetime import datetime

#information obtained from jsons below
PROGRAM_DIR = Path(__file__).parent
DATA_DIR = PROGRAM_DIR /  "data"
DATA_DIR.mkdir(exist_ok=True)

STORED_EXPENSES_FILE = DATA_DIR / "stored_expenses.json"
STORED_ORDERS_FILE = DATA_DIR / "stored_orders.json"
STORED_NETVALUES_FILE = DATA_DIR / "stored_netvalues.json"


class netProfitCalculator:

    def __init__(self):
        self.total_expenses = None
        self.total_profits = None
        self.net_profit = None
        self.date = None
        self.profit_items_amount = None
        self.expense_items_amount = None

    def net_profit_object(self):
        #just made this return the dict, thought it was simpler than making it return a newly declared variable
        return {
            "total_expenses": self.total_expenses,
            "total_profits": self.total_profits,
            "net_profit": self.net_profit,
            "date": self.date,
            "profit_items_amount": self.profit_items_amount,
            "expense_items_amount": self.expense_items_amount,
        }
    
    def net_profit_calculation(self):
        #could import this into expense + profit Handler and have it run each time any change is made, but this seems simpler
        while True:
            self.empty_file_checker()

            self.clear_netvalues_file()

            self.fetch_expenses()

            self.fetch_profits()

            #added since self.total_expenses is negative
            self.net_profit = self.total_profits + self.total_expenses
            
            self.date = datetime.now().strftime("%m-%d-%Y")
            
            self.fetch_profit_items_amount()
            
            self.fetch_expenses_items_amount()

            self.save_net_profit_object()

            return print(f"Current file contents: {self.net_profit_object()}")

    @staticmethod
    def empty_file_checker():
        if not STORED_NETVALUES_FILE.exists():
            with STORED_NETVALUES_FILE.open("w", encoding="utf-8") as f:
               json.dump([], f) 

        if not STORED_EXPENSES_FILE.exists() or not STORED_ORDERS_FILE.exists():
            return print("DEBUG: stored_expenses.json  OR  stored_orders.json does not exist. net_profit_calculation funct")
        
    #add optional user input function for displaying data
    

    def fetch_expenses(self):
        with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
            stored_expenses_data = json.load(f)
            if not stored_expenses_data:
                self.total_expenses = 0
                return self.total_expenses
             
            self.total_expenses = stored_expenses_data[-1]["total_expenses"]

    def fetch_profits(self):
        with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
            stored_orders_data = json.load(f)
            if not stored_orders_data:
                self.total_profits = 0
                return self.total_profits
            
            self.total_profits = stored_orders_data[-1]["total_profit"]

    def fetch_profit_items_amount(self):
        with STORED_ORDERS_FILE.open("r", encoding="utf-8") as f:
            stored_order_data = json.load(f)
            stored_order_data_length = len(stored_order_data)
            self.profit_items_amount = stored_order_data_length
            
    def fetch_expenses_items_amount(self):
        with STORED_EXPENSES_FILE.open("r", encoding="utf-8") as f:
            stored_expense_data = json.load(f)
            stored_expense_data_length = len(stored_expense_data)
            self.expense_items_amount = stored_expense_data_length

    def save_net_profit_object(self):
        try:
            with STORED_NETVALUES_FILE.open("r", encoding="utf-8") as f:
                current_file = json.load(f)
        except json.JSONDecodeError:
            return print("DEBUG: JSONDecodeError save_net_profit_object function")
        
        current_file.append(self.net_profit_object())

        with STORED_NETVALUES_FILE.open("w", encoding="utf-8") as f:
            json.dump(current_file, f, indent=2)
    
    @staticmethod
    def clear_netvalues_file():
        if not STORED_NETVALUES_FILE.exists():
            return
        
        with STORED_NETVALUES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)

        data.clear()  #data.clear() is slightly faster despite (data = []) having better time complexity

        with STORED_NETVALUES_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    npc = netProfitCalculator()

    npc.net_profit_calculation()
