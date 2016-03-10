#!/usr/bin/env python
import os, re
import math
import matplotlib
# matplotlib.use('Agg')
import pylab
import cgitb; cgitb.enable() ## cgitb.enable(display=0, logdir=os.getcwd()+"/../cgi-logs/")

import config

# to find numpy and matplotlib
import sys
sys.path.insert(0,'/Library/Python/2.5/site-packages/')

from helpers import getStamp

class IgNavSummaryPlotter(object) :
    def __init__(self, rel, arch='slc5_ia32_gcc434'):
        self.data = None
        self.release = rel
        self.arch = arch

        day, stamp, cyc = getStamp(self.release)
        self.cycle = cyc
        
        self.outPath = config.siteInfo['OutPath']+'/'+self.release+'/'+self.arch
        if not os.path.exists(self.outPath):
            os.makedirs(self.outPath)

        self.candleNames = ["TTbar_GEN,SIM,DIGI,L1,DIGI2RAW_NOPILEUP",
                            "TTbar_GEN,FASTSIM_NOPILEUP",
                            "TTbar_HLT_NOPILEUP",
                            "TTbar_RAW2DIGI,RECO_NOPILEUP",
                            "TTbar_GEN,SIM,DIGI,L1,DIGI2RAW_LowLumiPileUp",
                            "TTbar_GEN,FASTSIM_LowLumiPileUp",
                            "TTbar_HLT_LowLumiPileUp",
                            "TTbar_RAW2DIGI,RECO_LowLumiPileUp",
                            ]

        self.infoTypes = ['PerfTicks counts', 'PerfTicks calls',
                          'MEM_TOTAL counts', 'MEM_TOTAL calls',
                          'MEM_LIVE(mid) counts','MEM_LIVE(mid) calls',
                          'MEM_LIVE(end) counts','MEM_LIVE(end) calls'
                          ]
            
    def readData(self):
        import config
        pklFileName = config.siteInfo['qaPath']+'/navigator-summary.pkl'
        pklIn = open(pklFileName,'r')
        from pickle import Unpickler
        upklr = Unpickler(pklIn)
        self.data = upklr.load()
        pklIn.close()

    def makeAllPlots(self):

        self.readData()
        
        candleNames = self.candleNames
        infoType    = self.infoTypes
        
        cycX = self.cycle.replace('.','_')
        f1 = {}
        for whatC in range(len(candleNames)):
            candleIn = candleNames[whatC]
            for candle, relInfo in self.data.items():
                if candle != candleIn : continue
                for rel, info in relInfo.items():
                    if len(info) != 8 : continue
                    if not rel.startswith('CMSSW_'+cycX): continue
                    for what in range(8):
                        key = candle+'_'+infoType[what].replace(' ','-')
                        if key not in f1.keys():
                            f1[key] = {}
                        f1[key][rel[6:]] = float(info[what])

        for candleIn in candleNames:
            # perfticks first, no second (calls) data
            iType = 'PerfTicks'
            key = candleIn+'_'+iType
            try:
                self.makePlot(iType, candleIn, f1[key+'-counts'], {})
            except KeyError:
                pass
            # now all the others, counts and calls
            for iType in ['MEM_TOTAL', 'MEM_LIVE(mid)', 'MEM_LIVE(end)']:
                key = candleIn+'_'+iType.replace(' calls','').replace(' counts','')
                try:
                    self.makePlot(iType, candleIn, f1[key+'-counts'], f1[key+'-calls'])
                except KeyError:
                    pass
    
    def makePlot(self, what, candle, info1, info2) :

        xVal  = []
        yVal1 = []
        yVal2 = []
        xLab  = []
        cnt = 0

        from operator import itemgetter
        sortedDetails = info1.items()
        sortedDetails.sort(key=itemgetter(0))
        for x,y in sortedDetails:
            xVal.append(x)
            yVal1.append(y)
            cnt += 1
            if cnt % 2 == 0 : xLab.append(x)
            else: xLab.append('')
        for x in xVal:
            for x2,y2 in info2.items():
                if x == x2: yVal2.append(y2)

	import matplotlib.pyplot as plt
        plt.title(candle)
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
	ax1.plot( yVal1, '-o',label=what+' counts')
	ax1.set_ylim(ymin=min(yVal1)*0.9, ymax=max(yVal1)*1.1)
        ax1.legend(loc=(0.6,0.9))
        
        if info2:
            ax2=ax1.twinx()
            ax2.plot( yVal2, 'g-o',label=what+' calls')
	    ax2.set_ylim(ymin=min(yVal2)*0.9, ymax=max(yVal2)*1.1)
            for t1 in ax2.get_yticklabels():
                t1.set_color('g')                
            ax2.legend(loc=(0.6,0.8))
            
	ax1.set_xticks( range(len(xLab)) )
        ax1.set_xticklabels( xLab,rotation=15)

	pylab.savefig(self.outPath+'/igp_'+candle+'_'+what.replace(' ','-')+'.png',format='png')
	plt.cla()

if __name__=="__main__" :
    ip = IgNavSummaryPlotter('CMSSW_3_8_X_2010-06-24-1300')
    ip.makeAllPlots()
    
