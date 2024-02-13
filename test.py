import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

from mpl_toolkits import mplot3d

data = pd.read_csv("angle.csv", delimiter=';')

scaler = MinMaxScaler(feature_range=(-1, 1))
normalized_x = scaler.fit_transform(data['x'].values.reshape(-1, 1))  
normalized_y = scaler.fit_transform(data['y'].values.reshape(-1, 1))  

# # Assuming your CSV has columns named 'Column1', 'Column2', and 'Column3'
# plt.figure(figsize=(8, 6))
# #plt.plot(data['x'], label='x')
# #plt.plot(data['y'], label='y')
# #plt.plot(data['angle'], label='angle')
# plt.plot(data['sin'], label='sin')
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Counter')
# plt.legend()
# plt.grid(True)
# plt.show()

# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# # Plot the first dataset
# ax1.plot(normalized_x, label='x', color='blue')
# ax1.plot(normalized_y, label='x', color='red')
# ax1.plot(data['sin'], label='sin', color='green')
# ax1.set_ylabel('X')
# ax1.legend()

# ax2.plot(normalized_x, normalized_y, color='orange')
# ax2.set_xlabel('Sin')

# plt.tight_layout()  # Adjust spacing between subplots
# plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(data['x'], data['y'], data['sin'], c='r', marker='o')

plt.show()