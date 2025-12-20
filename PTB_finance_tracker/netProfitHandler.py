from pathlib import Path
import json
from datetime import datetime

#filepath for stored_netvalues.json
PROGRAM_DIR = Path(__file__).parent
DATA_DIR = PROGRAM_DIR /  "data"
DATA_DIR.mkdir(exist_ok=True)

#file declaration
STORED_EXPENSES_FILE = DATA_DIR / "stored_expenses.json"
STORED_ORDERS_FILE = DATA_DIR / "stored_orders.json"
STORED_NETVALUES_FILE = DATA_DIR / "stored_netvalues.json"


class NetProfitCalculator:

    def __init__(self):
        #changed this for less TypeErrors being raised later
        self.total_expenses = 0
        self.total_profits = 0
        self.net_profit = 0
        self.date = ""
        self.profit_items_amount = 0
        self.expense_items_amount = 0

    def net_profit_object(self):
        return {
            "total_expenses": self.total_expenses,
            "total_profits": self.total_profits,
            "net_profit": self.net_profit,
            "date": self.date,
            "profit_items_amount": self.profit_items_amount,
            "expense_items_amount": self.expense_items_amount,
        }



    def net_profit_calculation(self,):
        self.empty_file_checker()

        orders_f = self.load_json(STORED_ORDERS_FILE)
        expenses_f = self.load_json(STORED_EXPENSES_FILE)

        self.update_expenses(expenses_f)
        self.update_profits(orders_f)

        #added since self.total_expenses is negative
        self.net_profit = self.total_profits + self.total_expenses
        self.date = datetime.now().strftime("%m-%d-%Y")
        
        self.update_profit_items_amount(orders_f)
        self.update_expenses_items_amount(expenses_f)

        self.save_net_profit_object()
        
        #i return the value here so the user knows what to pick, no show prompt is required because you can just isolate
        # the desired value from the self.net_project_object returned and make the user either display it or not at runtime
        return self.net_profit_object()



    def load_json(self, path: Path):
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def empty_file_checker():
        if not STORED_NETVALUES_FILE.exists():
            with STORED_NETVALUES_FILE.open("w", encoding="utf-8") as f:
               json.dump({}, f) 

        if not STORED_ORDERS_FILE.exists():
            raise FileNotFoundError("DEBUG: stored_orders.json does not exist.")
        
        if not STORED_EXPENSES_FILE.exists():
            raise FileNotFoundError("DEBUG: stored_expenses.json does not exist")

    def update_expenses(self, expenses_f):
            if not expenses_f:
                self.total_expenses = 0
                return
             
            self.total_expenses = sum(ii["expense_amount"] for ii in expenses_f)
            return

    def update_profits(self, orders_f):
            if not orders_f:
                self.total_profits = 0
                return 
            
            self.total_profits = sum(ii["amount_paid"] for ii in orders_f)
            return

    def update_profit_items_amount(self, orders_f):
            self.profit_items_amount = len(orders_f)
            return
            
    def update_expenses_items_amount(self, expenses_f):
            self.expense_items_amount  = len(expenses_f)
            return

    def save_net_profit_object(self):
        current_file_obj = self.net_profit_object()

        with STORED_NETVALUES_FILE.open("w", encoding="utf-8") as f:
            json.dump(current_file_obj, f, indent=2)
    

if __name__ == "__main__":
    npc = NetProfitCalculator()
    npc.net_profit_calculation()

