# Course Schedule Web Scrape

This is an idea I came up with as a personal intro to web scraping. The purpose of this program was to web scrape my schedule from the University of Kentucky's course planner and insert the data to my Google calendar using the Google Calendar API, which was a new experience for me as well.

Due to authorization issues, I could've get the webpage info I needed straight from the uky website. I copy and pasted the info into a separate file and went from there. Besides this issue, the program works.

It works for basic courses, not for courses with lab/recitation/extra days and missing time info. I might work on implementing that next and optimizing the code because I took some very naive approaches.

Use
- Copy/paste schedule into a file named calendar.html
- Change year and calendarId in `ws.py` if applicable
- Run with `python3 ws.py`
