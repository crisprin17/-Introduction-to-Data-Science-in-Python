import pandas as pd
census_df = pd.read_csv('census.csv')
census_df.head()

#Q5: Which state has the most counties in it? 
def answer_five():
    unique_counties = census_df[census_df['SUMLEV'] == 50].groupby('STNAME')['COUNTY'].nunique()#return number of unique element in the column county,where all the county are groupedfor each state
    return unique_counties.argmax()
 #Sol = 'Texas'   
 
 #Q6: Only looking at the three most populous counties for each state, what are the three most populous states
 #(in order of highest population to lowest population)? Use CENSUS2010POP.
 def answer_six():
    # apply function let you apply just about any function on all the values in a column.
    unique_counties = census_df[census_df['SUMLEV'] == 50].groupby('STNAME')['CENSUS2010POP'].apply(lambda x: x.nlargest(3).sum()).nlargest(3)
    return list(unique_counties.index)
 #Sol: ['California', 'Texas', 'Illinois']
 
 #Q7:Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
def answer_seven():
    counties = census_df[census_df['SUMLEV'] == 50].reindex(columns=[['CTYNAME','POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012','POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']])
    counties['diff'] = counties.max(axis=1) - counties.min(axis=1)
    counties = counties.set_index(['CTYNAME'])
    return counties['diff'].argmax()
 #Sol='Harris County'
 
 #Q8:In this datafile, the United States is broken up into four regions using the "REGION" column.
#Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
def answer_eight():
    region = census_df[((census_df['REGION'] == 1) | (census_df['REGION'] == 2) ) & (census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014']) & (census_df['CTYNAME'].str.startswith('Washington'))].reindex(columns=[['STNAME','CTYNAME']])
    return region
#Sol: 	STNAME	CTYNAME
#896	Iowa	Washington County
#1419	Minnesota	Washington County
#2345	Pennsylvania	Washington County
#2355	Rhode Island	Washington County
#3163	Wisconsin	Washington County
