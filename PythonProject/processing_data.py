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
noise = noise[10190:10500]

##3. Target slicing
ratio = 3
start_idx, end_idx = 755 * ratio, 838 * ratio
d = d_full[start_idx : end_idx]
start_idx, end_idx = 842*ratio, 930*ratio
validate_d = resample(d_full[start_idx : end_idx], len(d))
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
mag = 3.0

###(1) Loop 1(L): Adjusts for small variations in how long the noise lasted physically
for L in range(len(noise), 0, -L_step):
    ###2. Loop 2(τ): Adjusts for when it started
    for tau in range(0, len(noise) - L + 1, tau_step):
        n_segment = noise[tau: tau + L]
        noise_L = resample_noise_to_length(n_segment, len(d))

        ###3. Loop 3(α): Adjusts for how strong it was
        for alpha in np.arange(-mag, mag, alpha_step):
            if alpha == 0:
                continue

            current_score = calculate_score(d, noise_L, alpha)

            if current_score < best_score:
                best_score = current_score
                best_params = {'L': L, 'tau': tau, 'alpha': alpha}

#Finalization

##Creating the noise using the best L
best_L = best_params['L']
best_tau = best_params['tau']
best_alpha = best_params['alpha']

# final_noise = resample_noise_to_length(noise, best_L)
final_noise = resample_noise_to_length(noise[best_tau: best_tau + best_L], len(d))

##Subtraction the noise from the specific segment of d
###Use the best_tau to find exactly where to subtract it
cleaned_signal = d - (best_alpha * final_noise)

##Visualization
plt.figure(figsize = (12, 6))

plt.plot(d, label = 'Original Data (with Noise)', color = 'red', alpha = 0.5)
plt.plot(noise, label='Noise', color = 'orange', alpha = 0.5)
plt.plot(cleaned_signal, label = 'Cleaned Signal (Noise Removed)', color = 'blue', linewidth = 2)
plt.plot(validate_d, label = '2nd step', color = 'green', alpha = 0.5)

plt.title(f"Final Result: L = {best_L}, tau = {best_tau}, alpha = {best_alpha}")
plt.legend()
plt.grid(True)
plt.show()