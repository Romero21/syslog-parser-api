************************************************************************************************
******************Simple Palo Alto traffic log parser and REST API project**********************
************************************************************************************************

This project was developed to practise processing and analyzing traffic logs from Palo Alto firewall.
Logs are gathered by syslog server, parsed by indexing, stored in json file and then filtered by Flask REST API.

-Read requirements.txt file and install all needed packages before running 
-For testing, place project to location /var/log/remote as in current version paths are not variable
-Sample logs from rsyslog server in PA-SiteA folder
-Flow: PA-SiteA -> rsyslog -> parser.py -> data.json -> api.py

--------------------------------------------------------------------------------------------------

-Example of API calls:
http://localhost:5000/logs
-> Returns all traffic logs sorted by date in json format. 

root@kvm:/var/log/remote/Parser# curl http://localhost:5000/logs
{
  "7": {
    "DATE": "2026/05/05 06:47:18",
    "SRC IP": "172.16.1.10",
    "DST IP": "192.168.1.10",
    "SRC PORT": "0",
    "DST PORT": "0",
    "DST LOC": "Skipped",
    "APP": "icmp",
    "ACTION": "allow",
    "COUNT": "15"
  },
  "24": {
    "DATE": "2026/05/05 23:49:58",
    "SRC IP": "172.16.1.10",
    "DST IP": "8.8.4.4",
    "SRC PORT": "56850",
    "DST PORT": "53",
    "DST LOC": "United States, Ashburn",
    "APP": "udp",
    "ACTION": "allow",
    "COUNT": "1"
  },
  "31": {
    "DATE": "2026/05/05 23:50:44",
    "SRC IP": "172.16.1.10",
    "DST IP": "8.8.4.4",
    "SRC PORT": "44790",
    "DST PORT": "53",
    "DST LOC": "United States, Ashburn",
    "APP": "tcp",
    "ACTION": "allow",
    "COUNT": "1"
  },
...

--------------------------------------------------------------------------------------------------

http://localhost:5000/logs/<IP>
-> Returns all traffic logs where IP is as source or destination. 

root@kvm:/var/log/remote/Parser# curl http://localhost:5000/logs/151.101.130.49
{
  "145": {
    "DATE": "2026/05/06 00:05:00",
    "SRC IP": "172.16.1.10",
    "DST IP": "151.101.130.49",
    "SRC PORT": "47300",
    "DST PORT": "443",
    "DST LOC": "Canada, Montreal",
    "APP": "tcp",
    "ACTION": "allow",
    "COUNT": "1"
  },
  "194": {
    "DATE": "2026/05/06 02:55:07",
    "SRC IP": "172.16.1.10",
    "DST IP": "151.101.130.49",
    "SRC PORT": "47324",
    "DST PORT": "443",
    "DST LOC": "Canada, Montreal",
    "APP": "tcp",
    "ACTION": "allow",
    "COUNT": "1"
  }
}

----------------------------------------------------------------------------------------------------

http://localhost:5000/stats/top-dst/<n>
-> Returns n top talkers of destination IPs. 

root@kvm:/var/log/remote/Parser# curl http://localhost:5000/stats/top-dst/8
{
  "8.8.8.8": 171,
  "8.8.4.4": 109,
  "91.189.91.157": 38,
  "142.251.38.142": 8,
  "142.251.141.174": 7,
  "142.251.209.3": 4,
  "142.251.38.131": 3,
  "151.101.130.49": 2
}
