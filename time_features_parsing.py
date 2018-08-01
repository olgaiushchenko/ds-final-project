import pandas as pd
import timeit
import argparse

'''
------- Feature engineering for time columns. -------
cols = a list of column names that should be parse as datetime. 
Includes 7 of 10 date&time cols that will be used in next steps.
Parser block enables to name file to apply script to from terminal.
If enambled, umcomment row above it (12)
A slow way for the same parsing is below.
'''
#df = pd.read_csv('Fire_Dep_Call_20%.csv')
parser = argparse.ArgumentParser(description='Which file to use?')
parser.add_argument('file', metavar='file', type=str)
args = parser.parse_args()
file = args.file

df = pd.read_csv(file)
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

''' 
Slow way to parse datetime
'''
'''
df=pd.read_csv('Fire_Dep_Call_20%.csv', parse_dates=['Call Date', 'Received DtTm', 'Entry DtTm', 'Dispatch DtTm', 
            'Response DtTm', 'On Scene DtTm', 'Transport DtTm', 'Hospital DtTm', 'Available DtTm'],
            infer_datetime_format=True)
'''



'''
to measure time needed to covert to date time use:
import timeit
start_time = timeit.default_timer()
----here goes all the function----
elapsed = timeit.default_timer() - start_time
print('It took: '+ str(elapsed) + ' to run it.')
'''