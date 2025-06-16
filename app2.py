import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Streamlit page settings
st.set_page_config(layout="wide")

#st.title("Industrial Productivity vs Reaction Time")
#st.markdown("Use the sliders to explore how productivity changes for batch vs continuous plug flow reactors.")

# Sidebar controls
product_concentration_g_per_L = st.sidebar.slider("Concentration (g/L)", 1, 500, 100)
cycle_dosing_time_h = st.sidebar.slider("Cycle Time (h)", 0.0, 24.0, 10, step=0.01)
log_scale_y = st.sidebar.checkbox("Logarithmic Y-Axis", value=True)

log_min = st.sidebar.slider("Log Min Time (10^x sec)", -3.0, 5.0, 0.0, step=0.01)
log_max = st.sidebar.slider("Log Max Time (10^x sec)", -3.0, 5.0, 4.56, step=0.01)

# Derived values
product_concentration_kg_per_L = product_concentration_g_per_L / 1000
cycle_dosing_time_s = cycle_dosing_time_h * 3600

min_time = 10 ** log_min
max_time = 10 ** log_max
time_seconds = np.logspace(log_min, log_max, 1000)

residence_times_h = time_seconds / 3600
plug_flow = product_concentration_kg_per_L / residence_times_h * 24 * 365
batch_residence_times_h = (time_seconds + cycle_dosing_time_s) / 3600
batch_flow = product_concentration_kg_per_L / batch_residence_times_h * 24 * 365

# Custom ticks
custom_times = np.array([
    0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5,
    10, 30, 60, 120, 300, 600, 1200, 1800, 3600, 7200, 18000, 36000, 86400
])
custom_labels = [
    "1 ms", "2 ms", "5 ms", "10 ms", "20 ms", "50 ms", "0.1 s", "0.2 s", "0.5 s", "1 s", "2 s", "5 s",
    "10 s", "30 s", "1 min", "2 min", "5 min", "10 min", "20 min", "30 min", "1 h", "2 h", "5 h", "10 h", "24 h"
]

ticks_to_use = custom_times[(custom_times >= min_time) & (custom_times <= max_time)]
labels_to_use = [label for t, label in zip(custom_times, custom_labels) if min_time <= t <= max_time]

# Plotting
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
ax.plot(time_seconds, plug_flow, label="Continuous plug flow", color='#3F99AA')
ax.plot(time_seconds, batch_flow, label="Batch (Cycle + Dosing)", color='tab:orange')

ax.set_xscale("log")
ax.set_xticks(ticks_to_use)
ax.set_xticklabels(labels_to_use, rotation=45, ha="right")

if log_scale_y:
    ax.set_yscale("log")
else:
    ax.set_yscale("linear")

ax.set_xlabel("Chemical Reaction Time")
ax.set_ylabel("Industrial Productivity (t/y/m³)")
ax.legend()
ax.grid(True, which="both", ls="--", lw=0.5)
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,}'))
st.pyplot(fig)