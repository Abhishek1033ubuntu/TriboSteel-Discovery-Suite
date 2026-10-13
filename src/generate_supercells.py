"""
Module: Supercell Construction & POSCAR Exporter
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Copyright (c) 2026 Abhishek Singh
"""

import os
import random
import numpy as np
from ase import Atoms
from ase.build import bulk
from ase.io import write

from src.alloy_screening import run_screening_pipeline

MOLAR_MASSES = {
    "Fe": 55.845, "C": 12.011, "Cr": 51.996, 
    "Mo": 95.95, "Mn": 54.938, "Si": 28.085, "V": 50.941
}

def build_supercell_for_alloy(wt_percent, a_lat=2.866, dim=[4, 4, 4], seed=42):
    random.seed(seed)
    np.random.seed(seed)

    moles = {elem: (wt / MOLAR_MASSES[elem]) for elem, wt in wt_percent.items() if wt > 0}
    total_moles = sum(moles.values())
    at_percent = {elem: (m / total_moles) * 100.0 for elem, m in moles.items()}

    unit_cell = bulk("Fe", crystalstructure="bcc", a=a_lat, cubic=True)
    supercell = unit_cell.repeat(dim)
    total_host_sites = len(supercell)

    substitutional_elements = ["Cr", "Mo", "Mn", "Si", "V"]
    counts = {}
    for elem in substitutional_elements:
        if elem in at_percent and at_percent[elem] > 0:
            counts[elem] = int(round((at_percent[elem] / 100.0) * total_host_sites))

    host_indices = list(range(total_host_sites))
    random.shuffle(host_indices)
    symbols = np.array(supercell.get_chemical_symbols())

    current_idx = 0
    for elem, num in counts.items():
        symbols[host_indices[current_idx : current_idx + num]] = elem
        current_idx += num

    supercell.set_chemical_symbols(symbols)

    if "C" in at_percent and at_percent["C"] > 0:
        n_c_atoms = int(round((at_percent["C"] / 100.0) * total_host_sites))
        cell_matrix = supercell.get_cell()
        octahedral_fracs = []
        nx, ny, nz = dim
        for i in range(nx):
            for j in range(ny):
                for k in range(nz):
                    octahedral_fracs.append([(i + 0.5)/nx, j/ny, k/nz])

        chosen_indices = random.sample(range(len(octahedral_fracs)), min(n_c_atoms, len(octahedral_fracs)))
        c_positions = [np.dot(octahedral_fracs[idx], cell_matrix) for idx in chosen_indices]

        if c_positions:
            supercell.extend(Atoms("C" * len(c_positions), positions=c_positions))

    return supercell

def generate_all_poscars(top_n=10):
    df_ranked = run_screening_pipeline().head(top_n)
    
    for idx, row in df_ranked.iterrows():
        cid = f"NITRO_BRG_ALLOY_{idx:03d}"
        wt_comp = {
            "Fe": row["Fe"], "C": row["C"], "Cr": row["Cr"],
            "Mo": row["Mo"], "Mn": row["Mn"], "Si": row["Si"], "V": row["V"]
        }
        atoms = build_supercell_for_alloy(wt_comp)
        
        poscar_name = f"POSCAR_{cid}"
        write(poscar_name, atoms, format="vasp", vasp5=True, direct=True)
        print(f"  [+] Wrote {poscar_name} ({len(atoms)} total atoms)")

if __name__ == "__main__":
    generate_all_poscars()
