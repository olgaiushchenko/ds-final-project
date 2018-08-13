import pandas as pd
import numpy as np
import time_features


'''
------- Feature engineering for whole dataset. -------
Includes creating features and applying time_features and drop_invalid rows.
'''

def time_cols(df):
	'''
	Applying time_features script to enable timedate features.
	'''
	time_features.read_datetime(df)
	time_features.new_time_cols(df)
	time_features.fix_negative_values(df)


def fill_na_zip_nbhd(df):
	'''
	Create a dict based on neighborhoood-zipcode pairs and fill zipcode N/A from dict.
	Create a dict based on zipcode-neighborhoood pairs and fill neighborhoood N/A from dict.
	'''
	zipcodes = df[['Neighborhooods - Analysis Boundaries','Zipcode of Incident']]
	zipcodes = zipcodes[zipcodes['Zipcode of Incident'].notnull()]
	zips = list(zipcodes['Zipcode of Incident'].values)
	nbhds = list(zipcodes['Neighborhooods - Analysis Boundaries'].values)
	if len(zips) == len(nbhds):
		zipcodes_dict = dict(zip(nbhds,zips))
		nbhds_dict = dict(zip(zips,nbhds))

	df['Neighborhooods - Analysis Boundaries'] = df['Neighborhooods - Analysis Boundaries'].fillna(df['Zipcode of Incident'].map(nbhds_dict))
	df['Zipcode of Incident'] = df['Zipcode of Incident'].fillna(df['Neighborhooods - Analysis Boundaries'].map(zipcodes_dict))
	df['Zipcode of Incident'] = df['Zipcode of Incident'].astype(int)


def original_priority_na(df):
	'''
	Randomly fills NA in original priority based on share in whole dataframe.
	'''
	q = df['Original Priority'].value_counts(normalize=True) #counts share of valeus in col w/o N/A
	orig_prio_list = q.index.tolist()  #makes indeces(priorities types) to a list
	orig_prio_shares = q.tolist() #makes values of shares a list
	df['Original Priority'] = df['Original Priority'].fillna(pd.Series(np.random.choice(orig_prio_list, 
		p=orig_prio_shares, size=len(df))))


def call_group_na(df):
	'''
	Filling NA for call type group based on share in whole dataframe.
	'''
	w = df['Call Type Group'].value_counts(normalize=True) #counts share of values in col w/o N/A
	call_types_list = w.index.tolist()  #makes indeces(priorities types) to a list
	call_types_shares = w.tolist() #makes values of shares a list
	df['Call Type Group'] = df['Call Type Group'].fillna(pd.Series(np.random.choice(call_types_list, p=call_types_shares, size=len(df))))
    

def get_location(df):
	'''
	Extracting location coordinates from a tuple. Storing as absolute value to avoid 
	negative impact of predicted values.
	'''
	df['Location'] = df['Location'].astype(tuple)
	locations = df['Location'].str[1:-1].str.split(',', expand=True).astype(float)
	df[locations.columns] = abs(locations)


def historical_means(df):
	'''
	Counting historical mean for three features based on past.Never includes future periods.
	'''
	df['Unit_Type_Rolling'] = df.groupby('Unit Type')['Respond to Available'].rolling(10,min_periods=1).mean().reset_index(0,drop=True)
	df['Call_Type_Rolling'] = df.groupby('Call Type')['Respond to Available'].rolling(10,min_periods=1).mean().reset_index(0,drop=True)
	df['Unit_ID_Rolling'] = df.groupby('Unit ID')['Respond to Available'].rolling(10,min_periods=1).mean().reset_index(0,drop=True)


def clean_outliers(df):
	'''
	Drop rows with outlier values.
	'''

	df = df[(df['Respond to Available'] <= 360) & (df['Respond to Available']>5.1)]
	return df
   
    
    
def drop_useless(df):
	''' 
	Drop useless columns.
	'''
	df = df.drop(columns=['Call Number', 'Incident Number', 'Call Date', 'Watch Date', 
			'Received DtTm', 'Entry DtTm', 'Dispatch DtTm','Response DtTm', 
			'On Scene DtTm','Transport DtTm','Hospital DtTm', 'Call Final Disposition', 
			'Available DtTm', 'Supervisor District', 'Call Type Group','Month', 'WeekDay', 
			'Fire Prevention District','Address', 'City', 'Priority', 'Final Priority', 
			'Location', 'RowID', 'Battalion', 'ALS Unit'], errors='ignore', inplace=True)

def clean_na_rows(df):
	'''
	Drop any row containing NA for model performance. 
	Should be applied as last action in feature engineering to avoid 
	dropping potentially useful rows.
	'''
	df.dropna(how='any', inplace=True) 
	df.reset_index(drop=True, inplace=True)

def fix_box(df):
	'''
	Replace value 'AI02' with a numeric and store it as int so model takes this column 
	input as numeric. 
	'''
	if 'AI02' in df['Box'].values:
		df[df['Box'] == 'AI02'] = 0  
		df['Box'] = df['Box'].astype(int)


def run_features(df):
	'''
	Running all the functions from this script.
	'''
	time_cols(df)
	fill_na_zip_nbhd(df)
	original_priority_na(df)
	call_group_na(df)
	get_location(df)
	historical_means(df)
	df = clean_outliers(df)
	drop_useless(df)
	clean_na_rows(df)
	fix_box(df)
	return df
