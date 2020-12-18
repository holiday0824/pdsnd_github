import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january','february','march','april','may','june']
days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to analyze?\n(Chicago, New York, Washington)\n').lower()
        if city in CITY_DATA:
            break
    
    else:
            print('Your choice was not valid. Please choose from the list provided \n')


    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('For which month would you like to see data?\nEnter a month from January to June, or "all" to complie all months(Jan - Jun) \n').lower()
        if month in months or month == 'all':
            break
        else:
            print('That\'s not a valid entry. Please try again. \n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('For which day of the week would you like to see data?\nEnter a day of the week or "all to complie all days of the week. \n').lower()
        if day in days or day == 'all':
            break
        else:
            print('That\'s not a valid entry. Please try again. \n')

    print('-'*40)
    return city, month, day


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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour
    if month !='all':
        month = months.index(month)+1
        df = df[df['Month'] == month]
    if day !='all':
        df=df[df['Day of Week']==day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nFetching frequency data. Please wait\n')
    start_time = time.time()
    popular_month = df['Month'].mode()[0]
    popular_day = df['Day of Week'].mode()[0]
    popular_hr = df['Hour'].mode()[0]

    print('Riders rented the most in {}.\n The most popular day to rent was on{}.\n The most popular time to rent was at{}.'.format(popular_month,popular_day,popular_hr))


    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nFinding the most popular stations and trips...\n')
    start_time = time.time()
    common_start = df['Start Station'].mode()[0]
    common_end = df['End Station'].mode()[0]

    df['Station-Combo'] = df['Start Station'] + ' - ' + df['End Station']
    combo_station = df['Station-Combo'].mode()[0]

    # display most commonly used start station
    print("The most common start station is: " +
          common_start)

    # display most commonly used end station
    print("The most common end station is:" +
            common_end)

    # display most frequent combination of start station and end station trip
    print("Most frequented start and stop stations are: " +
            combo_station)

    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_dur = df['Trip Duration'].sum()
    mean_dur = df['Trip Duration'].mean()

    print('Total travel time was {} hrs.\nThe average travel time was {} mins.'.format(round(total_dur/3600,2), round(mean_dur/60,2)))



    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    user_type = df['User Type'].value_counts()
    gender_ct = 'I\'m not able to locate any gender data from this source.'
    birth_young = 'I\'m not able to locate any data from this source.'
    recent_birth = birth_young
    common_birth = birth_young

    if 'Gender' in df:

        gender_ct = df['Gender'].value_counts()

    if 'Birth Year' in df:
        birth_young = int(df['Birth Year'].min())
        recent_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode()[0])


    # Display gender distribution
    print('The gender distibution of riders\n{}\n\nThe earliest birth year is {}.\nThe most recent birth year is {}.\nThe most common birth year is {}.'.format(gender_ct, birth_young, recent_birth, common_birth))
    

    print("\nThis query took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(city, df):
    #Checks if the user would like to see a raw data export and prints 5 rows at a time
    first_row = 0
    last_row = 5
    while True:
        raw = input('\nWould you like me to print the next 5 rows of raw data for {} with the current filters? Please enter Yes or No.'.format(city.title()).lower())
        if raw == 'yes':
           print(df.iloc[first_row:last_row])
           first_row += 5
           last_row +=5
        elif raw == 'no':
            break
        else:
            print('That choice is invalid. Please retry your request. \n' )




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(city,df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
