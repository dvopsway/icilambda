icinga_api_endpoint = "https://127.0.0.1:4665/v1/objects"
enable_consul = False
consul_host = "localhost"
icinga_auth = ("root", "icinga")
icinga_headers = {"Accept": "application/json"}
excluded_machines = ['docker-icinga2']
excluded_services = ['ssh', 'ping4']
host = None

monitoring_profiles = {
    "base": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check"],
    "thumbor": ["disk_check", "mem_check", "load_check", "procs_check_thumbor", "iowait_check"],
    "mongo": ["disk_check", "mem_check", "load_check", "procs_check", "proc_mongo", "iowait_check"],
    "redis": ["disk_check", "mem_check", "load_check", "procs_check", "proc_redis", "iowait_check"],
    "haproxy": ["disk_check", "mem_check", "load_check", "procs_check", "proc_haproxy", "iowait_check"],
    "elasticsearch": ["disk_check", "mem_check", "load_check", "procs_check", "proc_elasticsearch", "iowait_check"],
    "dns": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check"],
    "cassandra": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check", "check_cassandra_client", "check_cassandra_cluster"],
    "vpn": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check"],
    "api": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check", "api_check"],
    "kafka": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check", "check_kafka"],
    "logstash": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check"],
    "solr": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check", "check_solr"],
    "storm": ["disk_check", "mem_check", "load_check", "procs_check", "iowait_check"]
}

if enable_consul:
    check_profile_on_consul = requests.get(
        "http://%s:8500/v1/kv/monitoring/conf/profiles.json" % consul_host)

    if len(check_profile_on_consul.content) != 0:
        monitoring_profiles = json.loads(json.loads(check_profile_on_consul.content)[
            0]['Value'].decode("base64"))

all_checks = {
    "disk_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "disk utilization",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_disk"
        }
    },
    "mem_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "memory utilization",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_mem"
        }
    },
    "load_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "cpu load",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_load"
        }
    },
    "procs_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "check processes",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_procs"
        }
    },
    "procs_check_thumbor": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "check processes",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_procs_thumbor"
        }
    },
    "iowait_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "check iostat",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_iowait"
        }
    },
    "cpu_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "check cpu",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_cpu"
        }
    },
    "file_descriptors": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "file descriptors",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_cpu"
        }
    },
    "read_only_fs": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "read only filesystem",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_rofs"
        }
    },
    "running_kernel": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "running kernel",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_running_kernel"
        }
    },
    "tcp_states": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "tcp connections",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_tcp_states"
        }
    },
    "proc_httpd": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "httpd process",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_httpd"
        }
    },
    "proc_redis": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "redis process",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_redis"
        }
    },
    "proc_haproxy": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "haproxy process",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_haproxy"
        }
    },
    "proc_supervisor": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "supervisor process",
            "check_command": "nrpe",
            "vars.nrpe_command": "icinga_check_supervisor"
        }
    },
    "proc_elasticsearch": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "elasticsearch process",
            "check_command": "tcp",
            "vars.tcp_port": 9200
        }
    },
    "proc_mongo": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "Mongo port check",
            "check_command": "tcp",
            "vars.tcp_port": 27017
        }
    },
   "api_check": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "api port check",
            "check_command": "tcp",
            "vars.tcp_port": 8080
        }
    },
    "check_cassandra_thrift": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "cassandra thrift port check",
            "check_command": "tcp",
            "vars.tcp_port": 9160
        }
    },
    "check_cassandra_client": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "cassandra client port check",
            "check_command": "tcp",
            "vars.tcp_port": 9042
        }
    },
    "check_cassandra_cluster": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "cassandra cluster port check",
            "check_command": "tcp",
            "vars.tcp_port": 7000
        }
    },
    "check_kafka": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "kafka port check",
            "check_command": "tcp",
            "vars.tcp_port": 9092
        }
    },
    "check_solr": {
        "templates": ["generic-service"],
        "attrs": {
            "display_name": "solr port check",
            "check_command": "tcp",
            "vars.tcp_port": 8080
        }
    }

}

if enable_consul:
    checks_on_consul = requests.get(
        "http://%s:8500/v1/kv/monitoring/conf/checks.json" % consul_host)

    if len(checks_on_consul.content) != 0:
        all_checks = json.loads(json.loads(checks_on_consul.content)[
            0]['Value'].decode("base64"))
