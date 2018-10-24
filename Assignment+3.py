
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[3]:

import pandas as pd
from functools import reduce

def answer_one():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols=[2,3,4,5], names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],  na_values=["..."] , encoding='utf8' )
    energy['Energy Supply'] *=1000000
    energy['Country'] = energy['Country'].str.replace(r"\(.*\)","").str.replace("\d","").replace({'Republic of Korea': 'South Korea', 'United States of America':'United States' , 'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom','China, Hong Kong Special Administrative Region': 'Hong Kong'})
    energy['Country']=energy['Country'].str.strip()
    
    GDP = pd.read_csv('world_bank.csv', skiprows=4,encoding='utf8' )
    GDP.rename(columns={'Country Name':'Country'}, inplace=True)
    GDP['Country'].replace({"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"}, inplace=True) 

    ScimEn = pd.read_excel('scimagojr-3.xlsx',encoding='utf8' )

   
    Mix = [energy, GDP, ScimEn]
# MixDF = pd.merge(energy, GDP,how='outer',on=['Country'])
    #MixDF = reduce(lambda left,right: pd.merge(left,right,on=['Country'],how='outer'), Mix)
    MixDF = pd.merge(pd.merge(energy, GDP,how='outer',on=['Country']),ScimEn,how='outer',on=['Country'])
    MixDF.set_index('Country', inplace = True)
    return MixDF[['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']][MixDF['Rank']<16]


answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[1]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[128]:

def answer_two():
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, skipfooter=38, usecols=[2,3,4,5], names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'],  na_values=["..."] )
    energy['Energy Supply'] *=1000000
    energy['Country'] = energy['Country'].str.replace(r"\(.*\)","").str.replace("\d","").replace({'Republic of Korea': 'South Korea', 'United States of America':'United States' , 'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom','China, Hong Kong Special Administrative Region': 'Hong Kong'})

    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    GDP.rename(columns={'Country Name':'Country'}, inplace=True)
    GDP['Country'].replace({"Korea, Rep.": "South Korea","Iran, Islamic Rep.": "Iran","Hong Kong SAR, China": "Hong Kong"}, inplace=True) 

    ScimEn = pd.read_excel('scimagojr-3.xlsx')

   
    Mix = [energy, GDP, ScimEn]
    union1 = pd.merge(energy, GDP,how='outer',on=['Country'])
    union2 = pd.merge(GDP, ScimEn,how='outer',on=['Country'])
    union3 = pd.merge(ScimEn, energy,how='outer',on=['Country'])
    union = union1 +union2+ union3
#    union = pd.merge(pd.merge(energy, GDP,how='outer',on=['Country']),ScimEn,how='outer',on=['Country'])
    inter1 = pd.merge(energy, GDP,how='inner',on=['Country'])
    inter2 = pd.merge(GDP, ScimEn,how='inner',on=['Country'])
    inter3 = pd.merge(energy,ScimEn,how='inner',on=['Country'])
    inter = inter1+ inter2+inter3   
# inter = pd.merge(pd.merge(energy, GDP,how='inner',on=['Country']),ScimEn,how='outer',on=['Country'])
    return len(union)-len(inter)
answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[95]:

def answer_three():
    Top15 = answer_one()
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    avgGDP = Top15[years].mean(axis=1, skipna =True).sort_values(ascending=False).rename('avgGDP')
    return avgGDP
answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[96]:

def answer_four():
    Top15 = answer_one()
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    avgGDP = Top15[years].mean(axis=1, skipna =True).sort_values(ascending=False).rename('avgGDP')
    idx = avgGDP.index[5]
    return Top15.loc[idx]['2015'] - Top15.loc[idx]['2006']
answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[97]:

import numpy as np
def answer_five():
    Top15 = answer_one()
    return (Top15['Energy Supply per Capita']).mean()
answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[98]:

def answer_six():
    Top15 = answer_one()
    return (Top15['% Renewable'].idxmax(), Top15['% Renewable'].max())

answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[99]:

def answer_seven():
    Top15 = answer_one()
    Top15['Ratio']=Top15['Self-citations']/Top15['Citations']
    return (Top15['Ratio'].idxmax(), Top15['Ratio'].max() )

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[100]:

def answer_eight():
    Top15 = answer_one()
    Top15['Capita']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
    
    return Top15['Capita'].sort_values(ascending=False).index[2]

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[106]:

def answer_nine():
    Top15 = answer_one()
    Top15['Capita']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['DocXpers'] = Top15['Citable documents']/Top15['Capita']
    #That calculates the correlation between your two columns 'Citable docs per Capita' and 'Energy Supply per Capita'
    return Top15['DocXpers'].corr(Top15['Energy Supply per Capita'])
answer_nine()


# In[11]:




# In[12]:

#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[110]:

def answer_ten():
    Top15 = answer_one()
    Top15.sort_values(by = "Rank", inplace = True)
    mediaval = Top15['% Renewable'].median()
    Top15['HighRenew'] = Top15['% Renewable']>mediaval 
    return Top15['HighRenew'].apply(lambda x: 1 if x else 0)
answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[124]:

import numpy as np
def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15['Capita']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
    return Top15.groupby(by = ContinentDict)['Capita'].agg({'size':np.size, 'sum': np.sum, 
                                                            'mean':np.mean, 'std':np.std})
answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[125]:

import pandas as pd
import numpy as np
def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    bins = pd.cut(Top15["% Renewable"], 5) #Cut % Renewable into 5 bins
    return Top15.groupby([ContinentDict, bins]).size()
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[126]:

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    return Top15['PopEst'].apply(lambda x: '{0:,}'.format(x))
answer_thirteen() 


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[19]:




# In[20]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!


# In[ ]:



