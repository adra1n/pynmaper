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

def redis_test(ip,port):
    print ip,port
    p=subprocess.Popen(['redis-cli', '-h', '115.236.98.44', '-p', '6379'],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #p.stdin.write('-h')
    stdoutdata, stderrdata = p.communicate('info')
    if('redis_version' in stdoutdata ):
        print 'alive'
    else:
        print stdoutdata

if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    redis_test(ip,port)