# TriboSteel-Discovery-Suite

> **Cost-Bounded Quantum-Mechanical Discovery and Thermochemical Engineering of Anti-Fretting Bearing Alloys for Extreme Environments**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![DFT VASP Verified](https://img.shields.io/badge/DFT-VASP%20Verified-00599C?style=flat-square&logo=vlc&logoColor=white)](https://www.vasp.at/)
[![ORCID 0009-0004-6913-096X](https://img.shields.io/badge/ORCID-0009--0004--6913--096X-a6ce39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0004-6913-096X)
[![Powered by Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?style=flat-square&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Open in Google Colab](https://img.shields.io/badge/Open%20in-Google%20Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)](https://colab.research.google.com/)
[![DOI 10.5281/zenodo.23349563](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.23349563-blue?style=flat-square)](https://zenodo.org/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

[![Alloy Core Target](https://img.shields.io/badge/Alloy%20Target-Fe--0.50C--3.00Cr--0.15Mo-darkgreen?style=flat-square)](#)
[![Process Gaseous FNC](https://img.shields.io/badge/Process-Gaseous%20FNC%20%28540%C2%B0C%29-orange?style=flat-square)](#)
[![Case Hardness](https://img.shields.io/badge/Case%20Hardness-%3E780%20HV-red?style=flat-square)](#)
[![Cost Multiplier](https://img.shields.io/badge/Cost%20Multiplier-1.702x%20vs%2052100-purple?style=flat-square)](#)

---

## 📌 Author Notice & Research Scope

> **Note on Research Background:**
> The author holds no formal academic specialization or industrial background in mechanical or metallurgical engineering. This repository represents an independent exploratory trial and computational proof-of-concept in advanced materials discovery, atomistic quantum modeling (DFT), and thermochemical process engineering. The formulations, kinetic diffusion models, and heat-treatment recipes are made available as a open-access reference for industrial metallurgists, foundry holding engineers, and computational materials scientists seeking to validate these candidate chemistries through physical trial heats.

---

## 📑 Executive Overview & Case Study

Rolling element bearings operating under heavy contact pressures ($P_{\text{max}} \ge 2.0\text{ GPa}$) in wind turbine main-shafts, aerospace actuators, rail axle boxes, and heavy electromechanical machinery suffer severe **rolling contact fatigue (RCF)** and **fretting corrosion**. Small-amplitude oscillatory micro-motion ($1\text{--}50\,\mu\text{m}$ slip) destroys surface passive oxide films, exposing reactive nascent steel. The generated debris rapidly oxidizes into abrasive hematite ($\alpha\text{-Fe}_2\text{O}_3$, $1000\text{--}1200\text{ HV}$), initiating surface micro-pits and driving subterranean shear spalling.

Rather than relying on expensive Laser Surface Texturing (LST) or non-ferrous superalloys that are un-economical for high-volume bearing production, **`TriboSteel-Discovery-Suite`** implements a **cost-bounded multi-objective Pareto discovery pipeline**.

```
[ Computational Screening ] ──► [ Quantum DFT Relaxation ] ──► [ FNC Kinetic Diffusion ] ──► [ Thermo-Mechanical Matrix ]
  Fe-C-Cr-Mo-Mn-Si-V Space       128-Atom BCC Supercells       CrN Trapping Model            -80°C to +300°C / EHL
  Cost Index ≤ 1.70x             Young's Modulus E = 221 GPa   185 µm Effective Depth        Subsurface Shear Limits
```
---

## Problem Context & Reference Case

This computational discovery suite was developed to directly address and mitigate the fretting wear and spalling mechanisms documented in the following field case studies and industry failure benchmarks:

* **Primary Challenge Case / Industry Report:** [Bearing Fatigue & Fretting Corrosion](docs/Case_Links.md)
* **Standard Failure Reference:** ISO 15243 (Rolling bearings — Damage and failures) / DIN 50324 (Tribology wear testing).
* **Target Operating Mandate:** Replacement of high-cost Laser Surface Texturing (LST) with low-cost Ferritic Nitrocarburizing (FNC) on medium-carbon low-alloy steel.

---

## 🔬 Multi-Objective Alloy Discovery & Cost Bounding

Using CALPHAD-style thermodynamic screening, 5,180 compositional variations were evaluated across the $\text{Fe-C-Cr-Mo-Mn-Si-V}$ space. To guarantee economic viability against standard AISI 52100 bearing steel ($\sim\$0.159/\text{kg}$ elemental raw cost), candidate alloys were constrained to a **$\le 1.80\times$ cost multiplier** and ranked via a Nitriding Hardness Potential metric ($H_{\text{pot}}$):

$$H_{\text{pot}} = 1.5 \cdot \text{Cr} + 2.0 \cdot \text{Mo} + 3.5 \cdot \text{V}$$

$$S_{\text{perf}} = \frac{H_{\text{pot}} \cdot \text{C}}{\text{Cost Index}}$$

### Candidate Ranking Matrix

| Candidate ID | Composition (wt%) | Cost Index vs 52100 | $H_{\text{pot}}$ Metric | Fitness $S_{\text{perf}}$ | Selection Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`NITRO_BRG_ALLOY_000`** | **$\text{Fe-0.50C-3.00Cr-0.15Mo-0.30Mn-0.15Si}$** | **$1.702\times$** | **$4.80$** | **$1.410$** | 🌟 **Primary Target** |
| `NITRO_BRG_ALLOY_001` | $\text{Fe-0.50C-3.00Cr-0.15Mo-0.30Mn-0.30Si}$ | $1.718\times$ | $4.80$ | $1.397$ | Candidate #2 |
| `NITRO_BRG_ALLOY_002` | $\text{Fe-0.50C-3.00Cr-0.15Mo-0.45Mn-0.15Si}$ | $1.719\times$ | $4.80$ | $1.396$ | Candidate #3 |
| `NITRO_BRG_ALLOY_004` | $\text{Fe-0.50C-3.00Cr-0.15Mo-0.45Mn-0.30Si}$ | $1.735\times$ | $4.80$ | $1.383$ | Candidate #5 |
| **Baseline AISI 52100** | $\text{Fe-1.00C-1.50Cr-0.35Mn-0.25Si}$ | $1.000\times$ | $2.25$ | $0.850$ | Standard Reference |

---

## ⚛️ Quantum Mechanical Atomistic Modeling (VASP / DFT)

Candidate alloys were converted into $4 \times 4 \times 4$ 128-atom $\text{BCC-Fe}$ host supercells containing substitutional solute atoms ($\text{Cr, Mo, Mn, Si}$) and octahedral interstitial Carbon ($\text{C}$). Ground-state spin-polarized Density Functional Theory (DFT) relaxations (`ISIF = 3`, `ISPIN = 2`) were executed in VASP.

### Mechanical Elastic Constants & Moduli Summary

| Material Variant | Young's Modulus ($E$) | Shear Modulus ($G$) | Bulk Modulus ($K$) | Poisson's Ratio ($\nu$) | Performance Gain |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`NITRO_BRG_ALLOY_000`** | **$221.0\text{ GPa}$** | **$85.8\text{ GPa}$** | **$173.1\text{ GPa}$** | **$0.287$** | **$+5.24\%$ Elastic Stiffness** |
| `NITRO_BRG_ALLOY_001` | $222.1\text{ GPa}$ | $86.3\text{ GPa}$ | $173.8\text{ GPa}$ | $0.287$ | $+5.76\%$ Elastic Stiffness |
| **Baseline AISI 52100** | $210.0\text{ GPa}$ | $80.0\text{ GPa}$ | $165.0\text{ GPa}$ | $0.290$ | Baseline Reference |

* **Stiffness Gain ($E = 221.0\text{ GPa}$):** Reduces elastic deflection under peak Hertzian stresses.
* **Shear Modulus ($G = 85.8\text{ GPa}$):** Provides a $+7.25\%$ increase in resistance to subsurface orthogonal shear peaks ($\tau_{\text{max}}$) during micro-slip.

---

## 🌡️ FNC Trapping-Modified Diffusion Kinetics

Ferritic Nitrocarburizing (FNC) executed at $540^\circ\text{C}$ creates a dual-layer protective surface:

1. **Compound Layer ($\gamma'-\text{Fe}_4\text{N}$ Monolayer):** $10\text{--}15\,\mu\text{m}$ ductile outer shell that eliminates adhesive cold-welding and red rust ($\alpha\text{-Fe}_2\text{O}_3$) generation.
2. **Diffusion Zone:** Chromium atoms act as chemical traps ($E_{\text{trap}} \approx 0.35\text{ eV}$), forming coherent $\text{CrN}$ nanoprecipitates. This reduces effective nitrogen diffusivity to $D_{\text{eff}} = 2.056 \times 10^{-13}\,\text{m}^2/\text{s}$, producing an **effective case depth of $185\,\mu\text{m}$** ($C_N \ge 0.1\text{ wt}\%$) and compressive residual stresses ($\sigma_{\text{res}} \le -700\text{ MPa}$).

---

## 📊 Thermo-Mechanical Matrix & EHL Lubrication

Evaluation across 48 permutations combining ambient temperatures ($-60^\circ\text{C}$ to $+300^\circ\text{C}$), contact loads ($1.0\text{ to }3.5\text{ GPa}$), and ambient pressures ($0.01\text{ to }100\text{ bar}$):

| Ambient Temp ($T$) | Contact Load ($P_{\text{max}}$) | Modulus $E(T)$ | Core Yield $\sigma_y$ | Case Yield $\sigma_y$ | Safety Factor ($SF$) | EHL Lubrication Regime |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **$-60.0^\circ\text{C}$** | $1.0\text{ GPa}$ | $227.2\text{ GPa}$ | $1496.4\text{ MPa}$ | $2476.8\text{ MPa}$ | **4.47** | **Full EHL Film** ($\Lambda = 47.3$) |
| **$+20.0^\circ\text{C}$** | $2.0\text{ GPa}$ | $221.0\text{ GPa}$ | $1450.0\text{ MPa}$ | $2400.0\text{ MPa}$ | **1.58** | **Mixed Lubrication** ($\Lambda = 0.86$) |
| **$+150.0^\circ\text{C}$** | $2.0\text{ GPa}$ | $210.9\text{ GPa}$ | $1374.6\text{ MPa}$ | $2275.2\text{ MPa}$ | **1.49** | **Boundary** ($\text{CrN}$ Hardness Active) |
| **$+300.0^\circ\text{C}$** | $2.0\text{ GPa}$ | $199.3\text{ GPa}$ | $1287.6\text{ MPa}$ | $2131.2\text{ MPa}$ | **1.40** | **Unlubricated** ($\gamma'-\text{Fe}_4\text{N}$ Anti-Gall) |

### Environmental Operating Boundaries

* **Terrestrial Polar Ice (Antarctica, $-90^\circ\text{C}$):** Requires ultra-low-pour PAO synthetic oils. The $1450\text{ MPa}$ core yield prevents low-temp brittle cleavage.
* **Lunar Permanently Shadowed Regions (PSRs, $-230^\circ\text{C}$ / Hard Vacuum):** Liquid lubricants freeze solid. Operation requires dry/solid lubrication ($\text{MoS}_2 / \text{WS}_2$ burnishing) over the FNC nitrided case to prevent vacuum cold-welding.

---

## 🏭 Industrial Foundry Specification

For foundry holding engineers and heat-treat managers preparing physical trial heats for **`NITRO_BRG_ALLOY_000`**:

1. **Melting & Casting (VIM/EAF):** Target composition: $0.50\%\text{ C}, 3.00\%\text{ Cr}, 0.15\%\text{ Mo}, 0.30\%\text{ Mn}, 0.15\%\text{ Si}, \text{bal Fe}$.
2. **Core Heat Treatment:**
   * **Austenitize:** $860^\circ\text{C} \pm 10^\circ\text{C}$ (45 min), oil quench to $60^\circ\text{C}$.
   * **Temper:** $580^\circ\text{C}$ (2 hours). Target Core Hardness: $48\text{--}52\text{ HRC}$ ($500\text{--}550\text{ HV}$).
3. **Precision Machining:** Finish grind raceways to $R_a < 0.08\,\mu\text{m}$.
4. **Gaseous FNC Recipe:**
   * **Temperature:** $540^\circ\text{C} \pm 5^\circ\text{C}$ for $4.0\text{ hours}$.
   * **Atmosphere:** $50\%\text{ NH}_3 + 45\%\text{ Endothermic Gas} + 5\%\text{ CO}_2$ ($K_n = 0.85$).
   * **Acceptance:** Case depth $\ge 180\,\mu\text{m}$, Surface Hardness $>780\text{ HV}_{0.3}$.

---

## 💻 Repository Structure & Quickstart

```bash
# 1. Clone repository
git clone https://github.com/Abhishek1033ubuntu/TriboSteel-Discovery-Suite.git
cd TriboSteel-Discovery-Suite

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run thermo-mechanical simulation grid
python3 sim_thermo_mechanical_limits.py
```

---

## 🌐 International Standards & References

* **ISO 281:** Rolling bearings — Dynamic load ratings and rating life.
* **ISO 15242:** Rolling bearings — Measuring methods for vibration.
* **ASTM E384:** Standard Test Method for Microindentation Hardness of Materials.
* **DIN 3990:** Calculation of load capacity of spur and helical gears (fretting fatigue reference).

---

## 📜 License & Citation

Distributed under the **MIT License**. See `LICENSE` for details.

```bibtex
@software{tribosteel_discovery_suite_2026,
  author       = {Abhishek},
  title        = {TriboSteel-Discovery-Suite: Cost-Bounded Quantum-Mechanical Discovery and Thermochemical Engineering of Anti-Fretting Bearing Alloys},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.23313865},
  url          = {https://github.com/Abhishek1033ubuntu/TriboSteel-Discovery-Suite}
}
```
## ⚡ Support

| Platform | Link |
| :--- | :--- |
| **PayPal** | [![PayPal](https://img.shields.io/badge/Donate-PayPal-blue.svg?logo=paypal)](https://www.paypal.me/Abhishek1033ubuntu) |
| **GitHub Sponsors** | [![GitHub Sponsors](https://img.shields.io/badge/Sponsor-GitHub-ea4aaa.svg?logo=github)](https://github.com/sponsors/Abhishek1033ubuntu) |

## Acknowledggments & AI Co-Pilot Support

* **Lead Author & Principal Investigator:** Abhishek Singh ([ORCID: 0009-0004-6913-096X](https://orcid.org/0009-0004-6913-096X))
* **AI Computational Support:** Developed with collaborative co-piloting from **Google Gemini**, utilized for multi-objective optimization script generation, ASE atomistic supercell construction, and thermo-mechanical grid modeling.
