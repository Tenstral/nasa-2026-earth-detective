from pathlib import Path

def replace_in_file(path_str, old_text, new_text):
    p = Path(path_str)
    if not p.exists():
        print(f"File not found: {path_str}")
        return
    c = p.read_text(encoding="utf-8")
    if old_text not in c:
        print(f"Warning: target text not found in {path_str}:\n{old_text[:60]}...")
        return
    c = c.replace(old_text, new_text)
    p.write_text(c, encoding="utf-8")
    print(f"Updated {path_str}")

# 1. exposure_table.md
replace_in_file(
    "outputs/v3/exposure/exposure_table.md",
    "demonstrating that this exposure is consistent with intensive groundwater abstraction exceeding recharge rather than rainfall deficit.",
    "showing that this exposure is consistent with intensive groundwater abstraction exceeding recharge rather than rainfall deficit."
)

# 2. extremes_synthesis.md
replace_in_file(
    "outputs/v3/extremes/extremes_synthesis.md",
    "demonstrates that seasonal storage rebound alone averages",
    "shows that seasonal storage rebound alone averages"
)
replace_in_file(
    "outputs/v3/extremes/extremes_synthesis.md",
    "confirming that seasonal flooding cannot compensate",
    "indicating that seasonal flooding cannot compensate"
)

# 3. flood_events_context.md
replace_in_file(
    "outputs/v3/extremes/flood_events_context.md",
    "demonstrating that regional extremes can diverge sharply from national seasonal statistics.",
    "showing that regional extremes can diverge sharply from national seasonal statistics."
)

# 4. narrative_EN.md
replace_in_file(
    "outputs/v3/full_record/narrative_EN.md",
    "demonstrates stationary annual rainfall nationally",
    "shows stationary annual rainfall nationally"
)
replace_in_file(
    "outputs/v3/full_record/narrative_EN.md",
    "indicating that terrestrial storage loss in the Bengal Basin is concentrated in the deep subsurface, consistent with unconfined aquifer drawdown from dry-season Boro rice irrigation rather than topsoil desiccation.",
    "most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural extraction from the deep subsurface."
)

# 5. three_way_slopes_and_transition.md
replace_in_file(
    "outputs/v3/full_record/three_way_slopes_and_transition.md",
    "Monte Carlo null simulations demonstrate that a pure step offset",
    "Monte Carlo null simulations show that a pure step offset"
)
replace_in_file(
    "outputs/v3/full_record/three_way_slopes_and_transition.md",
    "scaling demonstrates that the statistical power",
    "scaling shows that the statistical power"
)

# 6. gldas_partition_summary.md
replace_in_file(
    "outputs/v3/gldas_split/gldas_partition_summary.md",
    "Because GLDAS Noah 2.1 simulates topsoil dynamics but omits deep unconfined aquifer abstraction, this partitioning demonstrates that terrestrial storage loss in the Bengal Basin is concentrated overwhelmingly in the deep subsurface, consistent with unconfined aquifer drawdown from dry-season Boro rice irrigation rather than topsoil desiccation.",
    "Because GLDAS Noah 2.1 simulates topsoil dynamics but omits deep unconfined aquifer abstraction, most of the decline is not accounted for by simulated soil moisture; groundwater and surface water cannot be separated here. This pattern is consistent with, not proof of, agricultural extraction from the deep subsurface."
)

# 7. imerg_vs_power_summary.md
replace_in_file(
    "outputs/v3/imerg_vs_power/imerg_vs_power_summary.md",
    "This audit demonstrates that these trends are non-climatic artifacts",
    "This audit shows that these trends are non-climatic artifacts"
)
replace_in_file(
    "outputs/v3/imerg_vs_power/imerg_vs_power_summary.md",
    "cannot be attributed to a declining rainfall influx.",
    "occurs without a corresponding decline in rainfall influx."
)

# 8. epoch_comparison.md
replace_in_file(
    "outputs/v3/full_record/epoch_comparison.md",
    "confirming that water storage depletion is **continuing at a similar rate**",
    "indicating that water storage depletion is **continuing at a similar rate**"
)

# 9. README.md
replace_in_file(
    "README.md",
    "terrestrial water storage depletion concentrated in northern agricultural divisions (Rajshahi and Rangpur).",
    "terrestrial water storage depletion observed in northern agricultural divisions (Rajshahi and Rangpur)."
)
replace_in_file(
    "README.md",
    "confirmed that the rate of storage loss in GRACE-1 vs GRACE-FO is statistically indistinguishable",
    "shows that the rate of storage loss in GRACE-1 vs GRACE-FO is statistically indistinguishable"
)
replace_in_file(
    "README.md",
    "with statistically confirmed long-term water storage loss",
    "with statistically significant long-term water storage loss"
)
replace_in_file(
    "README.md",
    "demonstrating that extreme rainfall events cannot compensate for unconfined aquifer overdraft.",
    "showing that extreme rainfall events cannot compensate for secular subsurface drawdown."
)
print("Finished updates.")
