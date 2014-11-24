import sys
from urllib.error import URLError
import urllib.request
import urllib.parse
import cgi
import posixpath

from rfc3987 import match

from icalendar import Calendar


ical = sys.argv[1]
filterList = sys.argv[2:]
outputFilename = ''


def setOutputFilename():
    global outputFilename, schedule
    if match(ical, 'URI'): # Remote URL
        try:
            schedule = urllib.request.urlopen(ical, None)
        except URLError:
            print("Error while retrieving iCalendar file from URL: " + ical)
            sys.exit(1)

        cdHeader = schedule.getheader('Content-Disposition')
        if not None == cdHeader:
            _, params = cgi.parse_header(cdHeader)
            outputFilename = params['filename']
        else:
            outputFilename = 'filtered.ics'
    else: #Local file
        schedule = open(ical)
        outputFilename = posixpath.splitext(ical)[0] + '_filtered.ics'


def printMessage():
    msg = []
    # Wenn recurring Event, Takt ausgeben, ansonsten Startdatum
    if 'RRULE' in event and 'FREQ' in event['RRULE']:
        msg.extend(event['RRULE']['FREQ'])
    else:
        msg.append(event['DTSTART'].dt)

    msg.append(event['SUMMARY'])

    print(' '.join(str(eventString) for eventString in msg))


def writeFilteredFile():
    filtered_file = open(outputFilename, 'wb')
    filtered_file.write(filtered.to_ical())
    filtered_file.close()


setOutputFilename()

filterList = [key.lower() for key in filterList]

filtered = Calendar()

calendar = Calendar.from_ical(schedule.read())

for event in calendar.walk():
    if 'SUMMARY' in event.keys():
        summary = event['SUMMARY'].lower()
        if any(key in summary for key in filterList):
            # printMessage()                # Prints info message
            filtered.add_component(event)   # Adds component to resulting iCal file

writeFilteredFile()
