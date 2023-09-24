from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter

import numpy as np
import pandas as pd
import random
import json
import time


fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(elev=20, azim=45)
init_temp = 500
num_iters = 50000

# Collecting the data for the surface
x_data, y_data, z_data = [], [], []

for rate in np.arange(0.75, 1.00, 0.01):
    rate_val = round(rate, 2)
    filename = f"{init_temp}_{rate_val}_{num_iters}_results.csv"
    temp_df = pd.read_csv(filename)
    rate_series = [rate_val] * num_iters
    
    # Take every 2nd iteration
    selected_iterations = temp_df['Iterations'][::2]
    selected_scores = temp_df['Scores'][::2]
    rate_series = [rate_val] * len(selected_iterations)
    
    x_data.extend(selected_iterations)
    y_data.extend(rate_series)
    z_data.extend(selected_scores)


# Define a grid and interpolate data onto the grid
xi, yi = np.linspace(min(x_data), max(x_data), 100), np.linspace(min(y_data), max(y_data), 100)
xi, yi = np.meshgrid(xi, yi)
zi = griddata((x_data, y_data), z_data, (xi, yi), method='linear')

# Apply a Gaussian filter to smooth the data
zi_smooth = gaussian_filter(zi, sigma=1)

# Creating the smoothed surface plot
ax.plot_surface(xi, yi, zi_smooth, cmap='viridis', alpha=0.5)

ax.set_xlabel('Iterations')
ax.set_ylabel('Scores')
ax.set_zlabel('Cooling Rate')

plt.title('Progression of Objective Score for Different Cooling Rates, iters=50,000')

# Generate mp4
# Function to update the view angle
def update(frame):
    ax.view_init(elev=10, azim=frame)
    return fig,

# Create an animation that rotates the plot by 360 degrees
ani = FuncAnimation(fig, update, frames=np.arange(0, 360, 1), interval=75)

# Save the animation as a video file
ani.save('3d_rotation_scores_graph_final0.gif', writer='pillow', dpi=150)

plt.show()
