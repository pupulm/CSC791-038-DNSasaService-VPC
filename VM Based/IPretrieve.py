import sys
import libvirt
import random
import time
import paramiko


def getIP(name,if1):
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
             #print "Ip address of",key,"is:",address['addr'],"/",address['prefix']

#print ipaddress
    if ipaddress!="":
    #print "entered"
        ssh.connect(ipaddress,port,username,password)
    else:
        return -1
    cmd = 'ip addr show'
    stdin,stdout,stderr = ssh.exec_command(cmd)
    output=stdout.readlines()
    resp = ''.join(output)
#print("\nthe interface details of this remote device are:\n")
#print(resp)
    f = resp.split('\n')
#print f
    counter = 0
    temp = ""
    for i in f:
        if 'eth'+str(counter) in i:
            interface =  i.split()
            temp = 'eth'+str(counter)
            counter = counter+1
        elif  len(temp)!=0 and'inet' in i and 'inet6' not in i:
            interface = i.split('inet')
            if temp==if1:
                #print temp,interface[1].split()[0].split('/')[0]
                return interface[1].split()[0].split('/')[0]
            temp = ""
    conn.close()
    return -1

