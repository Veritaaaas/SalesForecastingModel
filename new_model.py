import pandas as pd
import matplotlib.pyplot  as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime

# Read the data
df = pd.read_csv('static/csv_files/Bakery_sales.csv')

# dropping negative values
df = df[df['Quantity'] >= 0]

# dropping the first column
df = df.drop(df.columns[0], axis=1)

#converting date to datetime
df['date'] = pd.to_datetime(df['date'])

# setting date as index
df.set_index('date', inplace=True)

def predict_model(article, start_date, end_date):

    # searching for the given product
    product = df[df['article'] == article]

    # sampling the quantity data into weekly basis
    weekly_sales = product['Quantity'].resample('W').sum()

    # fitting the data into the model
    model = SARIMAX(weekly_sales, order=(0,0,0), seasonal_order=(0,1,0,52))
    model_fit = model.fit()
    
    # converting into datetime format
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Calculate the number of weeks between the end of the training data and the end date
    weeks_between = int((end_date - weekly_sales.index[-1]).days // 7) + 1

    # Get forecast for the specified date range
    forecast = model_fit.get_forecast(steps=weeks_between)
    
    # saves the forecast into csv file
    forecast_df = pd.DataFrame(forecast.predicted_mean)
    forecast_df = forecast_df.loc[start_date:end_date]
    forecast_df.to_csv('forecast.csv')

    # Plotting the results
    plt.figure(figsize=(10,5))
    plt.plot(weekly_sales, label='Train')
    plt.plot(forecast.predicted_mean, label='Prediction')
    plt.legend(loc='best')
    plt.title(article + ' Sales Prediction')
    plt.savefig('static/images/my_plot.png')

    
