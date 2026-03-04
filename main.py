import pydicom
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

# === CONFIGURATION ===
# Ensure this matches your desktop path exactly!
FILE_PATH = r"C:\Users\USER\OneDrive\Desktop\Physics_project\test.dcm"

def run_sph411_project():
    print("--- SPH 411: STARTING ANALYSIS ---")
    
    # CHECKPOINT 1: Does the file exist?
    if not os.path.exists(FILE_PATH):
        print(f"ERROR: File not found at {FILE_PATH}")
        print("Switching to MANUAL DATA MODE for Thesis Graph...")
        kvp, ma, measured_noise = 120, 10, 31.68
    else:
        # CHECKPOINT 2: Can we read the DICOM?
        try:
            ds = pydicom.dcmread(FILE_PATH)
            kvp = getattr(ds, 'KVP', 120)
            ma = getattr(ds, 'XRayTubeCurrent', 10)
            
            # ROI Math: Middle 30x30 pixels
            img = ds.pixel_array
            y, x = img.shape
            roi = img[y//2-15:y//2+15, x//2-15:x//2+15]
            measured_noise = np.std(roi)
            print(f"SUCCESS: Read {kvp}kVp and {ma}mAs from DICOM.")
        except Exception as e:
            print(f"DICOM Error: {e}")
            kvp, ma, measured_noise = 120, 10, 31.68 # Fallback to your terminal result

    # --- PHASE 2: MATH & SIMULATION ---
    # Generating the 1/sqrt(Dose) Curve
    mas_range = np.array([10, 50, 100, 150, 200, 250])
    # Physics Law: Noise is inversely proportional to sqrt(mAs)
    noise_curve = measured_noise * np.sqrt(ma / mas_range)

    # --- PHASE 3: VISUALIZATION ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    # Graph 1: The Dose-Noise Curve
    ax1.plot(mas_range, noise_curve, 'r-o', label='Theoretical Noise Floor')
    ax1.scatter(ma, measured_noise, color='blue', s=200, label='Your Measured Point', zorder=5)
    ax1.axhline(y=15, color='green', linestyle='--', label='Clinical Limit (<15 HU)')
    ax1.set_title(f"Radiation Dose vs. Image Noise ({kvp} kVp Protocol)")
    ax1.set_xlabel("Tube Current (mAs)")
    ax1.set_ylabel("Measured Noise (SD in HU)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Table 2: The Results Matrix
    table_data = []
    for m, n in zip(mas_range, noise_curve):
        status = "ACCEPTABLE" if n < 15 else "TOO NOISY"
        table_data.append([m, round(n, 2), status])
    
    columns = ["Current (mAs)", "Noise (HU)", "Clinical Quality"]
    ax2.axis('tight')
    ax2.axis('off')
    ax2.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center')
    
    print("--- ANALYSIS COMPLETE: Generating Figure 4.1 ---")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_sph411_project()


