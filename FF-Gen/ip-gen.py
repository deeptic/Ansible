#!/usr/bin/env python
from pprint import pprint
from jnpr.junos import Device
import yaml
import sys
import os
import jinja2
import ipaddress
from glob import glob
from jinja2 import Template
from netaddr.ip import IPNetwork, IPAddress

src1_start = IPAddress ('191.0.0.0')
dst1_start = IPAddress ('38.0.1.1')

yamlfile = open("roles/ff-gen/vars/main.yml", "wb")

yamlfile.write("---\n")
yamlfile.write("builddir: /etc/ansible/playbooks/FF-Gen\n")
yamlfile.write("\n")

yamlfile.write("ips:\n")

for x in range(0,25600,256):
    data = " - [ " + "'" + str(src1_start) + "'" + ' , ' + "'" + str(dst1_start + x) + "'" + " ]" + "\n"
    yamlfile.write(data)






