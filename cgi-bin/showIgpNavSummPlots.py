#!/usr/bin/env python26

import os, sys, time, re, urllib, cgi, httplib

import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")

scriptPath = '/var/www/cgi-bin/'
if scriptPath not in sys.path:
    sys.path.append(scriptPath)

# make sure we have the config info for the web pages
import config

# get the helpers to check the inputs from the web
from helpers import isValidRelease, isValidPlat, getValgrindErrors

class NavSumm(object):

    def __init__(self):
        pass
    
    # --------------------------------------------------------------------------------
    
    def showNavSumm(self):

        import getopt
        options = sys.argv[1:]
        try:
            opts, args = getopt.getopt(options, 'h',['help'])
        except getopt.GetoptError:
            usage()
            sys.exit(-2)

        pageTitle = 'CMSSW Integration Build QA page -- IgProf Navigator Overview'
        from  TWikiFormatter import TWikiFormatter
        formatter = TWikiFormatter(pageTitle)
        
        rel = None
    	form = cgi.FieldStorage()
    	release=''
    	arch=''
    	prodArch='slc5_ia32_gcc434'
    	if "release" in form and "arch" in form :
    	    release = form["release"].value
    	    arch = form["arch"].value
    	    
    	    if not isValidPlat(arch) or not isValidRelease(release):
    	        formatter.writeH3( "ERROR: Illegal arch ("+arch+") and/or release ("+release+") given. Aborting." )
    	        return
    	else :
    	    formatter.writeH3( "ERROR: no arch ("+arch+") or release ("+release+") given. Aborting." )
    	    return
    	
    	summary = False
    	if 'summaryOnly' in form :
    	    summary = True
    	
    	import datetime
    	import re
    	rc, yr,mon,day,hr = re.search('CMSSW_(\d+_\d+|\d+_\d+_.+)_X_(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)\d\d',release).groups()
    	buildDate = datetime.date(int(yr), int(mon), int(day))
    	wkDay = buildDate.strftime('%a').lower()
    	stamp = rc.replace('_','.')+'-'+wkDay+'-'+hr
    	
    	import config
    	relpath = config.siteInfo['afsPath']+'/'+arch+'/www/'+wkDay+'/'+stamp+'/'+release+'/'
    	OutRel  = config.siteInfo['OutHtml']+'/'+release
    	OutArch = config.siteInfo['OutHtml']+'/'+release+'/'+arch
    	formatter.writeH1(pageTitle)
    	backToPortal = ' <a href="'+config.siteInfo['HtmlPath']+'showIB.html">Back to IB portal</a>'
    	formatter.writeH3(backToPortal)
    	
    	# --------------------------------------------------------------------------------
    	# first collect all information ...
        from makeIgNavSummPlots import IgNavSummaryPlotter
        ip = IgNavSummaryPlotter(release)
        import glob
        pngPath = config.siteInfo['OutPath']+'/'+release+'/'+arch
        pngFiles = glob.glob(pngPath+'/igp*.png')
        # if not pngFiles:
        formatter.write("creating plots ...")
        ip.makeAllPlots()
        pngFiles = glob.glob(pngPath+'/igp*.png')

    	formatter.write('<h4>Click on any plot to zoom in, double-click to reset size</h4>')
    	
        iTypes = ['PerfTicks', 'MEM_TOTAL', 'MEM_LIVE(mid)', 'MEM_LIVE(end)']
        formatter.startTable([1,2,3,4],['candle']+iTypes)
        for candle in ip.candleNames:
            row = [candle]
            for infoType in iTypes:
                pngName = '/igp_'+candle+'_'+infoType.replace(' ','-').replace('-calls','').replace('-counts','')+'.png'
                if pngPath+pngName not in pngFiles:
                    formatter.write('ERROR: no file found for '+pngPath+pngName+'<br/>')
                else:
                    pngUrl = pngPath.replace(config.siteInfo['OutPath'], config.siteInfo['OutHtml'])+pngName
                    pngID = pngName[1:].replace('igp_','').replace('.png','')
                    row.append('<img src="'+pngUrl+'" width="300px" height="200px" onclick="enlarge(this)" ondblclick="ensmall(this)" id="'+pngID+'">'+''+'</img>')
            formatter.writeRow(row)
        formatter.endTable()

if __name__ == "__main__" :

    im = NavSumm()
    im.showNavSumm()

