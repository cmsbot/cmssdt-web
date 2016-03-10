#!/usr/bin/env bash

# to make sure the page is visible most of the time, even during update,
# we first write to a temporary file, then move this in place.

/data/sdt/SDT/cgi-bin/showIB.py | grep -v 'Content-Type' >/data/sdt/SDT/html/showIB.html-tmp
mv /data/sdt/SDT/html/showIB.html-tmp /data/sdt/SDT/html/showIB.html

