
import pandas as pd
import numpy as np
import create_y
import feature_engineering_multi
from sklearn.model_selection import train_test_split
from catboost import Pool, CatBoostRegressor, cv
from sklearn.metrics import mean_squared_log_error, mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error, median_absolute_error
import pickle
import argparse


#FILE PARSER BLOCK TO EXECUTE FROM TERMINAL
parser = argparse.ArgumentParser(description='Which dataset to use?')
parser.add_argument('file', metavar='file', type=str)
args = parser.parse_args()
file = args.file

# READ DATA SET
df = pd.read_csv(file)
#df = pd.read_csv('data/Fire_Dep_Call_50%.csv')

#CREATE Y COLUMN AND APPLY FEATURE ENGINEERING

df_full = feature_engineering_multi.run_features(df)

#SPLIT X AND Y
y = df_full['Respond to Available']
X = df_full.drop(columns=['Respond to Available'])

#SPLIT INTO TRAIN AND TEST
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, shuffle=False)

#MODEL
cat_features=[
    0,
    1,
    3,
    5,
    7,
    9
]

train_pool = Pool(X_train, y_train, cat_features=cat_features)
test_pool = Pool(X_test, cat_features=cat_features)

print('Pools create, working on fitting.')
model = CatBoostRegressor(iterations=200, depth=16,learning_rate=0.1, one_hot_max_size=3)
model.fit(train_pool)

print('Predicting y_test values')
pred = model.predict(test_pool)
pred[pred < 0] = 0 #eliminated false negatives with 0


#SCORES
mae = mean_absolute_error(y_test,pred)
mse = mean_squared_error(y_test,pred)
rmse = model.score(test_pool, y_test)
r2_score_val = r2_score(y_test,pred)

print ('Mean absolute error: ', str(mae))
print ('Mean squared error: ', str(mse))
print ('Root squared eroor: ', str(rmse))
print ('Score of determination: ', str(r2_score_val))




#PICKLE THE MODEL
with open('model_catboost.pkl', 'wb') as f:
	# Write the model to a file.
	pickle.dump(model, f)



