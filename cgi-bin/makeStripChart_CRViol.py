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
        data={'title':[],'catch':[],'flags':[],'pragma':[],'debug':[],'using':[],'copy':[]}
        server = Server()
        db = server.get_or_create_db("testdb")
        sk=[self.arch,self.rel,"crViol",["00","00","00","00"]]
        ek=[self.arch,self.rel,"crViol",["99","99","99","99"]]
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
                        data['catch'].append(float(result['value'][4]['catch']))
                        data['flags'].append(float(result['value'][4]['flags']))
                        data['pragma'].append(float(result['value'][4]['pragma']))
                        data['debug'].append(float(result['value'][4]['debug']))
                        data['using'].append(float(result['value'][4]['using']))
                        data['copy'].append(float(result['value'][4]['copy']))
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
        plot.suptitle('Code Rule Violations')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['using'], '-o',label='Rule 1')
        ax.set_ylim( ymax=max(data['using'])+2.0 ,ymin=min(data['using'])-1.0 )
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['debug'], '-o',label='Rule 2')
        ax.set_ylim(ymax=max(data['debug'])+2.0,ymin=min(data['debug'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['catch'], '-o',label='Rule 3')
        ax.set_ylim(ymax=max(data['catch'])+2.0,ymin=min(data['catch'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/30.png',format='png')

        plot, axs = plt.subplots(nrows=3)
        plot.suptitle('Code Rule Violations')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['copy'], '-o',label='Rule 4')
        ax.set_ylim(ymax=max(data['copy'])+2.0,ymin=min(data['copy'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['pragma'], '-o',label='Rule 5')
        ax.set_ylim(ymax=max(data['pragma'])+2.0,ymin=min(data['pragma'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['flags'], '-o',label='Rule 6')
        ax.set_ylim(ymax=max(data['flags'])+2.0,ymin=min(data['flags'])-1.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/31.png',format='png')



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

    
    
