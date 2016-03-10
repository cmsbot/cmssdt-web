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

class makeBenchmark(object) :
    def __init__(self, rel,arch,outpath):
	#arch=arch.replace('amd64','ia32') # amd64 is not support
	self.outPath=outpath
	url = config.siteInfo['macms01Path']+'/showTimeMemInfo.py?rel='+rel+'\&arch='+arch
        self.page = os.popen('wget --no-check-certificate -nv -o /dev/null -O- '+url)
    
    def mkBench(self) :
	data=[]
	data_create={'title':[], 'vmem':[],'rss':[],'cputime':[],'cputime_err':[],'rawsize':[],'recosize':[]}
	lines=[]
	hist=[]
	lines=self.page.readlines()
	for line in lines :
            if line[0:4]=='step' :
                import copy
                y=copy.deepcopy(data_create)
                data.append(y)
            elif line[:2] =='<a' :
                slist=line.split()
                data[-1]['title'].append( str(slist[1][75:95]) )
                data[-1]['vmem'].append(float(slist[3]))
                data[-1]['rss'].append(float(slist[4]))
                data[-1]['cputime'].append(float(slist[5]))
                data[-1]['cputime_err'].append(float(slist[7]))
                data[-1]['rawsize'].append(float(slist[14]))
                data[-1]['recosize'].append(float(slist[15]))
            else :
                continue
            
	if len(data) ==0 :
		return False
	if len(data[0]['title'])==0 :
		return False
	import matplotlib.pyplot as plt
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ind=range( len(data[0]['title']) )
	if len(data[0]['title'])>10 :
            for x in ind :
                if x%6!=0 :
                    data[0]['title'][x]=''
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	ax.plot( data[0]['vmem'], '-o',label='step1_ProdMinBias+RECOPROD1')
	ax.plot( data[1]['vmem'], '-o',label='step2_ProdMinBias+RECOPROD1')
	ax.plot( data[2]['vmem'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	ax.plot( data[3]['vmem'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymax=(max(max(data[0]['vmem'],data[1]['vmem'],data[2]['vmem'],data[3]['vmem']))*1.3))
	ax.legend()
	pylab.savefig(self.outPath+'/1.png',format='png')
	plt.cla()
	
	
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	ax.plot( data[0]['rss'], '-o',label='step1_ProdMinBias+RECOPROD1')
	ax.plot( data[1]['rss'], '-o',label='step2_ProdMinBias+RECOPROD1')
	ax.plot( data[2]['rss'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	ax.plot( data[3]['rss'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymax=(max(max(data[0]['rss'],data[1]['rss'],data[2]['rss'],data[3]['rss']))*1.3))
	ax.legend()
	pylab.savefig(self.outPath+'/2.png',format='png')
	plt.cla()
	
	
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	ax.plot( data[0]['cputime'], '-o',label='step1_ProdMinBias+RECOPROD1')
	ax.plot( data[1]['cputime'], '-o',label='step2_ProdMinBias+RECOPROD1')
	ax.plot( data[2]['cputime'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	ax.plot( data[3]['cputime'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymax=(max(max(data[0]['cputime'],data[1]['cputime'],data[2]['cputime'],data[3]['cputime']))*1.4))
	ax.legend()
	pylab.savefig(self.outPath+'/3.png',format='png')
	plt.cla()
	
	
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	ax.plot( data[0]['cputime_err'], '-o',label='step1_ProdMinBias+RECOPROD1')
	ax.plot( data[1]['cputime_err'], '-o',label='step2_ProdMinBias+RECOPROD1')
	ax.plot( data[2]['cputime_err'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	ax.plot( data[3]['cputime_err'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymax=(max(max(data[0]['cputime_err'],data[1]['cputime_err'],data[2]['cputime_err'],data[3]['cputime_err']))*1.4))
	ax.legend()
	pylab.savefig(self.outPath+'/4.png',format='png')
	plt.cla()
	
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	ax.plot( data[0]['rawsize'], '-o',label='step1_ProdMinBias+RECOPROD1')
	# ax.plot( data[1]['rawsize'], '-o',label='step2_ProdMinBias+RECOPROD1')
	ax.plot( data[2]['rawsize'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	# ax.plot( data[3]['rawsize'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymin=0, ymax=(max(max(data[0]['rawsize'],data[1]['rawsize'],data[2]['rawsize'],data[3]['rawsize']))*1.4), emit=True)
	ax.legend()
	pylab.savefig(self.outPath+'/5.png',format='png')
	plt.cla()
	
	ax.set_xticks(ind)
	ax.set_xticklabels( data[0]['title'],rotation=15)
	# ax.plot( data[0]['recosize'], '-o',label='step1_ProdMinBias+RECOPROD1')
	ax.plot( data[1]['recosize'], '-o',label='step2_ProdMinBias+RECOPROD1')
	# ax.plot( data[2]['recosize'], '-o',label='step1_ProdTTbar+RECOPROD1+ALCATT1')
	ax.plot( data[3]['recosize'], '-o',label='step2_ProdTTbar+RECOProd1+ALCATT1')
	ax.set_ylim(ymin=0, ymax=(max(max(data[0]['recosize'],data[1]['recosize'],data[2]['recosize'],data[3]['recosize']))*1.4), emit=True)
	ax.legend()
	pylab.savefig(self.outPath+'/6.png',format='png')
	plt.cla()



if __name__=="__main__" :
    mbn = makeBenchmark('1')
    mbn.mkBench()
    
