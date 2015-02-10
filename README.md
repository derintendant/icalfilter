ical
====

Script to filter events based on a keyword. When omitting the -i option, it reads from stdin, allowing to pipe e.g. a webcal via curl.
The filter file is a simple text file with one search term per line.
Output is done to stdout.

Usage
------

    filter.py -i input_file -f filter_file

