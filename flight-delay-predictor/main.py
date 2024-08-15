##############

#TO-DO: SPLIT INTO FUNCTIONS AND CREATE DRIVER (currently on model)
#CHECK IF YOU NEED TO RETURN THE df FOR SETTER FUNCTIONS  

##############

import pandas as pd
import math

######### Scikit Algorithms #########
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

####### GRAPH PLOTTING #######
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve

from datetime import datetime




def open_csv():
    # open and read data file
    df = pd.read_csv('flight-delay-predictor/airlinedelaycauses_DelayedFlights.csv')
    return df


def remove_extra(df):
    # remove extra columns at end
    df = df.drop(['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
                'LateAircraftDelay'], axis=1)

    # remove columns except these
    df = df[["Month", "DayofMonth", "DayOfWeek", "Origin", "Dest", "CRSDepTime",
            "ArrDelay"]]
    df = df.dropna(how='any')  # clean by dropping any rows with a NaN value
    return df


def origins(o_airports, df): #o_airports is list of airports (ex: o_airports = ['SLC', 'OAK'])
    
    #########
    # Biggest hubs for DELTA, AMERICAN, UNITED, SOUTHWEST, ALASKA respectively
    # o_airports = ['ATL', 'DFW', 'ORD', 'DEN', 'SEA']
    #########

    keywords = '|'.join(o_airports)
    df = df[df['Origin'].str.contains(keywords)]  # only keep flights originating from keyword airports
    return df


def destinations(d_airports, df):
    # keys = ['MDW', 'LAS', 'OAK', 'PHX', 'SEA'] # only keep flights arriving to keyword airports
    keywords = '|'.join(d_airports)
    df = df[df['Dest'].str.contains(keywords)]
    return df    


"""
def check_empty_rows(df):
    ##### EMPTY CHECKS #####
    # print(df.isnull().sum()) # prints nunmber of empty rows?
    # print(df[df.isnull().values.any(axis=1)].head()) # prints how many empty columns?

    # df = df.iloc[:100000] # keep only do 1000 rows
    
    return df
"""
    
def quantize(df, delay, origin, dest): # parameter delay is int that states how many minutes counts as "delayed" (ex: 15) 
    indices_to_drop = []
    filtered_df = df[(df['Origin'] == origin) & (df['Dest'] == dest)]
    # round down and simplify the departure time to only account for the hour
    for index, row in filtered_df.iterrows():
        filtered_df.loc[index, 'CRSDepTime'] = math.floor(row['CRSDepTime'] / 100)
        if row['ArrDelay'] <= 0:  # drop flights that had no delay
            indices_to_drop.append(index)
        #### change values so "delay"+ minutes late = 1, under "delay" minutes late = 0
        if row['ArrDelay'] >= delay:
            filtered_df.loc[index, 'ArrDelay'] = 1
        else:
            filtered_df.loc[index, 'ArrDelay'] = 0

    filtered_df = filtered_df.drop(indices_to_drop) # actually remove rows that had no delay 
    return filtered_df

# count and print how many occurances of the origin/dest pair there are and how many are delayed

"""
def check_occurances(origin, dest, df): 
    ######## CHECK OCCURANCES
    # originn = 'SLC'
    # destt = 'DTW'
    # Filter the DataFrame for the specific origin and destination
    filtered_df = df[(df['Origin'] == origin) & (df['Dest'] == dest)]

    # Get the number of rows
    row_count = len(filtered_df)

    print(f"Number of rows where Origin is {origin} and Dest is {dest}: {row_count}")

    count_delay_1 = (filtered_df['ArrDelay'] == 1).sum()
    print(f"Number of rows where Origin is {origin}, Dest is {dest}, and ArrDelay is 1.0 (delayed): {count_delay_1}")
"""

def dummy(df):
    # dummify the origin and destination columns
    df = pd.get_dummies(df, columns=['Origin', 'Dest'])
    # print(df.head())

    return df
    


############## MODEL

# returns df, learned model, and accuracy of model
def trees(df): 
    # split into training and testing rows/columns
    train_x, test_x, train_y, test_y = train_test_split(df.drop('ArrDelay', axis=1),
                                                        df['ArrDelay'],
                                                        test_size=0.3,
                                                        random_state=42)

    model = RandomForestClassifier(random_state=18)
    model.fit(train_x, train_y)  # make decision trees

    ##### ACCURACY TESTS #####
    accuracy = model.score(test_x, test_y) # get model accuracy

    # probabilities = model.predict_proba(test_x)
    # print(roc_auc_score(test_y, probabilities[:, 1]))

    # predict = model.predict(test_x)
    # print(confusion_matrix(test_y,predict))

    return df, model, accuracy



###### CREATING PREDICTION ######

def predict_delay(departure_date_time, origin, destination, df, model):

    try:
        departure_date_time_parsed = datetime.strptime(departure_date_time,
                                                       '%m/%d/%Y %H:%M:%S')
    except ValueError as e:
        return f'Error parsing date/time - {e}'

    month = departure_date_time_parsed.month
    day = departure_date_time_parsed.day
    day_of_week = departure_date_time_parsed.isoweekday()
    hour = departure_date_time_parsed.hour

    origin = origin.upper()
    destination = destination.upper()

    # Get the unique origins and destinations from the dataset
    origin_columns = [col for col in df.columns if col.startswith('Origin_')]
    destination_columns = [col for col in df.columns if col.startswith('Dest_')]

    # Initialize the input data dictionary
    input_data = {
        'Month': month,
        'DayofMonth': day,
        'DayOfWeek': day_of_week,
        'CRSDepTime': hour
    }

    # Add origin columns
    for col in origin_columns:
        input_data[col] = 1 if f'Origin_{origin}' == col else 0

    # Add destination columns
    for col in destination_columns:
        input_data[col] = 1 if f'Dest_{destination}' == col else 0

    # Convert input_data to a DataFrame
    input_df = pd.DataFrame([input_data])

    # Predict the probability of delay
    return model.predict_proba(input_df)[0][0]  # Probability of on time (0)
    # if want probability of delay, use [0][1]


# # Example usage
# print("The probability of the flight being on-time is",
#       predict_delay('07/10/2008 21:45:00', origin, dest))



# driver
def main():
    print("\n\n\nWelcome to Flight Model Predictor!")
    print("Created by: Aayush Sharma")
    print("\n")
    print("Input a major airport's flight route, time, and minutes of delay you want to calculate by. \nBased on 2008 data,"
          " get a prediction on if it will be delayed or not!")
    print("\nPlease note that commercial air traffic in 2008 took a big hit in terms of on-time performance, " 
          "and numbers will likely be lower than expected.")
    
    
    date = input("\nEnter the flight's departure date in the format mm/dd: ").strip()
    time = input("Enter the time of the flight in the format hh:mm: ").strip()
    o_airports = input("Enter an origin airport you would like to search for: ").strip().upper()
    d_airports = input("Enter a destination airport you would like to search for: ").strip().upper()
    print("\nLoading.. please wait")
    df = open_csv() # open, read, and create dataframe
    df = remove_extra(df) # clean and simplify dataframe

    df = origins(o_airports, df)
    df = destinations(d_airports, df)
    
    delay = int(input("\nEnter the amount of delay (in minutes) you would like to sort by (how late is too late?): "))
    
    df = quantize(df, delay, o_airports, d_airports)

    df = dummy(df)
    df, model, accuracy = trees(df)

    departure_date_time = (f"{date}/2008 {time}:00")
    probability_on_time = (float(predict_delay(departure_date_time, o_airports, d_airports, df, model)))*100

    print(f"\nThe probability that your selected flight will be on-time is {probability_on_time:.0f}%.")
    print(f"The model's accuracy is {accuracy}.\n")



main()