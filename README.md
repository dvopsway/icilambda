# Icilambda : Managing icinga2 using lambda 

## Introduction

The project primarily aims at simplyfying how monitoring is done in cloud (AWS), it uses power of icinga2 api, consul kv, aws tags and serverless technology(AWS Lambda) to manage monitoring seemlessly across environments.

## Project

This project help you setup monitoring based on simpla role based aws tags, you can use consul ks as well to keep you settings. Lambda functions reads those tags and sets up montitoring or delete it.

###Flow Chart

![Icilambda flow chart](https://github.com/dvopsway/icilambda/blob/master/Flow%20Chart.png)

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
