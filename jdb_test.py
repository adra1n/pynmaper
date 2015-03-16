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

def jdb_test():
    p=subprocess.Popen(['jdb'],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    print stdoutdata
    print stderrdata

if __name__ == '__main__':
    jdb_test()
