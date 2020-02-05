import os
import sys
import libvirt
import paramiko


def Vrrpconfig(vmip):
    ssh = paramiko.SSHClient()
    port = 22
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vmip,port,'root','root')
    #stdin,stdout,stderr = ssh.exec_command("yum install keepalived")
    stdin,stdout,stderr = ssh.exec_command("echo 'net.ipv4.ip_nonlocal_bind=1' >> /etc/sysctl.conf")
    sftp = ssh.open_sftp()
    sftp.put('keepalived.conf', '/etc/keepalived/keepalived.conf')
    stdin,stdout,stderr = ssh.exec_command("chmod 644 /etc/keepalived/keepalived.conf")
    stdin,stdout,stderr = ssh.exec_command("service keepalived start")
    sftp.close()


def getIP(DNS):
    conn = libvirt.open('qemu:///system')
    if conn == None:
        print 'Failed to open connection to qemu'
        exit(1)
    try:
        domain = conn.lookupByName(DNS)
    except:
        print "Not able to connect"
        exit(0)
    ifaces = domain.interfaceAddresses(0)
    ipaddress = ""
    for key in ifaces:
        for address in ifaces[key]['addrs']:
            ipaddress = address['addr']

    return ipaddress


if len(sys.argv)<3:
    print "Tenant name and L2DNS name is required for the script"
    exit(0)

folders = os.listdir('/etc/tenants')
Tenant = sys.argv[1]
VMname = sys.argv[2]

if Tenant not in folders:
    print "Incorrect Tenant id"
    exit(0)

files = os.listdir('/etc/tenants/'+Tenant)
flag= 0
for i in range(0,len(files)):
    if VMname.lower() == files[i].lower().split('.')[0] and "-l2dns" in files[i].lower():
        flag=1
        ip = getIP(VMname)
        if ip=="":
            print "Not able to get the ip address"
            exit(0)
        Vrrpconfig(ip)
        print "High availability configuration done.."

if flag==0:
    print "Error with the VM name"

