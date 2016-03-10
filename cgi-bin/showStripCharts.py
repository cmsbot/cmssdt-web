#!/usr/local/bin/python2.6

import os, sys, time, re, urllib, cgi, httplib

import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")

scriptPath = '/var/www/cgi-bin/'
if scriptPath not in sys.path:
    sys.path.append(scriptPath)

# make sure we have the config info for the web pages
import config

# get the helpers to check the inputs from the web
from helpers import isValidRelease, isValidPlat, getValgrindErrors

class GetPath(object) :

    def __init__(self, formatter, relPath, release, arch) :
        import datetime
        self.relPath = relPath
        self.release = release
        self.arch = arch
        self.prodArch = 'slc5_ia32_gcc434'
        self.formatter = formatter

        self.cfgInfo   = None
        self.scramInfo = None
        self.pycfgInfo = None

        self.igInfo = None

    def __del__(self):
        pass


    def MakeLog(self) :
        if not os.path.isdir( config.siteInfo['OutPath']+'/'+self.release) :
            os.system('mkdir -p '+ config.siteInfo['OutPath']+'/'+self.release)

	outpath=config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch

        if not os.path.isdir( outpath ) :
            os.system('mkdir -p ' + outpath ) 


        if not os.path.exists( outpath+'/16.png' ) or time.time()-os.path.getmtime(outpath+'/16.png')>43200 :
	        from makeBenchmark_w_CouchDB import makeBenchmark
       		BenchMark = makeBenchmark(self.release,self.arch, outpath )
       		BenchMark.mkBench()
		os.system('mv 11.png 12.png 13.png 14.png 15.png 16.png '+outpath)

        if not os.path.exists( outpath+'/21.png') or time.time()-os.path.getmtime(outpath+'/21.png')>7200 :
	        from makeStripChart_DirSize import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 21.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/22.png') or time.time()-os.path.getmtime(outpath+'/22.png')>7200 :
	        from makeStripChart_DupDict import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 22.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/23.png') or time.time()-os.path.getmtime(outpath+'/23.png')>7200 : 
	        from makeStripChart_AddOn import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 23.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/24.png') or time.time()-os.path.getmtime(outpath+'/24.png')>7200 :
	        from makeStripChart_RelVals import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 24.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/26.png') or time.time()-os.path.getmtime(outpath+'/26.png')>7200 :
	        from makeStripChart_BldTests import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 26.png 27.png 28.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/29.png') or time.time()-os.path.getmtime(outpath+'/29.png')>18000 :
	        from makeStripChart_Valgrind import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 29.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/30.png') or time.time()-os.path.getmtime(outpath+'/30.png')>7200 :
	        from makeStripChart_CRViol import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 30.png 31.png'+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
        if not os.path.exists( outpath+'/40.png') or time.time()-os.path.getmtime(outpath+'/40.png')>7200 :
	        from makeStripChart_IGProf import makeStripChart
       		StripChart = makeStripChart(self.release,self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
       		StripChart.mkStripChart()
		os.system('mv 40.png 41.png 42.png 43.png 44.png 45.png 46.png 47.png 48.png'+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)

class InfoMaker(object):

    def __init__(self):
        self.GP = None

    def showQAInfo(self):

        import getopt, re
        options = sys.argv[1:]
        try:
            opts, args = getopt.getopt(options, 'h',['help'])
        except getopt.GetoptError:
            usage()
            sys.exit(-2)

        from  TWikiFormatter import TWikiFormatter

        rel = None
    	form = cgi.FieldStorage()
    	release=''
    	arch=''
    	prodArch='slc5_ia32_gcc434'
        if "release" in form and "arch" in form :
            release = form["release"].value
            arch = form["arch"].value
            print "Release:",release
            rc,rcex,yr,mon,day,hr = re.search('CMSSW_(\d+_\d+(_.+|))_X_(\d\d\d\d)-(\d\d)-(\d\d)-(\d\d)\d\d',release).groups()
            series = 'CMSSW_'+rc+'_X'
            release=series+'_2000-01-01-0000'
     	    
    	    if not isValidPlat(arch) or not isValidRelease(release):
                formatter = TWikiFormatter('CMSSW Integration Build QA page',"")
    	        formatter.writeH3( "ERROR: Illegal arch ("+arch+") and/or release ("+release+") given. Aborting." )
    	        return
    	else :
    	    formatter.writeH3( "ERROR: no arch ("+arch+") or release ("+release+") given. Aborting." )
    	    return
    	
    	summary = False
    	if 'summaryOnly' in form :
    	    summary = True
    	
        formatter = TWikiFormatter('StripCharts', release=release)

    	import datetime
    	import re
    	buildDate = datetime.date(int(yr), int(mon), int(day))
    	wkDay = buildDate.strftime('%a').lower()
    	stamp = rc.replace('_','.')+'-'+wkDay+'-'+hr
    	
    	import config
    	relpath = config.siteInfo['afsPath']+'/'+arch+'/www/'+wkDay+'/'+stamp+'/'+release+'/'
    	OutRel  = config.siteInfo['OutHtml']+'/'+release
    	OutArch = config.siteInfo['OutHtml']+'/'+release+'/'+arch
    	formatter.writeH1("Strip Charts")
    	backToPortal = '<a href="'+config.siteInfo['CgiHtmlPath']+'showIB.py">Back to IB portal</a>'
	formatter.writeH3('Release series '+ series + ' for architecture '+arch)
	formatter.writeH3 (backToPortal)
    	
    	# --------------------------------------------------------------------------------
    	# first collect all information ...
    	
    	# prepare the plots and other info
    	self.GP = GetPath(formatter, relpath, release, arch)
    	self.GP.MakeLog()
      
	# redo the collection for the prod arch as well if we're called for a different arch
        # but only for the items which are not architecture specific
        if arch != prodArch: 
            GP = GetPath(formatter, relpath, release, prodArch)
            GP.MakeLog()
    	
    	
    	
    	formatter.write('<p>Click on any plot to zoom in, double-click to reset size</p>')
    	
    	formatter.startTable(2,['VMEM','RSS','CPU time'])
    	pngPath = OutArch.replace(config.siteInfo['OutHtml'],config.siteInfo['OutPath'])
    	msgPngNA = "Not (yet) available "
    	msgPng = []
#    	if os.path.exists(pngPath+'/11.png') :
 	msgPng.append( '<img src=\"'+OutArch+'/11.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="Virtual memory info" />')
#    	else:
#    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/12.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/12.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="RealSize  memory info" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/13.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/13.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="cpu" alt="CPU Time info" />')
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
    	formatter.endTable()
    	
    	formatter.write("<br/>")
    	formatter.startTable(2,['RAW size','RECO size','Dir size'])
    	msgPng = []
    	if os.path.exists(pngPath+'/15.png'):
    	    msgPng.append('<img src=\"'+OutArch+'/15.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="RAW File size info" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/16.png'):
    	    msgPng.append('<img src=\"'+OutArch+'/16.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="RECO File size info" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/21.png'):
    	    msgPng.append('<img src=\"'+OutArch+'/21.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="dir size info" />')
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
	formatter.endTable()

    	formatter.write("<br/>")
    	formatter.startTable(2,['Duplicate Dictionaries','Add On Tests','Rel Vals'])
    	msgPng = []
    	if os.path.exists(pngPath+'/22.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/22.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="Duplicate Dictionaries" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/23.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/23.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="Add On Tests" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/24.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/24.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="cpu" alt="Rel Vals" />')
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
    
	formatter.endTable()

    	formatter.write("<br/>")
    	formatter.startTable(2,['Build Errors','Build Errors','BuildError'])
    	msgPng = []
    	if os.path.exists(pngPath+'/26.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/26.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="Build Errors" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/27.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/27.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="Build Errors" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/28.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/28.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="cpu" alt="Build Errors" />')
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
    
	formatter.endTable()

    	formatter.write("<br/>")
    	formatter.startTable(2,['Valgrind Errors','Code Rule Violations','Code Rule Violations'])
    	msgPng = []
    	if os.path.exists(pngPath+'/29.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/29.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="Valgrind Errors" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/30.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/30.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="Code Rule Violations" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/31.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/31.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="cpu" alt="Code Rule Violations" />')
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
    
	formatter.endTable()
    	
    	formatter.write("<br/>")
    	formatter.startTable(2,['IGProf','IGProf'])
    	msgPng = []
    	if os.path.exists(pngPath+'/41.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/41.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="IGProf" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/42.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/42.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="IGProf" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
	formatter.endTable()
    	    

    	formatter.write("<br/>")
    	formatter.startTable(2,['IGProf','IGProf'])
    	msgPng = []
    	if os.path.exists(pngPath+'/43.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/43.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="IGProf" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/44.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/44.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="IGProf" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
	formatter.endTable()
    	    
    	formatter.write("<br/>")
    	formatter.startTable(2,['IGProf','IGProf'])
    	msgPng = []
    	if os.path.exists(pngPath+'/45.png') :
    	    msgPng.append( '<img src=\"'+OutArch+'/45.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="vmem" alt="IGProf" />')
    	else:
    	    msgPng.append(msgPngNA)
    	if os.path.exists(pngPath+'/46.png') :
    	    msgPng.append('<img src=\"'+OutArch+'/46.png\" width=300px height=200px onclick="enlarge(this)" ondblclick="ensmall(this)" id="rss" alt="IGProf" />')    
    	else:
    	    msgPng.append(msgPngNA)
    	formatter.writeRow( msgPng )
	formatter.endTable()
    	    
    	    
    def usage(self) :
        print 'usage : ',sys.argv[0]
        print ""
        return

if __name__ == "__main__" :

    im = InfoMaker()
    im.showQAInfo()

