#!/usr/bin/env python

import os, sys, glob, time
import config
from helpers import archList

def ageOfBuild(release):
    import datetime
    import re
    searchResult = re.search('CMSSW_(\d+_\d+|\d+_\d+_.+)_X_(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)\d\d',release)
    if not searchResult:
        print "STRANGE: no search result found for ", release
        return 99
    
    rc, yr,mon,day,hr = searchResult.groups()
    buildDate = datetime.datetime(int(yr), int(mon), int(day))
    return (datetime.datetime.now() - buildDate).days

topDir = config.siteInfo['OutPath']
os.chdir(topDir)

fullList = glob.glob('CMSSW_*')

webLogCGIBase =  config.siteInfo['CgiHtmlPath']
chkTime = time.time()

os.system('mv -f ./logs/refreshQASummaries.log ./logs/refreshQASummaries.log-bkp')
logFile = open('./logs/refreshQASummaries.log','w')
for item in fullList:
    for arch in archList:

        # build, arch = item.split('/')
        build = item
        if ageOfBuild(build) > 2: continue # only process the IB of the last N days

    	import urllib2
    	qaSummPageURL = webLogCGIBase+'newQA.py?'
    	qaSummPageURL += 'arch='+arch+'&release='+build+'&summaryOnly=1'
    	
        try:
            page = urllib2.urlopen(qaSummPageURL)
            lines = page.readlines()
            page.close()
        except:
            msg = "Error processing " +qaSummPageURL+ ' for '+ item+'\n'
            logFile.write(msg)
            print msg
            continue
    	
    	logFile.write( "processed " + item + '\n')

logFile.close()
