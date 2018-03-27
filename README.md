# AWS-Inventory
This is a dynamic inventory script for ansible written in python.  It works in a single AWS account scenario.  

## usage
```ansible-playbook -i aws-inventory.py <playbookname>```
- the default use case.  this calls the script from ansible and the inventory of ec2-instances is dynamically pulled

 ```python aws-inventory.py --list```
 - outputs json to stdout.  Ansible calls the script through this method.
 
 ```python aws-inventory.py --file```
 - outputs IP addresses to a flat file and to json
