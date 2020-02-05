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
    cmd = 'iptables -I INPUT -p icmp -s 192.168.230.0/24 -d 192.168.230.0/24 -j DROP'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    conn.close()
    return -1

folders = os.listdir('/etc/tenants')

tenantvm = {}
L1dns=""
L2dns = {}
L3dns = {}
for i in range(0,len(folders)):
    files = os.listdir('/etc/tenants/'+folders[i])
    if "-L1" in folders[i]:
        L1dns = folders[i].split('.json')[0]
    else:
        tenantvm[folders[i]] = []
        L2dns[folders[i]] = []
        L3dns[folders[i]] = []
        for j in range(0,len(files)):
            if "VM" in files[j]:
                tenantvm[folders[i]].append(files[j].split('.json')[0])
            elif "-L2DNS" in files[j]:
                L2dns[folders[i]].append(files[j].split('.json')[0])
                temp = files[j].split('.json')[0]
                L2dns[folders[i]].append(temp[:len(temp)-1]+"2")
            elif "-L3DNS" in files[j]:
                 L3dns[folders[i]].append(files[j].split('.json')[0])

getIP(L1dns)

for i in tenantvm:
    tenant = tenantvm[i]
    for j in range(0,len(tenant)):
        getIP(tenantvm[i][j])

for i in L2dns:
    l2dns = L2dns[i]
    for j in range(0,len(l2dns)):
        getIP(L2dns[i][j])
