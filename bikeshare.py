import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


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
    city = ""
    while city not in CITY_DATA:
        city = input("Please select the city you would like to analyze: "
                     "(All, Chicago, New York or Washington)\n").lower()
        if city == 'all':
            break
    # get user input for month (all, january, february, ... , june)
    month_text = ""
    while month_text not in months:
        month_text = input("Please select the month you would like to analyze: (All, January, February,...)\n").lower()
    month = months.index(month_text)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_text = ""
    while day_text not in week:
        day_text = input("Please select the day of the week you would like to analyze: "
                         "(All, Sunday, Monday,...)\n").lower()
    day = week.index(day_text)
    print('-'*40)
    return city, month, day


def load_data(city, month, day):

    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (int) month - name of the month to filter by, or "all" to apply no month filter
        (int) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # print("month: {}\nweekday: {}".format(month, day))
    if city == 'all':
        csv = []
        for city in CITY_DATA:
            csv.append(pd.read_csv(CITY_DATA[city]))
        df = pd.concat(csv)
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_week'] = df['Start Time'].dt.weekday
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Station Combination'] = df['Start Station'] + ' x ' + df['End Station']
    if month != 0:
        df = df.loc[df['Month'] == month]
    if day != 7:
        df = df.loc[df['Day_of_week'] == day]
    return df


def time_stats(df):

    input('Press Enter to analyze the stats...')

    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df_month = df.groupby(['Month'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')
    df_month['Month'] = df_month['Month'].apply(lambda x: months[x].title())
    common_month = df_month.loc[df_month.Count == df_month.Count.max(), 'Month'].values[0]
    month_count = df_month.Count.max()

    # display the most common day of week
    df_weekday = df.groupby(['Day_of_week'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')
    df_weekday['Day_of_week'] = df_weekday['Day_of_week'].apply(lambda x: week[x].title())
    common_weekday = df_weekday.loc[df_weekday.Count == df_weekday.Count.max(), 'Day_of_week'].values[0]
    weekday_count = df_weekday.Count.max()

    # display the most common start hour
    df_hour = df.groupby(['Start Hour'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')
    common_hour = df_hour.loc[df_hour.Count == df_hour.Count.max(), 'Start Hour'].values[0]
    hour_count = df_hour.Count.max()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Printing date stats results
    print('A - MONTH STATS\n\nMost Common Month: {}\nNumber of Trips: {}'.format(common_month, month_count))
    print('-' * 40)
    print('B - WEEKDAY STATS\n\nMost Common Weekday: {}\nNumber of Trips: {}'.format(common_weekday, weekday_count))
    print('-' * 40)
    print('C - START HOUR STATS\n\nMost Common Start Hour: {}\nNumber of Trips: {}'.format(common_hour, hour_count))
    print('-' * 40)

    # Give more details about stats
    detail = ""
    choices = ['a', 'b', 'c', 'none']
    while detail not in choices:
        while detail != 'none':
            detail = input('Choose the letter of the stats you wan/´t more details: (A. B, C, or None: ').lower()
            print('-' * 40)
            if detail == 'a':
                print('COMMON MONTH DETAILS\n')
                print(df_month)
                print('-' * 40)
            elif detail == 'b':
                print('COMMON WEEKDAY DETAILS\n')
                print(df_weekday)
                print('-' * 40)
            elif detail == 'c':
                print('COMMON START HOUR DETAILS\n')
                print(df_hour.head())
                print('-' * 40)


def station_stats(df):

    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    df_start_station = df.groupby(['Start Station'],sort=False).size().sort_values(ascending=False).reset_index(
        name='Count')
    common_start_station = df_start_station.loc[df_start_station.Count == df_start_station.Count.max(),'Start Station'].values[0]
    start_station_count = df_start_station.Count.max()

    # display most commonly used end station
    df_end_station = df.groupby(['End Station'], sort=False).size().sort_values(ascending=False).reset_index(
        name='Count')
    common_end_station = df_end_station.loc[df_end_station.Count == df_end_station.Count.max(),
                                            'End Station'].values[0]
    end_station_count = df_end_station.Count.max()

    # display most frequent combination of start station and end station trip
    df_comb_stations = df.groupby(['Station Combination'], sort=False).size().sort_values(
        ascending=False).reset_index(name='Count')
    common_comb_stations = df_comb_stations.loc[df_comb_stations.Count == df_comb_stations.Count.max(),
                                                'Station Combination'].values[0]
    comb_stations_count = df_comb_stations.Count.max()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    # Printing station results
    print('A - START STATION STATS\n\nMost Common Start Station: {}\nNumber of Trips: {}'.format(common_start_station,
                                                                                            start_station_count))
    print('-' * 40)
    print('B - END STATION STATS\n\nMost Common End Station: {}\nNumber of Trips: {}'.format(common_end_station,
                                                                                        end_station_count))
    print('-' * 40)
    print('C - START X END STATION COMBINATION STATS\n\nMost Common Start x End Station: {}\nNumber of Trips: {}'.format(common_comb_stations, comb_stations_count))
    print('-' * 40)

    # Give more details about stats
    detail = ""
    choices = ['a', 'b', 'c', 'none']
    while detail not in choices:
        while detail != 'none':
            detail = input('Choose the letter of the stats you wan/´t more details: (A. B, C, or None: ').lower()
            print('-' * 40)
            if detail == 'a':
                print('COMMON START STATION DETAILS\n')
                print(df_start_station.head())
                print('-' * 40)
            elif detail == 'b':
                print('COMMON END STATION DETAILS\n')
                print(df_end_station.head())
                print('-' * 40)
            elif detail == 'c':
                print('COMMON START X END STATION COMBINATION DETAILS\n')
                print(df_comb_stations.head())
                print('-' * 40)


def trip_duration_stats(df):

    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    df_travel_time = df.groupby(['Trip Duration'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')
    common_travel_time = df_travel_time.loc[df_travel_time.Count == df_travel_time.Count.max(),
                                        'Trip Duration'].values[0]
    travel_trip_count = df_travel_time.Count.max()

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    # Printing trip results
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('A - TRIP DURATION STATS\n\nMost Common Trip Durations: {} seconds\nNumber of Trips: {}'.format(
        common_travel_time,
                                                                                                 travel_trip_count))
    print('-'*40)
    print('B - MEAN TRIP DURATION\n')
    print('{} seconds'.format(mean_travel_time))
    print('-'*40)

    # Give more details about stats
    detail = ""
    choices = ['a', 'b', 'none']
    while detail not in choices:
        while detail != 'none':
            detail = input('Choose the letter of the stats you wan/´t more details: (A. B, or None: ').lower()
            print('-' * 40)
            if detail == 'a':
                print('COMMON TRAVEL TIME DETAILS\n')
                print(df_travel_time.head())
                print('-' * 40)
            elif detail == 'b':
                print('MEAN TRIP DURATION DETAILS\n')
                print('The Mean Value is a calculation. Therefore, there is no detail breakdown!')
                print('-' * 40)


def user_stats(df):

    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df_user_types = df.groupby(['User Type'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')

    # Display counts of gender
    df_no_na = df.dropna(axis=0)
    df_gender = df_no_na.groupby(['Gender'], sort=False).size().sort_values(ascending=False).reset_index(name='Count')

    # Display earliest, most recent, and most common year of birth
    df_birth = df_no_na.groupby(['Birth Year'], sort=False).size().sort_values(ascending=False).reset_index(
        name='Count')
    common_birth = df_birth.loc[df_birth.Count == df_birth.Count.max(), ['Birth Year']].values[0]
    birth_count = df_birth.Count.max()
    recent_birth = df['Birth Year'].max()
    earliest_birth = df['Birth Year'].min()

    # Printing user types results
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('OBS: Information regarding user types does not consider registries with missing value')
    print('A - USER TYPE\n')
    print(df_user_types)
    print('-' * 40)
    print('GENDER\n')
    print(df_gender)
    print('-' * 40)
    print('C - BIRTH YEAR STATS\n\nMost Common Birth Year: {}\nMost Common Birth Year Count: {}'.format(
            common_birth, birth_count))
    print('Most Recent Birth Year: {}\nEarliest Birth Year: {}'.format(
            recent_birth, earliest_birth))
    print('-'*40)


def show_raw_data(df):

    question = input('Do you want to take a look on the raw data? (y/n): ')
    if question == 'y':
        for i in range(5, len(df.index), 10):
            print(df.head(i))
            answer = input('Keep showing? (y/n): ')
            if answer == 'n':
                break


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
