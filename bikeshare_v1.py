# general description
#
# this program was created by Marko Maschek as project for the Udacity Nanodegree: Programming for Data Science
# from April to November 2021
#
# definitions & inputs
# v1 outputs blocks of rows of data upon request
# v1 has inputs for the cities based on full names, no shortcuts, and accepts lower case inputs
# 07.11.2021


import time
import pandas as pd
import numpy as np
# bikeshre_v1.py
import math

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
separator_line = 110

# first function
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # specifiy local inputs for this function
    months_list = {'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april', 'may': 'may', 'jun': 'june', 'all': 'all'}
    days_list = {'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday', 'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday', 'all': 'all'}
    cities_list = {'chicago': 'chicago', 'new york city': 'new york city', 'washington': 'washington'}
    nr_loops = 3 # number of trial inputs

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # set first input inputy_city to start off
    input_city = ''
    err_code_city = 0
    input_ctr = 0
    while input_city not in cities_list:
        input_city = str(input("\n Please Enter City Name -  Washington, New York City or Chicago:")).lower()
        input_ctr += 1
        if input_ctr >= nr_loops and input_city not in cities_list:
            print("\n You Entered {}, Enter Chicago, New York City or Chicago & Restart".format(input_city))
            err_code_city = -1
            break


    # TO DO: get user input for month (all, january, february, ... , june)
    input_month = ''
    err_code_month = 0
    input_ctr = 0
    while input_month not in months_list:
        input_month = str(input("\n Please Enter Month -  jan, feb, mar, apr, may, jun or all:")).lower()
        input_ctr += 1
        if input_ctr >= nr_loops and input_month not in months_list:
            print("\n You Entered {}, Enter jan, feb, mar, apr, may, jun or all & Restart".format(input_month))
            err_code_month = -1
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    input_day = ''
    err_code_day = 0
    input_ctr = 0
    while input_day not in days_list:
        input_day = str(input("\n Please Enter Weekday -  mon, tue, wed, thu, fri, sat, sun or all:")).lower()
        input_ctr += 1
        if input_ctr >= nr_loops and input_day not in days_list:
            print("\n You Entered {}, Enter mon, tue, wed, thu, fri, sat, sun or all & Restart".format(input_day))
            err_code_day = -1
            break
    # for est purposes - print('you entered: {}, {}, {}'.format(input_city, input_month, input_day))

    # transform into variable for further use if all inputs were valid if not send placeholder 'na'
    if err_code_city + err_code_month + err_code_day < 0:
        # alternatively fixed valid inputs for further testing
        input_city = 'na'
        input_month = 'na'
        input_day = 'na'
    else:
        input_city = cities_list[input_city]
        input_month = months_list[input_month]
        input_day = days_list[input_day]
    print('\n Your Input: City - {}, Month - {}, Day - {}'.format(input_city.title(), input_month.title(), input_day.title()))
    print('-'*separator_line)
    return input_city, input_month, input_day


# second function
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe, variable is in notation (ex) Friday, Monday in the column
        df = df[df['day_of_week'] == day.title()]

    return df


# third function
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = df['month'].mode()[0]
    # print('\n the most popular month is :', int(popular_month))
    print('\n Most Popular Month:', months[int(popular_month) - 1].title())

    # TO DO: display the most common weekday
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # find the most popular month
    popular_weekday = df['day_of_week'].mode()[0]
    print('\n Most Popular Weekday:', popular_weekday)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular month
    popular_hour = df['hour'].mode()[0]
    print('\n Most Popular Start Hour:', math.ceil(popular_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*separator_line)


# fourth function
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_sta = df['Start Station'].mode()[0]
    print('\n Most Common Start Station: ', common_start_sta)

    # TO DO: display most commonly used end station
    common_end_sta = df['End Station'].mode()[0]
    print('\n Most Common End Station:', common_end_sta)
    # print(df['End Station'].value_counts())

    # TO DO: display most frequent combination of start station and end station trip
    combo = df['Start Station'] + " & " + df['End Station']
    print('\n Most Frequent Combo of Start & End Station:',combo.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*separator_line)

# fifth function
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('\n Total Cumulated Trip Time {} Hours'.format(math.ceil(total_trip_time/3600)))

    # TO DO: display mean travel time
    mean_trip_time = df['Trip Duration'].mean()
    print('\n Mean Trip Time {} Minutes'.format(math.ceil(mean_trip_time/60)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*separator_line)


# sixth function
def user_stats(df, city_input):
    """Displays statistics on bikeshare users
    Args:
        (str) city_input - name of the city to analyze
        washington has no gender and birth data and would produce an error """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\n Distribution by User Types:\n', user_types)

    # TO DO: Display counts of gender
    # not available for washington
    if city_input != 'washington':
        gender_types = df['Gender'].value_counts()
        print('\n Distribution by Gender:\n', gender_types)

    # TO DO: Display earliest, most recent, and most common year of birth
    # not available for washington
        birth_year_min = df['Birth Year'].max()
        birth_year_max = df['Birth Year'].min()
        birth_year_common = df['Birth Year'].mode()[0]
        print('\n Summary Birth Years:')
        print('\n The Earliest Birth Year in Sample {}, the Most Recent {} and the Most Common {}'.format(math.ceil(birth_year_max), math.ceil(birth_year_min), math.ceil(birth_year_common)))
    else:
        print('\n No Gender & Birth Data available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*separator_line)


# display block data of 5 rows if requested
def display_block(df):
    # define length for block
    block_length = 5
    view_data = str(input("\n Would you like to view 5 rows of individual trip data? Enter yes / no?")).lower()
    start_loc = 0
    while (view_data != 'no' and start_loc < df.shape[0] - block_length):
        print(df.iloc[start_loc : start_loc + block_length])
        start_loc += block_length
        view_data = str(input("\n Do you wish to continue? Enter yes / no? ")).lower()


def main():
    while True:
        city, month, day = get_filters()
        df_filtered = load_data(city, month, day)
        time_stats(df_filtered)
        station_stats(df_filtered)
        trip_duration_stats(df_filtered)
        user_stats(df_filtered, city)
        display_block(df_filtered)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
