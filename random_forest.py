import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

data = pd.read_csv("walmart-sales-dataset-of-45stores.csv")

data = pd.get_dummies(data, columns=['Store'], drop_first=True)

data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
data['DayOfWeek'] = data['Date'].dt.dayofweek  # Monday=0, Sunday=6
data['Month'] = data['Date'].dt.month
data['Year'] = data['Date'].dt.year

X = data.drop(columns=['Weekly_Sales', 'Temperature', 'Unemployment', 'Fuel_Price', 'Date'])

y_sales = data['Weekly_Sales']
y_temp = data['Temperature']
y_unemployment = data['Unemployment']
y_fuel = data['Fuel_Price']

# Train-test split for Weekly_Sales
X_train, X_test, y_train_sales, y_test_sales = train_test_split(X, y_sales, test_size=0.2, random_state=42)

# Train-test split for Temperature
X_train, X_test, y_train_temp, y_test_temp = train_test_split(X, y_temp, test_size=0.2, random_state=42)

# Train-test split for Unemployment
X_train, X_test, y_train_unemployment, y_test_unemployment = train_test_split(X, y_unemployment, test_size=0.2,
                                                                              random_state=42)

X_train, X_test, y_train_fuel, y_test_fuel = train_test_split(X, y_fuel, test_size=0.2, random_state=42)

rf_sales = RandomForestRegressor(n_estimators=100, random_state=42)
rf_temp = RandomForestRegressor(n_estimators=100, random_state=42)
rf_unemployment = RandomForestRegressor(n_estimators=100, random_state=42)
rf_fuel = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the models
rf_sales.fit(X_train, y_train_sales)
rf_temp.fit(X_train, y_train_temp)
rf_unemployment.fit(X_train, y_train_unemployment)
rf_fuel.fit(X_train, y_train_fuel)

print(f"R-squared for Weekly_Sales: {rf_sales.score(X_test, y_test_sales)}")

# Evaluate Temperature model
print(f"R-squared for Temperature: {rf_temp.score(X_test, y_test_temp)}")

# Evaluate Unemployment model
print(f"R-squared for Unemployment: {rf_unemployment.score(X_test, y_test_unemployment)}")

# Evaluate Temperature model
print(f"R-squared for Fuel: {rf_fuel.score(X_test, y_test_fuel)}")


