#!/usr/bin/env python2

import os

# ================================================================================

class Reporter :

    "print outs to web pages, html et al ... "
    
    # --------------------------------------------------------------------------------
    def __init__(self) :
        self.headersDone = False
        return

    # --------------------------------------------------------------------------------
    def __del__(self) :
        if self.headersDone :
            self.trailers()
        else: # in case nothing has been written yet, output an empty page ...
            print "Content-Type: text/html"     # HTML is following
            print                               # blank line, end of headers
            print "<html> "
            print "</html> "
        
        return

    # --------------------------------------------------------------------------------
    def error(self, msgs) :
        self.headers()
        self.writeOut( ["<H1>Error</H1>"] + msgs )
        return

    # --------------------------------------------------------------------------------
    def warning(self, msgs) :
        self.headers()
        self.writeOut( ["<H1>Warning</H1>"] + msgs )
        return

    # --------------------------------------------------------------------------------
    def info(self, msgs) :
        self.headers()
        self.writeOut( ["<H1>Info</H1>"] + msgs )

        return

    # --------------------------------------------------------------------------------
    def write(self, msgs, bold=False) :
        self.headers()
        self.writeOut( msgs, bold )

        return

    # --------------------------------------------------------------------------------
    def writeRaw(self, msgs) :
        for line in msgs :
            print line
        return
	
    # --------------------------------------------------------------------------------
    def headers(self, title="CMS SDT") :
        # make sure to write the headers only once ...
        if not self.headersDone :
            print "Content-Type: text/html"     # HTML is following
            print                               # blank line, end of headers
        
            print "<html> "
            print "<head> "
            print "<TITLE>" + title + "</TITLE>"
            print "</head> "
            print "<body>"
        self.headersDone = True

        return

    # --------------------------------------------------------------------------------
    def writeOut(self, msgs, bold=False) :
        print "<p>"
        if bold:
            print "<b>"

        for line in msgs :
            print line

        if bold:
            print "</b>"
        print "</p>"
        return
    
    # --------------------------------------------------------------------------------
    def trailers(self) :
        # write only if headers have been written ...
        if self.headersDone :
            print "</body>"
            print "</html> "
            pass
        return
    # --------------------------------------------------------------------------------

