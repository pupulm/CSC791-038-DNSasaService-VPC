import os
import sys

if len(sys.argv)<2:
    print "This script requires arguments: vpc/subnet/container/dns"
    exit(0)

funcType = sys.argv[1]
if "vpc" in funcType.lower():
    os.system("sudo ansible-playbook vpc_create.yml")
    os.system("sudo ansible-playbook vpc_writedb.yml")
    print "VPC created as per the input"
elif "subnet" in funcType.lower():
    os.system("sudo ansible-playbook create_subnet.yml")
    os.system("sudo ansible-playbook write_subnetdb.yml")
    print "Subnet created as per the input"
elif "container" in funcType.lower():
    os.system("sudo ansible-playbook create_tenant_cont.yml")
    os.system("sudo ansible-playbook write_container_db.yml")
    print "Tenant Containers created as per the input"
elif "dns" in funcType.lower():
    print "Please Enter the level of DNS you want to create"
    dnsLevel = raw_input()
    if dnsLevel.lower() in "l2dns":
        os.system("sudo ansible-playbook create_L2dnscontainer.yml")
        os.system("sudo ansible-playbook write_L2dnscontainer.yml")
        print "L2DNS created as per the input"

    elif dnsLevel.lower() in "l3dns":
        os.system("sudo ansible-playbook create_L3dnscontainer.yml")
        os.system("sudo ansible-playbook write_dnscontl3_db.yml")
        print "L3DNS created as per the input"





