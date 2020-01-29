import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('-'*40)
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input('Which city do you like to analyze? Please choose a city from chicago, '
                         'new york city, or washington: ').lower()
            if city not in CITY_DATA.keys():
                raise ValueError
            break
        except ValueError:
            print('That\'s not a valid input, please enter a city name again.\n')

    print('-'*40)
    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input('Which month do you like to analyze? Please enter a month name from january to june, '
                          'or "all" to select all months: ').lower()
            if month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
                raise ValueError
            break
        except ValueError:
            print('That\'s not a valid input, please enter a month name again, or "all" to select all months.\n')

    print('-'*40)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input('Which day of week do you like to analyze? Please enter a weekday name from monday to sunday, '
                        'or "all" to select the entire week: ').lower()
            if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
                raise ValueError
            break
        except ValueError:
            print('That\'s not a valid input, please enter a weekday name again, or "all" to select the entire week.\n')


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['month'].unique()) > 1:
        max_idx = df.groupby('month')['Start Time'].count().idxmax() - 1
        print('The most popular month of travel is', months[max_idx])

    # display the most common day of week
    if len(df['day_of_week'].unique()) > 1:
        print('The most popular day of week of travel is',
              df.groupby('day_of_week')['Start Time'].count().idxmax())

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    max_hour = df.groupby('hour')['Start Time'].count().idxmax()
    if max_hour == 0:
        print('The most popular hour of day of travel is 12 AM')
    elif 0 < max_hour < 12:
        print('The most popular hour of day of travel is', max_hour, 'AM')
    elif max_hour == 12:
        print('The most popular hour of day of travel is', max_hour, 'PM')
    else:
        print('The most popular hour of day of travel is', max_hour-12, 'PM')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station is', df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['start_end_station'] = df['Start Station'] + ' and ' + df['End Station']
    print('The most frequent combination of start station and end station trip is',
          df['start_end_station'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total time people spent on the trip are', df['Trip Duration'].sum()/(3600*24),
          'days')

    # display mean travel time
    print('The average time people spent on the trip are', df['Trip Duration'].mean()/60,
          'minutes')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_count = df['User Type'].value_counts()
    print('There are', len(user_count), 'types of users. '
          'Their counts are as follows:')
    for i in range(len(user_count)):
        print(user_count.index[i],': ',user_count[i])

    # Display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('The gender counts are as follows:')
        for i in range(len(gender_count)):
            print(gender_count.index[i],': ',gender_count[i])

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('The earliest year of birth is', int(df['Birth Year'].min()))
        print('The most recent year of birth is', int(df['Birth Year'].max()))
        print('The most common year of birth is', int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def print_lines_generator(df):
    """ This is a generator function to yield 5 lines of dataframe sequentially """
    i = 0
    while(i < df.shape[0] - 5):
        pd.set_option('display.max_columns', None) # display all columns
        yield df.iloc[i:i+5,]
        i += 5
    if i >= df.shape[0] - 5:
        yield df.iloc[i:,]


def print_lines(df):
    """ Prompt the user for input to print 5 lines of raw data sequentially """
    gen_fun = print_lines_generator(df)
    while True:
        try:
            lines = input('Do you want to see 5 lines of raw data? Please type yes or no: ').lower()
            if lines == 'yes':
                try:
                    print(next(gen_fun))
                except StopIteration:
                    print('You have reached the end of this file. Exiting...')
                    break
            elif lines == 'no':
                break
            else:
                raise ValueError
        except ValueError:
            print('That\'s not a valid input! Please enter yes or no.\n')


def get_restart_prompt():
    """ This function is used to prompt for user input about whether to restart the program """
    while True:
        try:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart in ['yes' , 'no']:
                return restart
            else:
                raise ValueError
        except ValueError:
            print('Sorry. I cannot understand what you mean.')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_lines(df)

        if get_restart_prompt() == 'yes':
            continue
        else:
            print('Thank you for your interests in our US Bike Share data. Have a great day and goodbye~~~~~~')
            break


if __name__ == "__main__":
	main()
