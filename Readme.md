# Flight Fare Prediction

This project aims to solve the problem of predicting the predicting the Flight Fare price, using Sklearn's supervised machine learning techniques. It is a classification problem and predictions are carried out on dataset, Several regression techniques have been studied, including XGboost and Random forests of decision trees.

💿 Installing
1. Environment setup.
```
conda create --prefix venv python=3.9 -y
```
```
conda activate venv/
````
2. Install Requirements and setup
```
pip install -r requirements.txt
```
5. Run Application
```
Flask
```


🔧 Built with
- Flask
- Python 3.9
- Machine learning
- 🏦 Industrial Use Cases

## Models Used
* Linear Regression
* Lasso Regression
* Ridge Regression
* K-Neighbors Regressor
* Decision Tree
* Random Forest Regressor
* XGBRegressor
* CatBoosting Regressor
* AdaBoost Regressor

* GridSearchCV is used for Hyperparameter Optimization in the pipeline.

* Any modification has to be done in  Inside Config.yaml which can be done in route **/update_model_config**

## `packagePrediction` is the main package folder which contains 

**Artifact** : Stores all artifacts created from running the application

**Components** : Contains all components of Machine Learning Project
- DataIngestion
- DataValidation
- DataTransformations
- ModelTrainer
- ModelEvaluation
- ModelPusher

Frontend to show Artifact, Experiment, Model Training, Saved Models, logs which can be accessed from the developer

**Routes for An API**:
```
/predict
```
* Predict Route for User to predict 

*Example Input For Prediction*: 
    "Airline" :  "Jet Airways", <br/>
   "Date_of_Journey" :  "9/10/2019",<br/>
   "Source" :  "Banglore",<br/>
   "Destination" :  "Cochin",<br/>
   "Dep_Time" :  "20:25",<br/>
   "Arrival_Time" :  "04:25",<br/>
   "Duration" :  "19h",<br/>
   "Total_Stops" : 1,<br/>




**Custom Logger and Exceptions** are used in the Project for better debugging purposes.

## Conclusion
- This Project can be used in real-life by Users to predict that the Flight Price
