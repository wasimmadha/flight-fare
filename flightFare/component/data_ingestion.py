from flightFare.entity.config_entity import DataIngestionConfig
import sys, os
from flightFare.exception import FlightFareException
from flightFare.logger import logging
from flightFare.entity.artifact_entity import DataIngestionArtifact
from six.moves import urllib
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit


class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>' * 20}Data Ingestion log started.{'<<' * 20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise FlightFareException(e, sys)

    def download_data(self) -> str:
        try:
            # extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            # folder location to download file
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            os.makedirs(raw_data_dir, exist_ok=True)

            flight_file_name = "Data_train.csv"

            raw_file_path = os.path.join(raw_data_dir, flight_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{raw_file_path}]")
            urllib.request.urlretrieve(download_url, raw_file_path)
            logging.info(f"File :[{raw_file_path}] has been downloaded successfully.")
            return raw_file_path

        except Exception as e:
            raise FlightFareException(e, sys) from e

        
    @classmethod
    def transform_x(self, X):
        X["Journey_day"] = pd.to_datetime(X["Date_of_Journey"], format="%d/%m/%Y").dt.day
        X["Journey_month"] = pd.to_datetime(X["Date_of_Journey"], format = "%d/%m/%Y").dt.month
        print(X.columns)
        X.drop(["Date_of_Journey"], axis = 1, inplace = True)

        # Extracting Hours
        X["Dep_hour"] = pd.to_datetime(X["Dep_Time"]).dt.hour

        # Extracting Minutes
        X["Dep_min"] = pd.to_datetime(X["Dep_Time"]).dt.minute

        # Now we can drop Dep_Time as it is of no use
        X.drop(["Dep_Time"], axis = 1, inplace = True)

        X["Arrival_hour"] = pd.to_datetime(X.Arrival_Time).dt.hour

        # Extracting Minutes
        X["Arrival_min"] = pd.to_datetime(X.Arrival_Time).dt.minute

        # Now we can drop Arrival_Time as it is of no use
        X.drop(["Arrival_Time"], axis = 1, inplace = True)


        X = X.drop(X[X["Airline"]== "Trujet"].index)

        # Assigning and converting Duration column into list
        duration = list(X["Duration"])

        for i in range(len(duration)):
            if len(duration[i].split()) != 2:    # Check if duration contains only hour or mins
                if "h" in duration[i]:
                    duration[i] = duration[i].strip() + " 0m"   # Adds 0 minute
                else:
                    duration[i] = "0h " + duration[i]           # Adds 0 hour

        duration_hours = []
        duration_mins = []
        for i in range(len(duration)):
            duration_hours.append(int(duration[i].split(sep = "h")[0]))    # Extract hours from duration
            duration_mins.append(int(duration[i].split(sep = "m")[0].split()[-1]))   # Extracts only 

        X["Duration_hours"] = duration_hours
        X["Duration_mins"] = duration_mins

        X.drop(["Duration"], axis = 1, inplace = True)

        X.drop(["Route", "Additional_Info"], axis = 1, inplace = True)

        X.replace({"non-stop": 0, "1 stop": 1, "2 stops": 2, "3 stops": 3, "4 stops": 4}, inplace = True)
        print(X["Price"])
        return X

    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            flight_file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Reading csv file: [{flight_file_path}]")
            flight_data_frame = pd.read_csv(flight_file_path)

            flight_data_frame["price_cat"] = pd.cut(
                flight_data_frame["Price"],
                bins=[1700, 5000, 10000, 15000, 20000, 25000, np.inf],
                labels=[1, 2, 3, 4, 5, 6]
            )

            logging.info(f"Splitting data into train and test")

            strat_train_set = None
            strat_test_set = None

            split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            for train_index, test_index in split.split(flight_data_frame, flight_data_frame["price_cat"]):
                strat_train_set = flight_data_frame.loc[train_index].drop(["price_cat"], axis=1)
                strat_test_set = flight_data_frame.loc[test_index].drop(["price_cat"], axis=1)
            
            strat_train_set = DataIngestion.transform_x(strat_train_set)
            strat_test_set = DataIngestion.transform_x(strat_test_set)

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                           file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                          file_name)

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
                logging.info(f"Exporting training dataset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path, index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                                            test_file_path=test_file_path,
                                                            is_ingested=True,
                                                            message=f"Data ingestion completed successfully."
                                                            )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise FlightFareException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            raw_file_path = self.download_data()
            return self.split_data_as_train_test()
        except Exception as e:
            raise FlightFareException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>' * 20}Data Ingestion log completed.{'<<' * 20} \n\n")
