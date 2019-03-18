import httplib2
import os

from bs4 import BeautifulSoup as soup
# import requests
import re

import pytz
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta

from googleapiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'UKY Schedule Webscrape'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'uky-web-scrape-calendar.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

eventIdList = []
calendarId = 'primary'
# calendarId = 'un1nmhba2l7vfm5vvie66m6nrk@group.calendar.google.com'

def getService():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    return discovery.build('calendar', 'v3', http=http)

def main():
    choiceText = "\n1. Add\n2. Delete\n3. Exit\nChoice: "
    choice = int(input(choiceText))

    while choice == 1 or choice == 2:
        if choice == 1:
            add()
        # elif choice == 2:
            # delete()
        choice = int(input(choiceText))

    exit()

def add():
    # url = 'https://myuk.uky.edu/zAPPS/CourseCatalog/Schedule/Print/2018/010'
    # res = requests.get(url)
    # page_html = res.text
    # page_soup = soup(page_html, "html.parser")
    # print(page_soup)

    fileName = "calendar.html"
    page_html = open(fileName, 'r').read()
    page_soup = soup(page_html, "html.parser")

    # httplib2.debuglevel = 4
    service = getService()

    six_months = date.today() + relativedelta(months=+6)
    year = str(six_months.year)

    timeZone = "America/New_York"

    courses = page_soup.findAll("div", {"class": "table-thin-row small"})

    for course in courses:
        title = " ".join(course.find("strong", {"class": "text-dark"}).text.split())
        section = course.findAll("div")[4].text
        courseType = course.findAll("div")[5].text.strip()

        p = re.compile(r'Section ')
        newSection = p.sub("", section)
        summary = title + " - " + newSection

        weekdays = course.findAll("div")[7].text
        if weekdays == "TBD": # for online classes that do not have a time or location
            continue

        hour = course.findAll("div")[8].text
        dates = course.findAll("div")[9].text.strip()

        hourList = hour.split(" - ")
        datesList = dates.split("-")
        googleDateTimeList = []
        for i in range(0, len(datesList)):
            h = ''.join(hourList[i].split(" "))
            new_time = dt.strptime(h, '%I:%M%p').strftime("%H:%M")
            new_time += ":00"
            unformattedTime = datesList[0] + " " + year + " " + new_time
            naive = dt.strptime(unformattedTime, '%b %d %Y %H:%M:%S')
            local = pytz.timezone(timeZone)
            local_dt = local.localize(naive, is_dst=None)
            googleDateTimeList.append(local_dt.strftime("%Y-%m-%d"+"T"+"%H:%M:%S"+"-05:00"))
        googleDateTimeStart = googleDateTimeList[0]
        googleDateTimeEnd = googleDateTimeList[1]

        classEndTime = ''.join(hourList[1].split(" "))
        new_time = dt.strptime(classEndTime, '%I:%M%p').strftime("%H:%M")
        new_time += ":00"
        unformattedTime = datesList[1] + " " + year + " " + new_time
        naive = dt.strptime(unformattedTime, '%b %d %Y %H:%M:%S')
        naive += timedelta(hours=48) # make two days ahead because recurrence is inclusive of end time
        local = pytz.timezone(timeZone)
        local_dt = local.localize(naive, is_dst=None)
        until = local_dt.strftime("%Y%m%d"+"T"+"%H%M%S"+"Z")

        weekdays = list(weekdays)
        days = ""
        for char in weekdays:
            if char == 'M': days += "MO"
            elif char == 'T': days += "TU"
            elif char == 'W': days += "WE"
            elif char == 'R': days += "TH"
            else: days += "FR"
            days += ","
        days = days[:-1] # remove last comma

        recurrence = "RRULE:FREQ=WEEKLY;UNTIL={};BYDAY={}".format(until, days)

        building = course.findAll("div")[11].text
        room = course.findAll("div")[12].text
        location = building + " " + room

        instuctor = course.findAll("div")[13].text.strip()

        description = courseType + "\n" + instuctor

        event = {
          'summary': summary,
          'location': location,
          'description': description,
          'start': {
            'dateTime': googleDateTimeStart,
            'timeZone': timeZone,
          },
          'end': {
            'dateTime': googleDateTimeEnd,
            'timeZone': timeZone,
          },
          'recurrence': [
            recurrence
          ]
        }
        event = service.events().insert(calendarId=calendarId, body=event).execute()
        print('Event created for {}: {}'.format(title, event.get('htmlLink')))

        # eventURL = event.get('htmlLink')
        # eventIdIndex = eventURL.rfind("=")
        # eventId = eventURL[eventIdIndex+1:]
        # eventIdList.append(eventId)

# def delete():
#     service = getService()
#     for id in eventIdList:
#         event = service.events().delete(calendarId=calendarId, eventId=id).execute()
#         print(event)

if __name__ == '__main__':
    main()
