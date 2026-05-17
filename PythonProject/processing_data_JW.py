import pandas as pd
import numpy as np
from scipy.signal import resample
import matplotlib.pyplot as plt

def load_target_fz(filename):
    # Use latin1 to avoid the UnicodeDecodeError
    df = pd.read_csv(filename, sep='\t', skiprows=17, encoding='latin1')
    df = df.drop(0).reset_index(drop=True)
    # Target the 13th column for Fz as identified in image_cbd817.jpg
    fz_col = pd.to_numeric(df.iloc[:, 15], errors='coerce').fillna(0).values
    return fz_col


def find_best_denoising(d, noise, L_range, L_step,
                        tau_step,
                        s_range, s_step):

    D, N = len(d), len(noise)
    d_sq_cumsum = np.concatenate([[0], np.cumsum(d ** 2)])
    d_total_sq = d_sq_cumsum[-1]

    best = {'score': np.inf, 'L': None, 'tau': None, 's': None, 'w': None,
    'alpha': None}
    L_min, L_max = L_range
    s_min, s_max = s_range

    for L in range(L_min, min(L_max, N)+1, L_step):
        for tau in range(0, N-L+1, tau_step):
            n_segment = noise[tau: tau + L]

            for s in range(max(s_min, 1), min(s_max, D)+1, s_step):
                noise_resized = resample(n_segment, s)

                n_sq = np.dot(noise_resized, noise_resized)
                if n_sq < 1e-10:
                    continue

                dot_prod = np.correlate(d, noise_resized, mode='valid')
                alphas = dot_prod / n_sq

                w_starts = np.arange(D-s+1)
                window_energe = d_sq_cumsum[w_starts + s] - d_sq_cumsum[w_starts]
                residual_window_energy = window_energe - (alphas ** 2) * n_sq

                outside_energy = d_total_sq - window_energe
                scores = outside_energy + residual_window_energy

                best_w_idx = np.argmin(scores)
                if scores[best_w_idx] < best['score']:
                    best = {
                        'score': scores[best_w_idx],
                        'L': L,
                        'tau': tau,
                        's': s,
                        'w': int(w_starts[best_w_idx]),
                        'alpha': float(alphas[best_w_idx])
                    }
    return best

d_full = load_target_fz('20250828_GG_T001_GRF.txt')
noise = load_target_fz('20250226_test_perturb1.txt')

noise = noise[10190:10500]
ratio = 3
start_idx, end_idx = 755 * ratio, 838 * ratio
d = d_full[start_idx : end_idx]
start_idx, end_idx = 842*ratio, 930*ratio
validate_d = d_full[start_idx : end_idx]

best = find_best_denoising(d, noise, L_range=(1, len(noise)), L_step=1,
    tau_step=1, s_range=(1, len(d)), s_step=1)

print(best)

n_seg = noise[best['tau']: best['tau'] + best['L']]
final_noise = resample(n_seg, best['s'])
cleaned = d.copy().astype(float)
cleaned[best['w']: best['w'] + best['s']] -= best['alpha'] * final_noise

##Visualization
plt.figure(figsize = (12, 6))

plt.plot(d, label = 'Original Data (with Noise)', color = 'red', alpha = 0.5)
plt.plot(cleaned, label = 'Cleaned Signal (Noise Removed)', color = 'blue', linewidth = 2)
plt.plot(validate_d, label = '2nd step', color = 'green', alpha = 0.5)
plt.plot(noise, label='Noise', color = 'orange', alpha = 0.5)
plt.title(f"Final Result: L = {best['L']}, tau = {best['tau']}, alpha = {best['alpha']}")
plt.legend()
plt.grid(True)
plt.show()