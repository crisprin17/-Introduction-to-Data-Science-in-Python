import pandas as pd

df = pd.read_csv('olympics.csv',index_col=0,skiprows=1)
df.head()
for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':  
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df
# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[1]

#Q1 = Which country has won the most gold medals in summer games?
def answer_one():
    return df['Gold'].argmax()
#Sol= 'United States'

#Q2: Which country had the biggest difference between their summer and winter gold medal counts?
def answer_two():
    wint_gold = df['Gold.1']
    summ_gold = df['Gold']
    diff = (summ_gold - wint_gold).abs()
    return diff.argmax()
 #Sol = 'United States'
 
 #Q3: Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?
 #Only include countries that have won at least 1 gold in both summer and winter.
 def answer_three():
    wint_gold = df['Gold'][df['Gold']>=1]
    summ_gold = df['Gold.1'][df['Gold.1']>=1]
    tot_gold  = df['Gold.2']
    reldiff = (summ_gold - wint_gold).abs()/tot_gold
    return reldiff.argmax()
  #Sol = 'Bulgaria'
  
  #Q4: Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2) counts for 3 points,
  #silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. 
  #The function should return only the column (a Series object) which you created, with the country names as indices.
  def answer_four():
    totgold = df['Gold.2']*3
    totsilv = df['Silver.2']*2
    totbron = df['Bronze.2']*1
    return totgold+totsilv+totbron
  points = answer_four()
  points.count()
  #Sol:146

