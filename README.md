# [MyUK Course Schedule Web Scrape](https://github.com/jordangeorge/schedule-web-scrape)

### Contents
- gui.py
  - PyQt5 interface for adding to calendar
- gui_funcs.py
  - Functions for gui.py
- ws.py
  - Terminal file

### About
This is an idea I came up with as a personal intro to web scraping. The purpose of this program was to web scrape my schedule from the University of Kentucky's course planner and insert the data to my Google calendar using the [Google Calendar API](https://developers.google.com/calendar/), which was a new experience for me as well. I also created a simple GUI using [PyQt5](https://pypi.org/project/PyQt5/).

Due to authorization issues, I couldn't get the webpage info I needed straight from the uky website. I copied and pasted the schedule HTML from MyUK into a separate file and went from there. Besides this issue, the program works.

In terms of constraints, it works for basic courses, not for recitation courses, online courses, courses with labs or extra days, and missing time info. I might work on implementing that next and optimizing the code. Also, it is assumed that this will be used when the student registers for courses for the next semester so the year for the google calendar is set for six months in advance. I suppose another constraint would be that this cannot be used for winter sessions; only fall and spring.

### Use (for UK students)
- Clone the repo/project
- Option 1: **ws.py**
  - Copy/paste your schedule into a file named **calendar.html** and put it into the cloned repo.
  - Run with `python ws.py` in the terminal.
  - Check that your Google Calendar has been updated.
- Option 2: **gui.py**
  - Copy/paste your schedule into a file and put it into the cloned repo. Name doesn't matter as you'll be selecting it within the GUI.
  - Run with `python gui.py` in the terminal. The user will be prompted to select their schedule HTML file and can choose a different calendar ID if they so chose.
  - Check that your Google Calendar has been updated.

<hr>

### Later functionality
- gui.py and ws.py
  - Delete functionality
