#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import env
import os
from sklearn.model_selection import train_test_split


# In[2]:


def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''
    Function allows user to access Codeup database using their own 
    credentials stored in  their env.py file
    '''
    
# Returns with correct address/password combinat to access the database
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


# In[3]:


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


# In[4]:


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


# In[5]:


def handle_nulls(df):
    '''
    Gets rid of the rows with any null values and returns a new null-free df
    '''
    
# drops the rows with any null values and returns a new null-free df
    df = df.dropna()
    
    
    return df


# In[6]:


def float_to_int(df):
    '''
    Converts our fips, bedrooms, calculatedfinishedsquarefeet, lotsizesquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
    '''
# converts our fips, bedrooms, calculatedfinishedsquarefeet, taxvaluedollarcnt, and yearbuilt from floats to integers
    df["fips"] = df["fips"].astype(int)
    df["yearbuilt"] = df["yearbuilt"].astype(int)
    df["bedroomcnt"] = df["bedroomcnt"].astype(int)
    df["taxvaluedollarcnt"] = df["taxvaluedollarcnt"].astype(int)
    df["calculatedfinishedsquarefeet"] = df["calculatedfinishedsquarefeet"].astype(int)
    df["lotsizesquarefeet"] = df["lotsizesquarefeet"].astype(int)
    
    return df


# In[7]:


def clean_zillow(df):
    '''
    Groups our functions used to clean up our data into a single function for ease of use
    '''
    df.drop_duplicates(inplace=True)
    df = handle_nulls(df)
    df = float_to_int(df)
    df['county'] = df['fips'].astype(str)
    df['county'] = df['county'].replace(['6037.0', '6059.0', '6111.0'], ['Los Angeles', 'Orange', 'Ventura'])
    
    return df


# In[8]:


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


# In[9]:


def wrangle_zillow():
    '''
    Function that acquires zillow data using the new_zillow_data function and 
    caches it, as a csv file, if there isn't already a local copy
    '''
    df = get_zillow_data()
    df = clean_zillow(df)
    train, validate, test = split_zillow(df)
    
    return train, validate, test


# In[10]:


def scale_zillow(train, validate, test,
                 cols_to_scale = ['bedroomcnt', 'bathroomcnt', 'calculatedfinishedsquarefeet', 'lotsizesquarefeet', 'taxvaluedollarcnt']):
    '''
    Accepts train, validate, and test as inputs from split data then returns scaled versions for each one
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


cols_to_drop = 'parcelid', 'id', 


cols_to_convert = 'TBD' 

