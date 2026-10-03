import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import shapely
import numpy as np

# 1. Load the GRACE / GRACE-FO Mascon NetCDF dataset
nc_file = "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
ds = xr.open_dataset(nc_file, decode_times=False)

# Normalize CF units convention for time decoding
if "Units" in ds["time"].attrs and "units" not in ds["time"].attrs:
    ds["time"].attrs["units"] = ds["time"].attrs["Units"]
ds = xr.decode_cf(ds)

# 2. Slice the spatial bounding box for Bangladesh
# Coordinates: Lat 20.4°N - 26.8°N, Lon 88.0°E - 92.8°E
bd_sub = ds["lwe_thickness"].sel(lat=slice(20.4, 26.8), lon=slice(88.0, 92.8))

# 3. Exact country boundary polygon masking
# Download/load high-resolution (10m) country borders
shp = shpreader.natural_earth("10m", "cultural", "admin_0_countries")
bd_geom = [
    r.geometry
    for r in shpreader.Reader(shp).records()
    if r.attributes.get("NAME") == "Bangladesh" or r.attributes.get("ADMIN") == "Bangladesh"
][0]

# Generate 2D coordinates meshgrid & test containment with shapely
lon2d, lat2d = np.meshgrid(bd_sub.lon.values, bd_sub.lat.values)
mask = shapely.contains_xy(bd_geom, lon2d, lat2d)

# Mask out areas outside Bangladesh (replaces them with NaN)
bd_masked = bd_sub.where(mask)

# 4. Select time step (latest available or change to 0 for 2002)
time_idx = -1
data_timestep = bd_masked.isel(time=time_idx)
date_str = str(data_timestep.time.dt.strftime("%B %Y").values)

# 5. Plot Bangladesh
fig = plt.figure(figsize=(9, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# Set geographic boundaries to frame Bangladesh neatly
ax.set_extent([87.8, 93.0, 20.4, 26.8], crs=ccrs.PlateCarree())

# Add administrative boundaries and coastline
ax.add_geometries([bd_geom], ccrs.PlateCarree(), facecolor="none", edgecolor="black", linewidth=1.5)
ax.coastlines(resolution="10m", color="black", linewidth=1.0)
ax.add_feature(cfeature.RIVERS, edgecolor="dodgerblue", linewidth=0.7, alpha=0.7)

# Gridlines with degrees
gl = ax.gridlines(draw_labels=True, dms=False, x_inline=False, y_inline=False, alpha=0.3)
gl.top_labels = False
gl.right_labels = False

# Plot mascon cells
mesh = data_timestep.plot.pcolormesh(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="RdBu",
    vmin=-25,
    vmax=25,
    cbar_kwargs={
        "label": "Liquid Water Equivalent Anomaly (cm)",
        "orientation": "vertical",
        "pad": 0.04,
        "shrink": 0.85,
        "extend": "both"
    }
)

plt.title(
    f"GRACE Mascon — Bangladesh Only\n({date_str})",
    fontsize=14,
    fontweight="bold",
    pad=15
)

# 6. Save image and display
output_image = "bangladesh_plot.png"
plt.savefig(output_image, dpi=200, bbox_inches="tight")
print(f"Bangladesh plot successfully saved to {output_image}")
plt.show()
