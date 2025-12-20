from pathlib import Path
import json

from netProfitHandler import NetProfitCalculator

#directory declarations
PROGRAM_DIR = Path(__file__).parent
DATA_DIR = PROGRAM_DIR /  "data"
DATA_DIR.mkdir(exist_ok=True)

STORED_EXPENSES_FILE = DATA_DIR / "stored_expenses.json"
STORED_ORDERS_FILE = DATA_DIR / "stored_orders.json"
STORED_NETVALUES_FILE = DATA_DIR / "stored_netvalues.json"


YES_VALUES = {"y", "yes", "t", "true"}
NO_VALUES = {"no", "n", "f", "false"}



#     UTILITY FUNCTIONS

#yes/no logic with type hinting
def is_yes_utils(s: str) -> bool:
    return bool(s and s.strip().lower() in YES_VALUES)
    
def is_no_utils(s: str) -> bool:
    return bool(s and s.strip().lower() in NO_VALUES)

#json stuff
def load_json_utils(f_path: Path):
    if not f_path.exists():
        return []
    
    try:
        with f_path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Json file is corrupted. Returned empty list in its place.")
        return []

def save_json_utils(f_path: Path, data):
    with f_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        return

def ge_file_checker(path: Path):
    try:
        orders = load_json_utils(path)
    except FileNotFoundError:
        print(f"{path} does not exist. Creating new file...")
        orders = []
        save_json_utils(path, orders)
    except json.JSONDecodeError:
        print("stored_orders.json is corrupted.")
        
    return



#                NPC TOTAL FUNCTIONS

#core total logic
def npc_confirm(show=None):
    npc = NetProfitCalculator()
    req = npc.net_profit_calculation()


    if show == "total_expenses":
        #printing isn't necessary, could just print at runtime. im just lazy
        return print(req["total_expenses"])
         
    if show == "total_profits":
        return print(req["total_profits"])

    if show is None:
        return req

    #gets value out of object returned by net_profit_calculation
    return req.get(show)

