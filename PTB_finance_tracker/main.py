from profitHandler import ProfitCalculator
from expenseHandler import ExpenseCalculator
from netProfitHandler import NetProfitCalculator


def run_profit():
        pc = ProfitCalculator()
        pc.DEBUG_profit_prompt_handler()

def run_expense():
        ec = ExpenseCalculator() 
        ec.DEBUG_expense_prompt_handler()
    
def run_net_profit():
        npc = NetProfitCalculator()
        npc.net_profit_calculation()

def exit_function():
        print("Exited at the Top Level.")
        raise SystemExit

def main():
    #using a dispatch table instead of an elif line for scalability
    dispatch = {
        "profit": run_profit,
        "expense": run_expense,
        "net_profit": run_net_profit,

        "exit": exit_function,
    }

    alias_list = {
        "profit": ("p", "profit", "profitapplication"),
        "expense": ("e", "expense", "expenseapplication"),
        "net_profit": ("c", "check", "checkstats", "stats"),

        "exit": ("exit", "stop"),
    }
    while True:
        initial_input = input("CHOOSE: Profit application (p), Expense application (e), Check stats (c), or Exit (exit): ")
        initial_stripped = initial_input.strip().lower()

        for command, aliases_var in alias_list.items():
            if initial_stripped in aliases_var:
                dispatch[command]()
                break
        else:
            print("Invalid Input. Reprompting...")
            continue

if __name__ == "__main__":
    main()

    #to do:
#make dispatch table for profitHandler and expenseHandler
# need to more efficiently implement import_utils functions (like load/save_json_utils)
