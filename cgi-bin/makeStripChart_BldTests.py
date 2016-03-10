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
	#arch=arch.replace('amd64','ia32') # amd64 is not support
	self.outPath=outpath
	self.arch=arch
        self.rel=getReleaseSeries(rel)
	 
    def mkStripChart(self) :

###
# Make dup dict strip charts
###
        data={'title':[],'dwnlError':[],'depViolations':[],'linkError':[],'pythonErr':[],'dictError':[],'miscError':[],'compError':[],'compWarn':[],'unitTestErrs':[]}
        server = Server()
        db = server.get_or_create_db("testdb")
        sk=[self.arch,self.rel,"showIBbld",["00","00","00","00"]]
        ek=[self.arch,self.rel,"showIBbld",["99","99","99","99"]]
        results = db.view("apps/by_release_filename",obj=None, wrapper=None,startkey=sk,endkey=ek)
        titleold=''
        for result in results:
#                print result
                ymdh=result['value'][3].split('-')
                title=ymdh[1]+'-'+ymdh[2]+'-'+ymdh[3][0]+ymdh[3][1]+'00'
                if title==titleold :
                        db.delete_doc(result['id'])
                else:
                        data['title'].append(title)
                        data['dwnlError'].append(float(result['value'][4]['dwnlError']))
                        data['depViolations'].append(float(result['value'][4]['depViolations']))
                        data['linkError'].append(float(result['value'][4]['linkError']))
                        data['pythonErr'].append(float(result['value'][4]['pythonErr']))
                        data['dictError'].append(float(result['value'][4]['dictError']))
                        data['miscError'].append(float(result['value'][4]['miscError']))
                        data['compError'].append(float(result['value'][4]['compError']))
                        data['compWarn'].append(float(result['value'][4]['compWarn']))
                        data['unitTestErrs'].append(float(result['value'][4]['unitTestErrs']))
                        titleold=title
#               print data['title']
        if len(data) ==0 :
                return False
        if len(data['title'])==0 :
                return False
#	print data
        import matplotlib.pyplot as plt
        ind=range( len(data['title']) )
        if len(data['title'])>10 :
            for x in ind :
                if x%10!=0 :
                    data['title'][x]=''

        plot, axs = plt.subplots(nrows=3)
        plot.suptitle('Build Errors')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['dictError'], '-o',label='Dictionary')
        ax.set_ylim( ymax=max(data['dictError'])+2.0 ,ymin=min(data['dictError'])-1.0 )
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['compError'], '-o',label='Compilation')
        ax.set_ylim(ymax=max(data['compError'])+2.0,ymin=min(data['compError'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['linkError'], '-o',label='Link')
        ax.set_ylim(ymax=max(data['linkError'])+2.0,ymin=min(data['linkError'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/26.png',format='png')

        plot, axs = plt.subplots(nrows=3)
        plot.suptitle('Build Errors')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['pythonErr'], '-o',label='Python')
        ax.set_ylim(ymax=max(data['pythonErr'])+2.0,ymin=min(data['pythonErr'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['compWarn'], '-o',label='Comp. Warnings')
        ax.set_ylim(ymax=max(data['compWarn'])+2.0,ymin=min(data['compWarn'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['dwnlError'], '-o',label='Download')
        ax.set_ylim(ymax=max(data['dwnlError'])+2.0,ymin=min(data['dwnlError'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/27.png',format='png')

        plot, axs = plt.subplots(nrows=3)
        plot.suptitle('Build Errors')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['miscError'], '-o',label='Misc')
        ax.set_ylim(ymax=max(data['miscError'])+2.0,ymin=min(data['miscError'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['unitTestErrs'], '-o',label='Download')
        ax.set_ylim(ymax=max(data['unitTestErrs'])+2.0,ymin=min(data['unitTestErrs'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['depViolations'], '-o',label='Dep. Violations')
        ax.set_ylim(ymax=max(data['depViolations'])+2.0,ymin=min(data['depViolations'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/28.png',format='png')



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
    cycle = "CMSSW_4_2_X"
    tgtDir = os.path.join( getLatestIB(cycle), arch)

    mbn = makeStripChart(cycle,arch,tgtDir)
    mbn.mkStripChart()

    
    
