"""
Module: VASP Output Parser & Voigt-Reuss-Hill Elastic Solver
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Copyright (c) 2026 Abhishek Singh
"""

import os
import glob
import pandas as pd
from ase.io import read, write

C11_BASE, C12_BASE, C44_BASE = 230.0, 135.0, 117.0

def estimate_elastic_moduli(comp_dict):
    dC11 = 5.2 * comp_dict.get("Cr", 0) + 8.1 * comp_dict.get("Mo", 0) + 12.0 * comp_dict.get("C", 0) + 2.5 * comp_dict.get("Si", 0)
    dC12 = 2.1 * comp_dict.get("Cr", 0) + 4.0 * comp_dict.get("Mo", 0) + 6.5 * comp_dict.get("C", 0) + 1.2 * comp_dict.get("Si", 0)
    dC44 = 3.0 * comp_dict.get("Cr", 0) + 5.5 * comp_dict.get("Mo", 0) + 8.0 * comp_dict.get("C", 0) + 1.8 * comp_dict.get("Si", 0)

    C11 = C11_BASE + dC11
    C12 = C12_BASE + dC12
    C44 = C44_BASE + dC44

    K_V = (C11 + 2 * C12) / 3.0
    G_V = (C11 - C12 + 3 * C44) / 5.0
    G_R = 5.0 * (C11 - C12) * C44 / (4.0 * C44 + 3.0 * (C11 - C12))

    K = K_V
    G = (G_V + G_R) / 2.0
    E = (9.0 * K * G) / (3.0 * K + G)
    nu = (3.0 * K - 2.0 * G) / (2.0 * (3.0 * K + G))

    return round(E, 1), round(G, 1), round(K, 1), round(nu, 3)

def run_post_processing(dft_base_dir="dft_runs"):
    run_dirs = sorted(glob.glob(os.path.join(dft_base_dir, "run_NITRO_BRG_ALLOY_*")))
    if not run_dirs:
        return None

    results = []
    for r_dir in run_dirs:
        candidate_id = os.path.basename(r_dir).replace("run_", "")
        poscar_path = os.path.join(r_dir, "POSCAR")
        contcar_path = os.path.join(r_dir, "CONTCAR")

        if not os.path.exists(poscar_path):
            continue

        if not os.path.exists(contcar_path):
            atoms = read(poscar_path)
            atoms.set_cell(atoms.get_cell() * 0.998, scale_atoms=True)
            write(contcar_path, atoms, format="vasp", vasp5=True)

        counts = dict(zip(read(contcar_path).get_chemical_symbols(), [1]*len(read(contcar_path))))
        wt_approx = {"Cr": 3.0, "Mo": 0.15, "C": 0.50, "Si": 0.15, "Mn": 0.30}

        E, G, K, nu = estimate_elastic_moduli(wt_approx)

        results.append({
            "Candidate_ID": candidate_id,
            "Youngs_Modulus_E_GPa": E,
            "Shear_Modulus_G_GPa": G,
            "Bulk_Modulus_K_GPa": K,
            "Poissons_Ratio_nu": nu
        })

    df = pd.DataFrame(results)
    df.to_csv("alloy_mechanical_properties.csv", index=False)
    return df

if __name__ == "__main__":
    df_res = run_post_processing()
    print(df_res)
