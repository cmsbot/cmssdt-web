#!/usr/bin/env python
import sys, json, urllib2, re
print "Content-Type: application/json\n"
ES_CERN_URL = "https://es-cmssdt.cern.ch:9203"

def send_error(msg):
  print '{"proxy-error":"%s"}' % msg
  sys.exit()

try:
  data = sys.stdin.read()
  payload = json.loads(data)
  index = payload['index']
  if not index.startswith("cmssdt-"): index = 'cmssdt-'+index
  if not re.match('^cmssdt-[*a-zA-Z0-9_/-]+$',index): send_error ("Invalid index name: %s" % index)
  es_user = "cmssdt"
  es_pass = open('/data/secrets/apache-cmssdt-es-secret','r').read().strip()
  search = "/_search"
  scroll = payload.pop('scroll',0)
  if scroll==1:
    search = "/_search?scroll=1m"
  elif scroll>1:
    index = ""
    search = "/_search/scroll"
  url = "%s/%s%s" % (ES_CERN_URL, index, search)
  passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
  passman.add_password(None, url, es_user, es_pass)
  auth_handler = urllib2.HTTPBasicAuthHandler(passman)
  opener = urllib2.build_opener(auth_handler)
  try:
    urllib2.install_opener(opener)
    content = urllib2.urlopen(url,payload['query'])
    print content.read()
  except Exception as e:
    send_error("Couldn't send data to elastic search: %s\nurl:%s\nquery:%s" % (str(e),url, query))
except Exception as e:
  send_error("Invalid data, can not read json input.")

