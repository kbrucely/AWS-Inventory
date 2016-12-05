#!/usr/bin/python

import boto3
import json
import sys

#tells boto3 what service this is
ec2 = boto3.resource('ec2')
#this pulls all running instances into the instances collection
instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])


#declare a dictionary and start storing stuff by platform
hostList = []
for instance in instances:
    hostList.append(instance.private_ip_address)

linuxList = []
windowsList = []
for instance in instances:
    if instance.platform != 'windows':
        linuxList.append(instance.private_ip_address)
    else:
        windowsList.append(instance.private_ip_address)

#add the hosts to the json output    
output = dict(all=dict (hosts=hostList), linux=dict(hosts=linuxList), windows=dict(hosts=windowsList))

if len(sys.argv) == 1:
    print ('please run with parameter --file for file output and --list for json output to console')
    sys.exit()


#dump to file if user asks.  json and regular text
if sys.argv[1]=='--file':
    with open('jsonoutput.txt', 'w') as outfile:
        json.dump(output, outfile,indent=4)

    with open('regoutput.txt', 'w') as outfile:
        for instance in instances:
            outfile.write(instance.private_ip_address+'\n')  

elif sys.argv[1]=='--list':
#dump to std out for ansible
    print (json.dumps(output,indent=4))

elif sys.argv[1]=='--host':
    emptyDict=dict()
    print (json.dumps(emptyDict,indent=4))

else:
    print ('please run with parameter --file for file output and --list for json output to console')
