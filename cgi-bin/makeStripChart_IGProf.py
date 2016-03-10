#!/usr/local/bin/python2.6
import os, re, sys
import math
import matplotlib
import pylab
import config
from helpers import getReleaseSeries

# sys.path.append('/usr/local/lib/python2.6/site-packages/couchdbkit-0.4.6-py2.6.egg')
from couchdbkit import *
import urllib2

class makeStripChart(object) :
    def __init__(self, rel,arch,outpath):
	self.outPath=outpath
	self.arch=arch
        self.rel=getReleaseSeries(rel)
	self.ser=self.rel[:-2]
 
    def mkStripChart(self) :

	data=[]
	data_create={'title':[], 'data':[]}
	hist=[]
	steps=[ "TTbar-GEN,FASTSIM,HLT:GRun-LowLumiPileUp-RAWSIM-MEM_LIVE",
			"TTbar-GEN,FASTSIM,HLT:GRun-LowLumiPileUp-RAWSIM-MEM_MAX",
			"TTbar-GEN,FASTSIM,HLT:GRun-LowLumiPileUp-RAWSIM-MEM_TOTAL",
			"TTbar-GEN,FASTSIM,HLT:GRun-LowLumiPileUp-RAWSIM-PERF_TICKS",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-LowLumiPileUp-RAWSIM-MEM_LIVE",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-LowLumiPileUp-RAWSIM-MEM_MAX",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-LowLumiPileUp-RAWSIM-MEM_TOTAL",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-LowLumiPileUp-RAWSIM-PERF_TICKS",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-NOPILEUP-RAWSIM-MEM_LIVE",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-NOPILEUP-RAWSIM-MEM_MAX",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-NOPILEUP-RAWSIM-MEM_TOTAL",
			"TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-NOPILEUP-RAWSIM-PERF_TICKS",
			"TTbar-HLT:GRun-LowLumiPileUp-RAWSIM-MEM_LIVE",
			"TTbar-HLT:GRun-LowLumiPileUp-RAWSIM-MEM_MAX",
			"TTbar-HLT:GRun-LowLumiPileUp-RAWSIM-MEM_TOTAL",
			"TTbar-HLT:GRun-LowLumiPileUp-RAWSIM-PERF_TICKS",
			"TTbar-HLT:GRun-NOPILEUP-RAWSIM-MEM_LIVE",
			"TTbar-HLT:GRun-NOPILEUP-RAWSIM-MEM_MAX",
			"TTbar-HLT:GRun-NOPILEUP-RAWSIM-MEM_TOTAL",
			"TTbar-HLT:GRun-NOPILEUP-RAWSIM-PERF_TICKS",
			"TTbar-RAW2DIGI,RECO-NOPILEUP-RECOSIM-MEM_LIVE",
			"TTbar-RAW2DIGI,RECO-NOPILEUP-RECOSIM-MEM_MAX",
			"TTbar-RAW2DIGI,RECO-NOPILEUP-RECOSIM-MEM_TOTAL",
			"TTbar-RAW2DIGI,RECO-NOPILEUP-RECOSIM-PERF_TICKS" ]

	for step in steps:
		import copy
        	y=copy.deepcopy(data_create)
        	data.append(y)
        	server = Server()
        	db = server.get_or_create_db("testdb")
		sk=[self.arch,self.rel,step,["00","00","00","00"]]
		ek=[self.arch,self.rel,step,["99","99","99","99"]]
   		results = db.view("apps/by_release_filename",obj=None, wrapper=None,startkey=sk,endkey=ek)
		titleold=''
		for result in results:
			ymdh=result['value'][3].split('-')
			title=ymdh[1]+'-'+ymdh[2]+'-'+ymdh[3][0]+ymdh[3][1]+'00'
			if title==titleold :
				db.delete_doc(result['id'])
			else:
	    	        	data[-1]['title'].append(title)
        	        	data[-1]['data'].append( float(result['value'][4]['cumulative']) )
				titleold=title

	if len(data) ==0 :
		return False
	if len(data[0]['title'])==0 :
		return False
	import matplotlib.pyplot as plt

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-GEN,FASTSIM,HLT:GRun-LowLumiPileUp-MC_XY_VZ-RAWSIM')

	ind=range( len(data[0]['title']) )
	if len(data[0]['title'])>10 :
       		for x in ind :
             		if x%10!=0 :
            	   		data[0]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[0]['data'], '-o',label='MEM_LIVE')
	ax.set_ylim( ymax=max(data[0]['data'])*1.01,ymin=min(data[0]['data'])*0.99 )
	ax.legend(loc=0)
		
	ind=range( len(data[1]['title']) )
	if len(data[1]['title'])>10 :
		for x in ind :
			if x%2!=0 :
                    		data[1]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[1]['title'],rotation=15,size='xx-small')
        ax.plot( data[1]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[1]['data'])*1.01,ymin=min(data[1]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[2]['title']) )
	if len(data[2]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[2]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[2]['title'],rotation=15,size='xx-small')
     	ax.plot( data[2]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[2]['data'])*1.01,ymin=min(data[2]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[3]['title']) )
	if len(data[3]['title'])>10 :
            for x in ind :
                if x%2!=0 :
                    data[3]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[3]['data'], '-o',label='PERF_TICKS')
	#ax.set_ylim(ymax=max(data[3]['data'])*1.01,ymin=min(data[3]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/41.png',format='png')

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-GEN,SIM,DIGI,L1,DIGI2RAW-LowLumiPileUp-MC_XY_VZ-RAWSIM')
	ind=range( len(data[0]['title']) )
	if len(data[4]['title'])>100 :
      		for x in ind :
               		if x%2!=0 :
               	   		data[4]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[4]['title'],rotation=15,size='xx-small')
	ax.plot( data[4]['data'], '-o',label='MEM_LIVE')
	ax.set_ylim( ymax=max(data[4]['data'])*1.01,ymin=min(data[4]['data'])*0.99 )
	ax.legend(loc=0)
	
	ind=range( len(data[5]['title']) )
	if len(data[5]['title'])>10 :
            for x in ind :
		if x%2!=0 :
               		data[5]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[5]['title'],rotation=15,size='xx-small')
        ax.plot( data[5]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[5]['data'])*1.01,ymin=min(data[5]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[6]['title']) )
	if len(data[6]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[6]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[6]['title'],rotation=15,size='xx-small')
     	ax.plot( data[6]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[6]['data'])*1.01,ymin=min(data[6]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[7]['title']) )
	if len(data[3]['title'])>10 :
            for x in ind :
                if x%2!=0 :
                    data[7]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[7]['title'],rotation=15,size='xx-small')
        ax.plot( data[7]['data'], '-o',label='PERF_TICKS')
	ax.set_ylim(ymax=max(data[7]['data'])*1.01,ymin=min(data[7]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/42.png',format='png')

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-HLT:GRun-LowLumiPileUp-STARTXY_VZ-RAWSIM')
	ind=range( len(data[8]['title']) )
	if len(data[8]['title'])>10 :
      		for x in ind :
              		if x%2!=0 :
              	   		data[8]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[8]['title'],rotation=15,size='xx-small')
	ax.plot( data[8]['data'], '-o',label='MEM_LIVE')
	ax.set_ylim( ymax=max(data[8]['data'])*1.01,ymin=min(data[8]['data'])*0.99 )
	ax.legend(loc=0)
	
	ind=range( len(data[9]['title']) )
	if len(data[9]['title'])>10 :
            for x in ind :
		if x%2!=0 :
               		data[9]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[9]['title'],rotation=15,size='xx-small')
        ax.plot( data[9]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[9]['data'])*1.01,ymin=min(data[9]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[10]['title']) )
	if len(data[10]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[10]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[10]['title'],rotation=15,size='xx-small')
     	ax.plot( data[10]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[10]['data'])*1.01,ymin=min(data[10]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[11]['title']) )
	if len(data[11]['title'])>10 :
            for x in ind :
                if x%2!=0 :
                    data[11]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[11]['title'],rotation=15,size='xx-small')
        ax.plot( data[11]['data'], '-o',label='PERF_TICKS')
	ax.set_ylim(ymax=max(data[11]['data'])*1.01,ymin=min(data[11]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/43.png',format='png')
	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-HLT:GRun-LowLumiPileUp-STARTXY_VZ-RAWSIM')
	ind=range( len(data[12]['title']) )
	if len(data[12]['title'])>10 :
        	for x in ind :
                	if x%2!=0 :
               	   		data[12]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[12]['title'],rotation=15,size='xx-small')
	ax.plot( data[12]['data'], '-o',label='MEM_LIVE')
	ax.set_ylim( ymax=max(data[12]['data'])*1.01,ymin=min(data[12]['data'])*0.99 )
	ax.legend(loc=0)
		
	ind=range( len(data[13]['title']) )
	if len(data[13]['title'])>10 :
            for x in ind :
		if x%2!=0 :
               		data[13]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[13]['title'],rotation=15,size='xx-small')
        ax.plot( data[13]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[13]['data'])*1.01,ymin=min(data[13]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[14]['title']) )
	if len(data[14]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[14]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[14]['title'],rotation=15,size='xx-small')
     	ax.plot( data[14]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[14]['data'])*1.01,ymin=min(data[14]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[15]['title']) )
	if len(data[15]['title'])>10 :
            for x in ind :
                if x%2!=0 :
                    data[15]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[15]['title'],rotation=15,size='xx-small')
        ax.plot( data[15]['data'], '-o',label='PERF_TICKS')
	ax.set_ylim(ymax=max(data[15]['data'])*1.01,ymin=min(data[15]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/44.png',format='png')
	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-HLT:GRun-NOPILEUP-STARTXY_VZ-RAWSIM')

	ind=range( len(data[16]['title']) )
	if len(data[16]['title'])>10 :
       		for x in ind :
               		if x%2!=0 :
              	   		data[16]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[16]['title'],rotation=15,size='xx-small')
	ax.plot( data[16]['data'], '-o',label='MEM_LIVE')
	ax.set_ylim( ymax=max(data[16]['data'])*1.01,ymin=min(data[16]['data'])*0.99 )
	ax.legend(loc=0)
	
	ind=range( len(data[17]['title']) )
	if len(data[17]['title'])>10 :
            for x in ind :
		if x%2!=0 :
               		data[17]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[17]['title'],rotation=15,size='xx-small')
        ax.plot( data[17]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[17]['data'])*1.01,ymin=min(data[17]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[18]['title']) )
	if len(data[18]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[18]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[18]['title'],rotation=15,size='xx-small')
     	ax.plot( data[18]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[18]['data'])*1.01,ymin=min(data[18]['data'])*0.99)
	ax.legend(loc=0)
	
	ind=range( len(data[19]['title']) )
	if len(data[19]['title'])>10 :
		for x in ind :
	        	if x%2!=0 :
	                	data[19]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[19]['title'],rotation=15,size='xx-small')
        ax.plot( data[19]['data'], '-o',label='PERF_TICKS')
	ax.set_ylim(ymax=max(data[19]['data'])*1.01,ymin=min(data[19]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/45.png',format='png')
	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('TTbar-RAW2DIGI,RECO-NOPILEUP-MC_XY_VZ-RECOSIM')

	ind=range( len(data[20]['title']) )
	if len(data[20]['title'])>10 :
    		for x in ind :
              		if x%2!=0 :
	      	   		data[20]['title'][x]=''
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[20]['title'],rotation=15,size='xx-small')
	ax.plot( data[20]['data'], '-o',label='MEM_LIVE')
#	ax.set_ylim( ymax=max(data[20]['data'])*1.01,ymin=min(data[20]['data'])*0.99 )
	ax.legend(loc=0)
	
	ind=range( len(data[21]['title']) )
	if len(data[21]['title'])>10 :
		for x in ind :
			if x%2!=0 :
                   		data[21]['title'][x]=''
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[21]['title'],rotation=15,size='xx-small')
	ax.plot( data[21]['data'], '-o',label='MEM_MAX')
	ax.set_ylim(ymax=max(data[21]['data'])*1.01,ymin=min(data[21]['data'])*0.99)
	ax.legend(loc=0)
	
	ind=range( len(data[22]['title']) )
	if len(data[22]['title'])>10 :
       	    for x in ind :
                if x%2!=0 :
       	            data[22]['title'][x]=''
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[22]['title'],rotation=15,size='xx-small')
     	ax.plot( data[22]['data'], '-o',label='MEM_TOTAL')
	ax.set_ylim(ymax=max(data[22]['data'])*1.01,ymin=min(data[22]['data'])*0.99)
	ax.legend(loc=0)

	ind=range( len(data[23]['title']) )
	if len(data[23]['title'])>10 :
            for x in ind :
                if x%2!=0 :
                    data[23]['title'][x]=''
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[23]['title'],rotation=15,size='xx-small')
        ax.plot( data[23]['data'], '-o',label='PERF_TICKS')
	#ax.set_ylim(ymax=max(data[23]['data'])*1.01,ymin=min(data[23]['data'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/46.png',format='png')


def getLatestIB(cycle):

    import time
    tgtDir = ''
    latest = 9999999
    now = time.time()
    host,domain = config.getHostDomain()
    ibTopDir = config.sitesInfo[host]['OutPath']
    for ibDir in os.listdir( ibTopDir ):
        if not ibDir.startswith(cycle): continue
        statinfo = os.stat(  os.path.join(ibTopDir,ibDir) )
        if now - statinfo.st_ctime < latest:
            latest = now - statinfo.st_ctime
            tgtDir = os.path.join(ibTopDir,ibDir)

    return tgtDir

if __name__=="__main__" :

    arch = "slc5_amd64_gcc434"
    cycle = "CMSSW_4_3_X"
    tgtDir = os.path.join( getLatestIB(cycle), arch)

    mbn = makeStripChart(cycle,arch,tgtDir)
    mbn.mkStripChart()
 
    
    #mbn = makeStripChart ('1')
