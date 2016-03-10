#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Andreas Pfeiffer on 2008-12-13.
Copyright (c) 2008 CERN. All rights reserved.
"""

import sys, os, time

sys.path.append( os.path.join('/afs/cern.ch/user/a/andreasp/', 'install', 'lib64', 'python2.3', 'site-packages' ) )
from pysqlite2 import dbapi2 as sqlite

class ShowDB(object):
    def __init__(self):
        """docstring for __init__"""
        fileName = os.path.join(os.environ['HOME'],'buildSpace','buildSpaceDBNew')        
        self.con = sqlite.connect(fileName)
        self.cur = self.con.cursor()
        self._verbose = False

    def __del__(self):
        """docstring for __del__"""
        self.con.rollback()
        self.con.close()

    def verbose(self):
        self._verbose = True

    def show(self, dateSel=None):
        """docstring for show"""

        if not dateSel:
            dateSel = time.strftime('%Y%m%d')

        userMap = {}
        self.cur.execute('SELECT * from UserInfo')
        for entry in self.cur:
            id, acct, name, mail = entry
            userMap[acct] = (name, mail)

        print '{ "aaData": [ '

        self.cur.execute('SELECT * from SpaceInfo where datestamp="'+dateSel+'"')
        spaceRows = self.cur.fetchall()
        
        for row in spaceRows:
            id, stamp, host, disk, free = row
            freeMB = free/1024.
            freeGB = free/1024./1024.
            msg = '[ "'+host+'", "'+disk+'", '+str(freeGB) +' ],'

            print msg

            if not self._verbose: continue

            mailList = []
            cmd = 'SELECT * from DirInfo where '
            cmd += ' datestamp="'+dateSel+'" '
            cmd += ' AND host="'+host+'" '
            cmd += ' AND disk="'+disk+'" '
            print ""
            self.cur.execute(cmd)
            for entry in self.cur:
                id, stamp, host, disk, directory, used, acct = entry
                fullName = userMap[acct][0]
                mailAddr = userMap[acct][1]
                msg = ' %-20s : %10.2f   %-10s   %-25s   %s' % (directory, used/1024., acct, fullName, mailAddr)
                print msg
                if mailAddr not in mailList: mailList.append(mailAddr)
            print '\n', ",".join(mailList)
	    print '\n'+'-'*80+'\n'    

        print "] }"



def main():
    db = ShowDB()
#    if len(sys.argv) > 1: db.verbose()
    db.show()
    pass


if __name__ == '__main__':
    main()

