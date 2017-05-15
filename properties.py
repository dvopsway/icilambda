icinga_api_endpoint = "https://127.0.0.1:4665/v1/objects"
enable_consul = False
consul_host = "localhost"
icinga_auth = ("root", "icinga")
icinga_headers = {"Accept": "application/json"}
excluded_machines = ['docker-icinga2']
excluded_services = ['ssh', 'ping4']
host = None

monitoring_profiles = {
    "base": ["disk_check", "mem_check", "load_check", "procs_check"],
    "mongo": ["disk_check", "mem_check", "load_check", "procs_check", "proc_mongo"],
    "redis": ["disk_check", "mem_check", "load_check", "procs_check", "proc_redis"],
    "haproxy": ["disk_check", "mem_check", "load_check", "procs_check", "proc_haproxy", "proc_supervisor"],
    "elasticsearch": ["disk_check", "mem_check", "load_check", "procs_check", "proc_elasticsearch"],
}

all_checks = {
    "disk_check": {"templates": ["generic-service"],
                   "attrs": {
        "display_name": "disk utilization",
        "check_command": "disk",
        "vars.disk_all": True,
        "host_name": host
    }
    },
    "mem_check":  {"templates": ["generic-service"],
                   "attrs": {
        "display_name": "memory utilization",
        "check_command": "mem",
        "vars.mem_used": True,
        "vars.mem_warning": 90,
        "vars.mem_critical": 95,
        "host_name": host
    }
    },
    "load_check":  {"templates": ["generic-service"],
                    "attrs": {
        "display_name": "cpu load",
        "check_command": "load",
        "vars.load_percpu": True,
        "host_name": host
    }
    },
    "procs_check":  {"templates": ["generic-service"],
                     "attrs": {
        "display_name": "check processes",
        "check_command": "procs",
        "vars.procs_warning": 800,
        "vars.procs_critical": 1000,
                     "host_name": host
    }
    },
    "iostat_check": {
        "attrs": {
            "display_name": "check iostat",
            "check_command": "iostat",
            "vars.iostat_disk": 1,
            "vars.iostat_wtps": 800,
            "vars.iostat_wread": 5000,
            "vars.iostat_wwrite": 5000,
            "vars.iostat_ctps": 1000,
            "vars.iostat_cread": 7000,
            "host_name": host
        }
    },
    "cpu_check":  {"templates": ["generic-service"],
                   "attrs": {
        "display_name": "check cpu",
        "check_command": "cpu",
        "vars.crit_pct_user_cpu": 95,
        "vars.crit_pct_sys_cpu": 95,
        "host_name": host
    }
    },
    "file_descriptors":  {"templates": ["generic-service"],
                          "attrs": {
        "display_name": "file descriptors",
        "check_command": "file_descriptors",
        "host_name": host
    }
    },
    "read_only_fs":  {"templates": ["generic-service"],
                      "attrs": {
        "display_name": "read only filesystem",
        "check_command": "rofs",
        "host_name": host
    }
    },
    "running_kernel":  {"templates": ["generic-service"],
                        "attrs": {
        "display_name": "running kernel",
        "check_command": "running_kernel",
        "host_name": host
    }
    },
    "tcp_states":  {"templates": ["generic-service"],
                    "attrs": {
        "display_name": "tcp connections",
        "check_command": "tcp_states",
        "host_name": host
    }
    },
    "proc_httpd":  {"templates": ["generic-service"],
                    "attrs": {
        "display_name": "httpd process",
        "check_command": "procs",
        "vars.procs_command": "httpd",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    },
    "proc_mongo":  {"templates": ["generic-service"],
                    "attrs": {
        "display_name": "mongod process",
        "check_command": "procs",
        "vars.procs_command": "mongod",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    },
    "proc_redis":  {"templates": ["generic-service"],
                    "attrs": {
        "display_name": "redis process",
        "check_command": "procs",
        "vars.procs_command": "redis",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    },
    "proc_haproxy":  {"templates": ["generic-service"],
                      "attrs": {
        "display_name": "haproxy process",
        "check_command": "procs",
        "vars.procs_command": "haproxy",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    },
    "proc_supervisor":  {"templates": ["generic-service"],
                         "attrs": {
        "display_name": "supervisor process",
        "check_command": "procs",
        "vars.procs_command": "supervisord",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    },
    "proc_elasticsearch":  {"templates": ["generic-service"],
                            "attrs": {
        "display_name": "elasticsearch process",
        "check_command": "procs",
        "vars.procs_command": "elasticsearch",
        "vars.procs_warning": "1:",
        "vars.procs_critical": "1:",
        "vars.procs_metric": "PROCS",
        "host_name": host
    }
    }
}
