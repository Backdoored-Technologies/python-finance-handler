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
        return json.dump(data, f, indent=2)
    

#core total logic
def npc_confirm(show_prompt=False):
    #gotta create an instance so it's runnable
    npc = NetProfitCalculator()
    return npc.net_profit_calculation(show_prompt=show_prompt)

#to do:
#factor import_utils.py into profitHandler and optimize it
#after this optimize expenseHandler.py
#then sleep