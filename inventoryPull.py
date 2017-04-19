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
hostNameList = []
for instance in instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            tag = tags['Value']
    hostList.append(instance.private_ip_address)
    hostNameList.append(tag)


linuxList = []
windowsList = []
linuxNameList = []
windowsNameList = []

for instance in instances:
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            tag = tags['Value']
    if instance.platform != 'windows':
        linuxList.append(instance.private_ip_address)
        linuxNameList.append(tag)
    else:
        windowsList.append(instance.private_ip_address)
        windowsNameList.append(tag)


#add the hosts to the json output    
output = dict(all=dict (hosts=hostList), linux=dict(hosts=linuxList), windows=dict(hosts=windowsList))
nameOutput = dict(all=dict (hosts=hostNameList), linux=dict(hosts=linuxNameList), windows=dict(hosts=windowsNameList))

if len(sys.argv) == 1:
    print ('please run with parameter --file for file output and --list for json output to console')
    sys.exit()


#dump to file if user asks.  json and regular text
if sys.argv[1]=='--IP':
    with open('jsonoutput.txt', 'w') as outfile:
        json.dump(output, outfile,indent=4)

    with open('regoutput.txt', 'w') as outfile:
        outfile.write('[all]'+'\n')
        for x in hostList:
            outfile.write(x+'\n')  
        outfile.write('\n'+'[linux]'+'\n')
        for x in linuxList:
            outfile.write(x+'\n')  
        outfile.write('\n'+'[windows]'+'\n')
        for x in windowsList:
            outfile.write(x+'\n')  

elif sys.argv[1]=='--name':
    with open('jsonoutput.txt', 'w') as outfile:
        json.dump(nameOutput, outfile,indent=4)

    with open('regoutput.txt', 'w') as outfile:
        outfile.write('[all]'+'\n')
        for x in hostNameList:
            outfile.write(x+'\n')
        outfile.write('\n'+'[linux]'+'\n')
        for x in linuxNameList:
            outfile.write(x+'\n')
        outfile.write('\n'+'[windows]'+'\n')
        for x in windowsNameList:
            outfile.write(x+'\n')

elif sys.argv[1]=='--list':
#dump to std out for ansible
    print (json.dumps(output,indent=4))

elif sys.argv[1]=='--host':
    emptyDict=dict()
    print (json.dumps(emptyDict,indent=4))

else:
    print ('please run with parameter --IP for ip output, --name for name output and --list for json output to console')
