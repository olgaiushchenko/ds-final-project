import pandas as pd

'''
------- Feature engineering for time columns. -------
cols = a list of column names that should be parse as datetime. 
Includes 7 of 10 date&time cols that will be used in next steps.
'''
df = pd.read_csv('Fire_Dep_Call_20%.csv')
cols =['Received DtTm', 'Dispatch DtTm', 'Response DtTm','On Scene DtTm', 'Transport DtTm', 
		'Hospital DtTm', 'Available DtTm']

def read_datetime(cols,df):
	for col in cols:
		df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)

read_datetime(cols, df)


'''
Call to Dispatch = time from Call Received by 911 to the time unit is dispatched
Respond to On Scene = time from moment unit accepts case till they get to the scene
Respond to Availiable = time from moment unit accepts case till it is avaliable for new case
On Scene to Availiable = time from moment is on scene till is avaliable for new case
Total Call to Availiable = total time from call till unit is ready for new case
Hospital or Transport = column to indicate if unit had transport or hospital part
'''
def new_time_cols(df):
	df['Call to Dispatch'] = df['Dispatch DtTm']-df['Received DtTm']
	df['Respond to On Scene'] = df['On Scene DtTm']-df['Response DtTm']
	df['Respond to Available'] = df['Available DtTm']-df['Response DtTm']
	df['On Scene to Available'] = df['Available DtTm']-df['On Scene DtTm']
	df['Total Call to Available'] = df['Available DtTm']-df['Received DtTm']
	df['Hospital or Transport'] = ((df['Transport DtTm'].isna()) | (df['Hospital DtTm'].isna()))*1
