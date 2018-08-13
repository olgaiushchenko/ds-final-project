import pandas as pd

'''
------- Feature engineering for time columns. -------
cols = a list of column names that should be parsed as datetime. 
Includes only columns that will be used in next steps.
 Two more are processed as part of create_y script 
'''


def read_datetime(df):
	'''
	cols = a list of column names that should be parse as datetime. 
	df = pandas dataframe to apply this parsing.
	'''
	cols =['Received DtTm', 'Dispatch DtTm', 'Response DtTm', 'Available DtTm']
	for col in cols:
		df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)


def new_time_cols(df):
	'''
	Respond to Availiable = time from moment unit accepts case till it is avaliable 
	for new case. Count time in minutes.
	Call to Dispatch = time from Call Received by 911 to the time unit is dispatched.
	Total count in minutes.
	Hospital or Transport = column to indicate if unit had transport or hospital part.
	Month = Month of call received. Values range [1,12].
	WeekDay = Day of the week of call received. 0 = Sunday. Value Range [0,6].
	Hours = Hour of the call received. Range [0:23].
	Minutes = Minute of the call received. Range [0:59].
	'''
	df['Respond to Available'] = df['Available DtTm']-df['Response DtTm']
	df['Respond to Available'] = df['Respond to Available'].map(lambda t: t.total_seconds()/60)

	df['Call to Dispatch'] = df['Dispatch DtTm']-df['Received DtTm']
	df['Call to Dispatch'] = df['Call to Dispatch'].map(lambda t: t.total_seconds()/60)
	df['Hospital or Transport'] = (~(df['Transport DtTm'].isna() & df['Hospital DtTm'].isna()))
	df['Hospital or Transport'] = df['Hospital or Transport'].astype(bool)

	df['Month']=df['Received DtTm'].dt.month
	df['WeekDay']=df['Received DtTm'].dt.weekday
	df['Hours']=df['Received DtTm'].dt.hour
	df['Minutes']=df['Received DtTm'].dt.minute


def fix_negative_values(df):
	'''
	Eliminate negative time values that occur by mistake of input data.
	'''
	df['Respond to Available'] = df['Respond to Available'].map(lambda x: max(x,0))
	df['Call to Dispatch'] = df['Call to Dispatch'].map(lambda x: max(x,0))