from profitHandler import profitCalculator
from expenseHandler import expenseCalculator
from netProfitHandler import netProfitCalculator

from pathlib import Path
import json
from datetime import datetime

if __name__ == "__main__":
    print("Placeholder.")

    while True:
        ptb_input = input("Profit application (p), Expense application (e), Check stats (c), or Exit (exit): ")
        stripped = ptb_input.strip().lower()

        if stripped in ["p", "profit", "profitapplication"]:
            pc = profitCalculator("Example User")
            pc.DEBUG_profit_prompt_handler()
        elif stripped in ["e", "expense", "expenseapplication"]:
            ec = expenseCalculator() 
            ec.DEBUG_expense_prompt_handler()
        elif stripped in ["c", "check", "checkstats", "stats"]:
            npc = netProfitCalculator()
            npc.net_profit_calculation()
        elif stripped in ["exit", "stop"]:
            print("Exited Program.")
            break
        else:
            print("Reprompting...")
            continue