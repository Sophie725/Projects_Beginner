"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample
from scipy.interpolate import interp1d

# --- 1. DATA INGESTION & TYPE CONVERSION ---
def load_and_clean_bioware(filename):
    # Load with latin1 to handle the micro symbol (0xb5) and skip headers
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    # Remove the unit row (index 0)
    df = df.drop(0).reset_index(drop=True)
    # Convert Fz to numeric; text becomes NaN then 0 to avoid 'float and str' errors
    df['Fz'] = pd.to_numeric(df['Fz'], errors='coerce').fillna(0)
    return df

# Load both files
df_noisy = load_and_clean_bioware('20250828_GG_T001_GRF.txt') # data_file_2
df_noise_ref = load_and_clean_bioware('20250226_test_perturb1.txt')     # data_file_1

# --- 2. SOLVING THE MISMATCHES ---

# A. Sampling Rate Mismatch (Problem 1)
# File 2 is 1200Hz, File 1 is 1000Hz. We resample File 1 to 1200Hz.
fs_target = 1200
fs_source = 1000
num_samples_new = int(len(df_noise_ref) * (fs_target / fs_source))
noise_resampled = resample(df_noise_ref['Fz'].values, num_samples_new)

# B. Segmentation (Problem 3: t1, t2)
# Using your mentor's specific step indices for the target signal
start_idx, end_idx = 755*3, 838*3 
target_signal = df_noisy['Fz'].iloc[start_idx:end_idx].values

# Extract a segment of noise of the same length from the resampled noise reference
noise_segment = noise_resampled[:len(target_signal)]

# C. Amplitude Scaling (Problem 2: Alpha Optimization)
# We find alpha by comparing the standard deviation (energy) of the noise floors
# Use the first 200 samples of the noisy file as the target noise floor reference
noise_floor_target = df_noisy['Fz'].head(200).values
alpha = np.std(noise_floor_target) / np.std(noise_segment)

# --- 3. THE CLEANING OPERATION ---
# Formula: clean = noisy - (alpha * noise)
adjusted_noise = alpha * noise_segment
cleaned_signal = target_signal - adjusted_noise

# --- 4. VISUALIZATION (THE 3-STEP PROOF) ---
fig, ax = plt.subplots(3, 1, figsize=(12, 15))

# Plot 1: Contaminated Data
ax[0].plot(target_signal, color='red', label='Noisy Fz (File 2)')
ax[0].set_title("Step 1: Segmented Noisy Data (Signal + Noise)")
ax[0].set_ylabel("Force (N)")
ax[0].legend()

# Plot 2: Adjusted Noise Reference
ax[1].plot(adjusted_noise, color='gray', linestyle='--', label='Adjusted Noise (File 1)')
ax[1].set_title(f"Step 2: Noise Reference (Resampled to {fs_target}Hz, alpha={alpha:.4f})")
ax[1].set_ylabel("Force (N)")
ax[1].legend()

# Plot 3: Cleaned Data
ax[2].plot(cleaned_signal, color='blue', label='Cleaned Fz')
ax[2].set_title("Step 3: Final Signal (Noise Removed via Subtraction)")
ax[2].set_xlabel("Samples")
ax[2].set_ylabel("Force (N)")
ax[2].legend()

plt.tight_layout()
plt.show()

print(f"Optimization Complete. Applied Alpha: {alpha:.4f}")

"""
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample, wiener
from scipy.fft import fft, ifft

# --- 1. DATA INGESTION & CLEANING ---
def load_and_clean(filename):
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    df = df.drop(0).reset_index(drop=True)
    df['Fz'] = pd.to_numeric(df['Fz'], errors='coerce').fillna(0)
    return df

df_noisy = load_and_clean('20250828_GG_T001_GRF.txt')
df_noise_ref = load_and_clean('20250226_test_perturb1.txt')

# Prepare signals (Resample 1000Hz -> 1200Hz)
num_samples_new = int(len(df_noise_ref) * (1200 / 1000))
noise_ref_long = resample(df_noise_ref['Fz'].values, num_samples_new)

# Target footstep segment
start_idx, end_idx = 755*3, 838*3
d = df_noisy['Fz'].iloc[start_idx:end_idx].values # Desired (noisy) signal
x = noise_ref_long[:len(d)]                       # Reference (noise) signal

# --- 2. LMS ALGORITHM (ADAPTIVE NOISE CANCELLATION) ---
def lms_filter(x, d, mu=0.01, order=4):
    n = len(d)
    w = np.zeros(order)
    y = np.zeros(n)
    e = np.zeros(n)
    for i in range(order, n):
        x_window = x[i:i-order:-1]
        y[i] = np.dot(w, x_window)
        e[i] = d[i] - y[i]
        w = w + 2 * mu * e[i] * x_window
    return e # The error signal is the cleaned signal

clean_lms = lms_filter(x, d, mu=0.001)

# --- 3. WIENER FILTER (STATISTICAL OPTIMIZATION) ---
# Scipy's wiener filter performs a local variance-based estimate
clean_wiener = wiener(d, mysize=7)

# --- 4. SPECTRAL SUBTRACTION (FREQUENCY DOMAIN) ---
def spectral_subtraction(noisy_signal, noise_ref):
    D = fft(noisy_signal)
    N = fft(noise_ref)
    
    # Calculate magnitudes
    mag_D = np.abs(D)
    mag_N = np.abs(N)
    
    # Subtract noise magnitude from noisy magnitude (ensure no negative values)
    mag_clean = np.maximum(mag_D - mag_N, 0.1 * mag_D)
    
    # Reconstruct signal using original phase
    phase_D = np.angle(D)
    clean_fft = mag_clean * np.exp(1j * phase_D)
    return np.real(ifft(clean_fft))

clean_spectral = spectral_subtraction(d, x)

# --- 5. COMPARATIVE VISUALIZATION ---
plt.figure(figsize=(14, 10))

plt.subplot(4, 1, 1)
plt.plot(d, color='red', alpha=0.5, label='Original Noisy')
plt.title("Step 1: Contaminated Data")
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(clean_lms, color='blue', label='LMS Adaptive Filter')
plt.title("Step 2: LMS Result (Adaptive Sample-by-Sample)")
plt.legend()

plt.subplot(4, 1, 3)
plt.plot(clean_wiener, color='green', label='Wiener Filter')
plt.title("Step 3: Wiener Result (Statistical Smoothing)")
plt.legend()

plt.subplot(4, 1, 4)
plt.plot(clean_spectral, color='purple', label='Spectral Subtraction')
plt.title("Step 4: Spectral Subtraction Result (Frequency Domain)")
plt.xlabel("Samples")
plt.legend()

plt.tight_layout()
plt.show()

"""
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample

# --- 1. TARGETED DATA LOADING (Column 13 for Fz) ---
def load_target_fz(filename):
    # Using latin1 to handle the BioWare symbols
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    df = df.drop(0).reset_index(drop=True)
    
    # Target the 13th column (index 13) for Fz as seen in your code
    fz_col = pd.to_numeric(df.iloc[:, 13], errors='coerce').fillna(0).values
    return fz_col

# Load your specific files
noisy_fz_full = load_target_fz('20250828_GG_T001_GRF.txt')
noise_ref_raw = load_target_fz('20250226_test_perturb1.txt')

# --- 2. PREPARING THE SEGMENT (The "Second Part") ---
# Resample noise reference from 1000Hz to 1200Hz
num_samples_new = int(len(noise_ref_raw) * (1200 / 1000))
noise_resampled = resample(noise_ref_raw, num_samples_new)

# Mentor's specific footstep window (the second part)
start_idx, end_idx = 755*3, 838*3
d = noisy_fz_full[start_idx:end_idx]      # The noisy footstep (Desired signal)
x = noise_resampled[:len(d)]              # Matching noise reference

# --- 3. ADAPTIVE NOISE CANCELLATION (LMS) ---
def lms_anc(x, d, mu=0.01, order=16):
    n = len(d)
    w = np.zeros(order)
    y = np.zeros(n)
    e = np.zeros(n)
    for i in range(order, n):
        x_window = x[i:i-order:-1]
        y[i] = np.dot(w, x_window)
        e[i] = d[i] - y[i]
        w = w + 2 * mu * e[i] * x_window
    return e # This is the "Clean" signal residue

# Apply the filter
clean_fz = lms_anc(x, d, mu=0.02, order=32)

# --- 4. VISUALIZATION OF THE OPTIMIZED OUTPUT ---
plt.figure(figsize=(12, 6))
plt.plot(d, color='red', alpha=0.4, label='Original Noisy Fz (Column 13)')
plt.plot(clean_fz, color='blue', linewidth=1.5, label='ANC Optimized Fz')

plt.title("Mentor-Ordered Optimization: Fz Noise Removal (Second Part Only)")
plt.xlabel("Samples (at 1200Hz)")
plt.ylabel("Vertical Force (N)")
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()

# Calculate and show the improvement
snr_before = 10 * np.log10(np.var(d) / np.var(d - clean_fz))
print(f"Targeting Column 13...")
print(f"Calculated SNR Improvement: {snr_before:.2f} dB")
"""

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
x = noise_resampled[:len(d)]              # Noise Reference Segment

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