import pydicom
import matplotlib.pyplot as plt
import numpy as np

# --- CONFIGURATION ---
# Ensure your image is in the 'Physics_project' folder and named 'test.dcm'
FILE_PATH = r"C:\Users\USER\OneDrive\Desktop\Physics_project\'test.dcm'"
ROI_SIZE = 30  # Size of the square box for noise measurement (30x30 pixels)

def run_physics_analysis():
    try:
        # 1. Load the DICOM file
        ds = pydicom.dcmread(r"C:\Users\USER\OneDrive\Desktop\Physics_project\'test.dcm'")
        image = ds.pixel_array
        
        # 2. Extract Dose-related parameters for the thesis
        kvp = getattr(ds, 'KVP', 'N/A')
        ma = getattr(ds, 'XRayTubeCurrent', 'N/A')
        exposure = getattr(ds, 'Exposure', 'N/A')
        
        # 3. Calculate Noise (Standard Deviation) in the center of the image
        rows, cols = image.shape
        center_y, center_x = rows // 2, cols // 2
        
        # Define the ROI area
        roi = image[center_y-ROI_SIZE:center_y+ROI_SIZE, 
                    center_x-ROI_SIZE:center_x+ROI_SIZE]
        
        mean_hu = np.mean(roi)
        noise_sigma = np.std(roi)
        
        # 4. Print Results to Terminal
        print("-" * 30)
        print("RESEARCH DATA ACQUISITION")
        print("-" * 30)
        print(f"Protocol: {ds.ProtocolName if 'ProtocolName' in ds else 'Abdominal'}")
        print(f"Peak Voltage (kVp): {kvp} kV")
        print(f"Tube Current (mAs): {ma} mA")
        print(f"Mean Signal: {mean_hu:.2f} HU")
        print(f"Image Noise (Sigma): {noise_sigma:.2f} HU")
        print("-" * 30)

        # 5. Professional Visualization
        plt.figure(figsize=(10, 8))
        plt.imshow(image, cmap=plt.cm.bone)
        
        # Draw the ROI box where noise was measured
        rect = plt.Rectangle((center_x-ROI_SIZE, center_y-ROI_SIZE), 
                             ROI_SIZE*2, ROI_SIZE*2, 
                             edgecolor='red', fill=False, linewidth=2, label='Noise ROI')
        plt.gca().add_patch(rect)
        
        plt.title(f"Abdominal CT: {kvp}kV | Noise: {noise_sigma:.2f} HU")
        plt.colorbar(label="Hounsfield Units (HU)")
        plt.legend()
        plt.show()

    except FileNotFoundError:
        print(f"ERROR: Could not find '{FILE_PATH}'. Please ensure it is in your project folder.")
    except Exception as e:
        print(f"AN ERROR OCCURRED: {e}")

if __name__ == "__main__":
    run_physics_analysis()