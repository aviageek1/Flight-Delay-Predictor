import pandas as pd
import math

######### Scikit Algorithms
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

####### PLOTTING GRAPHS ####
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve

from datetime import datetime


# open data file
df = pd.read_csv('airlinedelaycauses_DelayedFlights.csv')

# remove extra columns at end
df = df.drop(['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay',
              'LateAircraftDelay'], axis=1)

# remove columns except these
df = df[["Month", "DayofMonth", "DayOfWeek", "Origin", "Dest", "CRSDepTime",
         "ArrDelay"]]
df = df.dropna(how='any')  # clean by dropping any rows with a NaN value

# Biggest hubs for DELTA, AMERICAN, UNITED, SOUTHWEST, ALASKA respectively
# o_airports = ['ATL', 'DFW', 'ORD', 'DEN', 'SEA']
o_airports = ['SLC', 'OAK']
keywords = '|'.join(o_airports)

df = df[df['Origin'].str.contains(
    keywords)]  # only flights originating from keyword airports
# keys = ['MDW', 'LAS', 'OAK', 'PHX', 'SEA'] #only these destinations
# words = '|'.join(keys)
# df = df[df['Dest'].str.contains(words)]
print(len(df))  # print number of rows

##### EMPTY CHECKS #####
# print(df.isnull().sum()) # prints nunmber of empty rows?
# print(df[df.isnull().values.any(axis=1)].head()) # prints how many empty columns?


# df = df.iloc[:100000] # keep only do 1000 rows


indices_to_drop = []
# round down and simplify the departure time to only account for the hour
for index, row in df.iterrows():
    df.loc[index, 'CRSDepTime'] = math.floor(row['CRSDepTime'] / 100)
    if row['ArrDelay'] <= 0:  # drop flights that had no delay
        indices_to_drop.append(index)
    # df.loc[index, 'ArrDelay'] = round(df.loc[index, 'ArrDelay'] / 10) * 10 # quantize values into 10s

    #### change values so 15+ minutes late = 1, under 15 minutes late = 0
    if row['ArrDelay'] >= 15:
        df.loc[index, 'ArrDelay'] = 1
    else:
        df.loc[index, 'ArrDelay'] = 0

df = df.drop(indices_to_drop)
print(len(df))  # print number of rows

######## CHECK OCCURANCES

originn = 'SLC'
destt = 'DTW'
# Filter the DataFrame for the specific origin and destination
filtered_df = df[(df['Origin'] == originn) & (df['Dest'] == destt)]

# Get the number of rows
row_count = len(filtered_df)

print(
    f"Number of rows where Origin is {originn} and Dest is {destt}: {row_count}")

count_delay_1 = (filtered_df['ArrDelay'] == 1).sum()
print(
    f"Number of rows where Origin is {originn}, Dest is {destt}, and ArrDelay is 1.0 (delayed): {count_delay_1}")

# dummify the origin and destination columns
df = pd.get_dummies(df, columns=['Origin', 'Dest'])
# print(df.head())

############## MODEL

# split into training and testing rows/columns
train_x, test_x, train_y, test_y = train_test_split(df.drop('ArrDelay', axis=1),
                                                    df['ArrDelay'],
                                                    test_size=0.3,
                                                    random_state=42)

model = RandomForestClassifier(random_state=18)
model.fit(train_x, train_y)  # make decision trees

##### ACCURACY TESTS #####
# print(model.score(test_x, test_y)) # get model accuracy

probabilities = model.predict_proba(test_x)


# print(roc_auc_score(test_y, probabilities[:, 1]))

# predict = model.predict(test_x)
# print(confusion_matrix(test_y,predict))


###### CREATING PREDICTION ######

def predict_delay(departure_date_time, origin, destination):

    try:
        departure_date_time_parsed = datetime.strptime(departure_date_time,
                                                       '%d/%m/%Y %H:%M:%S')
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


# Example usage
print("The probability of the flight being on-time is",
      predict_delay('07/10/2008 21:45:00', originn, destt))
