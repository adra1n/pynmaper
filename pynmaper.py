import nmap
import sys
import telnetlib
import subprocess

import threading
import time
import Queue

def write_re(host,port,state,product):
    result='host:%s\tport : %s\tstate : %s\tproduct:%s' % (host,port,state,product)
    with open('result.txt','a') as f:
        f.write(result+'\n')


def telnet_test(ip,port):

    tn=telnetlib.Telnet(ip,port)
    tn.write('stats\n')
    memcache=tn.read_until('STAT pid ')
    if memcache:
        return 1
    tn.write('exit\n')
    print 'finish'

def redis_test(ip,port):
    #print ip,port
    p=subprocess.Popen(['redis-cli', '-h', '%s' %ip, '-p', '%s' %port],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #p.stdin.write('-h')
    if('redis_version' in stdoutdata ):
        return  1
    else:
        pass

def jdb_test(ip,port):
    p=subprocess.Popen(['jdb','-attach','%s:%s' %(ip,port)],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    stdoutdata, stderrdata = p.communicate()
    if('Initializing jdb' in stdoutdata):
        return 1
    else:
        print stderrdata
        pass


def rsync_test(ip,port):
    p=subprocess.Popen(['rsync','--port=%s' %port,'%s::' %ip],shell=True,stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    #p.stdin.write('-h')
    stdoutdata, stderrdata = p.communicate()
    if stdoutdata:
        return stdoutdata
    else:
        print stdoutdata
    pass

def pyscanner(ip,port):
    nm=nmap.PortScanner()
    nm.scan(hosts=ip, arguments='-sV -sS -T4 -p%s' % port)
    #print nm.scaninfo()
    print nm.command_line()
    print nm.all_hosts()
    for host in nm.all_hosts():
        #write_re(host)
        #write_re('---------------------')
        #print('Host : %s (%s)' % (host, nm[host].hostname()))
        #print('State : %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            #print('---------')
            #print('Protocol : %s' % proto)
            if proto == 'tcp' or proto=='udp':
                #print nm[host][proto]
                lport = nm[host][proto].keys()
                lport.sort()
                for port in lport:

                    #print result
                    if nm[host][proto][port]['product']=='Memcached':
                        b=telnet_test(host,port)
                        if b:
                            write_re(host,port, nm[host][proto][port]['state'],'memcache')
                    elif nm[host][proto][port]['product']=='Redis key-value store':
                        b=redis_test(host,port)
                        if b:
                            write_re(host,port, nm[host][proto][port]['state'],'redis')
                    elif nm[host][proto][port]['product']=='Java Debug Wire Protocol':
                        b=jdb_test(host,port)
                        if b:
                            write_re(host,port, nm[host][proto][port]['state'],'java debug')
                    elif nm[host][proto][port]['product']=='rsync':
                        data=rsync_test(host,port)
                        if data:
                            write_re(host,port, nm[host][proto][port]['state'],'rsync')
                            write_re(data)
                    else:
                        write_re(host,port, nm[host][proto][port]['state'],nm[host][proto][port]['product'])


SHARE_Q = Queue.Queue()
_WORKER_THREAD_NUM = 50

class MyThread(threading.Thread) :
    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func
    def run(self) :
        self.func()

def do_something(item) :
    ip=sys.argv[1]
    port=sys.argv[2]
    print(ip+'.'+str(item),port)
    pyscanner(ip+'.'+str(item),port)

def worker() :
    global SHARE_Q
    while True :
        if not SHARE_Q.empty():
            item = SHARE_Q.get()
            do_something(item)
            time.sleep(1)
            SHARE_Q.task_done()

def main() :
    global SHARE_Q
    threads = []
    for task in xrange(200,255) :
        SHARE_Q.put(task)

    for i in xrange(_WORKER_THREAD_NUM) :
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads :
        thread.join()
    SHARE_Q.join()
if __name__ == '__main__':
    main()

