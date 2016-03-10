#!/usr/bin/env python

import os, sys, re
import glob

def getCmds(inDirName):

    if not os.path.exists(inDirName): return None
    
    wfRe  = re.compile(r'^(.+\s+to execute|)\s+cd (?P<wf>\d+\.?\d*_.*)\s*$')
    cmdRe = re.compile(r'^\s*(?P<cmd>(cmsDriver.py|dbs\s+search)\s+.*)\s*>\s+(?P<step>step\d+)_.*$')
    stepRe = re.compile(r'^.*?;\s*exit:\s*(?P<step>((\d+\s*)+)).*$')

    cmdMap = {}
    lastWf = ''
    maxSteps = 0
    for inFileName in glob.glob(inDirName+"/runall.log*"):
      logFile = open(inFileName, 'r')
      log = logFile.readlines()
      logFile.close()

      for line in log:
        stepMatch = stepRe.match(line)
        if stepMatch:
            steps = len(stepMatch.group('step').split())
            if steps > maxSteps: maxSteps = steps
	    continue
	   
        wfMatch  = wfRe.match(line)
        cmdMatch = cmdRe.match(line)

        if wfMatch:
            lastWf = wfMatch.group('wf')
            if lastWf not in cmdMap.keys():
                   cmdMap[lastWf] = {}

        if cmdMatch:
            if lastWf.strip() == '' :
                print "WARNING: found empty wf for ", line
                continue
            cmdMap[lastWf][cmdMatch.group('step')] = cmdMatch.group('cmd')

    return (cmdMap,maxSteps)

def show(cmdMap):

    if not cmdMap:
        print "no log file info found"
        return

    print "found ", len(cmdMap.keys()), 'workflows:'
    for wf, cmds in cmdMap.items():
        try:
            print '%30s : %s' % ( wf, cmds['step1'] )
        except KeyError:
            print "ERROR for wf, cmds", wf, cmds
        for step in ['step2', 'step3', 'step4']:
            if step in cmds:
                print '%30s : %s' % ( '' , cmds[step])

            
if __name__ == '__main__':

    (cm,maxStep) = getCmds('.')
    show(cm)
