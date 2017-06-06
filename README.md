# Icilambda : Managing icinga2 using lambda 
[![StackShare](https://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/dvopsway/icilambda)

## Introduction

The project primarily aims at simplyfying how monitoring is done in cloud (AWS), it uses power of icinga2 api, consul kv, aws tags and serverless technology(AWS Lambda) to manage monitoring seemlessly across environments.

## Project

This project helps you setup monitoring based on simpla role based aws tags, you can use consul kv as well to keep your settings. Lambda functions read those tags and create montitoring or delete it respectively. We are using nrpe agents right now, because we are using icinga2 api to create or delete monitoring, if we use icinga2 agent, then we won't be able to delete that node monitoring using api.

<p align="center">
  <img width="720" height="600" src="https://raw.githubusercontent.com/dvopsway/icilambda/master/Flow%20Chart.png">
</p>

## AWS Lambda Part 

The project has two lambda handlers:

```
add_checks.lambda_handler():
```

This handler starts with getting monitoring information based on tags set in aws instances and create a required checks profile for them, in case you want to override them create a kv in consul under monitoring/hostname.json with monitoring information. Once this information is collected it uses icinga api to create those checks. In case the checks are already there it simply moves on. With services this handler is also responsible for adding hosts and hostgroups. 

```
remove_checks.lambda_handler()
```

This handler is responsible for removing services which are not required anymore based on profile changes or required state changes, it also makes sure a host monitoring is removed if that host is terminated in AWS.

## Usage instruction


if you want to disable consul overriding make following setting false in properties.py

```
enable_consul = False
```

### Consul Configs:

In case you have enabled consul configs in properties.py. Following is the assumed kv paths:

- monitoring - top level dir in consul kv
  - nodes - This directory is used to override node tags.
    - node1.json - node1 is hostname with which machine is registered in icinga
    - node2.json 
  - conf
    - checks.json - used to overide all_checks variable in properties.py
    - profiles.json - used to override monitoring_profiles variablkes in properties.py
    
### Configs in properties.py

create monitoring profiles in properties.py based on your tag of aws instance:

for e.g:
```
monitoring_profiles = {
    "base": ["disk_check", "mem_check", "load_check", "procs_check"],
    "mongo": ["disk_check", "mem_check", "load_check", "procs_check", "proc_mongo"],
    "redis": ["disk_check", "mem_check", "load_check", "procs_check", "proc_redis"],
    "haproxy": ["disk_check", "mem_check", "load_check", "procs_check", "proc_haproxy", "proc_supervisor"],
    "elasticsearch": ["disk_check", "mem_check", "load_check", "procs_check", "proc_elasticsearch"],
}
```
The key in above dictionary will be set as tags on aws, key name will be 'Monitor' value would be profile name: for e.g for redis machine tag created would be:
```
Monitor : redis
```

Make sure checks that checks for tags you have defined in monitoring_profile have their definition in all_checks variable in properties.py
for e.g
```
all_checks = {
    "disk_check": {"templates": ["generic-service"],
                   "attrs": {
        "display_name": "disk utilization",
        "check_command": "disk",
        "vars.disk_all": True,
        "host_name": host
    }
    }
}
```
for more examples of checks, checkout properties.py

Make sure parameters in properties.py are updated, create a zip of files directly, that will be your lambda package. Deploy this lambda package in VPC (private subnets) which has access to consul cluster, icinga2 server. Also make sure that lambda role you are using should have access to read ec2 information. 

with the same zip file create two lambda functions:
- add_icinga_checks : lambda handler will be add_checks.lambda_handler .
- remove_icinga_checks : lambda handler will be remove_checks.lambda_handler .

To trigger these alerts use cloudwatch crons. 
- add_checks can run in every 15 mins.
- remove_checks will run more frequently to remove noise from system as soon as possible, a good number is every 2 mins.

Tip:
You can add these lambda code behind an api gateway to make the execution on demand, and call the url in userdata passed to the machine on its launch.
