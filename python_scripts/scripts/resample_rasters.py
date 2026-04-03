# Resampling raster layers to match reference raster (TWI)
# Author: Yaggesh Sharma

import os
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Input and output paths
input_folder = r'input folder'
output_folder = r'output folder'

# Create output folder if not exists
os.makedirs(output_folder, exist_ok=True)

# Reference raster (TWI)
ref_raster_path = os.path.join(input_folder, 'TWI.tif')

# Read reference raster properties
with rasterio.open(ref_raster_path) as ref:
    ref_transform = ref.transform
    ref_width = ref.width
    ref_height = ref.height
    ref_crs = ref.crs

def resample_raster(input_path, output_path):
    with rasterio.open(input_path) as src:
        kwargs = src.meta.copy()
        kwargs.update({
            'crs': ref_crs,
            'transform': ref_transform,
            'width': ref_width,
            'height': ref_height
        })

        with rasterio.open(output_path, 'w', **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=ref_transform,
                    dst_crs=ref_crs,
                    resampling=Resampling.bilinear
                )

# Loop through all raster files
for file in os.listdir(input_folder):
    if file.endswith('.tif'):
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)
        print(f"Resampling: {file}")
        resample_raster(in_path, out_path)

print("Resampling completed successfully.")
