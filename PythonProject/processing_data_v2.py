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
    fz_col = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0).values
    return fz_col


"""d: the whole data with noise, noise: the only datasets only made up of noise"""
d_full = load_target_fz('20250828_GG_T001_GRF.txt')
noise = load_target_fz('20250226_test_perturb1.txt')

##2. Hardware Alignment - Resample noise reference (1000Hz -> 1200Hz) to fix Sampling Mismatch
# num_samples_new = int(len(noise) * (1200 / 1000))
# noise_aligned = resample(noise, num_samples_new)
noise_aligned = noise[10190:10500]

##3. Target slicing
start_idx, end_idx = 755 * 3, 838 * 3
d = d_full[start_idx : end_idx]

start_idx, end_idx = 842*3, 930*3
validate_d = d_full[start_idx : end_idx]
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
    return np.sum(residual ** 2)

"""
# For checking how the Manual Test Score works
test_score = calculate_score(d[0:100], noise_aligned[0:100], 1.0)
print(f"Manual Test Score: {test_score}")
"""

##Searching Loops
best_score = float("inf")
best_params = {"L": 0, "tau": 0, "alpha": 0}

L_step = 1
tau_step = 1
alpha_step = 0.01

###(1) Loop 1(L): Adjusts for small variations in how long the noise lasted physically
for L in range(len(d), len(d)//2, -L_step):
    noise_L = resample_noise_to_length(noise_aligned, L)

###2. Loop 2(τ): Adjusts for when it started
    for tau in range(0, len(d) - L + 1, tau_step):
        d_segment = d[tau: tau + L]

###3. Loop 3(α): Adjusts for how strong it was
        for alpha in np.arange(-2.0, 2.0, alpha_step):
            current_score = calculate_score(d_segment, noise_L, alpha)

            if current_score < best_score:
                best_score = current_score
                best_params = {'L': L, 'tau': tau, 'alpha': alpha}

#Finalization

##Creating the noise using the best L
best_L = best_params['L']
best_tau = best_params['tau']
best_alpha = best_params['alpha']

final_noise = resample_noise_to_length(noise_aligned, best_L)

##Subtraction the noise from the specific segment of d
###Use the best_tau to find exactly where to subtract it
d_segment = d[best_tau : best_tau + best_L]
cleaned_signal = d_segment - (best_alpha * final_noise)

##Visualization
plt.figure(figsize = (12, 6))

plt.plot(d_segment, label = 'Original Data (with Noise)', color = 'red', alpha = 0.5)
plt.plot(noise_aligned, label = 'Noise', color = 'orange', linestyle = '--')
plt.plot(cleaned_signal, label = 'Cleaned Signal (Noise Removed)', color = 'blue', linewidth = 2)
plt.plot(validate_d, label = '2nd step', color = 'green', linestyle = '--')
plt.title(f"Final Result: L = {best_L}, tau = {best_tau}, alpha = {best_alpha}")
plt.legend()
plt.grid(True)
plt.show()