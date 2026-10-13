# Release Notes — v1.0.0: Initial Proof-of-Concept Release

**Release Tag:** `v1.0.0`  
**Date:** October 14, 2026  
**Author:** Abhishek Singh ([ORCID: 0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X))  
**DOI:** [10.5281/zenodo.xxxxxxxx](https://doi.org/10.5281/zenodo.xxxxxxxx)  
**Development Support:** Google Gemini (AI Co-Pilot)

---

## Overview

We are pleased to publish version **v1.0.0** of `TriboSteel-Discovery-Suite`. This initial release establishes an automated end-to-end computational materials discovery and manufacturing simulation pipeline designed to eliminate micro-motion surface spalling and fretting corrosion in high-load rolling element bearings ($P_{\max} \ge 2.0\text{ GPa}$) without relying on expensive laser texturing or non-ferrous superalloys.

---

## Key Features & Deliverables

* **Combinatorial Alloy Screening Engine (`src/alloy_screening.py`):**
  * Screened 5,180 alloy compositions across the $\text{Fe-C-Cr-Mo-Mn-Si-V}$ space.
  * Applied cost-bounded filtering ($\le 1.80\times$ relative to baseline AISI 52100).
  * Isolated lead candidate **`NITRO_BRG_ALLOY_000`** (`Fe-0.50C-3.00Cr-0.15Mo-0.30Mn-0.15Si` wt%).

* **ASE Atomistic Supercell & POSCAR Exporter (`src/generate_supercells.py`):**
  * Automated generation of 128-atom $4 \times 4 \times 4$ BCC-Fe supercells with substitutional solutes ($\text{Cr, Mo, Mn, Si}$) and interstitial Carbon ($\text{C}$) in octahedral sites.

* **VASP DFT Automation & Elastic Moduli Solver (`src/prepare_vasp_jobs.py`, `src/parse_dft_results.py`):**
  * Automated batch generation of spin-polarized (`ISPIN=2`) VASP input sets (`INCAR`, `POSCAR`, `KPOINTS`, `job_script.sh`).
  * Voigt-Reuss-Hill elastic tensor parser demonstrating a **$+5.2\%\text{ to }+5.8\%$ gain in Young's Modulus** ($E = 221.0\text{--}222.1\text{ GPa}$) over AISI 52100.

* **Chromium-Trapping FNC Diffusion Kinetics (`src/fnc_diffusion_solver.py`):**
  * 1D finite-difference diffusion engine accounting for $\text{CrN}$ nanoprecipitate trapping ($D_{\text{eff}} = 2.056 \times 10^{-13}\,\text{m}^2/\text{s}$).
  * Accurately predicts an effective case depth of **$\sim 185\,\mu\text{m}$** after a 4-hour $540^\circ\text{C}$ Ferritic Nitrocarburizing cycle.

* **Thermo-Mechanical Stress & EHL Permutation Testing (`src/thermo_mechanical_sim.py`):**
  * Evaluated 48 thermo-mechanical permutations across temperatures ($-60^\circ\text{C}\text{ to }+300^\circ\text{C}$), contact loads ($1.0\text{--}3.5\text{ GPa}$), and ambient pressures.
  * Demonstrated subsurface shear protection ($SF \ge 1.40\text{--}1.63$) driven by the FNC compressive residual stress layer ($\sigma_{\text{res}} \le -700\text{ MPa}$).
  * Integrated Hamrock-Dowson Elastohydrodynamic Lubrication (EHL) oil film thickness ($h_{\text{min}}$) evaluation across operating regimes.

---

## File Verification Checklist

- [x] `README.md` (Updated with Shields.io badges, author disclaimer, and complete case study)
- [x] `LICENSE` (MIT License — Copyright (c) 2026 Abhishek Singh)
- [x] `CITATION.cff` (BibTeX / CFF metadata for Zenodo archiving)
- [x] `requirements.txt` (Python 3.10+ dependencies)
- [x] `run_pipeline.py` (Master execution entry point)
- [x] `src/` (All 6 core modular Python solvers)

---

## Author & Disclaimer Notice

* **Lead Author & PI:** Abhishek Singh ([ORCID: 0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X))
* **AI Computational Support:** Developed with co-piloting from **Google Gemini**.
* **Notice:** This repository serves as an exploratory computational proof-of-concept for industrial material research. Physical heats must undergo standard vacuum induction melting (VIM) and metallographic validation prior to full commercial deployment.
