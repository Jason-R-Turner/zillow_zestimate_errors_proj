#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import sklearn
import env
import os
from sklearn.model_selection import train_test_split


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Function allows user to access Codeup database using their own 
    credentials stored in  their env.py file
    '''
    
# Returns with correct address/password combinat to access the database
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'



def new_zillow_data():
    '''
    SQL query that joins three other tables to properties_2017
    '''
    
    sql_query = '''
                SELECT * FROM properties_2017
                right join predictions_2017 using (parcelid)
                join propertylandusetype using (propertylandusetypeid)
                where propertylandusedesc = "Single Family Residential" OR "Inferred Single Family Residential"
                '''
    
# Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
# Returns the called dataframe
    return df



def get_zillow_data():
    '''
    Function allows user to access zillow_data from Codeup database and write it\n
    to a csv file then returns the dataframe.
    '''
    
# if statement that checks if there's already a .csv file to use 
    if os.path.isfile('zillow.csv'):
        
# If csv file exists read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
# Alternative if no csv file found then
    else:
        
# Read fresh data from db into a DataFrame
        df = new_zillow_data()
        
# Cache data for local use
        df.to_csv('zillow.csv')

# Returns requested df
    return df



def handle_nulls(df):
    '''
    Gets rid of the rows with any null values and returns a new null-free df
    '''
    
# drops the rows with any null values and returns a new null-free df
    df = df.dropna()
    
    
    return df



def float_to_int(df):
    '''
    Converts our fips, bedrooms, calculatedfinishedsquarefeet, lotsizesquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
    '''
# converts our fips, bedrooms, calculatedfinishedsquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
# Use pandas.to_datetime() to convert string to datetime format
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    df["lotsizesquarefeet"] = df["lotsizesquarefeet"].astype(int)
    df["regionidcity"] = df["regionidcity"].astype(int)
    df["regionidzip"] = df["regionidzip"].astype(int)
    df["structuretaxvaluedollarcnt"] = df["structuretaxvaluedollarcnt"].astype(int)
    df["landtaxvaluedollarcnt"] = df["landtaxvaluedollarcnt"].astype(int)
    df["censustractandblock"] = df["censustractandblock"].astype(int)
    
    return df

def convert_date(df):
    df["transactiondate"] = pd.to_datetime(df["transactiondate"])
    
    return df


def drop_cols(df):
    '''
    Drops unnecessary columns mostly due to practically duplicate information
    'propertylandusetypeid' and 'assessmentyear' since there's only 1 value, for single family
    homes 'roomcnt' seems to be missing data which are represented by '0'
    '''
    cols_to_drop = ['propertylandusetypeid', 'id', 'id.1', 'calculatedbathnbr', 'fullbathcnt', 'finishedsquarefeet12', 'regionidcounty', 'roomcnt', 'assessmentyear', 'propertylandusedesc']
    df = df.drop(columns=cols_to_drop, axis=1)
    return df


def clean_zillow(df):
    '''
    Groups our functions used to clean up our data into a single function for ease of use.
    '''
    df.drop_duplicates(inplace=True)
    df = drop_cols(df)
    df = handle_nulls(df)
    df = float_to_int(df)
    df = convert_date(df)
    df['county'] = df['fips'].astype(str)
    
    return df
#     df['county'] = df['county'].replace(['6037.0', '6059.0', '6111.0'], ['Los Angeles', 'Orange', 'Ventura'])


def split_zillow(df):
    '''
    Takes our df and splits it into train, validate, and test dfs for exploration, fitting, validation, and testing
    '''
    
# splits the full data set 80/20 into train and test dataframes stratified 
# around taxvaluedollarcnt, the target variable, using the train_test_split function
    train, test = train_test_split(df, 
                               train_size = 0.80, 
                               stratify = df.fips, 
                               random_state=2468)

# splits the train dataframe 60/40 into the new train and validate dataframes
# they're stratified around taxvaluedollarcnt again using the train_test_split function
    train, validate = train_test_split(train,
                                    train_size = 0.60,
                                    stratify = train.fips,
                                    random_state=2468)
    
# returns the three dataframes we'll use for training, validation, and testing
    return train, validate, test




def wrangle_zillow():
    '''
    Function that acquires zillow data using the new_zillow_data function and 
    caches it, as a csv file, if there isn't already a local copy
    '''
    df = get_zillow_data()
    df = clean_zillow(df)
    train, validate, test = split_zillow(df)
    
    return train, validate, test




def scale_zillow(train, validate, test,
                 cols_to_scale = ['logerror', 'bedroomcnt', 'bathroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'structuretaxvaluedollarcnt', 'taxvaluedollarcnt', 'landtaxvaluedollarcnt', 'taxamount']):
    '''
    Accepts train, validate, and test as inputs from split data then returns scaled versions for each one using Robust Scaler.
    '''
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    scaler = sklearn.preprocessing.RobustScaler()

    scaler.fit(train[cols_to_scale])
    
    train_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(train[cols_to_scale]), columns=train[cols_to_scale].columns.values).set_index([train.index.values])
                                                  
    validate_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(validate[cols_to_scale]), columns=validate[cols_to_scale].columns.values).set_index([validate.index.values])
    
    test_scaled[cols_to_scale] = pd.DataFrame(scaler.transform(test[cols_to_scale]), columns=test[cols_to_scale].columns.values).set_index([test.index.values])
    
    return train_scaled, validate_scaled, test_scaled


def remove_columns(df, cols_to_remove):  
    df = df.drop(columns=cols_to_remove)
    return df


def get_upper_outliers(s, k):
    '''
    Given a series and a cutoff value, k, returns the upper outliers for the
    series.

    The values returned will be either 0 (if the point is not an outlier), or a
    number that indicates how far away from the upper bound the observation is.
    '''
    q1, q3 = s.quantile([.25, .75])
    iqr = q3 - q1
    upper_bound = q3 + k * iqr
    return s.apply(lambda x: max([x - upper_bound, 0]))

def add_upper_outlier_columns(df, k):
    '''
    Add a column with the suffix _outliers for all the numeric columns
    in the given dataframe.
    '''

    for col in df.select_dtypes('number'):
        df[col + '_outliers'] = get_upper_outliers(df[col], k)

    return df


def percentage_dropper(df):
    df = df.loc[:, df.isnull().mean() < .02]
    return df
# bathroomcnt_outliers
# bedroomcnt_outliers
# calculatedfinishedsquarefeet_outliers
# lotsizesquarefeet_outliers
# structuretaxvaluedollarcnt_outliers
# taxvaluedollarcnt_outliers
# landtaxvaluedollarcnt_outliers
# taxamount_outliers

