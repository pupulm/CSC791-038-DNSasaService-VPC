import os
from time import sleep

num_of_vms_del = input("Enter the number of VMs to delete\n")
vm_names = []

for vm in range(num_of_vms_del):
    vm_names.append(raw_input("Enter the vm "+str(vm+1)+" name\n"))

    print "Deleting VMs\n"

for vm_name in vm_names:
    os.system("sudo virsh destroy " + vm_name)
    sleep(1)
    os.system("sudo virsh undefine " + vm_name)
    sleep(1)

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

