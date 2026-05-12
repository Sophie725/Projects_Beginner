# Setting
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import resample

#set_up
##1. Load the Noise Template
def load_target_fz(filename):
    # Use latin1 to avoid the UnicodeDecodeError
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    df = df.drop(0).reset_index(drop=True)
    # Target the 13th column for Fz as identified in image_cbd817.jpg
    fz_col = pd.to_numeric(df.iloc[:, 13], errors='coerce').fillna(0).values
    return fz_col


"""d: the whole data with noise, noise: the only datasets only made up of noise"""
d_full = load_target_fz('20250828_GG_T001_GRF.txt')
noise = load_target_fz('20250226_test_perturb1.txt')

##2. Hardware Alignment - Resample noise reference (1000Hz -> 1200Hz) to fix Sampling Mismatch
num_samples_new = int(len(noise) * (1200 / 1000))
noise_resampled = resample(noise, num_samples_new)

##3. Target slicing
start_idx, end_idx = 755 * 3, 838 * 3
d = d_full[start_idx : end_idx]
"""
# For debugging
print(f"Length of d: {len(d)}")
print(f"Length of noise: {len(noise)}")
"""

# Optimization using loops
##Resampling using L
def resample_noise_to_length(noise_template, L):
    """
    Adjust the noise template to a specific length L.
    This handles the horizontal stretching/shrinking.
    This uses the scipy.signal.resample
    """
    return resample(noise_template, L)

##Scoring
def calculate_score(d_segment, noise_L, alpha):
    residual = d_segment - (alpha * noise_L)
    return np.sum(np.abs(residual))

test_score = calculate_score(d[0:100], noise_aligned[0:100], 1.0)
print(f"Manual Test Score: {test_score}")
###(1) Loop 1(L): Adjusts for small variations in how long the noise lasted physically

###2. Loop 2(τ): Adjusts for when it started
###3. Loop 3(α): Adjusts for how strong it was