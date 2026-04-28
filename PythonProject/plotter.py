import pandas as pd
import matplotlib.pyplot as plt

# 1. Load your new CSV file
df = pd.read_csv('output.csv')

# 2. Clean the column names (removes hidden spaces)
df.columns = df.columns.str.strip()

# 3. SAFETY STEP: Drop the first row if it contains units (like 'N' or 's')
# Then convert everything to numbers (floats)
df = df.iloc[1:].apply(pd.to_numeric)

# 4. Select your data
time = df['abs time (s)']
fx = df['Fx.1']
fy = df['Fy.1']
fz = df['Fz.1']

# 5. Create the combined plot
plt.figure(figsize=(12, 6))

plt.plot(time, fx, label='Fx (Medial-Lateral)', color='blue')
plt.plot(time, fy, label='Fy (Anterior-Posterior)', color='green')
plt.plot(time, fz, label='Fz (Vertical)', color='red')

# 6. Formatting for your mentor
plt.title('Gait Perturbation Analysis: Force Plate 1')
plt.xlabel('Time (seconds)')
plt.ylabel('Force (Newtons)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 7. Show the graph
plt.tight_layout()
plt.show()