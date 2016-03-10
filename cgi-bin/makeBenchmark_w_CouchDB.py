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

class makeBenchmark(object) :
    def __init__(self, rel,arch,outpath):
	self.outPath=outpath
	self.arch=arch
        self.rel=getReleaseSeries(rel)
 
    def mkBench(self) :

	data=[]
	data_create={'title':[], 'vmem':[],'rss':[],'cputime':[],'cputime_err':[],'rawsize':[],'recosize':[]}
	hist=[]
	steps=["step1_ProdMinBias","step2_ProdMinBias","step1_ProdTTbar","step2_ProdTTbar"]
	for step in steps:
		import copy
        	y=copy.deepcopy(data_create)
        	data.append(y)
        	server = Server()
        	db = server.get_or_create_db("perfdb")
		sk=[self.arch,self.rel,step,["00","00","00","00"]]
		ek=[self.arch,self.rel,step,["99","99","99","99"]]
   		results = db.view("apps/by_release_testname",obj=None, wrapper=None,startkey=sk,endkey=ek)
		titleold=''
		for result in results:
			ymdh=result['value']['release'].split('-')
			title=ymdh[1]+'-'+ymdh[2]+'-'+ymdh[3][0]+ymdh[3][1]+'00'
			if title==titleold :
				db.delete_doc(result['id'])
			else:
	    	        	data[-1]['title'].append(title)
        	        	data[-1]['vmem'].append( result['value']['vmem'] )
                		data[-1]['rss'].append(result['value']['rss'])
               			data[-1]['cputime'].append(result['value']['cputime'])
                		data[-1]['cputime_err'].append(result['value']['cputime_err'])
                		data[-1]['rawsize'].append(result['value']['rawsize'])
                		data[-1]['recosize'].append(result['value']['recosize'])
				titleold=title
	if len(data) ==0 :
		return False
	if len(data[0]['title'])==0 :
		return False
	import matplotlib.pyplot as plt
	ind=range( len(data[0]['title']) )
	if len(data[0]['title'])>10 :
            for x in ind :
                if x%10!=0 :
                    data[0]['title'][x]=''

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('VMEM')
	ax = axs[0]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[0]['vmem'], '-o',label='MinBias step1')
	ax.set_ylim( ymax=max(data[0]['vmem'])*1.01,ymin=min(data[0]['vmem'])*0.99 )
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[1]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[1]['vmem'], '-o',label='MinBias step2')
	ax.set_ylim(ymax=max(data[1]['vmem'])*1.01,ymin=min(data[1]['vmem'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[2]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[2]['vmem'], '-o',label='TTbar step1')
	ax.set_ylim(ymax=max(data[2]['vmem'])*1.01,ymin=min(data[2]['vmem'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[3]
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[3]['vmem'], '-o',label='TTbar step2')
	ax.set_ylim(ymax=max(data[3]['vmem'])*1.01,ymin=min(data[3]['vmem'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/11.png',format='png')

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('RSS')
	ax = axs[0]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[0]['rss'], '-o',label='MinBias step1')
	ax.set_ylim(ymax=max(data[0]['rss'])*1.01,ymin=min(data[0]['rss'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[1]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[1]['rss'], '-o',label='MinBias step2')
	ax.set_ylim(ymax=max(data[1]['rss'])*1.01,ymin=min(data[1]['rss'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[2]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[2]['rss'], '-o',label='TTbar step1')
	ax.set_ylim(ymax=max(data[2]['rss'])*1.01,ymin=min(data[2]['rss'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[3]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[3]['rss'], '-o',label='TTbar step2')
	ax.set_ylim(ymax=max(data[3]['rss'])*1.01,ymin=min(data[3]['rss'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/12.png',format='png')
	
	
	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('CPU Time')
	ax = axs[0]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[0]['cputime'], '-o',label='MinBias step1')
	ax.set_ylim(ymax=max(data[0]['cputime'])*1.01,ymin=min(data[0]['cputime'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[1]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[1]['cputime'], '-o',label='MinBias step2')
	ax.set_ylim(ymax=max(data[1]['cputime'])*1.01,ymin=min(data[1]['cputime'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[2]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[2]['cputime'], '-o',label='TTbar step1')
	ax.set_ylim(ymax=max(data[2]['cputime'])*1.01,ymin=min(data[2]['cputime'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[3]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[3]['cputime'], '-o',label='TTbar step2')
	ax.set_ylim(ymax=max(data[3]['cputime'])*1.01,ymin=min(data[3]['cputime'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/13.png',format='png')

	plot, axs = plt.subplots(nrows=4)
	plot.suptitle('CPU Time Error')
        ax = axs[0]
        ax.cla()
        ax.set_xticks(ind)
        ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[0]['cputime_err'], '-o',label='MinBias step1')
        ax.set_ylim(ymax=max(data[0]['cputime_err'])*1.01,ymin=min(data[0]['cputime_err'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
        ax = axs[1]
        ax.cla()
        ax.set_xticks(ind)
        ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[1]['cputime_err'], '-o',label='MinBias step2')
        ax.set_ylim(ymax=max(data[1]['cputime_err'])*1.01,ymin=min(data[1]['cputime_err'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
        ax = axs[2]
        ax.cla()
        ax.set_xticks(ind)
        ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[2]['cputime_err'], '-o',label='TTbar step1')
        ax.set_ylim(ymax=max(data[2]['cputime_err'])*1.01,ymin=min(data[2]['cputime_err'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
        ax = axs[3]
        ax.cla()
        ax.set_xticks(ind)
        ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
        ax.plot( data[3]['cputime_err'], '-o',label='TTbar step2')
        ax.set_ylim(ymax=max(data[3]['cputime_err'])*1.01,ymin=min(data[3]['cputime_err'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
        pylab.savefig(self.outPath+'/14.png',format='png')
	
	plot, axs = plt.subplots(nrows=2)
	plot.suptitle('Raw Size')
	ax = axs[0]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[0]['rawsize'], '-o',label='MinBias step1')
	ax.set_ylim(ymax=max(data[0]['rawsize'])*1.01,ymin=min(data[0]['rawsize'])*0.99, emit=True)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[1]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[2]['rawsize'], '-o',label='TTbar step1')
	ax.set_ylim( ymax=max(data[2]['rawsize'])*1.01,ymin=min(data[2]['rawsize'])*0.99, emit=True)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/15.png',format='png')
	
	plot, axs = plt.subplots(nrows=2)
	plot.suptitle('Reco Size')
	ax = axs[0]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[1]['recosize'], '-o',label='MinBias step2')
	ax.set_ylim(ymax=max(data[0]['recosize'])*1.1,ymin=min(data[0]['recosize'])*0.9)
	ax.legend(loc=0)
	ax.label_outer()
	ax = axs[1]
	ax.cla()
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15,size='xx-small')
	ax.plot( data[3]['recosize'], '-o',label='TTbar step2')
	ax.set_ylim(ymax=max(data[3]['recosize'])*1.01,ymin=min(data[3]['recosize'])*0.99)
	ax.legend(loc=0)
	ax.label_outer()
	pylab.savefig(self.outPath+'/16.png',format='png')


if __name__=="__main__" :

    mbn = makeBenchmark('1')
    mbn.mkBench()

    
    
