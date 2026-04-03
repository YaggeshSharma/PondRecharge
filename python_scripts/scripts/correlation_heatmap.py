# Correlation heatmap for recharge determining factors
# Author: Yaggesh Sharma

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# File path
file_path = r'R:\Phd_KHU\Research_work\IWMI\Moradabad_zone\pond_data_final.csv'

# Load dataset
data = pd.read_csv(file_path)

# Selected parameters (consistent with KDE)
parameters = [
    'Soil Moisture',
    'Permeability',
    'Rainfall',
    'GWL',                     # Groundwater Level
    'Soil Organic Matter',
    'Temperature',             # Land Surface Temperature
    'Turbidity',
    'TWI',
    'NDVI',
    'CN'                       # Curve Number
]

# Check columns
print(data.columns.tolist())

# Filter dataset
correlation_data = data[parameters]

# Compute correlation matrix
correlation_matrix = correlation_data.corr()

# Plot heatmap
plt.figure(figsize=(10, 8), dpi=300)

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap=sns.diverging_palette(220, 10, as_cmap=True),
    fmt=".2f",
    square=True,
    linewidths=0.5,
    linecolor='white',
    cbar=True
)

plt.tight_layout()
plt.show()
