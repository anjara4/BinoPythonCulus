import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Assuming 'data.csv' is your data file
data = pd.read_csv('AlDu00_26-01-2024_13-40_InfiniteV_Target.csv', sep=';')

# Create a linear regression model
model = LinearRegression()

# Fit the model to your data
model.fit(data[['time']], data['x'])

# Now you can use the fitted model to predict 'x' based on 'time'
predicted_x = model.predict(data[['time']])

# Plot actual vs predicted data
plt.scatter(data['time'], data['x'], color='blue')
plt.plot(data['time'], predicted_x, color='red')
plt.show()
