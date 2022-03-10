
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
no
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). Use while loop to handle invalid inputs

    citylist = ["chicago", "new york city", "washington"]
    monthlist = ["january", "february", "march", "april", "may", "june", "all"]
    daylist = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]

    city = input("For which city would you like bikeshare data? (Chicago, New York City or Washington) ").lower()
    while city not in citylist:
        print("City not found.  Please enter either Chicago, New York City or Washington")
        city = input("For which city would you like bikeshare data? (Chicago, New York City or Washington) ").lower()
    else:
        print("Great! You are analyzing {}".format(city.title()))

    month = input("For which month would you like bikeshare data? (January, February, March, April, May, June) To see all 6 months, enter all: ").lower()
    while month not in monthlist:
            print("Month not found.  Please enter January, February, March, April, May, June or all")
            month = input("For which month would you like bikeshare data? (January, February, March, April, May, June) To see all 6 months, enter all: ").lower()
    else:
            print("Ok You are analyzing {}".format(month.title()))

    day = input("For which day of the week would you like bikeshare data?. (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) To see all 7 days, type all: ").lower()
    while day not in daylist:
             print("Day not found.  Please enter Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or all")
             day = input("For which day of the week would you like bikeshare data?. (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) To see all 7 days, type all: ").lower()
    else:
             print("Ok You are analyzing {}".format(day.title()))

    print('-'*40)
    # print (city, month, day)
    return city, month, day

"""_____Load Data function_________________________________________________________"""

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
    # read data file for user entered city
    df = pd.read_csv(CITY_DATA[city])

    #convert start time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #create columns for month, day of week, and hour
    df['month'] = df['Start Time'].dt.month

    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # df['day_of_week'] = df['Start Time'].dt.day_name    -for use with newer version of pandas

    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        #use index of the monthlist to get an integer for the month
        monthlist = ["january", "february", "march", "april", "may", "june"]
        month = monthlist.index(month) + 1

        #filter by month to get new filtered dataframe
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

"""_____Time Statistics function_________________________________________________________"""

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
       If data is filtered for a specific month and day,
       most frequent month and day make no sense - so handle with msg"""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most popular month
    if month == 'all':
        popular_month_num = df['month'].mode()[0]
        monthlist = ["january", "february", "march", "april", "may", "june"]
        popular_month = monthlist[popular_month_num-1].title()
        print('Most popular month is: ', popular_month)

    else:
        print('Most common month: Not available since data filtered by month')
    # TO DO: display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        #print('day in df is: ', df['day_of_week'])
        print('Most popular day is: ', popular_day)
    else:
        print('Most common day: Not available since data filtered by day')

    # TO DO: display the most common start hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""_____Station Statistics function_________________________________________________________"""

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #  display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most popular start station is: ', popular_start)
    #  display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most popular end station is: ', popular_end)

    #  display most frequent combination of start station and end station trip
    # create combo column
    df['Station Combo']= df['Start Station'] + ' to ' + df['End Station']
    popular_station_combo = df['Station Combo'].mode()[0]
    print('Most popular station combination is: ', popular_station_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""_____Trip Statistics function_________________________________________________________"""

def convert(seconds):
    min, sec = divmod(seconds,60)
    hour, min = divmod(min, 60)
    day, hour = divmod(hour, 24)
    return "%d:%02d:%02d:%02d" % (day,hour,min,sec)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #  display total travel time
    t = df['Trip Duration'].sum()
    tot_travel_time = convert(t)
    print('Total travel time in days, hours, minutes, seconds is: ',tot_travel_time)
    #  display mean travel time
    a = df['Trip Duration'].mean()
    avg_travel_time = convert(a)
    print('Average travel time in hours, minutes, seconds is: ', avg_travel_time)
"""_____User Statistics function_________________________________________________________"""

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #  Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The total number of users by user type is: ', '\n',user_types)
    #  Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print("\nThe total number of users by gender is: ",'\n',user_gender)
    else:
        print("No gender data available for this city")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        oldest = df['Birth Year'].min()
        youngest = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print('The oldest user was born in: ',int(oldest))
        print('The youngest user was born in: ',int(youngest))
        print('Most users were born in: ',int(common))
    else:
        print("No birth year data available for this city")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""__________ Handle response to yes or no question ______________
 If the user enters yes, function returns True;
 If user enters no, function returns False;
 If user enters something else, ask again for valid entry"""

def get_y_or_no(question):
    y_or_no = ['yes', 'no']
    prompt = f'{question} ?  Please enter yes or no:'
    ans = input(prompt).lower()
    while ans not in y_or_no:
        print('\nEntry not valid. Please enter yes or no.\n')
        ans = input('\n'+(prompt)+'\n').lower()
    return(ans)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        #Ask if would like to see 5 rows of data
        prows = 0
        show_rows = get_y_or_no('\nWould you like to see 5 rows of data?\n')
        pd.set_option('display.max_columns', 200)
        while show_rows == 'yes':
            print(df[prows:prows+5])
            show_rows = get_y_or_no('\nWould you like to see 5 more rows of data?\n')
            prows +=5

    #Ask if would like to run analysis again
        restart = get_y_or_no('\nWould you like to restart? Enter yes or no.\n')
        if restart != 'yes':
            break

if __name__ == "__main__":
	main()
