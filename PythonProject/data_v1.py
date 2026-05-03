import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# --- 1. DATA INGESTION & TARGET SELECTION ---
# headers are on line 18 (index 17), units on line 19
df = pd.read_csv('20250828_GG_T001_GRF.txt', sep='\t', skiprows=17, encoding='latin1')
df = df.drop(0).reset_index(drop=True) # Remove the unit row

# Post-doc's Guide: Select the FIRST set of Fx, Fy, Fz (Columns 1, 2, 3)
# Using iloc to avoid duplicate column name issues
df_target = df.iloc[:, [0, 1, 2, 3]].copy()
df_target.columns = ['time', 'Fx', 'Fy', 'Fz']
df_target = df_target.apply(pd.to_numeric, errors='coerce')

# --- 2. PIPELINE STEP 1: SEGMENT NOISE & CONTAMINATED DATA ---
# Segment Noise: Extract pure noise from the initial static period (first 200 samples)
noise_segment = df_target['Fz'].head(200).values

# Segment Contaminated Data: Find the first footstep
# We'll use idxmax to find the peak and take a 1.0s window around it
max_idx = df_target['Fz'].idxmax()
# 1200Hz sampling rate means 600 samples = 0.5s
start_idx, end_idx = max(0, max_idx - 600), min(len(df_target), max_idx + 600)

contaminated_signal = df_target['Fz'].iloc[start_idx:end_idx].values
time_axis = df_target['time'].iloc[start_idx:end_idx].values

# --- 3. PIPELINE STEP 2: STRETCH NOISE DATA ---
# Mentors's Instruction: Stretch the noise to match the step length
x_old = np.linspace(0, 1, len(noise_segment))
x_new = np.linspace(0, 1, len(contaminated_signal))
interpolator = interp1d(x_old, noise_segment, kind='linear')
stretched_noise = interpolator(x_new)

# --- 4. PIPELINE STEP 3: REMOVE NOISE ---
# Final Step: Subtract the stretched noise from the contaminated signal
cleaned_signal = contaminated_signal - stretched_noise

# --- 5. VISUALIZATION (THE 3-STEP PROOF) ---
fig, ax = plt.subplots(3, 1, figsize=(12, 15))

# Plot 1: Contaminated Data
ax[0].plot(time_axis, contaminated_signal, color='red', label='Contaminated Fz')
ax[0].set_title("Step 1: Segmented Contaminated Data (First Set of Columns)")
ax[0].set_ylabel("Vertical Force (N)")
ax[0].legend()

# Plot 2: Stretched Noise
ax[1].plot(time_axis, stretched_noise, color='gray', linestyle='--', label='Stretched Noise Profile')
ax[1].set_title("Step 2: Stretched Noise Data (Interpolated to Match Step Length)")
ax[1].set_ylabel("Noise Magnitude (N)")
ax[1].legend()

# Plot 3: Cleaned Data
ax[2].plot(time_axis, cleaned_signal, color='blue', label='Cleaned Fz')
ax[2].set_title("Step 3: Final Cleaned Data (Noise Removed via Subtraction)")
ax[2].set_xlabel("Time (s)")
ax[2].set_ylabel("Vertical Force (N)")
ax[2].legend()

plt.tight_layout()
plt.show()