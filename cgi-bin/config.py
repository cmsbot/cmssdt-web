def getHostDomain():
    import socket
    fqdn = socket.getfqdn().split('.')
    host = ''
    domain=''
    if len(fqdn) > 1:
        host = fqdn[0]
        domain=fqdn[-2]+'.'+fqdn[-1]
    else :
    	host=socket.getfqdn()
    	domain=''
    return host,domain

sitesInfo = {
              'cmssdt' :
                    { 'afsPath'     : '/data/sdt/buildlogs/',
                      'OutPath'     : '/data/sdt/sdtQA/intbld/',
                      'CgiHtmlPath' : 'http://cmssdt.cern.ch/SDT/cgi-bin/',
                      'OutHtml'     : 'http://cmssdt.cern.ch/SDT/intbld/',
                      'macms01Path' : 'http://cmssdt.cern.ch/SDT/cgi-bin/',
                      'qaPath'      : '/data/intBld/incoming/'
                     },
            }
siteInfo = sitesInfo['cmssdt']
