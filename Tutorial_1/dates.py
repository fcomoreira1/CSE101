#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

def hello_world():
    """
        returns 'Hello world!'
    """
    return 'Hello world!'

def check_day(n):
    """
    Given an integer between 1 and 7 inclusive,
    return either string 'work!' or string 'rest!'
    depending on whether the day is a workday or not
    """
    if n < 1 or n > 7:
        return None
    if n >= 6:
        return "rest!"
    return "work!"

def name_of_month(m):
    """Given an integer m between 1 and 12 inclusive,
    indicating a month of the year, returns the name of that month.
    For example: name_of_month(1) == 'January' and name_of_month(12) == 'December'.
    If the month does not exist (that is, if m is outside the legal range),
    then this function returns None.
    """
    if m < 1 or m > 12:  # Non-existent month
        return None
    if m == 1:
        return 'January'
    elif m == 2:
        return 'February'
    elif m == 3:
        return 'March'
    elif m == 4:
        return 'April'
    elif m == 5:
        return 'May'
    elif m == 6:
        return 'June'
    elif m == 7:
        return 'July'
    elif m == 8:
        return 'August'
    elif m == 9:
        return 'September'
    elif m == 10:
        return 'October'
    elif m == 11:
        return 'November'
    else:
        return 'December'

def str_with_suffix(n):
    """Convert the integer n to a string expressing the corresponding 
    position in an ordered sequence.
    Eg. 1 becomes '1st', 2 becomes '2nd', etc.
    """
    if int(n) % 100 == 11:
        return str(n) + 'th'
    elif int(n) % 100 == 12:
        return str(n) + 'th'
    elif int(n) % 100 == 13:
        return str(n) + 'th'
    if int(n) % 10 == 1:
        return str(n) + 'st'
    elif int(n) % 10 == 2:
        return str(n) + 'nd'
    elif int(n) % 10 == 3:
        return str(n) + 'rd'
    else:
        return str(n) + 'th'

def is_leap_year(n):
    """ 
        Return True if y is a leap year, False otherwise.
    """
    if n % 400 == 0:
        return True
    elif n % 100 == 0:
        return False
    elif n % 4 == 0:
        return True
    else:
        return False

def number_of_days(m, y):
    """
        Returns the number of days in month m of year y.
    """
    if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
        return 31
    elif m == 4 or m == 6 or m == 9 or m == 11:
        return 30
    else:
        if is_leap_year(y):
            return 29
        else:
            return 28

def date_string(d, m, y):
    """
        Returns a string representing date in words in the format
        'The D of M, Y' where D is the number of the day follow by suffix,
        M is the month in its word form and Y is the year.
    """

    day_string = str_with_suffix(d)
    month_string = name_of_month(m)
    if month_string == None or d > number_of_days(m, y):
        return 'Nonexistent date'
    else:
        return 'The ' + day_string + ' of ' + month_string + ', ' + str(y)

def time_string(n):
    """
        Returns a string descibing the corresponding number of days, hours,
        minutes and second to n seconds. Omits '0 days', '0 hours', '0 minutes'
    """
    quantity_days = int(n) // 86400
    n = int(n) % 86400
    quantity_hours = int(n) // 3600
    n = int(n) % 3600
    quantity_minutes = int(n) // 60
    quantity_seconds = int(n) % 60 

    string_days = ''
    string_hours = ''
    string_minutes = ''
    string_seconds = ''
    if quantity_days > 1:
        string_days = str(quantity_days) + ' days, '
    elif quantity_days == 1:
        string_days = '1 day, '
    if quantity_hours > 1:
        string_hours = str(quantity_hours) + ' hours, '
    elif quantity_hours == 1:
        string_hours = '1 hour, '
    if quantity_minutes> 1:
        string_minutes = str(quantity_minutes) + ' minutes, '
    elif quantity_minutes == 1:
        string_minutes = '1 minute, '
    if quantity_seconds == 1:
        string_seconds = '1 second'
    else:
        string_seconds = str(quantity_seconds) + ' seconds'
    
    return string_days + string_hours + string_minutes + string_seconds
