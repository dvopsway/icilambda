import requests
import json
import boto3
import collections
from properties import *
from icinga import *

ec = boto3.client('ec2')


def lambda_handler():
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': ['monitor', 'Monitor']},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print "Found %d instances that need monitoring" % len(instances)

    for instance in instances:
        try:
            monitoring_tag = [
                t.get('Value') for t in instance['Tags']
                if t['Key'] == 'Monitor'][0]
            host = [
                t.get('Value') for t in instance['Tags']
                if t['Key'] == 'Name'][0] + "." + domain_name
            state = instance['State']['Name']
            if str(state) == "running" or str(state) == "stopped":
                setup_hostgroup(monitoring_tag)
                if enable_consul:
                    check_consul = requests.get(
                        "http://%s:8500/v1/kv/monitoring/%s.json" % (consul_host, host))

                    print "Setting up monitoring for %s(%s)" % (instance['InstanceId'], host)
                    if setup_host(host, str(instance['PrivateIpAddress']), str(monitoring_tag)):
                        if len(check_consul.content) == 0:
                            for check in prepare_checks([monitoring_tag]):
                                setup_service(host, check, all_checks[check])
                        else:
                            checks_on_consul = json.loads(json.loads(check_consul.content)[
                                0]['Value'].decode("base64"))
                            for k, v in checks_on_consul.iteritems():
                                setup_service(host, k, v)
                else:
                    for check in prepare_checks([monitoring_tag]):
                        setup_service(host, check, all_checks[check])


        except IndexError:
            print "Couldn't find tag"

