import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

st.set_page_config(layout="wide")

# Sidebar inputs
st.sidebar.title("Process Parameters")

product_concentration_g_per_L = st.sidebar.slider("Concentration (g/L)", 1, 500, 100)
cycle_dosing_time_h = st.sidebar.slider("Cycle Time (h)", 0.0, 24.0, 10.0, step=0.1)
use_log_scale = st.sidebar.checkbox("Logarithmic Y-Axis", value=True)

# Log range slider (range: from 0.1 ms to 50 hours)
log_slider_range = st.sidebar.slider(
    "Zoom: Visible Time Range (log scale in 10^x seconds)",
    min_value=-4.0, max_value=5.7, value=(-2.0, 4.5), step=0.01
)

# Constants
SECONDS_IN_HOUR = 3600
MIN_TIME_S = 0.0001  # 0.1 ms
MAX_TIME_S = 50 * SECONDS_IN_HOUR  # 50 hours

# Full data range
time_seconds = np.logspace(np.log10(MIN_TIME_S), np.log10(MAX_TIME_S), 1000)
residence_times_h = time_seconds / SECONDS_IN_HOUR

# Calculations
product_concentration_kg_per_L = product_concentration_g_per_L / 1000
plug_flow = product_concentration_kg_per_L / residence_times_h * 24 * 365
batch_residence_times_h = (time_seconds + (cycle_dosing_time_h * SECONDS_IN_HOUR)) / SECONDS_IN_HOUR
batch_flow = product_concentration_kg_per_L / batch_residence_times_h * 24 * 365

# Create plot
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

ax.plot(time_seconds, plug_flow, label="Continuous Plug Flow", color="#3F99AA")
ax.plot(time_seconds, batch_flow, label="Batch (Cycle + Dosing)", color="tab:orange")

# Set scales
ax.set_xscale("log")
ax.set_yscale("log" if use_log_scale else "linear")

# Set axis limits based on zoom
zoom_min = 10 ** log_slider_range[1]
zoom_max = 10 ** log_slider_range[0]
ax.set_xlim(zoom_max, zoom_min)  # Inverted: longer times on left

# Custom ticks
custom_times = [
    50*3600, 10*3600, 5*3600, 2*3600, 3600, 1800, 600, 300, 120, 60, 30, 10, 5, 2, 1,
    0.1, 0.01, 0.001
]
custom_labels = [
    "50 h", "10 h", "5 h", "2 h", "1 h", "30 min", "10 min", "5 min", "2 min", "1 min",
    "30 s", "10 s", "5 s", "2 s", "1 s", "100 ms", "10 ms", "1 ms"
]
ax.set_xticks(custom_times)
ax.set_xticklabels(custom_labels, rotation=45, ha="right")

# Axes labels and legend
ax.set_xlabel("Chemical Reaction Time")
ax.set_ylabel("Industrial Productivity (t/y/m³)")
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))

# Grid and layout
ax.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.tight_layout()

# Display
st.pyplot(fig)
