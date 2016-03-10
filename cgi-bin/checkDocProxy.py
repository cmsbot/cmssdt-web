#!/usr/bin/env python

# make sure this is first to trap also problems in includes later
import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")

import os, sys, cgi, time, re

scriptPath = '/afs/cern.ch/cms/sdt/web/cgi-bin/'
if scriptPath not in sys.path:
    sys.path.append(scriptPath)

from Formatter import *

def doCheck () :

    form = cgi.FieldStorage()
    # cgi.print_form(form)
        
    inPath = None
    if form.has_key('inPath') :
        inPath = form['inPath'].value

    if not inPath.startswith('/data/sdt/buildlogs/') :
        print "wrong path!! ", inPath
        return

    sys.path.append('/afs/cern.ch/cms/sdt/internal/scripts')
    import checkDoc

    dc = checkDoc.DocuChecker()
    dc.checkAll(inPath)
    formatter=SimpleHTMLFormatter()
    dc.show( formatter )
    del formatter

    return

if __name__ == '__main__':
    doCheck()
    

