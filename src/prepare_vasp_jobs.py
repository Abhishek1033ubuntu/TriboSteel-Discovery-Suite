"""
TriboSteel-Discovery-Suite: Master End-to-End Pipeline
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Development Support: Google Gemini (AI Co-Pilot)
Copyright (c) 2026 Abhishek Singh. All rights reserved.
License: MIT
"""

import os
import glob
import re

INCAR_TEMPLATE = """! --- Electronic Convergence ---
PREC     = Accurate
ENCUT    = 520.0
EDIFF    = 1E-06
NELM     = 100
LREAL    = Auto

! --- Ionic & Cell Relaxation ---
IBRION   = 2
ISIF     = 3
NSW      = 150
EDIFFG   = -0.01
POTIM    = 0.2

! --- Spin Polarization & Smearing ---
ISPIN    = 2
ISMEAR   = 1
SIGMA    = 0.1

! --- Performance & Output ---
NCORE    = 4
LWAVE    = .FALSE.
LCHARG   = .TRUE.
"""

KPOINTS_TEMPLATE = """Gamma-Centered K-Mesh for 4x4x4 Supercell (L ~ 11.5 A)
0
Gamma
2 2 2
0 0 0
"""

SLURM_TEMPLATE = """#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --time=12:00:00
#SBATCH --partition=compute
#SBATCH --output=vasp.out
#SBATCH --error=vasp.err

module load vasp/6.4.0-intel

if [ -n "$VASP_POTCAR_DIR" ]; then
    python3 -c "from ase.io import read; atoms=read('POSCAR'); print(' '.join(dict.fromkeys(atoms.get_chemical_symbols())))" | \\
    xargs -I {{}} bash -c 'cat $VASP_POTCAR_DIR/{{}}/POTCAR' > POTCAR
fi

mpirun -np 64 vasp_std > run.log 2>&1
"""

def parse_poscar_species(poscar_path):
    with open(poscar_path, 'r') as f:
        lines = [f.readline().strip() for _ in range(7)]
    species = lines[5].split()
    counts = [int(x) for x in lines[6].split()]
    return list(zip(species, counts))

def generate_magmom_string(species_counts):
    mag_map = {"Fe": 2.2, "Cr": -1.0, "Mn": 2.0, "Mo": 0.0, "Si": 0.0, "V": 0.5, "C": 0.0}
    mag_tokens = [f"{count}*{mag_map.get(elem, 0.0)}" for elem, count in species_counts]
    return "MAGMOM   = " + " ".join(mag_tokens) + "\n"

def prepare_vasp_run_directories(output_base_dir="dft_runs"):
    poscar_files = sorted(glob.glob("POSCAR_NITRO_BRG_ALLOY_*"))
    if not poscar_files:
        return

    os.makedirs(output_base_dir, exist_ok=True)

    for poscar_file in poscar_files:
        match = re.search(r"POSCAR_(NITRO_BRG_ALLOY_\d+)", poscar_file)
        if not match:
            continue
            
        candidate_id = match.group(1)
        run_dir = os.path.join(output_base_dir, f"run_{candidate_id}")
        os.makedirs(run_dir, exist_ok=True)

        with open(poscar_file, 'r') as f_in, open(os.path.join(run_dir, "POSCAR"), 'w') as f_out:
            f_out.write(f_in.read())

        species_counts = parse_poscar_species(poscar_file)
        magmom_str = generate_magmom_string(species_counts)
        
        with open(os.path.join(run_dir, "INCAR"), 'w') as f_incar:
            f_incar.write(INCAR_TEMPLATE)
            f_incar.write(magmom_str)

        with open(os.path.join(run_dir, "KPOINTS"), 'w') as f_kpoints:
            f_kpoints.write(KPOINTS_TEMPLATE)

        with open(os.path.join(run_dir, "job_script.sh"), 'w') as f_job:
            f_job.write(SLURM_TEMPLATE.format(job_name=candidate_id))

if __name__ == "__main__":
    prepare_vasp_run_directories()
