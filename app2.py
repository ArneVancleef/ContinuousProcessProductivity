import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Sidebar inputs
st.sidebar.title("Process Parameters")

product_concentration_g_per_L = st.sidebar.slider("Concentration (g/L)", 1, 500, 100)
cycle_dosing_time_h = st.sidebar.slider("Cycle Time (h)", 0.0, 24.0, 5.0, step=0.01)
use_log_scale = st.sidebar.checkbox("Logarithmic Y-Axis", value=True)

# Time range selection with log slider
log_min, log_max = st.sidebar.slider(
    "Time Range (log scale, base 10, in seconds)",
    min_value=-3.0, max_value=5.0,
    value=(-2.0, 4.56),  # From 1 ms to ~10 hours
    step=0.01
)

# Compute time range in seconds (logspace)
time_seconds = np.logspace(log_min, log_max, 800)[::-1]  # Higher resolution + inverted
residence_times_h = time_seconds / 3600

# Calculate productivity
product_concentration_kg_per_L = product_concentration_g_per_L / 1000
plug_flow = product_concentration_kg_per_L / residence_times_h * 24 * 365
batch_residence_times_h = (time_seconds + (cycle_dosing_time_h * 3600)) / 3600
batch_flow = product_concentration_kg_per_L / batch_residence_times_h * 24 * 365

# Plot
fig, ax = plt.subplots(figsize=(12, 6), dpi=600)

ax.plot(time_seconds, plug_flow, label="Continuous Plug Flow", color="tab:blue")
ax.plot(time_seconds, batch_flow, label="Batch (Cycle + Dosing)", color="tab:orange")

ax.set_xscale("log")
if use_log_scale:
    ax.set_yscale("log")
else:
    ax.set_yscale("linear")

# Custom ticks
custom_times = [
    10 * 3600, 5 * 3600, 2 * 3600, 3600, 1800, 1200, 600, 300,
    120, 60, 30, 10, 5, 2, 1, 0.1, 0.01
]
custom_labels = [
    "10 h", "5 h", "2 h", "1 h", "30 min", "20 min", "10 min", "5 min",
    "2 min", "1 min", "30 s", "10 s", "5 s", "2 s", "1 s", "100 ms", "10 ms"
]
ax.set_xticks(custom_times)
ax.set_xticklabels(custom_labels, rotation=45, ha="right")

ax.invert_xaxis()
ax.set_xlabel("Chemical Reaction Time")
ax.set_ylabel("Industrial Productivity (t/y/m³)")
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

ax.grid(True, which="both", linestyle="--", linewidth=0.5)
st.pyplot(fig)
