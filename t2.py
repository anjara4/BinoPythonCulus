import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV data
#data = pd.read_csv('BoMa99_30-01-2024_09-56_InfiniteV_Target.csv', sep=";")
data = pd.read_csv('AlDu00_30-01-2024_10-10_InfiniteH_Target.csv', sep=";")


print("min x: " + str(data['x'].min()))
print("max x: " + str(data['x'].max()))
print("max - min: " + str(data['x'].max() - data['x'].min()))

print("min y: " + str(data['y'].min()))
print("max y: " + str(data['y'].max()))
print("max - min: " + str(data['y'].max() - data['y'].min()))

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(data['x'], data['y'])
plt.plot(data['x'] * 13, data['y'])
plt.title('Title of Your Plot')
plt.xlabel('X-Axis Label')
plt.ylabel('Y-Axis Label')
plt.grid(True)
plt.show()