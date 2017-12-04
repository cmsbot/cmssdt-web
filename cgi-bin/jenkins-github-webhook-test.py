#!/usr/bin/env python
import sys, json
import urllib2, urllib

try: jenkins_server=sys.argv[1]
except: jenkins_server="cmsjenkins03.cern.ch"
params = []
job="jenkins-installation-trigger-cli"
params.append({"name":"JOB_PARAM1","value":"cmssdt1"})
params.append({"name":"JOB_PARAM2","value":"cmssdt2"})
url = 'http://'+jenkins_server+':8080/jenkins/job/'+job+'/build'
jenkins_parameters = json.dumps({"parameter":params})
print jenkins_parameters,job
data = {
  "json": jenkins_parameters,
   "Submit": "Build"
}
try:
  data=urllib.urlencode(data)
  req = urllib2.Request(url=url,data=data,headers={"ADFS_LOGIN" : "cmssdt"})
  content = urllib2.urlopen(req).read()
except Exception as e:
  print "Unable to start jenkins job"

