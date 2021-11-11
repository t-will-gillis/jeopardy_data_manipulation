#!/usr/bin/env python
# coding: utf-8

# ### Project Goals
# You will work to write several functions that investigate a dataset of Jeopardy! questions and answers. Filter the dataset for topics that you’re interested in, compute the average difficulty of those questions, and train to become the next Jeopardy champion!

# In order to disply the full contents of a column, we’ve added this line of code to the top of your file:
# 
#     pd.set_option('display.max_colwidth', -1)
# 
# 

# In[62]:


import pandas as pd
import numpy as np



# The suggested line of code contains depreciated. Code should be as shown following:
pd.set_option('display.max_colwidth', None)

jeopardy_csv = pd.read_csv('jeopardy.csv')


# In[63]:


# The column headings contain whitespace. Strip out using lambda method 
jeopardy_csv = jeopardy_csv.rename(columns = lambda x: x.strip())
print(jeopardy_csv.columns)


# Write a function that filters the dataset for questions that contains all of the words in a list of words. For example, when the list ["King", "England"] was passed to our function, the function returned a DataFrame of 152 rows. Every row had the strings "King" and "England" somewhere in its " Question".

# In this useful?
# 
# *Comment: Python3 built-in function:*  **filter(function, iterable)**

# In[64]:


# Filter function to check if words are in dataset, first with suggested list
# Note: add leading space to ' king' in order to eliminate unwanted matches such as 'viking'
# Comment for function- we will always be using 'jeopardy_csv' as the data- eliminate the variable?
#
# words = [' King' ,'England']
# data = jeopardy_csv


# New filters following
words = ['Jupiter']
data = jeopardy_csv

def filter_data(dataset, wordlist):
    filter = lambda x: all(word.lower() in x.lower() for word in wordlist)
    return dataset.loc[dataset['Question'].apply(filter)]
    

filtered_data = filter_data(data, words)
print(filtered_data['Question'].head(3))





# 'Value' column data are strings beginning with dollar sign and include commas for the thousands, both of which need to be stripped. 'Final Jeopardy' values are None so these need to be addressed/ given a number value: Perhaps as the maximum value of '$', thus 2000? 
# 
# Convert and save 'Value' column as floats in new column so that the float values can be analysed.

# In[65]:


# Insert new column after existing 'Value' column, then a) delete '$' which always occurs in [0] position,
# b) replace ',' which occurs in values of thousands, c) all applied if lambda's x does not equal 'None', else 
# 'None' values replaced with value of 2000, and finally d) wrap method with float() in order to conver.

jeopardy_csv.insert(5, 'Value_Floats', jeopardy_csv.Value.apply(lambda x: float(x[1:].replace(',','') if x != 'None' else 2000)))

# To verify it is working:
print(jeopardy_csv.head())


# In[ ]:


# Experiment to check how function runs WITHOUT using dataset.loc[] . . .

# words = ['China']
# data = jeopardy_csv

# def filter_data(dataset, wordlist):
#     filter = lambda x: all(word.lower() in x.lower() for word in wordlist)
#     return dataset[dataset['Question'].apply(filter)]
    

# filtered_data = filter_data(data, words)
# print(filtered_data['Question'])


# In[ ]:


# versus using dataset.loc[]. 
# In this case, no apparent difference

# words = ['China']
# data = jeopardy_csv

# def filter_data(dataset, wordlist):
#     filter = lambda x: all(word.lower() in x.lower() for word in wordlist)
#     return dataset.loc[dataset['Question'].apply(filter)]
    

# filtered_data = filter_data(data, words)
# print(filtered_data['Question'])


# In[ ]:


# Check if 'Values_Float' for 'Round' = 'Final Jeopardy' successfully changed to 2000


print(jeopardy_csv.loc[116]['Value_Floats'])


# 
# Check difficulty based on average value of questions containing certain terms
# 

# In[ ]:


print('\n\nThe average value of questions containing the term(s) {} is {} points.'      .format(words, filtered_data['Value_Floats'].mean()))


# Write function that takes count of unique answers to the questions which satisfy the filter term.

# In[ ]:


# Python method .value_counts() return the info we are looking for...

def find_top_answers(dataset):
    return dataset['Answer'].value_counts()

print(find_top_answers(filtered_data))

print('''\n\nThe most-cited, unique answer to the question containing the term {} is \'{}\' which appears {} times in this dataset.'''.format(words, find_top_answers(filtered_data).index[0], find_top_answers(filtered_data)[0]))


# Explore from here! This is an incredibly rich dataset, and there are so many interesting things to discover. There are a few columns that we haven’t even started looking at yet. Here are some ideas on ways to continue working with this data:
# 
# Investigate the ways in which questions change over time by filtering by the date. How many questions from the 90s use the word "Computer" compared to questions from the 2000s?
# Is there a connection between the round and the category? Are you more likely to find certain categories, like "Literature" in Single Jeopardy or Double Jeopardy?
# Build a system to quiz yourself. Grab random questions, and use the input function to get a response from the user. Check to see if that response was right or wrong. Note that you can’t do this on the Codecademy platform — to do this, download the data, and write and run the code on your own computer!

# In[123]:


# Check how often various terms appear vs. the date
# First, create new column 'Air_Year' then check dates of when the 'dated_term' appears
# Ridiculously easy using .shape[]


# jeopardy_csv.insert(2, 'Air Year', jeopardy_csv['Air Date'].apply(lambda x: int(x[0:4])))

# Now use the np.percentile() function to subdivide the range of years (more or less) evenly.

total_shows = jeopardy_csv['Air Year'].count()
# first_third = jeopardy_csv['Air Year'].apply(lambda x: np.percentile(x, 50))
year_thirds = np.percentile(jeopardy_csv['Air Year'], [33, 67])

first_half = jeopardy_csv['Air Year'].mean()
print(total_shows)
print(year_thirds)
print(first_half)

def dated_term_ranges(dated_term):
    filtered_data = filter_data(jeopardy_csv, dated_term)
    dated_term_pre_00 = filtered_data[(filtered_data['Air Year'] <= 2000)].shape[0]
    dated_term_pre_06 = filtered_data[(filtered_data['Air Year'] <= 2006)].shape[0] - dated_term_pre_00
    dated_term_pre_12 = filtered_data[filtered_data['Air Year'] <= 2012].shape[0] - (dated_term_pre_06 + dated_term_pre_00)
    dated_term_total = filtered_data[filtered_data['Air Year'] < 2013].shape[0]
    print('\nGiven the term {}, how often does it appear:'.format(dated_term))
    print('\n\tThru year 2000: {} times or {}%'.format(dated_term_pre_00, round(dated_term_pre_00/dated_term_total*100,1)))
    print('\tFrom 2001 thru 2006: {} times or {}%'.format(dated_term_pre_06, round(dated_term_pre_06/dated_term_total*100, 1)))
    print('\tFrom 2007 thru 2012: {} times or {}%'.format(dated_term_pre_12, round(dated_term_pre_12/dated_term_total*100, 1)))

# Call to 'dated_term_ranges([''])' below should match 'total_shows' above...
dated_term_ranges([''])
dated_term_ranges(['fax'])
dated_term_ranges(['cellphone'])
dated_term_ranges(['computer'])
dated_term_ranges(['laptop'])
dated_term_ranges(['processor'])
dated_term_ranges(['aol'])


# In[ ]:





# In[ ]:




