import os
import sys

from flightFare.exception import FlightFareException
from flightFare.util.util import load_object
from flightFare.constant import COLUMNS

import pandas as pd


class FlightData:

    def __init__(self, Airline, Date_of_Journey,Source,Destination,Dep_Time,Arrival_Time,Duration,Total_Stops):
        try:
            self.Airline = Airline
            self.Date_of_Journey = Date_of_Journey
            self.Source = Source
            self.Destination = Destination
            self.Dep_Time = Dep_Time
            self.Arrival_Time = Arrival_Time
            self.Duration = Duration
            self.Total_Stops = Total_Stops
        except Exception as e:
            raise FlightFareException(e, sys) from e

    def transform_dataframe(self, flight_data_dict):
        df = pd.DataFrame.from_dict(flight_data_dict)
        
        journey_date = df.Date_of_Journey.iloc[0].split('/')
        df['Journey_day'] = journey_date[0]
        df['Journey_month'] = journey_date[1]


        Dep_Time = df.Dep_Time.iloc[0].split(':')
        df['Dep_hour'] = Dep_Time[0]
        df['Dep_min'] = Dep_Time[1]

        Arrival_Time = df.Arrival_Time.iloc[0].split(':')
        df['Arrival_hour'] = Arrival_Time[0]
        df['Arrival_min'] = Arrival_Time[1]

        duration = df.Duration.iloc[0]
        if len(duration.split()) != 2:    # Check if duration contains only hour or mins
            if "h" in duration:
                duration = duration.strip() + " 0m"   # Adds 0 minute
            else:
                duration = "0h " + duration           # Adds 0 hour

        df['Duration_hours'] = int(duration.split(sep = "h")[0])
        df['Duration_mins'] = int(duration.split(sep = "m")[0].split()[-1])

        df.drop(["Date_of_Journey", 'Dep_Time', 'Arrival_Time', 'Duration'], axis = 1, inplace = True)
        print(df)
        return df

    def get_flight_input_data_frame(self):

        try:
            flight_data_dict = self.get_flight_data_as_dict()
            print(flight_data_dict)
            return self.transform_dataframe(flight_data_dict)
        except Exception as e:
            raise FlightFareException(e, sys) from e

    def get_flight_data_as_dict(self):
        try:
            input_data = {
                "Airline": [self.Airline],
                "Date_of_Journey": [self.Date_of_Journey],
                "Source": [self.Source],
                "Destination": [self.Destination],
                "Dep_Time": [self.Dep_Time],
                "Arrival_Time": [self.Arrival_Time],
                "Duration": [self.Duration],
                "Total_Stops": [self.Total_Stops]
                }
            return input_data
        except Exception as e:
            raise FlightFareException(e, sys)


class predictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise FlightFareException(e, sys) from e

    def get_latest_model_path(self):
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise FlightFareException(e, sys) from e

    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            flight_value = model.predict(X)
            return flight_value
        except Exception as e:
            raise FlightFareException(e, sys) from e
