"""
Module: Thermo-Mechanical Stress & EHL Lubrication Permutations
Author: Abhishek Singh (https://orcid.org/0009-0004-6913-096X)
Development Support: Google Gemini (AI Co-Pilot)
Copyright (c) 2026 Abhishek Singh. All rights reserved.
License: MIT
"""

import numpy as np
import pandas as pd

temps_C = np.array([-60.0, 20.0, 150.0, 300.0])
p_contact_GPa = np.array([1.0, 2.0, 3.0, 3.5])
p_ambient_bar = np.array([0.01, 1.0, 100.0])

E0 = 221.0
sigma_y_core_20C = 1450.0
sigma_y_case_20C = 2400.0
sigma_res_surf = -750.0
case_depth_um = 185.0

alpha_E = 3.5e-4
alpha_sy = 4.0e-4

def evaluate_thermo_mechanical_grid():
    z_um = np.linspace(0, 500, 1000)
    sigma_res_z = sigma_res_surf * np.exp(-(z_um / (case_depth_um * 0.8))**2)
    
    results = []
    for T in temps_C:
        dT = T - 20.0
        E_T = E0 * (1.0 - alpha_E * dT)
        sy_core = sigma_y_core_20C * (1.0 - alpha_sy * dT)
        sy_case = sigma_y_case_20C * (1.0 - alpha_sy * dT)
        
        sy_z = sy_core + (sy_case - sy_core) * np.exp(-(z_um / case_depth_um)**1.5)
        
        for P0_GPa in p_contact_GPa:
            P0_MPa = P0_GPa * 1000.0
            a_contact = 200.0 * (P0_GPa / 2.0)**(1/3)
            zeta = z_um / a_contact
            sigma_vm = P0_MPa * (0.6 * np.exp(-((zeta - 0.48)/0.4)**2) + 0.3 * np.exp(-zeta))
            
            for P_amb in p_ambient_bar:
                p_amb_MPa = P_amb * 0.1
                sigma_eff = np.maximum(0.0, sigma_vm + 0.5 * sigma_res_z - 0.2 * p_amb_MPa)
                
                sf_z = sy_z / (sigma_eff + 1e-5)
                min_sf = np.min(sf_z)
                min_sf_depth = z_um[np.argmin(sf_z)]
                
                results.append({
                    "Temp_C": T,
                    "Contact_P_GPa": P0_GPa,
                    "Ambient_P_bar": P_amb,
                    "Modulus_E_GPa": round(E_T, 1),
                    "Min_Safety_Factor": round(min_sf, 2),
                    "Critical_Depth_um": round(min_sf_depth, 1),
                    "Status": "PASS (Safe)" if min_sf >= 1.2 else ("MARGINAL" if min_sf >= 1.0 else "FAIL (Yield)")
                })
                
    df = pd.DataFrame(results)
    df.to_csv("thermo_mechanical_simulation_results.csv", index=False)
    return df

if __name__ == "__main__":
    df_sim = evaluate_thermo_mechanical_grid()
    print(df_sim.head(10))
