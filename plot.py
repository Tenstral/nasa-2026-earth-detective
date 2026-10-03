import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 1. Open the GRACE / GRACE-FO Mascon NetCDF dataset
nc_file = "CSR_GRACE_GRACE-FO_RL0603_Mascons_all-corrections.nc"
ds = xr.open_dataset(nc_file, decode_times=False)

# Normalize 'Units' attribute so CF conventions decode dates accurately
if "Units" in ds["time"].attrs and "units" not in ds["time"].attrs:
    ds["time"].attrs["units"] = ds["time"].attrs["Units"]
ds = xr.decode_cf(ds)

# 2. Select variable and time slice (use latest available time step)
# 'lwe_thickness' represents Liquid Water Equivalent Thickness anomaly in cm
time_idx = -1  # Latest timestep (or change to 0 for initial 2002 step)
data = ds["lwe_thickness"].isel(time=time_idx)
date_str = str(data.time.dt.strftime("%B %Y").values)

# 3. Create figure with Robinson projection
fig = plt.figure(figsize=(12, 7))
ax = plt.axes(projection=ccrs.Robinson())

# 4. Add map features: coastlines, national borders, and gridlines
ax.coastlines(resolution="110m", color="black", linewidth=0.8)
ax.add_feature(cfeature.BORDERS, linestyle=":", edgecolor="gray", alpha=0.6)
ax.gridlines(draw_labels=True, alpha=0.3)

# 5. Plot the mascon grid data (diverging colormap centered at 0 anomaly)
data.plot.pcolormesh(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="RdBu",
    vmin=-30,
    vmax=30,
    cbar_kwargs={
        "label": "Liquid Water Equivalent Thickness (cm)",
        "orientation": "horizontal",
        "pad": 0.08,
        "shrink": 0.8,
        "extend": "both"
    }
)

plt.title(
    f"NASA GRACE / GRACE-FO Liquid Water Equivalent Anomaly ({date_str})",
    fontsize=13,
    fontweight="bold",
    pad=15
)

# 6. Save image and display
output_image = "grace_water_equivalent_plot.png"
plt.savefig(output_image, dpi=200, bbox_inches="tight")
print(f"Plot saved successfully to {output_image}")
plt.show()
