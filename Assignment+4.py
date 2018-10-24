
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[12]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[13]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[53]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''

    
    #uni = pd.read_csv('university_towns.txt',error_bad_lines=False, names=["State", "RegionName"],encoding='utf8' )
    #uni["RegionName"]=uni["State"]
    #state_index = uni['State'].str.contains('edit')
    #uni["State"]= uni[state_index]
    #uni["State"]= uni["State"].str.replace(r"\[.*\]","").str.replace("\d","").fillna( method='ffill')
    #uni['RegionName'] = uni['RegionName'].str.replace(r"\[.*\]","").str.replace("\d","")
    #uni =uni[uni['RegionName'] != uni['State']]
    #uni["RegionName"] = list(map(lambda x: x.split("(")[0].rstrip(),uni["RegionName"]))
    #uni["State"]= uni["State"].str.replace(r'\\n','')
    #uni.reset_index(inplace=True,drop=True)
    #return uni
    
    text_file = open("university_towns.txt")
    # Make a dictionary with key as the line number of the states that
    # have "[edit]" after them and value as state name itself without "[edit]"
    State = {idx: lines.strip().replace("[edit]", "")
             for idx,lines in enumerate(text_file) if "edit" in lines}
    # Convert the dictionary to a series
    State = pd.Series(State)
    # Create a data frame with one column as Region names
    university_towns = pd.read_csv("university_towns.txt", sep = "\n",
                                   header = None, names=["RegionName"])
    # Add the above series as a column in dataframe
    university_towns["State"] = State
    # Forward fill for the "State" Column
    university_towns = university_towns.fillna(method = 'ffill')
    # Drop all rows that has state names in the column "RegionName"
    university_towns = university_towns.drop(State.index)
    # Edit the Region names to get rid of everything except the names of the towns
    university_towns["RegionName"] = list(map(lambda x: x.split("(")[0].rstrip(),
                                              university_towns["RegionName"]))
    return university_towns    

get_list_of_university_towns()


# In[48]:

import pandas as pd
import numpy as np
def get_recession_start():
    '''From Bureau of Economic Analysis, US Department of Commerce, the GDP over time of the United States in 
    current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file gdplev.xls.
    For this assignment, only look at GDP data from the first quarter of 2000 onward.
    Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''

    GDP = pd.read_excel('gdplev.xls',skiprows=7, usecols=[4,6], names = ['Quarterly','GDP in billions of chained 2009 dollars'],encoding='utf8' )
    # Set Quarters as the index to the dataframe
    GDP = GDP[GDP['Quarterly']>='2000q1']
    #GDP.set_index("Quarterly", inplace = True)

    GDP['GDP in billions of chained 2009 dollars']= pd.to_numeric(GDP['GDP in billions of chained 2009 dollars'])

    quarters = []
    for i in range(len(GDP) - 2):
        if (GDP.iloc[i][1] > GDP.iloc[i+1][1] > GDP.iloc[i+2][1]):
            quarters.append(GDP.iloc[i+1][0])
    return quarters[0]

get_recession_start()


# In[49]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=7, usecols=[4,6], names = ['Quarterly','GDP in billions of chained 2009 dollars'],encoding='utf8' )
    GDP = GDP[GDP['Quarterly']>='2008q3']
    recession_end = []
    for i in range(len(GDP)- 2):
        if (GDP.iloc[i+2][1] > GDP.iloc[i+1][1] > GDP.iloc[i][1]):
            recession_end.append(GDP.iloc[i+2][0])
    return recession_end[0]
get_recession_end()


# In[50]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=7, usecols=[4,6], names = ['Quarterly','GDP in billions of chained 2009 dollars'],encoding='utf8' )
    GDP = GDP[GDP['Quarterly']>='2008q3'] 
    GDP = GDP[GDP['Quarterly']<='2009q4']
    GDP.set_index("Quarterly", inplace = True)
    return GDP['GDP in billions of chained 2009 dollars'].argmin()
get_recession_bottom()


# In[80]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    # Use this dictionary to map state names to two letter acronyms
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}  
    house = pd.read_csv('City_Zhvi_AllHomes.csv', usecols=[1,2, *range(63, 251)],encoding='utf8' )
    #use the states dictionary provided at the beginning of the notebook to map the column State values from abbreviations to names.
    house['State'] = house['State'].map(states)
    #set the columns ['State','RegionName'] as index of housing
    house.set_index(["State","RegionName"], inplace=True)
    #convert the column names from strings to date-time
    house.columns = pd.to_datetime(house.columns)
    #ressample= Convenience method for frequency conversion and resampling of time series
    #Q resample the columns as a quarterand take the mean of that
    house = house.resample('Q',axis=1).mean()
    #make sure you convert the column names from date-time back to strings as per the docstring,
    house = house.rename(columns=lambda x: str(x.to_period('Q')).lower())
    return house
    
convert_housing_data_to_quarters()


# In[82]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    recession_start = get_recession_start()
    recession_bottom = get_recession_bottom()
    university_towns = get_list_of_university_towns()
    newhousedata = convert_housing_data_to_quarters().copy()
    #Run a t-test to compare the ratio of the mean price of houses in university towns 
    newhousedata['PriceRatio'] = newhousedata[recession_start].div(newhousedata[recession_bottom])
    #To test the hypothesis (University towns have their mean housing prices less affected by recessions), 
    #we need to separate the university towns from non_university towns in hdf

    newhousedata.reset_index(inplace=True)

    unitown = pd.merge(university_towns,newhousedata,how='inner',on=['State','RegionName'])
    newhousedata.set_index(['State','RegionName'], inplace = True)
    unitown.set_index(['State','RegionName'], inplace = True)
    nonunitown = newhousedata.copy()
    nonunitown.subtract(unitown,fill_value=0)
    unitown=unitown.dropna()
    nonunitown = nonunitown.dropna()
    #we run the ttest on the price ratio column of each group
    tstat, p = tuple(ttest_ind(unitown['PriceRatio'], nonunitown['PriceRatio']))
    
    different = p < 0.05
    result = tstat < 0
    def better():
        if nonunitown['PriceRatio'].mean() < unitown['PriceRatio'].mean():
            return 'non-university town'
        else:
            return 'university town'
    return (different, p, better())
   # data = convert_housing_data_to_quarters().copy()
  #  data = data.loc[:,'2008q3':'2009q2']
#  data = data.reset_index()
  #  def price_ratio(row):
  #      return (row['2008q3'] - row['2009q2'])/row['2008q3']
    
   # data['up&down'] = data.apply(price_ratio,axis=1)
    #uni data 
    
  #  unitown = get_list_of_university_towns()['RegionName']
  #  unitown = set(unitown)

  #  def is_uni_town(row):
        #check if the town is a university towns or not.
   #     if row['RegionName'] in uni_town:
    #        return 1
    #    else:
       #     return 0
    #data['is_uni'] = data.apply(is_uni_town,axis=1)
    
    
    #not_uni = data[data['is_uni']==0].loc[:,'up&down'].dropna()
    #is_uni  = data[data['is_uni']==1].loc[:,'up&down'].dropna()
    #def better():
     #   if not_uni.mean() < is_uni.mean():
     #       return 'non-university town'
      #  else:
        #    return 'university town'
    #p_val = list(ttest_ind(not_uni, is_uni))[1]
    #result = (True,p_val,better())
    #return result
    

run_ttest()


# In[ ]:




# In[ ]:



