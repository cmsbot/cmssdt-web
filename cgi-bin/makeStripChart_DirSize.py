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
# Make dirsize strip charts
###
        data={'title':[], 'src':[],'lib':[],'bin':[]}
        server = Server()
        db = server.get_or_create_db("testdb")
        sk=[self.arch,self.rel,"newQA",["00","00","00","00"]]
        ek=[self.arch,self.rel,"newQA",["99","99","99","99"]]
        results = db.view("apps/by_release_filename",obj=None, wrapper=None,startkey=sk,endkey=ek)
        titleold=''
        for result in results:
                ymdh=result['value'][3].split('-')
                title=ymdh[1]+'-'+ymdh[2]+'-'+ymdh[3][0]+ymdh[3][1]+'00'
                if title==titleold :
                        db.delete_doc(result['id'])
                else:
                        data['title'].append(title)
                        data['bin'].append(float(result['value'][4]['dirsizebin']))
                        data['src'].append(float(result['value'][4]['dirsizesrc']))
                        data['lib'].append(float(result['value'][4]['dirsizelib']))
                        titleold=title
#               print data['title']
        if len(data) ==0 :
                return False
        if len(data['title'])==0 :
                return False
        import matplotlib.pyplot as plt
        ind=range( len(data['title']) )
        if len(data['title'])>10 :
            for x in ind :
                if x%10!=0 :
                    data['title'][x]=''

        plot, axs = plt.subplots(nrows=3)
        plot.suptitle('Directory Size')
        ax = axs[0]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['bin'], '-o',label='BIN')
        ax.set_ylim( ymax=max(data['bin'])+100.0,ymin=min(data['bin'])-100.0 )
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['src'], '-o',label='SRC')
        ax.set_ylim(ymax=max(data['src'])+100.0,ymin=min(data['src'])-100.0)
        ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.set_xticks(ind)
        ax.set_xticklabels( data['title'],rotation=15,size='xx-small')
        ax.plot( data['lib'], '-o',label='LIB')
        ax.set_ylim(ymax=max(data['lib'])+100.0,ymin=min(data['lib'])-100.0)
        ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/21.png',format='png')



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

    
    
