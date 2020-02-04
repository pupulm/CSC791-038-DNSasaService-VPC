# DNS-as-a-Service-VPC using containers

## VPC CRUD:  

**Create:**  
Tenant uploads the vars file with the name of vpc_variable.yml, and required parameters to create a vpc.  
Commands: sudo python main.py vpc    
Argument for this script is 'vpc'.  

**Read:**
List down the tenant specific parameters which are stored in the log files.  
Log file for each tenant is stored in /etc/tenants/<tenant_id>  
For VPC: Eg: t1vpc1.json consists the vpc configuration of tenant whose id is t1.  

**Update:**
No update can be made to VPC.

**Delete:**
Tenant can remove the vpc by running the python script delete_cont.py and then following the runtime interaction.

## Subnet CRUD:

**Create:**  
Tenant uploads the vars file with the name of subnet_vars.yml, and required parameters to create subnets in each vpc.  
Commands: sudo python main.py subnet  
Argument for this script is 'subnet'

**Read:**
List down the tenant specific parameters which are stored in the log files.  
Log file for each tenant subnet configuation is stored in /etc/tenants/<tenant_id>  
Eg: t1_subnet_1.json consists the subnet configuration of tenant whose id is t1  

**Update:**
No update can be made to subnet.  

**Delete:**
Tenant can remove the subnets by running the python script delete_cont.py and then following the runtime interaction.  

## Tenant specific containers CRUD:

**Create:**  
Tenant uploads the vars file in the name of ten_cont_vars.yml, with the required parameters to create containers in each vpc.  
Commands: sudo python main.py container  
Argument for this script is 'container'  

**Read:**
List down the tenant specific parameters which are stored in the log files.  
Log file for each tenant container configuration is stored in /etc/tenants/<tenant_id>  
Eg: T1_VM1.json consists the container configuration of tenant t1.  

**Update:**
No update can be made to container.  

**Delete:**
User can remove the containers by running the python script delete_cont.py  

## DNS server for every level:

**Create:**  
Tenant uploads the l2dns_vars.yml and L3dns_vars.yml to create DNS at vpc level and subnet level.  
Commands:  sudo python main.py dns  
Argument for this script is 'dns'  
User can follow the run time interaction to create level specific dns that is vpc level and subnet level.  

**Read:**
List down the DNS parameters which are stored in the log files.  
Log file for each tenant specific DNS is stored in /etc/tenants/<tenant_id>  
For DNS:   
Eg: DNS_T1_S1-L3DNS.json consists the DNS VM configuration at subnet level.  
Eg: t1-L2DNS1.json consists the DNS VM configuration at tenant level.  
 

**Update:**
No update can be made to DNS configuration.  

**Delete:** 
User can remove the DNS containers by running the python script delete_cont.py.  
command: sudo python delete_cont.py  

## Provider/ Developer Guide for Hypervisor Infrastructure:
* Make sure provider_ns network namespace is created in the hypervisor.  
* Create Provider DNS(L1dns) container using the script create_L1dnscontainer.yml.  
  command: sudo ansible-playbook create_L1dnscontainer.yml

## Docker images:
List of docker image types we have used.
* [DNS bind image](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/tree/master/containerproject/dnsconf/Dockerfile): Used for creating dns server containers.  
* [Centos image](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/blob/master/containerproject/instanceconf/Dockerfile): Used for client server containers with centos.  

## Tenants:
It is assumed that tenant will perform following steps in order to build the infrastructure.  
* Upload files first, for VPC creation: vpc_variable.yml  
* Upload file for subnet creation: subnet_vars.yml  
* Upload files for L2dns:l2dns_vars.yml , L3dns: L3dns_vars.yml  
* Upload file to create containers: ten_cont_vars.yml  

## Automation Scripts:
* DNSconfig.py: This script does the automation of copying named.conf, forward.com uploaded by the tenant to the shared volume in the hypervisor. This script also promts the user if he wants add to the firewall feature or not.
  README for the script [DNSconfig.py](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/blob/master/containerproject/scripts/DNSconfigREADME.md)
* selfhealing.py: This script implements a feature similar to kubernetes self healing feature. This script is configured as a CRON job by the provider if tenant chooses to opt for this feature. Instructions to configure cron job is provided in the script specific ReadMe.
README for the script [selfhealing.py](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/blob/master/containerproject/scripts/selfhealingREADME.md)  

## Prerequisites for ansible scripts:
* The execution of scripts assume that the controller network and provider namespace are already created.
* The docker image to build and create the DNS container is in the following path. [</containerproject/dnsconf>](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/tree/master/containerproject/dnsconf)  
* The docker image to build and create the tenant container is in the following path. [</containerproject/instanceconf>](https://github.ncsu.edu/schippa/DNS-as-a-Service-VPC/tree/master/containerproject/instanceconf)

## References:
* Setting up DNS:  
   https://www.isc.org/bind/  
   https://www.unixmen.com/setting-dns-server-centos-7/  
   https://www.itzgeek.com/how-tos/linux/centos-how-tos/configure-dns-bind-server-on-centos-7-rhel-7.html  
   https://www.digitalocean.com/community/tutorials/how-to-configure-bind-as-a-private-network-dns-server-on-centos-7  
* Self Healing kubernetes feature: https://www.stratoscale.com/blog/kubernetes/auto-healing-containers-kubernetes/  
* Centos Bind container: https://github.com/CentOS/CentOS-Dockerfiles/tree/master/bind/centos7  








