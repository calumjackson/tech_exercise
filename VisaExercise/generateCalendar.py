from datetime import date
import calendar
import time
import re
import sys

# Run requirements
# > python generateCalendar.py [[year (YYYY format)] [month (MM Format)]]


# Requirements
# 1. To return a calendar 'highlighting' the current date
# 2. To be able to format the year or month.
# 3. Year / Month specifed must be in valid range
# 4. To be able to access this somehow and to be returned as a visual reference
# 5. If year / month are different from current date, no need to highlight current date as it isn't there.
# 6. Still probably want to show the current date as that is the core requirement


# Things I would initally add with more time:
# Error Handling - allow for non-happy path scenarios to end gracefully or self-fix (i.e. month validation of value type as well as range)
# More practical way to define arguments being passed in
# Ability to define only a month or a year to overwrite
# Ability to determine month / year etc based on multiple different references 'June vs 06' etc
# Reviewed how this would be exposed to a client server basis.


# Simple is null function, no real validation etc around it.
def nvl(stringArg, stringIfNull):
    if stringArg is None:
        return stringIfNull
    else:
        return stringArg

# Assumes an invalid month would be returned as just the current month
def validateMonth(month_i, today_i):
    if (month_i == None): return today_i.month
    if (month_i >= 1 and month_i <= 12):
        return month_i
    else:
        # Should return error instead
        return today_i.month

# Assumes invalid is returned as current.
def validateYear(year_i, today_i):
    print year_i
    if (year_i == None): return today_i.year
    if (year_i >= 1970 and year_i <= 2037):
        return year_i
    else:
        # Should return error instead
        return today_i.year


def generateCalendar(year_i, month_i, today_i):
    # Log input values here
    year  = nvl(year_i, today_i.year)
    month = nvl(month_i, today_i.month)
    return calendar.month(year,month)


def highlight_date(calendar_v, today_i):
    # Lifted code which highlights text calendar day
    date  = today_i.day.__str__().rjust(2)
    rday  = ('\\b' + date + '\\b').replace('\\b ', '\\s')
    rdayc = "\033[7m" + date + "\033[0m"
    # 7 Swaps foreground and background colors
    higlighted_calendar_v = ( re.sub(rday, rdayc, calendar_v))
    return higlighted_calendar_v

def isCurrentMonth(year_in, month_in, today_i):
    if (today_i.month == month_in and today_i.year == year_in): return True
    return False

# Doesn't allow for only one and doesn't validate if they are passed in the other way around
def get_args():
    if len(sys.argv) == 3:
        return int(sys.argv[1]), int(sys.argv[2])
    else:
        return None, None

#
def main():
    year_in, month_in = get_args()
    today = date.today()

    # Validate Step
    year_in = validateYear(year_in, today)
    month_in = validateMonth(month_in, today)

    generatedCalendar = generateCalendar(year_in, month_in, today)  # current month

    if (isCurrentMonth(year_in, month_in, today)):
        generatedCalendar = highlight_date(generatedCalendar, today)

    print generatedCalendar
    # Show current date in case the calendar is overwritten and doesn't highlight it
    # Debatable whether this should be shown if the date IS highlighted, will do for now.
    print "Current Date: \n " + str(today)

main()
