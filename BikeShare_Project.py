#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Questions to be answered as per the assignment
'''
#1 Popular times of travel (i.e., occurs most often in the start time)

most common month
most common day of week
most common hour of day

#2 Popular stations and trip

most common start station
most common end station
most common trip from start to end (i.e., most frequent combination of start station and end station)

#3 Trip duration

total travel time
average travel time

#4 User info

counts of each user type
counts of each gender (only available for NYC and Chicago)
earliest, most recent, most common year of birth (only available for NYC and Chicago)'''


# In[2]:


#First import libraries
import pandas as pd
import numpy as np
import time
import math


# In[3]:


#Creating a dictionary of csv files of 3 datasets of 3 cities
CITY_DATA = { 'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv' }


# In[4]:


#Defining a function to handle user input and while loop to handle valid and valid inputs
def get_filters():
    """
    Asking user input for city, month and day
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply all months data
        (str) day - name of the day of week to filter by, or "all" to apply all days filter
    """
    print('Let\'s explore 2017 US bikeshare data!')

    # user input for city (chicago, new york city, washington).
    cities = ('chicago', 'new york', 'washington')
    while True:
        city = input('\nWhich city data you like to see- Chicago, New York, or Washington?\n').lower()
        if city not in cities:
            print('Invalid city, try again')
            continue
        else:
            break

    # user input for month (all, january, february, ... , june), all represents the values for all months
    months = ('all', 'january', 'february', 'march', 'april', 'may', 'june')
    while True:
        month = input('\nWhich month would you like to filter by: January, February, March, April, May, or June? else enter "all" to get all months data.\n').lower()
        if month not in months:
            print('Invalid month, try again')
            continue
        else:
            break

    # user input for day of week (all, monday, tuesday, ... sunday)
    days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
    while True:
        day = input('\nWhich day would you like to filter by: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? else enter "all" to get all days data.\n').lower()
        if day not in days:
            print('Invalid day, try again')
            continue
        else:
            break
    print('-'*40)        
    return city, month, day


# In[5]:


#Now define a function to load data into datafram for city, month and day 
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])

    #Now Start Time column is subjected to 'to_datetime' and creates 2 new columns i.e. month and day of week columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filters by month if applicable and creates new dataframe
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filters by day of week if applicable and creates new dataframe
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


# # Q1 Popular times of travel (i.e., occurs most often in the start time)

# In[6]:


#most common month
#most common day of week
#most common hour of day
#for most common month, day and hour , I am using mode method of pandas

def time_stats(df):
    #this function gives most frequent time data
    print('\nThe Most Frequent Times of Travel...\n')
    start_time = time.time()

    #the most common month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)

    #the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week:', common_day)

    #the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common starting hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# # Q2 Popular Stations and Trip

# In[7]:


#most common start station
#most common end station
#most common trip from start to end (i.e., most frequent combination of start station and end station)
def station_stats(df):
    """This function gives most popular stations and trip."""

    print('\nThe Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('Most commonly used start station:', common_start)

    # most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('Most commonly used end station:', common_end)

    # most frequent combination of start station and end station trip
    df['Frequent Trip'] = df['Start Station'] + ' to ' + df['End Station']
    common_trip = df['Frequent Trip'].mode()[0]
    print('Most common trip:', common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# # Q3 Analysis on Trip Duration
# 

# In[8]:


#total travel time
#average travel time

def trip_duration_stats(df):
    """shows analysis on total average trip duration"""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', total_travel_time, 'seconds')

    # mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# # Q4 Users statistics
# 

# In[9]:


#counts of each user type
#counts of each gender (only available for New York and Chicago)
#earliest, most recent, most common year of birth (only available for New York and Chicago)

def user_stats(df):
    """bikeshare users stats"""

    print('\nUser Stats...\n')
    start_time = time.time()

    # counts of user types
    user_type_count = df['User Type'].value_counts()
    print('User Type Count:\n', user_type_count)

    # counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print('\nGender Count:\n', gender_count)
    except KeyError:
        print('\nGender Count: No data available.')

    # shows earliest, most recent, and most common year of birth
    try:
        birth_min = int(df['Birth Year'].min())
        print('\nEarliest year of birth:', birth_min)
    except KeyError:
        print('\nEarliest year of birth: No data available.')

    try:
        birth_max = int(df['Birth Year'].max())
        print('Most recent year of birth:', birth_max)
    except KeyError:
        print('Most recent year of birth: No data available.')

    try:
        birth_mode = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', birth_mode)
    except KeyError:
        print('Most common year of birth: No data available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[10]:


def display_data(df):
    """To check raw data of top 5 rows"""

    show_data = input('\nWould you like to see 5 rows of raw data? yes or no:\n').lower()
    if show_data != 'no':
        i = 0
        while (i < df['Start Time'].count() and show_data != 'no'):
            print(df.iloc[i:i+5])
            i += 5
            more_data = input('\nWould you like to see 5 more rows of data? yes or no:\n').lower()
            if more_data != 'yes':
                break


# # Below code will make the code interactive - User input will be requested to process

# In[11]:


#Consolidation of all function under the main command function
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




