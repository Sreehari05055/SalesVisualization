import os
from pymongo import MongoClient
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

mongodb_uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(mongodb_uri)

db = client["Walmart"]
collection = db["WalmartData"]

# Fetch data
corpora = collection.find({},{'_id':0,'Weekly_Sales':1, 'Date': 1})

sales_data = pd.DataFrame(list(corpora))

# Convert the 'Date' column from string to datetime format
sales_data['Date'] = pd.to_datetime(sales_data['Date'], dayfirst=True)

sales_data['Weekly_Sales'] = sales_data['Weekly_Sales'].astype(float)

weekly_sales_data = sales_data.sort_values(by='Date')
# Rename columns for modeling needs
df = weekly_sales_data.rename(columns={'Date': 'ds', 'Weekly_Sales': 'y'})

# Initialize and fit the model
model = Prophet()
model.fit(df)

# Make future predictions
future = model.make_future_dataframe(periods=365)  # Forecast
forecast = model.predict(future)

# Plot the forecast
fig = model.plot(forecast)


plt.title('Sales Forecast', fontsize=14, fontweight='bold')
plt.xlabel('Date (YY-mm)', fontsize=12)
plt.ylabel('Sales Amount (10^6 M)', fontsize=12)

specific_dates = ['2013-10-01']  # Add the dates
specific_forecast = forecast[forecast['ds'].isin(specific_dates)]

print(specific_forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])

plt.savefig('sales_forecast.png', format='png')

plt.show()

