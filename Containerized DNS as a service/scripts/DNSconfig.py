import time
import sys
import pdb
import docker
import shlex
import time
import os
import subprocess
import paramiko


def getIp(Tenantid):
    files = os.listdir('/etc/tenants/'+Tenantid)
    for i in range(0,len(files)):
        cmd_list = "sudo docker inspect --format='{{ .NetworkSettings.IPAddress }}' "+files[i].split('.')[0]
        cmd_list = shlex.split(cmd_list)
        result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        if '_L3DNS' in files[i] or '_L2DNS' in files[i]:
            print files[i].split('.')[0],out.strip()

        elif 'vm' in files[i].lower():
            #print files[i],out
            name = files[i].split('.')[0]
            ssh = paramiko.SSHClient()
            port = 22
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(out,port,'root')
            cmd = 'ip addr show'
            stdin,stdout,stderr = ssh.exec_command(cmd)
            output=stdout.readlines()
            resp = ''.join(output)
            f = resp.split(name+'vif1')
            print name,f[1].split('inet')[1].split()[0].split('/')[0]
            ssh.close()


folders = os.listdir('/etc/tenants')
Tenant = sys.argv[1]

if Tenant not in folders:
    print "Incorrect Tenant id"
    exit(0)

print "Here are the list of containers and their IP's"
cmd_list = "sudo docker inspect --format='{{ .NetworkSettings.IPAddress }}' L1dns"
cmd_list = shlex.split(cmd_list)
result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()
print "L1dns", out.strip()

#files = os.listdir('/etc/tenants'+Tenant)
getIp(Tenant)
print "####"


containerName = raw_input("enter the name of the dns container to start configuring\n")
folders = os.listdir('/srv/docker')
if containerName not in folders:
    print "Container configuration not found"
    exit(0)

os.system("sudo cp -p forward.db /srv/docker/"+containerName+"/var/forward.db")
os.system("sudo cp -p named.conf /srv/docker/"+containerName+"/etc/named.conf")
os.system("sudo chmod 644 /srv/docker/"+containerName+"/var/forward.db")
os.system("sudo chmod 644 /srv/docker/"+containerName+"/etc/named.conf")
os.system("sudo chown root:root /srv/docker"+containerName+"/etc/named.conf")
os.system("sudo chown root:root /srv/docker"+containerName+"/var/forward.db")


os.system("sudo docker exec -itd "+containerName+" /usr/sbin/named -4 -u named -c /named/etc/named.conf")
os.system("sudo docker exec -itd "+containerName+" rndc reload")

print "DNS configuration done.."
## see about permissions 644 -rw-rw-r--
yesno = raw_input("Do you want to add firewall as a feature? Enter yes/no\n")
if yesno.lower() == "yes":
    os.system("sudo python containerfirewall.py")
    #print "Firewall configuration done..."
    exit(0)





