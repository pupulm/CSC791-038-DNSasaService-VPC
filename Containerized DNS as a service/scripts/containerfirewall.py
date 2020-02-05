import os
import sys
import time
import random
import paramiko
import subprocess
import shlex

username="root"
password="root"
    
ssh = paramiko.SSHClient()
port = 22
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

cmd_list = "sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' L1dns"
cmd_list = shlex.split(cmd_list)
result = subprocess.Popen(cmd_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = result.communicate()

print(out)
    
ssh.connect(out,port,username,password)

cmd = 'iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|09|proxypipe|03|net" --algo bm -j DROP'
stdin,stdout,stderr = ssh.exec_command(cmd)
cmd = 'iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|06|kitten|02|ru" --algo bm -j DROP'
stdin,stdout,stderr = ssh.exec_command(cmd)
cmd ='iptables -A INPUT -i eth0 -p udp --dport 53 -m string --hex-string "|03|www|07|puppies|04|woof" --algo bm -j DROP'
stdin,stdout,stderr = ssh.exec_command(cmd)
cmd = 'iptables -t mangle -I PREROUTING 1 -p icmp -m hashlimit --hashlimit-name icmp --hashlimit-mode srcip --hashlimit 20/second --hashlimit-burst 1 -j ACCEPT'
stdin,stdout,stderr = ssh.exec_command(cmd)
cmd ='iptables -t mangle -A PREROUTING -p icmp -j DROP'
stdin,stdout,stderr = ssh.exec_command(cmd)




