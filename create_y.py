import pandas as pd

'''
------- Feature engineering for label column. -------
Respond to Availiable = time from moment unit accepts case till it is avaliable 
for new case.
'''

cols =['Response DtTm', 'Available DtTm']
def read_datetime(cols,df):
	'''
	cols = a list of column names that should be parse as datetime. 
	df = pandas dataframe to apply this parsing.
	'''
	for col in cols:
		df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)


def new_time_cols(df):
	'''
	Respond to Availiable = time from moment unit accepts case till it is avaliable 
	for new case. Count time in minutes.
	'''
	df['Respond to Available'] = df['Available DtTm']-df['Response DtTm']
	df['Respond to Available'] = df['Respond to Available'].map(lambda t: t.total_seconds()/60)

def fix_negative_values(df):
	'''
	Eliminate negative time values from y column, that appear there by mistake of input data.
	'''
	df['Respond to Available'] = df['Respond to Available'].map(lambda x: max(x,0))


def all_y_col(df):
	'''
	Running all the functions to create y column in one.
	'''
	read_datetime(cols,df)
	new_time_cols(df)
	fix_negative_values(df)