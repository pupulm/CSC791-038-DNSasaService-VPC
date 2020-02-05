# DNS-as-a-Service-VPC

## VPC CRUD:  

**Create:**  
Input: Tenant uploads the vars file in the name of vpc_variable.yml, with the required parameters to create a vpc.
Commands: sudo ansible-playbook vpc_create.yml

**Read:**
List down the tenant specific parameters which are stored in the log files.
Log file for each tenant is stored in /etc/tenants/<tenant_id>
For VPC: Eg: t1vpc1.json consists the vpc configuration.

**Update:**
No update can be made to VPC.

**Delete:**
Tenant can remove the vpc by running the python script delete_dns.py and then following the runtime interaction.

## Subnet CRUD:

**Create:**  
Input: Tenant uploads the vars file in the name of subnet_vars.yml, with required parameters to create subnets in each vpc.  
Commands: sudo ansible-playbook create_subnet.yml

**Read:**
List down the tenant specific parameters which are stored in the log files.
Log file for each tenant subnet configuation is stored in /etc/tenants/<tenant_id>
For Subnet: Eg: t1_subnet_1.json consists the subnet configuration.

**Update:**
No update can be made to subnet.

**Delete:**
Not yet implemented.


## Tenant specific VM's CRUD:

**Create:**  
Input: Tenant uploads the vars file in the name of VM_vars.yml, with the required parameters to create VM's in each vpc.  
Commands: sudo ansible-playbook create_tenantvm.yml

**Read:**
List down the tenant specific parameters which are stored in the log files.
Log file for each tenant VM configuration is stored in /etc/tenants/<tenant_id>
For VM: Eg: T1_VM1.json consists the VM configuration.

**Update:**
No update can be made to VM.

**Delete:**
User can remove the VM's by running the python script delete_dns.py

## DNS server for every level:

**Create:**  
Input: Tenant uploads the DNS_VM_vars1.yml, DNS_VM_vars2.yml and DNS_VM_vars3.yml to create DNS at each level.  
Commands:  
          sudo ansible-playbook createL1DNS.yml  // creates DNS VM at provider level.  
          sudo ansible-playbook createL2DNS.yml  // creates DNS VM at tenant level.  
          sudo ansible-playbook createL3DNS.yml  // creates DNS VM at subnet level.  

**Read:**
List down the DNS parameters which are stored in the log files.  
Log file for each tenant specific DNS is stored in /etc/tenants/<tenant_id>  
For DNS:   
Eg: DNS_T1_S1-L3DNS.json consists the DNS VM configuration at subnet level.  
Eg: t1-L2DNS1.json consists the DNS VM configuration at tenant level.  
Eg: Provider level DNS configuration is stored in the /etc/tenants/L1DNS-L1/L1DNS-L1.json.  

**Update:**
No update can be made to DNS configuration (in the VM level).The config files for bind are manually updated.   

**Delete:** 
User can remove the DNS VM's by running the python script delete_dns.py.  
command: python delete_dns.py  


## Prerequisites for ansible scripts:
The execution of scripts assumes that the controller network and provider namespace are already created.   
The disk images to create the VM's should be stored in the following path:
/home/ece792/images/<file>.img  
The provider Namespace is set as provider_ns in the scripts.

