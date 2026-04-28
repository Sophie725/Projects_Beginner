import pandas as pd

file_name = '20250226_test_perturb1.txt'

# 1. Skip only 17 lines now to catch the headers on Line 18
df = pd.read_csv(file_name, skiprows=17, sep=None, engine='python', encoding='cp1252')

# 2. Delete the very first row of data (which is just the units: 's', 'N', 'N')
df = df.drop(0)

# 3. Clean up the column names
df.columns = df.columns.str.strip()

# 4. Save it as a fresh CSV
df.to_csv('output.csv', index=False)

print("Fixed! 'output.csv' now has the correct names: abs time (s), Fx, Fy, Fz.")