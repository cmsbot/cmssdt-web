#!/usr/bin/env python
# encoding: utf-8
"""
showTimeMemInfo.py

Created by Andreas Pfeiffer on 2009-04-17.
Copyright (c) 2009 CERN. All rights reserved.
"""

import cgi
import cgitb; cgitb.enable()

import sys, os, time, math
import getopt

import config

help_message = '''
The help message goes here.
'''

class LogAnalyzer(object):
    """docstring for LogAnalyzer"""
    def __init__(self, path=None, arch=None):
        super(LogAnalyzer, self).__init__()
        self.arch = arch
        if not self.arch:
            self.arch = 'slc4_ia32_gcc345'
        self.logPath = path
        if not self.logPath:
            self.logPath = config.siteInfo['qaPath']+'perfMatrix/'
            if not os.path.exists(self.logPath):
                self.logPath = '/Users/ap/Sites/perfMatrix/'
                
        self.reset()
        
    def reset(self):
        """docstring for reset"""

        self.infoMap = {}
        self.timeMap = {}
        self.fNameMap = {}
    
    def extractInfo(self, fileName=""):
        """docstring for extractInfo"""

        vmem = 0
        rss  = 0
        evtId = 0
        tevt = [0,0,0]
        startFound = False
        sumTime  = [0,0,0]
        sumTime2 = [0,0,0]
        inFile = open(fileName, 'r')
        evts = 0
        for line in inFile.xreadlines():
            if '%MSG-w' in line:
                startFound = True
            if startFound and '%MSG' in line and not '%MSG-w' in line:
                startFound = False
            
            #     MemoryCheck: event : VSIZE 984.438 0 RSS 700.746 0
            if startFound and 'MemoryCheck' in line[:len('MemoryCheck')]:
                words = line.split()
                vmem = float(words[4])
                rss  = float(words[7])
            
            #     TimeEvent> 20 1 5.72303 5.72213 249.465
            if 'TimeEvent> ' in line[:len('TimeEvent> ')]:
                if 'TimeEvent> 1 1 ' not in line[:20]:
                    evts += 1
                    words   = line.split()
                    evtId   = int(words[1])
                    tevt[0] = float(words[3])
                    tevt[1] = float(words[4])
                    tevt[2] = float(words[5])
                    for i in range(3):
                        sumTime[i] += tevt[i]
                        sumTime2[i] += tevt[i]*tevt[i]
                    
        inFile.close()
        
        if evts == 0: return

        avgTime = [0,0,0]
        sigTime = [0,0,0]
        for i in range(3):
            avgTime[i] = sumTime[i]/float(evts)
            sigTime[i] = math.sqrt( (sumTime2[i])/float(evts) - (avgTime[i]*avgTime[i]) )
            
        path, name = os.path.split(fileName)

        rel = path.split('/')[-3]
        if rel not in self.infoMap.keys(): self.infoMap[rel] = []

        relTime = self.getTime(rel)
        self.timeMap[relTime] = rel

        rawSize  = -1
        recoSize = -1
        try:
            filename = path+'/step1.root'
            if not os.path.exists(filename): filename = path+'/raw.root'
            rawStat = os.stat(filename)
            rawSize = float(rawStat.st_size)/1024./1024.
        except :
            pass
        try:
            filename = path+'/step2.root'
            if not os.path.exists(filename): filename = path+'/reco.root'
            recoStat = os.stat(filename)
            recoSize = float(recoStat.st_size)/1024./1024.
        except :
            pass

        name = name.replace('.log', '')
        # self.infoMap[rel].append( (name, evts, vmem, rss, tevt, rawSize, recoSize, sigTime) )
        self.infoMap[rel].append( (name, evts, vmem, rss, avgTime, rawSize, recoSize, sigTime) )
        self.fNameMap[rel] = fileName

        return

    def getTime(self, rel):
        """docstring for getTime"""
        cycle, stamp = rel.rsplit('_',1)
        yr, mon, day, hr = [int(x) for x in stamp[:-2].split('-')]
        import datetime
        timeStamp = datetime.datetime(yr, mon, day, hr)
        return time.mktime(timeStamp.timetuple())
        
    
    def showInfo(self):
        """docstring for showInfo"""

        print '<pre>'		
        #print '       release               nevt      vmem,    rss              time(sec)             raw (MB)  reco (MB)'
        print '       release               nevt      vmem,    rss                       avg time(sec)(ignoring 1st ev)                 raw (MB)  reco (MB)'
		
        #for name, info in self.infoMap.items():
        stampList = self.timeMap.keys()
        stampList.sort()
        for relTime in stampList:
            name = self.timeMap[relTime]
            info = self.infoMap[name]
            baseUrl = config.siteInfo['OutHtml']+'/perfMatrix/'+self.arch+'/'
            link = '<a href="'+baseUrl+self.fNameMap[name]+'">'+name+'</a>'
            print link,
            for item in info:
                print '  %3d    %7.2f  %7.2f ' % (item[1:4]),
                #print '  %7.3f  %7.3f  %8.2f ' %  (item[4][0],item[4][1],item[4][2]),
                print '  %7.3f +- %7.3f  %7.3f +- %7.3f  %8.2f +- %8.2f ' %  (item[4][0],item[7][0], item[4][1],item[7][1], item[4][2],item[7][2]),
                print '  %7.2f  %7.2f  ' %  item[5:7]

        print '</pre>'		
    
    def haveCycleInfo(self, cycle):
        """docstring for haveCycleInfo"""
        entries = os.listdir('.')
        for item in entries:
            if cycle in item: return True
        return False
        
    def analyze(self):
        """docstring for analyze"""
        
        startDir = os.getcwd()
        
        form = cgi.FieldStorage()
        ## cgi.print_form(form)
        relReq = '3_1_X'
        if form.has_key('rel') :
            relReq = form['rel'].value            
        arch = self.arch
        if form.has_key('arch'):
            arch = form['arch'].value
            self.arch = arch
            
        try:    
            os.chdir( os.path.join(self.logPath, arch) )
        except:
            print "Content-Type: text/html" 
            print '\n'
            print "<html> <head> </head> <body>"
            print "Error no info available for ", relReq, ' on ', arch
            print "</body></html> "
            return
            
        print "Content-Type: text/html" 
        print '\n'
        print "<html> <head> </head> <body>"
        if not self.haveCycleInfo(relReq):
            print "Error no info available for ", relReq, ' on ', arch
            print "</body></html> "
            return
        
        import glob
        
        print '<hr /><br />'

        # MinBias first:
        logFileList = glob.glob('./'+relReq+'*/perfMat/[1_,1.0_]*/step1_*log')
        print "step1_ProdMinBias+RECOPROD1"
        for logFile in logFileList:
            # print "checking ", logFile
            self.extractInfo(logFile)
        self.showInfo()
        self.reset()
        print '<hr /><br />'

        logFileList = glob.glob('./'+relReq+'*/perfMat/[1_,1.0_]*/step2_*log')
        print "step2_ProdMinBias+RECOPROD1"
        for logFile in logFileList:
            # print "checking ", logFile
            self.extractInfo(logFile)
        self.showInfo()
        self.reset()
        print '<hr /><br />'
        
        # TTbar now
        logFileList = glob.glob('./'+relReq+'*/perfMat/[2_,2.0_]*/step1_*log')
        print 'step1_ProdTTbar+RECOPROD1+ALCATT1'
        for logFile in logFileList:
            # print "checking ", logFile
            self.extractInfo(logFile)
        self.showInfo()
        self.reset()
        print '<hr /><br />'

        logFileList = glob.glob('./'+relReq+'*/perfMat/[2_,2.0_]*/step2_*log')
        print 'step2_ProdTTbar+RECOPROD1+ALCATT1'
        for logFile in logFileList:
            # print "checking ", logFile
            self.extractInfo(logFile)
        self.showInfo()
        self.reset()
        print '<hr /><br />'

        print '</body></html>'
        
class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "topDir="])
		except getopt.error, msg:
			raise Usage(msg)
		
		# option processing
		topDir = None
		for option, value in opts:
			if option == "-v":
				verbose = True
			if option in ("-h", "--help"):
				raise Usage(help_message)
			if option in ("-o", "--topDir"):
				topDir = value
		
		la = LogAnalyzer(topDir)
		la.analyze()
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		print >> sys.stderr, "\t for help use --help"
		return 2


if __name__ == "__main__":
	sys.exit(main())
