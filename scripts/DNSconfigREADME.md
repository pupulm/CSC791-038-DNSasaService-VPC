### This is the README for the script DNSconfig.py
1. This script does the automation by copying named.conf and forward.db to the specified containers.
2. named.conf and forward.db have to be uploaded by the user and should exist in the same directory.
3. The command to excute the script is:
   $sudo python DNSconfig.py <Tenant_id> 
4. Based on the tenant id the script displays tenant specific containers.
5. The user has to interact by giving the container name in which these files are to be copied.
6. This script prompts the user whether user wants firewall as the feature or not.
7. User can give yes to add the feature and no if he doesn't want.
