#!/usr/bin/env python

# make sure this is first to trap also problems in includes later
import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")

import os, sys, cgi, time, re

scriptPath = '/afs/cern.ch/cms/sdt/web/cgi-bin/'
if scriptPath not in sys.path:
    sys.path.append(scriptPath)

import Formatter

def cleanPath(path):
    return os.path.normpath(os.path.join('/',path))

class LogViewer(object):

    def __init__(self, formatter):

        self.formatter = formatter
        
        self.buildList = {}
        self.platCycleMap = {}
        
        self.platList = ['slc4_ia32_gcc345', 'slc4_amd64_gcc345', 'slc4_ia32_gcc412']
        
        self.webLogDirBase = '/data/sdt/buildlogs/'
        self.webLogDir = None # to be set up as base+plat+'/www/'
        
        self.webLogURLBase = 'http://cern.ch/cms-sdt/rc/'
        self.days = [ 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun' ]

        self.cycList = ['3.1', '3.0', '2.2']

        return

    # --------------------------------------------------------------------------------

    def getSummaryLogInfo(self, path):
        passed  = []
        failed  = []
        timeout = []

        logFileName = path+'/runall-report.log'
            
        try:
            sumLog = open(logFileName, 'r')
            lines = sumLog.readlines()
            sumLog.close()
        except:
            # .formatter.writeH3( "ERROR opening or reading logFile: "+logFileName )
            return passed, failed, timeout
        
        logRe = re.compile('\s*(cmsDriver.py\s*.*?) : ([PF].*)$')
        
        for line in lines:
            logMatch = logRe.match(line)
            if logMatch:
                job = logMatch.group(1)
                res = logMatch.group(2)
                if 'step2' in job or 'step3' in job: continue

                if 'PASSED' in res: passed.append(job.replace(' ','_'))

                if 'FAILED' in res:
                    exitCode = int(res.split()[-1])
                    if exitCode == 36608 :
                        timeout.append(job.replace(' ','_'))
                    else:
                        failed.append(job.replace(' ','_'))

        return passed, failed, timeout
    
    # --------------------------------------------------------------------------------

    
    def getSummaryLogInfo23(self, path, gt):
        passed = {'step2' : [], 'step3' : [] }
        failed = {'step2' : [], 'step3' : [] }

        logFileName = path+'/runall-report-step23-'+gt+'.log'
            
        try:
            sumLog = open(logFileName, 'r')
            lines = sumLog.readlines()
            sumLog.close()
        except:
            print "ERROR reading file !!", logFileName
            # .formatter.writeH3( "ERROR opening or reading logFile: "+logFileName )
            return passed, failed
        
        logRe = re.compile('\s*(.*).root : Step2-([PF].*?)\s*Step3-([PFN].*?)-\s*time:.*')
        
        for line in lines:
            logMatch = logRe.match(line)
            # print "checking line", line,'<br/>'
            if logMatch:
                job = logMatch.group(1)
                res2 = logMatch.group(2)
                res3 = logMatch.group(3)

                if 'PASSED' in res2: passed['step2'].append(job.replace(' ','_'))
                if 'PASSED' in res3: passed['step3'].append(job.replace(' ','_'))

                if 'FAILED' in res2: failed['step2'].append(job.replace(' ','_'))
                if 'FAILED' in res3: failed['step3'].append(job.replace(' ','_'))


        return passed, failed
    
    # --------------------------------------------------------------------------------

    def showLogs(self):

        pathReq = ""
        try:
            scriptName = os.environ["SCRIPT_NAME"]
            requestURI = os.environ["REQUEST_URI"]
            pathReq = cleanPath( requestURI.replace(scriptName,'') )

        except:
            pathReq = sys.argv[1]
            pass


        self.formatter.writeAnchor(ref='top')
        self.formatter.writeH2("CMSSW Integration Build test log viewer")

        topLogDir = '/data/sdt/buildlogs/'
        fullPath = topLogDir + pathReq
        normPath = os.path.normpath( fullPath )

        logBaseURL = 'http://cmssdt.cern.ch/SDT/html/rc/'

        self.formatter.write("Logs available in " + normPath)

        ib = normPath.split('/')[-2]
        self.formatter.writeH3('Integration Build ' + ib)

        passed1, failed1, timeout1 = self.getSummaryLogInfo(normPath)

        if not passed1 and not failed1 and not timeout1:
            self.formatter.writeH3("Test logs not yet available")
            return

        nPass1 = len(passed1)
        nFail1 = len(failed1)
        nTime1 = len(timeout1)

        pass23I, fail23I = self.getSummaryLogInfo23(normPath, 'IDEAL')

        if not pass23I and not fail23I :
            self.formatter.writeH3("Test logs (step23 IDEAL) not yet available")
        
        pass23S, fail23S = self.getSummaryLogInfo23(normPath, 'STARTUP')

        if not pass23S and not fail23S :
            self.formatter.writeH3("Test logs (step23 STARTUP) not yet available")

        p2i = len(pass23I['step2'])
        p3i = len(pass23I['step3'])
        f2i = len(fail23I['step2'])
        f3i = len(fail23I['step3'])

        p2s = len(pass23S['step2'])
        p3s = len(pass23S['step3'])
        f2s = len(fail23S['step2'])
        f3s = len(fail23S['step3'])
        
        self.formatter.startTable ( [15,15,15,15,15], ['Step','total', 'passed', 'failed', 'timeout'])
        self.formatter.writeRow(['step1'       , str(nPass1+nFail1+nTime1), str(nPass1), str(nFail1), str(nTime1)])
        
        self.formatter.writeRow(['step2/IDEAL'  , str( p2i+f2i ), str( p2i ), str( f2i ), 'N/A'])
        self.formatter.writeRow(['step3/IDEAL'  , str( p3i+f3i ), str( p3i ), str( f3i ), 'N/A'])
        self.formatter.writeRow(['step2/STARTUP', str( p2s+f2s ), str( p2s ), str( f2s ), 'N/A'])
        self.formatter.writeRow(['step3/STARTUP', str( p3s+f3s ), str( p3s ), str( f3s ), 'N/A'])
            
        self.formatter.endTable()

        self.formatter.writeH3('<a href="'+logBaseURL+pathReq+'/runall-report.log"> Summary log (runall-report.log) </a>')
        self.formatter.writeH3('<a href="'+logBaseURL+pathReq+'/runall-report-step23-IDEAL.log"> Summary log (runall-report-step23-IDEAL.log) </a>')
        self.formatter.writeH3('<a href="'+logBaseURL+pathReq+'/runall-report-step23-STARTUP.log"> Summary log (runall-report-step23-STARTUP.log) </a>')

        self.formatter.showLine()

        msgFail = '<a name="failed"> Failed tests step1: ('+str(nFail1)+') '
        msgFail += '</a>'
        self.formatter.writeH3(msgFail + ' <a href="#top"> back to top </a> ')
        for lineIn in failed1:
            line = lineIn.replace("'",'').replace('"','').replace('/', '_')
            outLine = '<a href="'+logBaseURL+pathReq+'/'+line+'.log"> '+line+' </a>'
            self.formatter.write(outLine + ' <br /><br />')

        for gt in ['IDEAL', 'STARTUP']:
            msgFail = 'Failed tests step23 '+gt+': ('  +str(f2i + f3i)+') '
            self.formatter.writeH3(msgFail)
            for step in ['step2', 'step3']:
                items = fail23I
                if 'STARTUP' in gt:
                    items = fail23S
                for lineIn in items[step]:
                    line = lineIn.replace("'",'').replace('"','').replace('/', '_')
                    line = gt+'/'+line+'.rootDir/cmsRun_'+step+'_'+gt+'_'+line
                    outLine = '<a href="'+logBaseURL+pathReq+'/'+line+'.log"> '+lineIn+' </a>'
                    self.formatter.write(outLine + ' <br /><br />')


        msgFail = 'Failed tests tep23 STARTUP: ('+str(f2s + f3s)+') '

        self.formatter.writeH3('<a name="timeout"> Tests (step1) timing out : ('+str(nTime1)+')</a> <a href="#top"> back to top </a> ')
        for lineIn in timeout1:
            line = lineIn.replace("'",'').replace('"','').replace('/','_')
            outLine = '<a href="'+logBaseURL+pathReq+'/'+line+'.log"> '+line+' </a>'
            self.formatter.write(outLine + ' <br /><br />')

        self.formatter.writeH3('<a name="passed"> Passed (step1) tests : ('+str(nPass1)+') </a> <a href="#top"> back to top </a> ')
        for lineIn in passed1:
            line = lineIn.replace("'",'').replace('"','').replace('/','_')
            line = line.replace("'",'').replace('"','')
            outLine = '<a href="'+logBaseURL+pathReq+'/'+line+'.log"> '+line+' </a>'
            self.formatter.write(outLine + ' <br /><br />')

        for gt in ['IDEAL', 'STARTUP']:
            msg = 'Passed tests step23 '+gt+': ('  +str(f2i + f3i)+') '
            self.formatter.writeH3(msg)
            for step in ['step2', 'step3']:
                self.formatter.writeH3("Step: "+step+' global tag: '+gt)
                items = pass23I
                if 'STARTUP' in gt:
                    items = pass23S
                for lineIn in items[step]:
                    line = lineIn.replace("'",'').replace('"','').replace('/', '_')
                    line = gt+'/'+line+'.rootDir/cmsRun_'+step+'_'+gt+'_'+line
                    outLine = '<a href="'+logBaseURL+pathReq+'/'+line+'.log"> '+lineIn+' </a>'
                    self.formatter.write(outLine + ' <br /><br />')

        return 

# ================================================================================

def main():

    style = """
    <style> table.header {
       background: #D1F9D1;
       color:  #990033;
    } </style>

    <style> td {
       text-align: center;
    } </style>

    <style> td.cellbold {
      font-weight : bold;
      background-color: #FFB875;
    } </style>

    <style> body {
       color:  #990033;
       link: navy;
       vlink: maroon;
       alink: tomato;
       background: #D1F9D1;
    } </style>
        """

    fmtr = Formatter.SimpleHTMLFormatter(title="Test Logs from CMSSW Integration Build", style=style)

    lv = LogViewer(fmtr)
    lv.showLogs()

    return


main()
