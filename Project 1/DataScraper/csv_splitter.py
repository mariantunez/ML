import sys
import pandas as pd
import random
from csv_generator import create_csv

#FLIGHTS_CSV_PATH = '../CSVFiles/FligthsData.csv'
TRAINING_CSV_PATH = '../CSVFiles/TrainingData.csv'
TEST_CSV_PATH = '../CSVFiles/TestData.csv'

def get_file_name():
    '''Prompts the command line for the dataset csv file name'''

    CSV_FORMAT = '.csv'
    file_csv_path = None

    while(file_csv_path == None):
        file_csv_path = input('Input File Name of Dataset to Split: ') 
    
    if(not file_csv_path.endswith(CSV_FORMAT)):
        file_csv_path = file_csv_path + CSV_FORMAT

    return file_csv_path


def get_split_percentage():
    '''Prompts the commans line for the % of data for training set'''
    percentage = None

    while(percentage == None or percentage < 1 or percentage > 100):
        percentage = int(input('Input Percentage for Trainning Set: '))

    return percentage


def split_csv():
    '''Create new csv files for new sets. Uses a list of random indices to define he order in 
    which it access data to append it to each csv file. Start by filling the training dasatet'''

    # Create csv for training and test sets
    create_csv(TRAINING_CSV_PATH)
    create_csv(TEST_CSV_PATH)

    csv_data = pd.read_csv(get_file_name())
    data_len = len(csv_data)

    # Determine rows for each set
    curr_training_data = 0
    training_percentage = get_split_percentage()
    training_data = int((data_len * training_percentage) / 100)
    test_data = data_len - training_data

    print('\nTotal Data: ' +  str(data_len) + " rows")
    print('Training DataSet:  ' + str(training_percentage) + '% [' + str(training_data) + ' rows] at ' + TRAINING_CSV_PATH)
    print('Test DataSet: '  + str(100 - training_percentage) + '% [' + str(test_data)  + ' rows] at ' + TEST_CSV_PATH)


    # Write random rows of the data set to CSVs
    index = list(range(0, data_len))
    random.shuffle(index)

    for i in index:
        row = csv_data.take([i])
        path = TEST_CSV_PATH

        # Write first random rows to training set
        if(curr_training_data < training_data):
            path = TRAINING_CSV_PATH
            curr_training_data += 1
        
        row.to_csv(path, header=False, index=False, mode='a') 


split_csv()
