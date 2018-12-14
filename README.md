# MyUk Course Schedule Web Scrape

This is an idea I came up with as a personal intro to web scraping. The purpose of this program was to web scrape my schedule from the University of Kentucky's course planner and insert the data to my Google calendar using the [Google Calendar API](https://developers.google.com/calendar/), which was a new experience for me as well. I also created a simple GUI using [PyQt5](https://pypi.org/project/PyQt5/).

Due to authorization issues, I couldn't get the webpage info I needed straight from the uky website. I copied and pasted the info into a separate file and went from there. Besides this issue, the program works.

It works for basic courses, not for recitation courses, online courses, courses with labs or extra days, and missing time info. I might work on implementing that next and optimizing the code because I took some very naive approaches.

### Use
- Copy/paste schedule into a file named calendar.html
- Change year and calendarId in `ws.py` if applicable
- Run with `python3 ws.py` or `python3 gui.py` for the interactive version

<hr>

### Later functionality
- ws.py
  - Undo
  - Try/except for online courses with TBD times
- gui.py
  - Error handling
  - Undo button
  - Aesthetics/design
