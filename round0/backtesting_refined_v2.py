import re
import os
import itertools
from tqdm import tqdm

from trader_params import modify_params, Product



def generate_param_combinations(param_grid):
    param_names = param_grid.keys()
    param_values = param_grid.values()
    combinations = list(itertools.product(*param_values))
    return [dict(zip(param_names, combination)) for combination in combinations]

def generate_pnl():
    os.system("prosperity3bt trader.py 0 --merge-pnl > backtest_logger_file.txt")

    log_file_path = 'backtest_logger_file.txt'
    print("passed")
    with open(log_file_path, 'r') as file:
        log_content = file.read()

    match = re.search(r'Total profit:\s*([\d,]+)', log_content)

    if match:
        total_profit = match.group(1)  
        total_profit = int(total_profit.replace(',', ''))
        print(f"Total profit: {total_profit}")
        return float(total_profit)
    else:
        print("Total profit not found.")



    


def generate_grid_search():
    generate_pnl()

    param_grid = {
    Product.RAINFOREST_RESIN: {
        "fair_value": [10000],
        "take_width": [0.5],
        "clear_width": [0.5],
        # for making
        "disregard_edge": [0.5],  # disregards orders for joining or pennying within this value from fair
        "join_edge": [0.5],  # joins orders within this edge
        "default_edge": [0.5],
        "soft_position_limit": [10],
    },
    Product.KELP: {
        "take_width": [0.5],
        "clear_width": [0.5],
        "prevent_adverse": [True],
        "adverse_volume": [15],
        "reversion_beta": [-0.229],
        "disregard_edge": [1],
        "join_edge": [0],
        "default_edge": [1],
    },
}
    param_combinations = generate_param_combinations(param_grid)
    for params in param_combinations:
        modify_params(params)
        pnl = generate_pnl()
        print(pnl)

generate_grid_search()



        
        