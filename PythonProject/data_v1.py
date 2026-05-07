import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample

# --- 1. DATA INGESTION (Focusing on Column 13 for Fz) ---
def load_target_fz(filename):
    # Use latin1 to avoid the UnicodeDecodeError
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    df = df.drop(0).reset_index(drop=True)
    # Target the 13th column for Fz as identified in image_cbd817.jpg
    fz_col = pd.to_numeric(df.iloc[:, 13], errors='coerce').fillna(0).values
    return fz_col

# Load the files
noisy_fz_full = load_target_fz('20250828_GG_T001_GRF.txt')
noise_ref_raw = load_target_fz('20250226_test_perturb1.txt')

# --- 2. SEGMENTATION & ALIGNMENT ---
# Resample noise reference (1000Hz -> 1200Hz) to fix Sampling Mismatch
num_samples_new = int(len(noise_ref_raw) * (1200 / 1000))
noise_resampled = resample(noise_ref_raw, num_samples_new)

# Extract only the second part (the footstep)
start_idx, end_idx = 755*3, 838*3
d = noisy_fz_full[start_idx:end_idx]      # Target Noisy Signal
# x = noise_resampled[:len(d)]              # Noise Reference Segment
x = noise_ref_raw[10190:10500]

# --- 3. ADAPTIVE NOISE CANCELLATION (LMS) ---
def lms_anc(x, d, mu=0.02, order=32):
    n = len(d)
    w = np.zeros(order)
    y = np.zeros(n) # The estimated noise
    e = np.zeros(n) # The cleaned signal (error)
    for i in range(order, n):
        x_window = x[i:i-order:-1]
        y[i] = np.dot(w, x_window)
        e[i] = d[i] - y[i]
        # Update weights based on LMS optimization
        w = w + 2 * mu * e[i] * x_window
    return e, y

clean_fz, estimated_noise = lms_anc(x, d)

# --- 4. THE THREE-STEP PROOF VISUALIZATION ---
fig, ax = plt.subplots(3, 1, figsize=(12, 15))

# Graph 1: The Raw Contaminated Data (Column 13)
ax[0].plot(d, color='red', label='Target Noisy Fz (Column 13)')
ax[0].set_title("Step 1: Segmented Noisy Data (Footstep Part Only)")
ax[0].set_ylabel("Force (N)")
ax[0].legend()

# Graph 2: The Optimized Noise Estimate
# This represents what the ANC algorithm identified as the "noise component"
ax[1].plot(estimated_noise, color='gray', linestyle='--', label='LMS Estimated Noise')
ax[1].set_title("Step 2: Adaptive Noise Estimate (Optimized via LMS)")
ax[1].set_ylabel("Noise Magnitude (N)")
ax[1].legend()

# Graph 3: The Final Cleaned Result
ax[2].plot(clean_fz, color='blue', label='Cleaned Fz (ANC Output)')
ax[2].set_title("Step 3: Final Pure Signal (Noise Removed)")
ax[2].set_xlabel("Samples")
ax[2].set_ylabel("Force (N)")
ax[2].legend()

plt.tight_layout()
plt.show()
