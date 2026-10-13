"""
TriboSteel-Discovery-Suite: Master End-to-End Pipeline
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Copyright (c) 2026 Abhishek Singh. All rights reserved.
License: MIT
"""

import os
import sys
from src.alloy_screening import run_screening_pipeline
from src.generate_supercells import generate_all_poscars
from src.prepare_vasp_jobs import prepare_vasp_run_directories
from src.parse_dft_results import run_post_processing
from src.fnc_diffusion_solver import run_fnc_kinetics_simulation
from src.thermo_mechanical_sim import evaluate_thermo_mechanical_grid

def main():
    print("=" * 80)
    print(" TriboSteel-Discovery-Suite: Automated Alloy & Heat Treatment Pipeline")
    print(" Author: Abhishek Singh | ORCID: 0009-0004-6913-096X")
    print("=" * 80 + "\n")

    # Step 1: CALPHAD-style Cost-Bounded Combinatorial Alloy Screening
    print("[1/6] Running Combinatorial Alloy Screening...")
    candidates_df = run_screening_pipeline()
    top_candidate = candidates_df.iloc[0].to_dict()
    print(f"      Top Candidate Identified: {top_candidate}\n")

    # Step 2: Supercell Construction & POSCAR Generation
    print("[2/6] Building ASE 128-Atom BCC Supercells & Exporting POSCARs...")
    generate_all_poscars()
    print("      POSCAR generation complete.\n")

    # Step 3: VASP DFT Job Preparation
    print("[3/6] Staging VASP Run Directories & Configuration Files...")
    prepare_vasp_run_directories()
    print("      VASP run directories staged under 'dft_runs/'.\n")

    # Step 4: DFT Results Processing & Voigt-Reuss-Hill Elastic Moduli
    print("[4/6] Parsing DFT Outputs & Evaluating Elastic Stiffness Moduli...")
    mechanical_df = run_post_processing()
    print("      Mechanical properties evaluated.\n")

    # Step 5: FNC Nitrogen Trapping-Modified Diffusion Simulation
    print("[5/6] Simulating Chromium-Trapping FNC Nitrogen Kinetics...")
    fnc_df = run_fnc_kinetics_simulation(temp_C=540.0, time_hours=4.0)
    print("      FNC kinetic diffusion profile generated.\n")

    # Step 6: Thermo-Mechanical Stress & EHL Permutation Testing
    print("[6/6] Executing Thermo-Mechanical Stress & EHL Permutation Grid...")
    thermo_df = evaluate_thermo_mechanical_grid()
    print("      Thermo-mechanical evaluation complete.\n")

    print("=" * 80)
    print(" Pipeline execution finished successfully.")
    print(" All data artifacts exported to workspace CSV/JSON files.")
    print("=" * 80)

if __name__ == "__main__":
    main()
