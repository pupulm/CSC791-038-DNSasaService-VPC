import time
import sys
import pdb
import docker
import shlex
import time
import os
import subprocess

def getName():
    cmd_list = "sudo docker ps -a --format '{{.Names}}'"
    cmd_list = shlex.split(cmd_list)
    result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    nameList = out.split('\n')
    return nameList[:len(nameList)-1]
##
nameList = getName()
"""
idList=[]
for i in range(0,len(nameList)):
    cmd_list = "sudo docker inspect --format='{{.Id}}' "+nameList[i]
    cmd_list = shlex.split(cmd_list)
    result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    idList.append(out)
"""
try:
    f = open('backup.txt','r')
    backup = f.read()
    oldlist = backup.split('\n')
    #print oldlist
    for i in range(0,len(oldlist)):
        #print "entered"
        if oldlist[i] not in nameList:
            os.system("docker run --name "+oldlist[i]+" -idt "+oldlist[i].lower())
    f.close()         
except:
    pass
f = open('backup.txt','w')
nameList = getName()
for i in range(0,len(nameList)):
    f.write(nameList[i])
    if i!=len(nameList)-1:
        f.write('\n')
f.close()
## commiting 

###
#### Recovery after removed 

for i in nameList:
    cmd1="docker inspect "+i+""
    cmd1=shlex.split(cmd1)
    result = subprocess.Popen(cmd1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "Running"], stdin=result.stdout, stdout=subprocess.PIPE)
    result.stdout.close()
    out, err = p2.communicate()
    if 'false' in out:
        os.system("docker start "+i)

## commiting 
for i in range(0,len(nameList)):
    print nameList[i],"in committing"
    os.system("docker commit "+nameList[i]+" "+nameList[i].lower())

cmd_list = "sudo docker images"
cmd_list = shlex.split(cmd_list)
result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()
imageList = out.split('\n')
for i in imageList:
    if len(i.split())!=0 and i.split()[0]=="<none>":
        os.system("sudo docker rmi "+i.split()[2])




