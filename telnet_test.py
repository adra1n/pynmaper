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
import telnetlib

def telnet_test(ip,port):

    tn=telnetlib.Telnet(ip,port)
    tn.write('info\n')
    redis=tn.read_until('redis_version')
    print redis
    tn.write('stats\n')
    memcache=tn.read_until('STAT pid ')
    print memcache
    tn.write('exit\n')
    print 'finish'

if __name__ == '__main__':
    ip=sys.argv[1]
    port=sys.argv[2]
    telnet_test(ip,port)
