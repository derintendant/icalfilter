import os

import sys

from icalendar import Calendar


schedule = open(sys.argv[1])
lookfor = [key.lower() for key in sys.argv[2:]]

filtered = Calendar()

calendar = Calendar.from_ical(schedule.read())


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
    global outputFilename, filtered_file
    outputFilename = os.path.splitext(sys.argv[1])[0] + '_filtered.ics'
    filtered_file = open(outputFilename, 'wb')
    filtered_file.write(filtered.to_ical())
    filtered_file.close()

for event in calendar.walk():
    if 'SUMMARY' in event.keys():
        summary = event['SUMMARY'].lower()
        if any(key in summary for key in lookfor):
            printMessage()                # Prints info message
            filtered.add_component(event) # Adds component to resulting iCal file

writeFilteredFile()
