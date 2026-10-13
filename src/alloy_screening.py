"""
Module: Alloy Screening & Cost Modeling
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Development Support: Google Gemini (AI Co-Pilot)
Copyright (c) 2026 Abhishek Singh. All rights reserved.
License: MIT
"""

import itertools
import pandas as pd

CONFIG = {
    "max_cost_multiplier": 1.80,
    "elemental_prices_usd_kg": {
        "Fe": 0.12, "C": 0.00, "Cr": 2.80, "Mo": 42.00, 
        "Mn": 1.95, "Si": 1.80, "V": 35.00
    },
    "grid_bounds": {
        "C":  {"min": 0.30, "max": 0.60, "step": 0.05},
        "Cr": {"min": 0.80, "max": 3.00, "step": 0.20},
        "Mo": {"min": 0.15, "max": 0.55, "step": 0.10},
        "Mn": {"min": 0.30, "max": 0.90, "step": 0.15},
        "Si": {"min": 0.15, "max": 0.60, "step": 0.15},
        "V":  {"min": 0.00, "max": 0.20, "step": 0.05}
    }
}

def calculate_cost_index(composition, spot_prices, baseline_cost):
    total_cost = sum((composition.get(elem, 0.0) / 100.0) * price 
                     for elem, price in spot_prices.items())
    return total_cost / baseline_cost

def run_screening_pipeline(cfg=CONFIG):
    prices = cfg["elemental_prices_usd_kg"]
    grid_cfg = cfg["grid_bounds"]
    
    baseline_cost = (97.5 / 100.0 * prices["Fe"]) + (1.5 / 100.0 * prices["Cr"])
    
    grid = {}
    for elem, bounds in grid_cfg.items():
        steps = int(round((bounds["max"] - bounds["min"]) / bounds["step"])) + 1
        grid[elem] = [round(bounds["min"] + i * bounds["step"], 2) for i in range(steps)]
        
    keys, values = zip(*grid.items())
    candidates = []
    
    for combo in itertools.product(*values):
        comp = dict(zip(keys, combo))
        comp["Fe"] = round(100.0 - sum(comp.values()), 2)
        
        if comp["Fe"] < 88.0:
            continue
            
        cost_index = calculate_cost_index(comp, prices, baseline_cost)
        
        if cost_index <= cfg["max_cost_multiplier"]:
            comp["cost_index"] = round(cost_index, 3)
            candidates.append(comp)
            
    df = pd.DataFrame(candidates)
    
    filtered = df[
        (df["C"] >= 0.35) & (df["C"] <= 0.50) &
        (df["Cr"] >= 1.00) &
        (df["Cr"] + df["Mo"] + df["V"] >= 1.50)
    ].copy()
    
    filtered["H_pot"] = round(1.5 * filtered["Cr"] + 2.0 * filtered["Mo"] + 3.5 * filtered["V"], 3)
    filtered["fitness_score"] = round((filtered["H_pot"] * filtered["C"]) / filtered["cost_index"], 3)
    
    ranked_df = filtered.sort_values(by="fitness_score", ascending=False).reset_index(drop=True)
    return ranked_df

if __name__ == "__main__":
    df_top = run_screening_pipeline()
    print(df_top.head(10))
