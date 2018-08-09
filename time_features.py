import pandas as pd

'''
------- Feature engineering for time columns. -------
cols = a list of column names that should be parsed as datetime. 
Includes only columns that will be used in next steps.
 Two more are processed as part of create_y script 
'''

cols =['Received DtTm', 'Dispatch DtTm']

def read_datetime(cols,df):
	'''
	cols = a list of column names that should be parse as datetime. 
	df = pandas dataframe to apply this parsing.
	'''
	for col in cols:
		df[col] = pd.to_datetime(df[col],format='%m/%d/%Y %I:%M:%S %p', infer_datetime_format=True)


def new_time_cols(df):
	'''
	Call to Dispatch = time from Call Received by 911 to the time unit is dispatched.
	Total count in minutes.
	Hospital or Transport = column to indicate if unit had transport or hospital part.
	Month = Month of call received. Values range [1,12].
	WeekDay = Day of the week of call received. 0 = Sunday. Value Range [0,6].
	Hours = Hour of the call received. Range [0:23].
	Minutes = Minute of the call received. Range [0:59].
	'''

	df['Call to Dispatch'] = df['Dispatch DtTm']-df['Received DtTm']
	df['Call to Dispatch'] = df['Call to Dispatch'].map(lambda t: t.total_seconds()/60)
	df['Hospital or Transport'] = (~(df['Transport DtTm'].isna() & df['Hospital DtTm'].isna()))

	df['Month']=df['Received DtTm'].dt.month
	df['WeekDay']=df['Received DtTm'].dt.weekday
	df['Hours']=df['Received DtTm'].dt.hour
	df['Minutes']=df['Received DtTm'].dt.minute


def fix_negative_values(df):
	'''
	Eliminate negative time values that occur due to 
	
	'''
	def get_max(x):
		return max(x,0)
	df['Call to Dispatch'] = df['Call to Dispatch'].map(get_max)
	df['Respond to On Scene'] =df['Respond to On Scene'].map(get_max)
	df['On Scene to Available']= df['On Scene to Available'].map(get_max)
	

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


def time_dummies(df):
	dum_list = ['Month', 'WeekDay', 'Hours', 'Minutes intervals']
	for col in dum_list:
		dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
		df[dummies.columns]= dummies