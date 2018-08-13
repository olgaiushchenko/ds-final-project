# Predicting San Francisco Fire Department unit availability time based on historical calls for service data.
SF Fire department deals with a range incidents apart from directly fire-related. Depending on incident complexity and type different teams and units are used. Combinations of features effect time required to solve incident. Using this details and time required to provide service I built prediction model for units avaliablility for each call. 
Models can be later used for predicting car sharing services availiablity, logistic companies, resources distribution based on tasks (incidents) as well as task management tool for tasks with not fixed time ranges.
Model is build using CatBoost Regressor (based on Gradient Boost Algorythm).

'Data' folder includes sample dataset, dictionary for features and link to full dataset.
'Scripts' folder includes python code for feature engineering, model pipeline and execution script.
'Notebooks' folder includes jupyter notebooks with models build, cross validations and EDA.

# Prerequisites
- Python 3.6
- pip
- git
- catboost


# Setup
```
$ pip install catboost
$ git clone https://github.com/olgaiushchenko/ds-final-project.git
$ wget https://data.sfgov.org/api/views/nuek-vuh3/rows.csv?accessType=DOWNLOAD
```
To run model from terminal:
```
$ python scripts/model.py
```
You will need to type name and location of file(dataset) to apply model to. Example: 
```
$python scripts/model.py data/dataset.csv
```
