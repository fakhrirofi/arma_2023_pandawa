# ARMA Student Design Competition 2023 - Pandawa Team

This repository contains the **FLAC2D (version 9.00)** scripts and modeling approach used by the **Pandawa Team** in the **2023 American Rock Mechanics Association (ARMA) Student Design Competition**.

## 🏆 Achievement
We are proud to announce that our team secured **2nd Place** in the 2023 ARMA Student Design Competition! 

🔗 **[View Award Announcement on LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7176290637376307201/)**

---

## 👥 Team: Pandawa Team
*   **Jimmi Ramadhani**
*   **Muhammad Fariz**
*   **Jeffry Candra Suranta Sembiring**
*   **Fakri Catur Rofi**
*   **Samantha Michelle Frampton**

**University:** Mining Engineering, UPN "Veteran" Yogyakarta, Indonesia.

---

## 📖 Project Overview
The competition challenge required teams to evaluate the stability of a **Cemented Paste Backfill (CPB)** stope exposed during **Vertical Retreat Mining (VRM)**. The analysis focused on maintaining stability while minimizing backfill costs through optimized material selection.

### Problem Statement Highlights
- **Geomaterials**: Cemented paste backfill and surrounding rock modeled as Mohr-Coulomb materials.
- **Geometry**: 3D stope (72m height, 27m length, 15m width) analyzed via a 2D longitudinal section.
- **Excavation**: 12 vertical cuts, each 6 meters high.
- **Stability Criterion**: A minimum Factor of Safety (FS) of **1.25** for the backfill when fully exposed.

---

## 🛠️ Technical Implementation
The core of our solution is the `backpillar_latest.py` script, which automates the stability analysis and optimization process in FLAC2D 9.00.

### Key Features
- **Automated Optimization**: A custom Python algorithm that iterates through backfill thicknesses and cement contents to find the most cost-effective stable configuration.
- **Multi-Layer Support**: Supports various cement contents (2%, 4%, 6%, 8%, 10%, and 12%) with corresponding cohesive strengths derived from 28-day cure lab tests.
- **Sequential Excavation**: Simulates 12 stages of vertical cuts (VRM) with automated model restoration and solving.
- **Safety Monitoring**: Real-time evaluation of the Factor of Safety (FS) and displacement history at each excavation step.
- **Data Visualization**: Automatically exports plots for x-displacement, displacement vectors, and failure states for every cut.

---

## 🚀 Getting Started

### Prerequisites
- **ITASCA FLAC2D version 9.00**
- **Python 3.x** environment integrated with FLAC2D.
- **Python Libraries**: `itasca`, `pandas`.

### Usage
1. Open FLAC2D 9.00.
2. Load the project workspace.
3. Configure the `result_dir` in `backpillar_latest.py` to your desired output path:
   ```python
   result_dir = "C:/Path/To/Your/Project/experiment.csv"
   ```
4. Run the script using the FLAC2D Python interpreter.

---

## 📂 Repository Structure
- `ARMA Student Competition Problem Statement 2023 FINAL.pdf`: Official competition guidelines.
- `Template new/backpillar_latest.py`: The main optimization and simulation script.
- `/plot`: Directory containing generated visualization plots (if applicable).
- `Sketch.dat`: FLAC2D geometry data.

