import os
import sys
import libvirt
import paramiko


def DNSconfig(vmip):
    ssh = paramiko.SSHClient()
    port = 22
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vmip,port,'root','root')
    sftp = ssh.open_sftp()
    sftp.put('forward.db', '/var/named/forward.db')
    sftp.put('named.conf','/etc/named.conf')
    ## write the DNS configurations using scp commands
    stdin,stdout,stderr = ssh.exec_command("chmod 775 /var/named/forward.db")
    stdin,stdout,stderr = ssh.exec_command("chmod 775 /etc/named.conf")
    stdin,stdout,stderr = ssh.exec_command("firewall-cmd --permanent --add-port=53/tcp")
    stdin,stdout,stderr = ssh.exec_command("firewall-cmd --permanent --add-port=53/tcp")
    stdin,stdout,stderr = ssh.exec_command("firewall-cmd --reload")

    stdin,stdout,stderr = ssh.exec_command("echo "" > /etc/resolve.conf")
    stdin,stdout,stderr = ssh.exec_command("systemctl enable named")
    stdin,stdout,stderr = ssh.exec_command("systemctl start named")
    
    sftp.close()

    return

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


#### Main

if len(sys.argv)<3:
    print "Tenant name and VM name is required for the script"
    exit(0)

folders = os.listdir('/etc/tenants')
Tenant = sys.argv[1]
VMname = sys.argv[2]

if Tenant not in folders:
    print "Incorrect Tenant id"
    exit(0)

if "-L1" in VMname:
    flag = 0
    for i in folders:
        if i.lower()==VMname.lower():
            flag=1
            ip = getIP(VMname)
            if ip=="":
                print "Not able to get the ip address"
                exit(0)
            DNSconfig(ip)
            print "DNS configuration done"
            b = raw_input("Do you want firewall as the feature ? Type yes/no")
            if b.lower()=="yes":
                os.system("sudo python firewall.py")
            exit(0)
    if flag==0:
        print "Incorrect L1DNS Name"
        exit(0)
else:
    files = os.listdir('/etc/tenants/'+Tenant)
    flag= 0
    for i in range(0,len(files)):
        if VMname.lower() == files[i].lower().split('.')[0]:
            ip = getIP(VMname)
            if ip=="":
                print "Not able to get the ip address"
                exit(0)
            DNSconfig(ip)
            print "DNS configuration done"
            exit(0)

print "Error with the VM name"

