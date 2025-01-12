import pandas as pd
from prophet import Prophet
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Connect to MySQL
engine = create_engine('mysql+mysqlconnector://root:Bit4$ree%400505@localhost/SalesVisualization')

# Fetch daily sales data
query = """
    SELECT 
        DATE(OrderDate) AS OrderDay, 
        SUM(TotalSales) AS DailyTotalSales 
    FROM 
        SalesTransactions 
    GROUP BY 
        OrderDay 
    ORDER BY 
        OrderDay;
"""

query1 = """SELECT
                CustomerID,
                LastShopDate
            FROM Customers;"""

# Load data
sales_data = pd.read_sql(query, engine)
customer_data = pd.read_sql(query1, engine)

# Ensure 'LastShopDate' is a datetime object
customer_data['LastShopDate'] = pd.to_datetime(customer_data['LastShopDate'])

# Calculate 'DaysSinceLastShop' for each customer
current_date = pd.to_datetime(sales_data['OrderDay'].max())
customer_data['DaysSinceLastShop'] = (current_date - customer_data['LastShopDate']).dt.days

# Aggregate 'DaysSinceLastShop' to daily averages
avg_days_per_day = customer_data.groupby(customer_data['LastShopDate'].dt.date)['DaysSinceLastShop'].mean()
avg_days_per_day = avg_days_per_day.rename_axis('OrderDay').reset_index()
avg_days_per_day['OrderDay'] = pd.to_datetime(avg_days_per_day['OrderDay'])

# Merge with sales data
sales_data['OrderDay'] = pd.to_datetime(sales_data['OrderDay'])
sales_with_factors = pd.merge(sales_data, avg_days_per_day, on='OrderDay', how='left')

# Fill missing 'DaysSinceLastShop' with the overall average
overall_avg_days = customer_data['DaysSinceLastShop'].mean()
sales_with_factors['DaysSinceLastShop'].fillna(overall_avg_days, inplace=True)

# Set missing dates in sales data
sales_with_factors.set_index('OrderDay', inplace=True)
sales_with_factors = sales_with_factors.asfreq('D', fill_value=0)
sales_with_factors.reset_index(inplace=True)

# Prepare data for Prophet
sales_with_factors.columns = ['ds', 'y', 'DaysSinceLastShop']  # Prophet expects 'ds' and 'y'

# Initialize the model and add the regressor
model = Prophet()
model.add_regressor('DaysSinceLastShop')  # Add external factor

# Fit the model
model.fit(sales_with_factors)

# Prepare future data
future = model.make_future_dataframe(periods=30)  # Forecast for the next 30 days
future = pd.merge(future, sales_with_factors[['ds', 'DaysSinceLastShop']], on='ds', how='left')

# Fill missing values for 'DaysSinceLastShop' in the future with the overall average
future['DaysSinceLastShop'].fillna(overall_avg_days, inplace=True)

# Predict
forecast = model.predict(future)

# Plot the forecast
fig = model.plot(forecast)

# Customize the plot
plt.title('Sales Forecast with External Factors', fontsize=14, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Sales Amount', fontsize=12)

# Save the plot
fig.savefig('forecast_with_regressor.png')

plt.show()