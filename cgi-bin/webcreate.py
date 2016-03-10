#!/usr/bin/env python
import os, sys, time, re, urllib, cgi, httplib
import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")
scriptPath = '/var/www/cgi-bin/'
if scriptPath not in sys.path:
    sys.path.append(scriptPath)
#os.environ[ 'HOME' ] = '/tmp/'

class GetPath(object) :

	def __init__(self, formatter, relPath, release, arch) :
		import datetime
		self.relPath = relPath
		self.release = release
		self.arch = arch
		self.formatter = formatter
	
	
	def __del__(self):
		pass
	
	def MakeLog(self) :
		import config
		from makeDepMetrics import mkDepMetrics
		DepMetric = mkDepMetrics(self.formatter, self.arch, self.release, self.relPath)
		result = DepMetric.makeSummary()
		pkglist= DepMetric.packlist()
		outputlist = DepMetric.repack(pkglist)
		if result is not False :
			DepMetric.dropdown(outputlist)
		else :
			pass
			
		if not os.path.isdir( config.siteInfo['OutPath']+'/'+self.release) :
			os.system('mkdir -p '+ config.siteInfo['OutPath']+'/'+self.release)
			from makeCfgInfo import makeCfgInfo
			CA = makeCfgInfo(self.relPath+'cfgInfo.log',config.siteInfo['OutPath']+'/'+self.release)
			CA.AnalyzeLog()
			from makeScramInfo import makeScramInfo
			ScramLog = makeScramInfo(self.relPath+'scramInfo.log',config.siteInfo['OutPath']+'/'+self.release)
			ScramLog.AnalyzeLog()
			from makePyCheck import makePyCheck
			PycfgLog = makePyCheck(self.relPath+'testLogs/chkPyConf.log',config.siteInfo['OutPath']+'/'+self.release)
			PycfgLog.AnalyzeLog()
		else :
			pass
		if not os.path.isdir( config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch) :
			os.system('mkdir -p ' + config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch) 
			from makeBenchmark import makeBenchmark
			BenchMark = makeBenchmark(self.release[:11],self.arch, config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
			if BenchMark.mkBench() is not False :
				os.system('mv 1.png 2.png 3.png 4.png 5.png 6.png '+config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch)
	
def usage() :
	print 'usage : ',sys.argv[0]
	print ""
	return

if __name__ == "__main__" :
	from  TWikiFormatter import TWikiFormatter
	formatter = TWikiFormatter('CMSSW integration Build')
	import getopt
	options = sys.argv[1:]
	try:
		opts, args = getopt.getopt(options, 'h',['help','dummy'])
	except getopt.GetoptError:
		usage()
		sys.exit(-2)

	rel = None
	dummy = False
	for o,a in opts:
		if o in ('-h','--help'):
			usage()
			sys.exit()
		if o in('--dummy') :
			dummy = True
        import config
	if dummy is False :
		form = cgi.FieldStorage()
		relpath=''
		release=''
		arch=''
		if "relpath" in form  and "release" in form and "arch" in form :
			relpath = form["relpath"].value
			release = form["release"].value
			arch = form["arch"].value
		else :
			print 'Error. I can not find relpath, release or arch.\n'
		import config
                relpathX = relpath.replace("/data/sdt/buildlogs/","/")
		OutRel = config.siteInfo['OutHtml']+'/'+release
		OutArch = config.siteInfo['OutHtml']+'/'+release+'/'+arch
		formatter.writeH1("CMSSWIntegration Build QA Info")
		formatter.writeH3('Integration Build '+ release + ' for architecture '+arch)
		formatter.writeH2("Architecture dependency Information")
		formatter.write('<hr size=5px>\n')
		formatter.writeH3("Ignominy Information")
		from  webcreate import GetPath
		GP = GetPath(formatter, relpath, release, arch)
		GP.MakeLog()
		formatter.writeH3('Timing/Memory/FileSize information')
		formatter.startUl()
		formatter.writeLi('<a href='+ config.siteInfo['macms01Path']+'showTimeMemInfo.py?rel='+release[:11]+'&arch='+arch+'>Using the timing/momory services on the Production MinBias and TTbar RelVals</a>')
		formatter.endUl()
		formatter.startTable(2,['VMEM',''])
		formatter.writeRow(['<div style="text-align:center">This picture explain a information of using virtual memory</div>','<img src=\"'+OutArch+'/1.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="Virtual memory info" />'])
		formatter.writeRow(['<div style="text-align:center"><b>RSS</b></div>',''])
		formatter.writeRow(['<div style="text-align:center">This picture explain a information of using real size memory</div>','<img src=\"'+OutArch+'/2.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="RealSize  memory info" />'])
		formatter.writeRow(['<div style="text-align:center"><b>CPU Time</b></div>',''])
		formatter.writeRow(['<div style="text-align:center">This picture explain a information of cpu time</div>','<img src=\"'+OutArch+'/3.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="CPU Time info" />'])
		formatter.writeRow(['<div style="text-align:center"><b>RAW Size</b></div>',''])
		formatter.writeRow(['<div style="text-align:center">This picture explain a information of RAW  file size</div>','<img src=\"'+OutArch+'/5.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="RAW File size info" />'])
		formatter.writeRow(['<div style="text-align:center"><b>RECO Size</b></div>',''])
		formatter.writeRow(['<div style="text-align:center">This picture explain a information of Reco file size</div>','<img src=\"'+OutArch+'/6.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="RECO File size info" />'])
		formatter.endTable()
		formatter.writeH3("Results from (limited) performance suite")
		formatter.startUl()
		formatter.writeLi("Results for limited performance suite are not (yet?) available.")
		formatter.writeLi('<a href="'+ config.siteInfo['macms01Path']+'showValgrind.py?ib='+release+'&arch='+arch+'">Valgrind results')
		formatter.writeLi('Detailed results from the (limited performance suite are available on <a href=\"http://cern.ch/cms-sdt/qa/igprof/navigator\">the navigator page.</a>')
		formatter.endUl()
		formatter.writeH3("Log file from the BuildManager")
		formatter.startUl()
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/rc/'+relpathX+'../fullLog">Log file from the BuildManager (check here if something _completly_ fails).</a>')
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/rc/'+relpathX+'prebuild.log">Log file from "scram p" and CVS checkout.  </a>')
		formatter.endUl()
		formatter.writeH3("Diretory listing for the test logs")
		formatter.startUl()
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/rc/'+relpathX+'testLogs"> Directory listing for the test logs (unit-tests, all raw test logs)</a>')
		formatter.endUl()
		formatter.writeH2("Architecture Independency Information")
		formatter.write('<hr size=5px>\n')
		formatter.writeH3("Info on scram warnings and errors")
		formatter.startUl()
		formatter.writeLi('<a href="../intbld/scramInfo.html">Info on scram warnings and errors </a>')
		formatter.endUl()
		formatter.writeH3("Number of old-style configuration files")
		formatter.startUl()
		formatter.writeLi("Number of old-style configuration files(*.cff, *.cfi, *.cfg) in release")
		formatter.endUl()
		formatter.startTable(2,['Configuration Checking','Graph'])
		formatter.writeRow(['<a href="http://cern.ch/cms-sdt/rc/'+relpathX+'cfgInfo.log" > Detail</a>','<img src=\"'+OutRel+'/cfgInfo.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="Virtual memory info" />'])
		formatter.endTable()
		formatter.writeH3("Log file for checking Python Configuration files")
		formatter.startUl()
		formatter.writeLi("Log file for checking Python Configuration files in release.")
		formatter.endUl()
		formatter.startTable(2,['Python Configuration Checking','Graph'])
		formatter.writeRow(['<a href="http://cern.ch/cms-sdt/rc/'+relpathX+'testLogs/chkPyConf.log"> Detail </a>','<img src=\"'+OutRel+'/ChkPy.png\" width=300px height=200px onclick="enlarge(this)" onmouseout="ensmall(this)" id="vmem" alt="Virtual memory info" />'])
		formatter.endTable()
		formatter.writeH3("Duplicate definitions of dictionaries")
		formatter.startUl()
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/cgi-bin/showDupDict.py/'+relpathX+'testLogs/dupDict-dup.log">Duplicate definitions of dictionaries as found in class_def.xml files</a>')
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/cgi-bin/showDupDict.py/'+relpathX+'testLogs/dupDict-lostDefs.log">Definition of dictionaries in the "wrong" library</a>')
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/cgi-bin/showDupDict.py/'+relpathX+'testLogs/dupDict-edmPD.log">Duplicate definitions of dictionaries as found in edmPlugins </a>')
		formatter.endUl()
		formatter.writeH3("Status of documentation")
		formatter.startUl()
		formatter.writeLi('<a href="http://cern.ch/cms-sdt/cgi-bin/checkDocProxy.py?inPath='+relpath+'/src">Status of documentation for each subsystem and package (takes a while)</a>')
		formatter.endUl()

		
	else :
		relpath='/data/sdt/buildlogs/slc5_amd64_gcc434/www/thu/3.6-thu-02/CMSSW_3_6_X_2010-02-11-0200/'
		release='CMSSW_3_6_X'
		arch='slc5_amd64_gcc434'
		from  webcreate import GetPath
		GP = GetPath(relpath, release, arch)
		GP.MakeLog()


