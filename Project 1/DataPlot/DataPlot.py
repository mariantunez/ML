import matplotlib.pyplot as plt
import matplotlib.dates as md
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

TIME_FORMAT = '%H:%M'
FLIGHTS_CSV_PATH = '../CSVFiles/FligthsData.csv'
csv_data = pd.read_csv(FLIGHTS_CSV_PATH)

# Retreive Dependent Variable
prices = list(csv_data['Price'])

# Retrieve Independent Variables
airlines = list(csv_data['Airline'])
weekdays = list(csv_data['Weekday'])
dates = list(csv_data['Date'])
departure_times = list(csv_data['Departure Time'])
departure_meridiems =  list(csv_data['Departure Meridiem'])


def convert_hour_format(times, meridiems):
    '''Converts time to 24 hours format based on the mediriems'''
    for i in range(0, len(times)):
        if(meridiems[i] == 'pm'):
            time = times[i].split(':')
            hour = int(time[0]) + 12
            new_hour = str(hour) + ':' + time[1]
            
            times[i] = new_hour
    
    times = pd.to_datetime(times, format=TIME_FORMAT)
    return times


def plot_by_price(title, yaxis):
    '''Plots price given Yaxis values'''
    plt.title('Prices by ' + title)
    plt.xlabel('Prices ($)')
    plt.ylabel(title)
    plt.scatter(prices, yaxis)
    plt.show()
    

def plot_hour_price(times):
    '''Plots price given the time in 24hr format'''
    ax=plt.gca()
    ax.yaxis.set_major_formatter(md.DateFormatter(TIME_FORMAT)) 
    plt.title('Prices by Hour')
    plt.xlabel('Prices ($)')
    plt.ylabel('Hour (24hr format)')
    plt.scatter(prices, times)
    plt.show()


def plot_variables():
    '''Calls plot functions for each independent variable'''
    # Plot time in 24 hour format
    departure_times_converted = convert_hour_format(departure_times, departure_meridiems)
    plot_hour_price(departure_times_converted)

    # Plot the remaining independent variables
    plot_by_price('Airlines', airlines)
    plot_by_price('Weekdays', weekdays)
    plot_by_price('Date', dates)
    plot_by_price('Meridiems', departure_meridiems)


def linear_regression(Yaxis):
    '''Performs Linear Regression Model'''
    def linear_model(x):
        return slope* x + intercept 

    x = np.array(prices).reshape((-1, 1))
    y = np.array(Yaxis)

    model = LinearRegression().fit(x, y)

    slope = model.coef_
    intercept = model.intercept_

    new_axis = list(map(linear_model, x))
        
    return new_axis

def plot_linear_regressions():
    '''Calls plot function forndependent variable after linear regresion'''
    plot_by_price('Date (Linear Regression)', linear_regression(dates))
    

plot_variables()
plot_linear_regressions()



