#-------------------------------------------------------------------------------
# Name:        ??1
# Purpose:
#
# Author:      Administrator
#
# Created:     13/03/2015
# Copyright:   (c) Administrator 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import sys

def jdb_test(ip,port):
    p=subprocess.Popen(['jdb','-attach','%s:%s' %(ip,port)],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    print stdoutdata
    print stderrdata

if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    jdb_test(ip,port)
