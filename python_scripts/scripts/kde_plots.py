# KDE plots for recharge determining factors
# Author: Yaggesh Sharma

import seaborn as sns
import matplotlib.pyplot as plt

# Check column names
print(data.columns.tolist())

# Selected variables
columns_to_plot = [
    'Soil Moisture',
    'Permeability',
    'Rainfall',
    'GWL',
    'Soil Organic Matter',
    'Temperature',
    'Turbidity',
    'TWI',
    'NDVI',
    'CN'
]

# Pond presence column (0 = no pond, 1 = pond)
hue_column = 'Ponds'

# Create subplot grid
n_cols = 4
n_rows = 3
fig, axes = plt.subplots(n_rows, n_cols, figsize=(24, 18), dpi=300)
axes = axes.flatten()

plot_index = 0

for column in columns_to_plot:
    if column in data.columns:
        sns.kdeplot(
            data=data,
            x=column,
            hue=hue_column,
            ax=axes[plot_index],
            fill=True,
            palette={0: "blue", 1: "orange"},
            common_norm=False
        )

        axes[plot_index].set_xlabel(column, fontsize=12, fontweight='bold')
        axes[plot_index].set_ylabel("Density", fontsize=12, fontweight='bold')
        axes[plot_index].set_title(column, fontsize=13, fontweight='bold')

        plot_index += 1

# Remove unused plots
for j in range(plot_index, len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()
