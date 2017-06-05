import requests
import json
from properties import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def prepare_checks(profiles):
    checks = []
    for each in profiles:
        try:
            checks = checks + monitoring_profiles[each]
        except:
            print "monitoring profile %s doesn't exist" % each
    return list(set(checks))


def setup_hostgroup(hostgroup):
    hostgroup_data = {"attrs": {"display_name": hostgroup}}

    check_hostgroup = requests.get("%s/hostgroups/%s" % (icinga_api_endpoint,
                                                         hostgroup), auth=icinga_auth, headers=icinga_headers, verify=False)
    if check_hostgroup == 200:
        print "Hostgroup %s already exists" % hostgroup
        return True
    else:
        r = requests.put("%s/hostgroups/%s" % (icinga_api_endpoint, hostgroup), data=json.dumps(
            hostgroup_data), auth=icinga_auth, headers=icinga_headers, verify=False)
        if r.status_code == 200:
            print "Hostgroup %s Added Successfully" % hostgroup
            return True
        else:
            print "couldn't add hostgroup %s" % hostgroup
            return False


def setup_host(host, address, hostgroup):
    host_data = {
        "templates": ["generic-host"],
        "attrs": {
            "address": address,
            "vars.hostgroups": "X,%s,X" % hostgroup,
            "groups": [hostgroup],
        }
    }
    check_host = requests.get("%s/hosts/%s" % (icinga_api_endpoint, host),
                              auth=icinga_auth, headers=icinga_headers, verify=False)
    if check_host.status_code == 200:
        print "Host %s already exists" % host
        return True
    else:
        r = requests.put("%s/hosts/%s" % (icinga_api_endpoint, host), data=json.dumps(
            host_data), auth=icinga_auth, headers=icinga_headers, verify=False)
        if r.status_code == 200:
            print "Host %s Added Successfully" % host
            return True
        else:
            print "Couldn't add host %s" % host
            print r.content
            return False


def setup_service(host, service, service_data):
    check_service = requests.get("%s/services/%s!%s" % (icinga_api_endpoint,
                                                        host, service), auth=icinga_auth, headers=icinga_headers, verify=False)
    if check_service.status_code == 200:
        print "Service %s already exists on host %s" % (service, host)
        return True
    else:
        r = requests.put("%s/services/%s!%s" % (icinga_api_endpoint, host, service),
                         data=json.dumps(service_data), auth=icinga_auth, headers=icinga_headers, verify=False)
        print r.status_code
        if r.status_code == 200:
            print "Service %s Added Successfully on Host %s" % (service, host)
            return True
        else:
            print "Couldn't add Service %s on Host %s" % (service, host)
            print r.content
            return False


def restart_icinga():
    restart_response = requests.post(
        "%s/actions/restart-process" % icinga_api_endpoint, auth=icinga_auth, headers=icinga_headers, verify=False)
    if restart_response == 200:
        print "icinga2 restarted successfully"
    else:
        print "couldn't get response for icinga2 restart , please verify once if icinga is up"


def get_icinga_state():
    icinga_data = {}
    icinga_state = requests.get("%s/services?attrs=display_name&attrs=check_command&joins=host.name&joins=host.address" %
                                (icinga_api_endpoint), auth=icinga_auth, headers=icinga_headers, verify=False)
    for k, v in json.loads(icinga_state.content).iteritems():
        for each in v:
            var = each['name'].split("!")
            if var[0] not in excluded_machines and var[1] not in excluded_services:
                if var[0] in icinga_data:
                    icinga_data[var[0]].append(var[1])
                else:
                    icinga_data[var[0]] = [var[1]]
    return icinga_data


def remove_service(host, service):
    check_service = requests.get("%s/services/%s!%s" % (icinga_api_endpoint,
                                                        host, service), auth=icinga_auth, headers=icinga_headers, verify=False)

    if check_service.status_code == 200:
        delete_service = requests.delete("%s/services/%s!%s?cascade=1" % (
            icinga_api_endpoint, host, service), auth=icinga_auth, headers=icinga_headers, verify=False)
        if delete_service.status_code == 200:
            print "Service %s is deleted from host %s" % (service, host)
            return True
        else:
            print "Couldn't delete Service %s from host %s" % (service, host)
            return False
    else:
        print "Service %s not found on Host %s" % (service, host)
        return True


def remove_host(host):
    check_host = requests.get("%s/hosts/%s" % (icinga_api_endpoint, host),
                              auth=icinga_auth, headers=icinga_headers, verify=False)

    if check_host.status_code == 200:
        delete_host = requests.delete("%s/hosts/%s?cascade=1" % (
            icinga_api_endpoint, host), auth=icinga_auth, headers=icinga_headers, verify=False)
        if delete_host.status_code == 200:
            print "Host %s is deleted" % host
            return True
        else:
            print "Couldn't delete Host %s" % host
            return False
    else:
        print "Host %s not found" % host
        return True
