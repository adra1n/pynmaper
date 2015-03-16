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

def rsync_test(ip,port):
    p=subprocess.Popen(['rsync','--port=%s' %port,'%s::' %ip],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #p.stdin.write('-h')
    stdoutdata, stderrdata = p.communicate()
    print stdoutdata
    print stderrdata
    pass

if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    rsync_test(ip,port)
