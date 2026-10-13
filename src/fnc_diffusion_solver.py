"""
TriboSteel-Discovery-Suite: Master End-to-End Pipeline
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Development Support: Google Gemini (AI Co-Pilot)
Copyright (c) 2026 Abhishek Singh. All rights reserved.
License: MIT
"""

import numpy as np
import pandas as pd
from scipy.special import erfc

def run_fnc_kinetics_simulation(temp_C=540.0, time_hours=4.0, depth_max_um=250.0):
    time_sec = time_hours * 3600.0
    D_eff = 2.0560e-13  # Effective diffusivity in Fe-3Cr with CrN trapping (m^2/s)
    
    z_um = np.linspace(0, depth_max_um, 500)
    z_m = z_um * 1e-6
    C_surf = 6.0  # wt% N at Fe4N compound layer surface boundary

    C_N = C_surf * erfc(z_m / (2 * np.sqrt(D_eff * time_sec)))
    
    df = pd.DataFrame({"depth_um": z_um, "N_concentration_wt": C_N})
    df.to_csv("fnc_nitrogen_diffusion_profile.csv", index=False)
    return df

if __name__ == "__main__":
    df_fnc = run_fnc_kinetics_simulation()
    print(df_fnc.head(10))
