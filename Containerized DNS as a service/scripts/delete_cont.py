import os
from time import sleep

num_of_cont_del = input("Enter the number of Containers to delete\n")
cont_names = []

for cont in range(num_of_cont_del):
    cont_names.append(raw_input("Enter the container "+str(cont+1)+" name: "))

    print "Deleting Containers\n"

for cont_name in cont_names:
    os.system("sudo docker stop " + cont_name)
    sleep(1)
    os.system("sudo docker rm " + cont_name)
    sleep(1)


num_veth_del = input("Enter the number of subnets to delete\n")
bridge_names=[]

netns_name=""
if num_veth_del>0:
    netns_name=raw_input("Enter the vpc in which they exist\n")
    
for veth in range(num_veth_del):
    bridge_names.append(raw_input("Enter the subnet name\n"))
    
print "Deleting Subnets\n"

for bridge_name in bridge_names:
    os.system("sudo ip link set "+bridge_name+"vif2 down")
    os.system("sudo ip link del "+bridge_name+"vif2")
    os.system("sudo virsh net-destroy "+bridge_name)
    os.system("sudo virsh net-undefine "+bridge_name)
    os.system("sudo ip link set "+bridge_name+" down")
    os.system("sudo brctl delbr "+bridge_name)


vpc_del = raw_input("Would you like to delete the vpc ? (yes/no)\n")

netns_name=""
if vpc_del == "yes":
    if len(netns_name) > 0:
        os.system("sudo ip netns exec provider_ns ip link del "+netns_name+"vpc1_if2")
        os.system("sudo ip netns del "+netns_name)
    else:
        netns_name = raw_input("Enter the vpc name\n")
        os.system("sudo ip netns exec provider_ns ip link del "+netns_name+"vpc1_if2")
        os.system("sudo ip netns del "+netns_name)
        sleep(1)

elif vpc_del != "no":
    print "Invalid option"
