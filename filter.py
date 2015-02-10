#!/usr/bin/env python3

import sys
import posixpath
import getopt

from icalendar import Calendar


def usage():
    print("Usage: " + sys.argv[0] + "[-i input_file] -f filter_file")


def main(argv):
    inputFile = sys.stdin
    fromStdin = True
    outputFilename = 'ical_filtered.ics'
    filterFilename=''
    filterlist = list()
    try:
        opts, args = getopt.getopt(argv, "hi:f:", ["help", "input=", "filter="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-i", "--input"):
            inputFilename = arg                                               # TODO: exception check
            outputFilename = posixpath.splitext(arg)[0] + '_filtered.ics'
            fromStdin = False
        if opt in ("-f", "--filter"):
            filterFilename = arg

    if filterFilename == '':
        usage()
        sys.exit(2)

    if not fromStdin:
        try:
            inputFile = open(inputFilename)
        except FileNotFoundError:
            print("ERROR: Input File not found")
            sys.exit(1)
        except PermissionError:
            print("ERROR: Permission denied while accessing Input File")
            sys.exit(1)

    try:
        with open(filterFilename) as filterfile:
            filterlist = filterfile.read().splitlines()
    except FileNotFoundError:
        print("ERROR: Filter File not found")
        sys.exit(1)
    except PermissionError:
        print("ERROR: Permission denied while accessing Filter File")
        sys.exit(1)

    filterlist = [key.lower() for key in filterlist]

    filtered = Calendar()

    calendar = Calendar.from_ical(inputFile.read())

    for event in calendar.walk():
        if 'SUMMARY' in event.keys():
            summary = event['SUMMARY'].lower()
            if any(key in summary for key in filterlist):
                filtered.add_component(event)   # Adds component to resulting iCal file

    writeFile(filename=outputFilename, filecontents=filtered.to_ical())


def writeFile(filename, filecontents):
    filtered_file = open(filename, 'wb')
    sys.stdout.write(filecontents.decode('utf-8'))
    filtered_file.close()

if __name__ == "__main__":
    main(sys.argv[1:])