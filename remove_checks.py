import requests
import json
import boto3
import collections
from properties import *
from icinga import *

ec = boto3.client('ec2')


def get_required_state():
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

    for instance in instances:

        monitoring_tag = [
            t.get('Value') for t in instance['Tags']
            if t['Key'] == 'Monitor'][0]
        host = [
            t.get('Value') for t in instance['Tags']
            if t['Key'] == 'Name'][0] + "." + domain_name

        if enable_consul:
            check_consul = requests.get(
                "http://%s:8500/v1/kv/monitoring/%s.json" % (consul_host, host))

            required_state = {}
            if len(check_consul.content) == 0:
                for check in prepare_checks([monitoring_tag]):
                    if host in required_state:
                        required_state[host].append(check)
                    else:
                        required_state[host] = [check]
            else:
                checks_on_consul = json.loads(json.loads(check_consul.content)[
                    0]['Value'].decode("base64"))
                for k, v in checks_on_consul.iteritems():
                    if host in required_state:
                        required_state[host].append(k)
                    else:
                        required_state[host] = [k]
        else:
            for check in prepare_checks([monitoring_tag]):
                if host in required_state:
                    required_state[host].append(check)
                else:
                    required_state[host] = [check]

        return required_state


def start_purging(required_state, icinga_state):
    hosts_removed = []
    for icinga_host, icinga_services in icinga_state.iteritems():
        for icinga_service in icinga_services:
            if icinga_host in required_state:
                if icinga_service not in required_state[icinga_host]:
                    remove_service(icinga_host, icinga_service)
            elif icinga_host not in hosts_removed:
                hosts_removed.append(icinga_host)
                remove_host(icinga_host)


def lambda_handler():
    required_state = get_required_state()
    icinga_state = get_icinga_state()
    start_purging(required_state, icinga_state)
