import json
import requests
import time

logs = r"/var/log/remote/PA-SiteA/1,2026.log"
ip_api = "http://ip-api.com/json/"

with open(logs) as f:
    f = f.readlines()

log_list = []

for line in f:
    if "TRAFFIC,start" in line:
        log_list.append(line)

ip_cache = {}
sessions = {}
i = 0

for log in log_list:
    log = list(log.split(","))
    if log[8] in ip_cache:
        True
    else:
        i += 1
        dst_loc = requests.get(ip_api+log[8]).json()
        if 'country' in dst_loc:
            ip_cache[log[8]] = str(dst_loc['country']) +", "+ str(dst_loc['city'])
        elif i >= 45:
            time.sleep(60)
        else:
            ip_cache[log[8]] = "Skipped"    
        
    sessions[log[22]] = {
            "DATE": log[6],
            "SRC IP": log[7],
            "DST IP": log[8],
            "SRC PORT": log[24],
            "DST PORT": log[25],
            "DST LOC": ip_cache[log[8]],
            "APP": log[29],
            "ACTION": log[30],
            "COUNT": log[23]
    }

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(sessions, f, ensure_ascii=False, indent=4)

