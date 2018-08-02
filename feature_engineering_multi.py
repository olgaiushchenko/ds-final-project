import pandas as pd
import numpy as np
from time_features import read_datetime
from time_features import new_time_cols

'''
Creating and droping features in columns(no rows involved)
'''

def drop_useless(df):
	''' give column name. In case we use tail csv they are unnamed. Drop useless columns.'''
	df = df.drop(columns=['Call Number','Incident Number', 'Call Date', 'Watch Date',
		'Call Final Disposition', 'Address', 'City', 'Battalion','Station Area', 
		'Box', 'Priority', 'Final Priority', 'Fire Prevention District', 'Supervisor District', 'RowID'], inplace=True)
	#return df


	# if len(df.columns) == 34:
	# 	df.columns = ['Call Number', 'Unit ID', 'Incident Number', 'Call Type', 'Call Date', 
	# 	'Watch Date', 'Received DtTm', 'Entry DtTm', 'Dispatch DtTm', 'Response DtTm', 
	# 	'On Scene DtTm', 'Transport DtTm', 'Hospital DtTm', 'Call Final Disposition', 
	# 	'Available DtTm', 'Address', 'City', 'Zipcode of Incident', 'Battalion', 
	# 	'Station Area', 'Box', 'Original Priority', 'Priority', 'Final Priority', 
	# 	'ALS Unit', 'Call Type Group', 'Number of Alarms', 'Unit Type', 
	# 	'Unit sequence in call dispatch', 'Fire Prevention District', 'Supervisor District', 
	# 	'Neighborhooods - Analysis Boundaries', 'Location', 'RowID']

cols =['Received DtTm', 'Dispatch DtTm', 'Response DtTm','On Scene DtTm', 'Transport DtTm', 
		'Hospital DtTm', 'Available DtTm']

def time_cols(df):
	read_datetime(cols, df)
	new_time_cols(df)


def fill_na_zipcode(df):
	'''
	Create a dict based on neighborhoood-zipcode pairs and fill zipcode N/A from dict
	'''
	if((df['Zipcode of Incident'].nunique()) <= (df['Neighborhooods - Analysis Boundaries'].nunique())):
		zipcodes = df[['Neighborhooods - Analysis Boundaries','Zipcode of Incident']]
		zipcodes = zipcodes[zipcodes['Zipcode of Incident'].notnull()]
		zips= list(zipcodes['Zipcode of Incident'].values)
		nbhds= list(zipcodes['Neighborhooods - Analysis Boundaries'].values)
		if len(zips) == len(nbhds):
			zipcodes_dict=dict(zip(nbhds,zips))

		else: 
			print('Count unique zipcodes != count neighborhooods, something went wrong.')
	else:
		print('More zipcodes than neighborhooods, we need new strategy!')

	df['Zipcode of Incident'] = df['Zipcode of Incident'].fillna(df['Neighborhooods - Analysis Boundaries'].map(zipcodes_dict))
	df['Zipcode of Incident'] = df['Zipcode of Incident'].astype(int)

def original_priority_na(df):
	#'''Randomly fills NA in original priority based on share in whole dataframe'''
	q = df['Original Priority'].value_counts(normalize=True) #counts share of valeus in col w/o N/A
	orig_prio_list = q.index.tolist()  #makes indeces(priorities types) to a list
	orig_prio_shares = q.tolist() #makes values of shares a list
	df['Original Priority'] = df['Original Priority'].fillna(pd.Series(np.random.choice(orig_prio_list, 
		p=orig_prio_shares, size=len(df))))

# def unit_type_dummies(df):
# 	dummies = pd.get_dummies(df['Unit Type'])
#	return pd.concat([df,dummies], axis=1)

def call_group_merge(df):
	def get_group(x):
		if x == 'Medical Incident':
			return 'Medical Incident'
		elif x == 'Structure Fire':
			return 'Structure Fire'
		elif x == 'Alarms':
			return 'Alarms'
		else:
			return 'Other'

	df['Call Type Merged']=df['Call Type'].map(get_group)
	# #df = pd.get_dummies(data=df, columns=['Call Type Merged'])
	# return pd.get_dummies(data=df, columns=['Call Type Merged'])


def call_group_na(df):
	'''
	Filling NA for call type group based on most popular group for each of calls. 
	Stored as dict. For most its 90%+ cases'''
	zx = df[['Call Type', 'Call Type Group']].groupby(['Call Type Group', 'Call Type']).size()
	zx_df = pd.DataFrame(zx)
	zx_df.columns = ['Count']
	zx_df = zx_df['Count'].unstack(level=0)
	q = zx_df.idxmax(axis=1)
	calls = list(q.index)
	groups = list(q.values)
	call_type_dict = dict(zip(calls,groups))
	df['Call Type Group'] = df['Call Type Group'].fillna(df['Call Type'].map(call_type_dict))
	
#dum_list = ['Unit Type', 'Call Type Merged']
def dummies_all(df):
	dum_list = ['Unit Type', 'Call Type Merged']
	for col in dum_list:
		dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
		df[dummies.columns]= dummies

	


# def call_merged_group(df):
# 	df['Medical Type'] = (df['Call Type']== 'Medical Incident')*1
# 	df['Structure Fire Type'] = (df['Call Type']== 'Structure Fire')*1
# 	df['Alarms Type'] = (df['Call Type']== 'Alarms')*1
# 	df['Other Type'] = ((df['Call Type'] != 'Medical Incident') & (df['Call Type'] != 'Structure Fire') & (df['Call Type'] != 'Alarms'))*1
#     