# Version 2.0
# This version is made for server use on https://replit.com/

from datetime import datetime
import arrow
from time import sleep
import flask
from threading import Thread
from os import path
import sys
import tweepy
import Keys as k

# Setup https server so https://uptimerobot.com/ can ping it
app = flask.Flask(__name__)
@app.route("/")
def index():
  return "Todays Holidays Twitter Bot"

def runapp():
  app.run("0.0.0.0", port=6969)

def run():
  Thread(target = runapp).start()

run()

# Get Seconds till Midnight
def secondsTilMidnight():
    EST = arrow.now('US/Eastern') 
    now = EST
    return ((24 - now.hour - 1) * 60 * 60) + ((60 - now.minute - 1) * 60) + (60 - now.second)

# Converts date to text file
dateToTxt = {"Jan": "january.txt", "Feb": "february.txt", "Mar": "march.txt", "Apr": "april.txt", "May": "may.txt", "Jun": "june.txt", 
"Jul": "july.txt", "Aug": "august.txt", "Sep": "september.txt", "Oct": "october.txt", "Nov": "novemvber.txt", "Dec": "december.txt"}

# Sets up tweepy
auth = tweepy.OAuthHandler(k.CONSUMER_KEY, k.CONSUMER_SECRET)
auth.set_access_token(k.ACCESS_KEY, k.ACCESS_SECRET)
api = tweepy.API(auth)

# Main loop
running = True
while running:
    # Get day and month
    EST = arrow.now('US/Eastern') 
    today = EST.strftime("%b %d")
    month = today.split()[0]
    day = today.split()[1]

    # Get holidays for today
    with open(f"Holidays/{dateToTxt[month]}", 'r') as f:
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
    enders = ["year", "month", "week", EST.strftime("%B").lower()]

    # Tweets Holidays
    sleepTime = secondsTilMidnight()/len(holidays)
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
            print(f"In {round(sleepTime/60)} minutes the next tweet will be posted")
            sleep(sleepTime)
    
    # In case code ends before the end of the day
    if day == EST.strftime("%d"):
        waitingForNextDay = True
        while waitingForNextDay:
            if day == EST.strftime("%d"):
                sleep(1)
            else:
                waitingForNextDay = False
    
    sleep(1)
