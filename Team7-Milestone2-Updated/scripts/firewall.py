import os
import sys
import libvirt
import random
import time
import paramiko

def getIP(name):
    username = "root"
    password = "root"

##############
    ssh = paramiko.SSHClient()
    port = 22
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
################

    conn = libvirt.open('qemu:///system')
    if conn == None:
        print 'Failed to open connection to qemu'
        exit(1)

    numorname = name
#domainIDs = conn.listDomainsID()
    try:
        num = int(numorname)
        domain = conn.lookupByID(num)
    #print "The domain name is: ",domain.name()
    except ValueError:
        domain = conn.lookupByName(numorname)
    #print "The domain ID is: ",domain.ID()
    ipaddress = ""
    ifaces = domain.interfaceAddresses(0)

    for key in ifaces:
        for address in ifaces[key]['addrs']:
                ipaddress = address['addr']
    if ipaddress!="":
        ssh.connect(ipaddress,port,username,password)
    else:
        return -1

    cmd = 'ip route del default via 192.168.230.1'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd = 'iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|09|proxypipe|03|net" --algo bm -j DROP'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd = 'iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|06|kitten|02|ru" --algo bm -j DROP'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd ='iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|03|www|07|puppies|04|woof" --algo bm -j DROP'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd = 'iptables -t mangle -A PREROUTING -p icmp -m hashlimit --hashlimit-name icmp --hashlimit-mode srcip --hashlimit 20/second --hashlimit-burst 1 -j ACCEPT'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    cmd ='iptables -t mangle -A PREROUTING -p icmp -j DROP'
    stdin,stdout,stderr = ssh.exec_command(cmd)

    conn.close()
    return -1

###main
folders = os.listdir('/etc/tenants')


L1dns=""
for i in range(0,len(folders)):
    files = os.listdir('/etc/tenants/'+folders[i])
    if "-L1" in folders[i]:
        L1dns = folders[i].split('.json')[0]
        break

getIP(L1dns)
