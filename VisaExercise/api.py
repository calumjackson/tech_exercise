import flask
from datetime import date
import calendar
import time
import re
import sys
from flask import render_template
from html.parser import HTMLParser


app = flask.Flask(__name__)
app.config["DEBUG"] = True

def nvl(stringArg, stringIfNull):
    if stringArg is None:
        return stringIfNull
    else:
        return stringArg

def validateMonth(month_i, today_i):
    if (month_i == None): return today_i.month
    if (month_i >= 1 and month_i <= 12):
        return month_i
    else:
        # Should return error instead
        return today_i.month

# Assumes invalid is returned as current.
def validateYear(year_i, today_i):
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

    # calendar.month(year, month)

    cal = calendar.HTMLCalendar()
    cal = cal.formatmonth(year, month)
    return cal
    return calendar.month(year,month)


def highlight_date(calendar_v, today_i):
    higlighted_calendar_v = calendar_v.replace('>%i<'%today_i.day, ' bgcolor="#FFFF00"><b><u>%i</u></b><'%today_i.day)

    # Lifted code which highlights text calendar day
    #date  = today_i.day.__str__().rjust(2)
    #rday  = ('\\b' + date + '\\b').replace('\\b ', '\\s')
    #rdayc = "\033[7m" + date + "\033[0m"
    # 7 Swaps foreground and background colors
    #higlighted_calendar_v = ( re.sub(rday, rdayc, calendar_v))
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

def main():
    year_in, month_in = 2021, 05
    today = date.today()

    # Validate Step
    year_in = validateYear(year_in, today)
    month_in = validateMonth(month_in, today)

    generatedCalendar = generateCalendar(year_in, month_in, today)  # current month

    if (isCurrentMonth(year_in, month_in, today)):
        generatedCalendar = highlight_date(generatedCalendar, today)

    todays_date_v = 'Todays Date: \n\n' + str(today)

    return render_template('response.html', title=generatedCalendar, todays_date=todays_date_v)


@app.route('/', methods=['GET'])
def home():
    return main()

app.run()
