import arcpy
import numpy as np
import pandas as pd

arcpy.env.overwriteOutput = True

raster_paths = {
    "Distance_River": r"C:\Users\user\Downloads\raster.gdb (2)\raster.gdb\Distan_River",
    "Distance_Industry": r"C:\Users\user\Downloads\raster.gdb (2)\raster.gdb\Distance_Industry",
    "Distance_Waste": r"C:\Users\user\Downloads\raster.gdb (2)\raster.gdb\Distance_waste",
    "Distance_Road": r"C:\Users\user\Downloads\raster.gdb (2)\raster.gdb\Distance_Road",
    "LULC": r"C:\Users\user\Downloads\raster.gdb (2)\raster.gdb\Aoi_LULC",
    "Population_Density": r"C:\Users\user\Documents\ArcGIS\Projects\MyProject6\myproject6.gdb\PoPN_Dens"
}


data_arrays = []
raster_names = []


for name, path in raster_paths.items():
    print(f"Reading raster: {name}")
    raster = arcpy.RasterToNumPyArray(path).astype(float)
    raster = raster.flatten()
    raster = raster[~np.isnan(raster)]
    data_arrays.append(raster)
    raster_names.append(name)


min_len = min(len(arr) for arr in data_arrays)
data_dict = {raster_names[i]: data_arrays[i][:min_len] for i in range(len(data_arrays))}
df = pd.DataFrame(data_dict)


df_norm = (df - df.min()) / (df.max() - df.min())

k = 1.0 / np.log(len(df_norm))
P = df_norm.div(df_norm.sum(axis=0), axis=1)
P = P.replace(0, 1e-10)
logP = np.log(P)
E = -k * (P * logP).sum(axis=0)

d = 1 - E
W = d / d.sum()


weights_table = pd.DataFrame({
    "Entropy (E)": E,
    "Diversification (1-E)": d,
    "Weight (W)": W
})
weights_table.index.name = "Criteria"

print(weights_table)