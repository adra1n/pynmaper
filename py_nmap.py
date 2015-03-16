import nmap
import sys
import telnetlib
import subprocess

def write(port,state,product):
    result='port : %s\tstate : %s\tproduct:%s' % (port,state,product)
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
    print ip,port
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
        write(host)
        write('---------------------')
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
                            write(port, nm[host][proto][port]['state'],'memcache')
                    elif nm[host][proto][port]['product']=='redis':
                        b=redis_test(host,port)
                        if b:
                            write(port, nm[host][proto][port]['state'],'redis')
                    elif nm[host][proto][port]['product']=='jdwp':
                        b=jdb_test(host,port)
                        if b:
                            write(port, nm[host][proto][port]['state'],'redis')
                    elif nm[host][proto][port]['product']=='rsync':
                        data=rsync_test(host,port)
                        if data:
                            write(port, nm[host][proto][port]['state'],'rsync')
                            write(data)
                    else:
                        write(port, nm[host][proto][port]['state'],nm[host][proto][port]['product'])


if __name__=="__main__":
    ip=sys.argv[1]
    port=sys.argv[2]
    pyscanner(ip,port)

