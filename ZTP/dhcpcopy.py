#!/usr/bin/env python    

import pexpect
import argparse

parser = argparse.ArgumentParser(description='Copy DHCP config file to remote server')
parser.add_argument("--host", dest="hostname", default="",metavar="HOST",help="Specify remote host")
parser.add_argument("--username", dest="username", metavar="USERNAME",help="Specify the username")
parser.add_argument("--password", dest="password", metavar="PASSWORD",help="Specify the password")
args = parser.parse_args()

host = args.hostname
user = args.username
var_password = args.password
logFile = "/Users/deeptic/Desktop/deeptic/Desktop/dhcpconf/plog.txt"
local = "/Users/deeptic/Desktop/deeptic/Desktop/dhcpconf/dhcpd.conf"
remotepath = "/home/devops/Desktop"
remote = user + '@' + host + ':' + remotepath 
    
try:
        var_command = "scp " + local + ' ' + remote
        
        
        var_child = pexpect.spawn(var_command)
        var_child.logfile= open(logFile, "w")
        i = var_child.expect(["password:", pexpect.EOF])

        if i==0:                 
                var_child.sendline(var_password)
                var_child.expect(pexpect.EOF)
        elif i==1: 
                print "Got the key or connection timeout"
                pass
                           

except Exception as msg:
        print "Terminating ... error !"
        print msg 
