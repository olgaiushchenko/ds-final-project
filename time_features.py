import pandas as pd

'''
------- Feature engineering for time columns. -------
cols = a list of column names that should be parse as datetime. 
Includes 7 of 10 date&time cols that will be used in next steps.
'''
#df = pd.read_csv('Fire_Dep_Call_20%.csv')
cols =['Received DtTm', 'Dispatch DtTm']

def read_datetime(cols,df):
	for col in cols:
		df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)


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
		
	def get_sec(time_str):
 		return time_str.total_seconds()

	df['Call to Dispatch'] = df['Call to Dispatch'].map(get_sec)

	df['Hospital or Transport'] = (~(df['Transport DtTm'].isna() & df['Hospital DtTm'].isna())).astype('int')

	df['Month']=df['Received DtTm'].dt.month
	df['WeekDay']=df['Received DtTm'].dt.weekday
	df['Hours']=df['Received DtTm'].dt.hour
	df['Minutes']=df['Received DtTm'].dt.minute


def fix_negative_values(df):
	def get_max(x):
		return max(x,0)
	df['Call to Dispatch'] = df['Call to Dispatch'].map(get_max)
	

def intervals(df):
	df['Minutes']=df['Received DtTm'].dt.minute
		
	def min_intervals(x):
		if x < 15:
			return '0-14'
		if x < 30:
			return '15-29'
		if x < 45:
			return '30-44'
		else:
			return '45-59'
	df['Minutes intervals'] = df['Minutes'].map(min_intervals)
