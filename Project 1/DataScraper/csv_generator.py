import pandas as pd
import os.path as path

COLUMNS = pd.DataFrame(columns = ['Airline','Weekday','Date', 'Departure Time', 'Departure Meridiem', 'Price'])

def create_csv(PATH):
    '''Create a CSV only with column name from a pandas DataFrame '''
    if((not path.exists(PATH)) or path.getsize(PATH)==0):
        COLUMNS.to_csv(PATH, header=True, index=False, mode='w')