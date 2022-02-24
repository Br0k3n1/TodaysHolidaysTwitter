# Version 1.0

from datetime import date, datetime
from time import sleep
from os import path
import sys
import tweepy
import Keys as k

# Get Seconds till Midnight
def secondsTilMidnight():
    now = datetime.now()
    return ((24 - now.hour - 1) * 60 * 60) + ((60 - now.minute - 1) * 60) + (60 - now.second)

# Converts date to text file
dateToTxt = {"Jan": "january.txt", "Feb": "february.txt", "Mar": "march.txt", "Apr": "april.txt", "May": "may.txt", "Jun": "june.txt", 
"Jul": "july.txt", "Aug": "august.txt", "Sep": "september.txt", "Oct": "october.txt", "Nov": "novemvber.txt", "Dec": "december.txt"}

# Sets up tweepy
auth = tweepy.OAuthHandler(k.CONSUMER_KEY, k.CONSUMER_SECRET)
auth.set_access_token(k.ACCESS_KEY, k.ACCESS_SECRET)
api = tweepy.API(auth)

# Get day and month
today = date.today().strftime("%b %d")
month = today.split()[0]
day = today.split()[1]

# Get holidays for today
with open(path.join(sys.path[0], f"Holidays\{dateToTxt[month]}"), 'r') as f:
    lines = f.readlines()
    holidays = []
    
    # Strips lines of \n character
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
    
    # Appends holidays to holiday list
    if f"{month.upper()} {day}" in lines:
        for i in range(lines.index(f"{month.upper()} {day}") + 1, len(lines)):
            if lines[i] != f"{month.upper()} {int(day) + 1}":
                holidays.append(lines[i])
            else:
                break
    else:
        print("ERROR: date not found in text file, ending program")
        exit()
    
# Special Enders
enders = ["year", "month", "week", date.today().strftime("%B").lower()]

# Tweets Holidays
for holiday in holidays:
    if 'day' in holiday.lower():
        api.update_status(f"Today is {holiday}")
        print(f'Tweeted: "Today is {holiday}"')
    elif holiday.split()[len(holiday.split()) - 1].lower() in enders:
        api.update_status(f"Today is the start of {holiday}")
        print(f'Tweeted: "Today is the start of {holiday}"')
    else:
        api.update_status(f"Today is {holiday} day")
        print(f'Tweeted: "Today is {holiday} day"')
    
    # Seperate tweets through out the day
    if holiday != holidays[len(holidays) - 1]:
        sleepTime = secondsTilMidnight() / len(holidays) - holidays.index(holiday) + 1
        sleep(sleepTime)
