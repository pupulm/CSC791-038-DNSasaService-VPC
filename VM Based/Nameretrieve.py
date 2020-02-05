import os
import json
import IPretrieve
import yaml

folders = os.listdir('/etc/tenants')

tenantvm = {}
L1dns=""
L2dns = {}
L3dns = {}
for i in range(0,len(folders)):
    files = os.listdir('/etc/tenants/'+folders[i])
    if "-L1" in folders[i]:
        L1dns = folders[i].split('.json')[0]
    else:
        tenantvm[folders[i]] = []
        L2dns[folders[i]] = []
        L3dns[folders[i]] = []
        for j in range(0,len(files)):
            if "VM" in files[j]:
                tenantvm[folders[i]].append(files[j].split('.json')[0])
            elif "-L2DNS" in files[j]:
                L2dns[folders[i]].append(files[j].split('.json')[0])
                temp = files[j].split('.json')[0]
                L2dns[folders[i]].append(temp[:len(temp)-1]+"2")
            elif "-L3DNS" in files[j]:
                L3dns[folders[i]].append(files[j].split('.json')[0])
"""
print tenantvm
print L1dns
print L2dns
print L3dns
"""
tenants = {}
for i in tenantvm:
    tenants[i]={}

for i in tenantvm:
    tenants[i]['VM'] = []
    tenant = tenantvm[i]
    for j in range(0,len(tenant)):
        ip = IPretrieve.getIP(tenantvm[i][j],'eth1')
        if ip!=-1:
            t = {tenantvm[i][j]:ip}
            tenants[i]['VM'].append(t)

for i in L2dns:
    tenants[i]['L2'] = []
    tenant = L2dns[i]
    for j in range(0,len(tenant)):
        ip = IPretrieve.getIP(L2dns[i][j],'eth0')
        if ip!=-1:
            t = {L2dns[i][j]:ip}
            tenants[i]['L2'].append(t)

for i in L3dns:
    tenants[i]['L3'] = []
    tenant = L3dns[i]
    for j in range(0,len(tenant)):
        ip = IPretrieve.getIP(L3dns[i][j],'eth0')
        if ip!=-1:
            t = {L3dns[i][j]:ip}
            tenants[i]['L3'].append(t)

tenants['L1'] = {L1dns:IPretrieve.getIP(L1dns,'eth0')}

print tenants
with open("vmips.yml",'w') as outfile:
    yaml.dump(tenants,outfile)

"""
raw = open("/etc/tenants/vmips.db","r+")
contents = raw.read().split("\n")
raw.seek(0)                        # <- This is the missing piece
raw.truncate()
raw.write(str(tenants))
raw.close()
"""




"""
IPretrieve.getIP(L1dns)

for i in tenantvm:
    tenant = tenantvm[i]
    for j in range(0,len(tenant)):
        IPretrieve.getIP(tenantvm[i][j])
"""
"""
for i in L2dns:
    tenant = tenantvm[i]
    for j in range(0,len(tenant)):
        IPretrieve.getIP(L2dns[i][j])
"""
