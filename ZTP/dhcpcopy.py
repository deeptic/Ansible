#!/usr/bin/env python

global logFile
global local
global remotepath


logFile = "/Users/deeptic/Desktop/deeptic/Desktop/dhcpconf/plog.txt"
local = "/Users/deeptic/Desktop/deeptic/Desktop/dhcpconf/dhcpd.conf"
remotepath = "/home/devops/Desktop"


def copyDhcp(host, user, password):
        import pexpect

        global sshServer

        remote = user + '@' + host + ':' + remotepath
        sshServer = user + '@' + host

        try:
                scp_command = "scp " + local + ' ' + remote

                session = pexpect.spawn(scp_command)
                session.logfile= open(logFile, "w")
                i = session.expect(["password:", pexpect.EOF])

                if i==0:
                        session.sendline(password)
                        print "File Copy Completed !"
                        session.expect(pexpect.EOF)
                elif i==1:
                        print "Got the key or connection timeout"
                        pass


        except Exception as msg:
                print "Terminating ... Error !"
                print msg




def runCmds(host, user, password):
                import pexpect

                global prompt
                prompt = '.*@.*\$'

                sshNewkey = 'Are you sure you want to continue connecting'

                session=pexpect.spawn("ssh %s" %sshServer)


                session.logfile= open(logFile, "w")

                chkKey=session.expect([sshNewkey,'password:',pexpect.EOF,pexpect.TIMEOUT],90) #0 if no key, 1 if has key

                if chkKey==0 :

                                print "\n\t => Server not known - Adding ssh key"

                                session.sendline("yes")

                                chkKey=session.expect([sshNewkey,'Password:',pexpect.EOF])

                if chkKey==1:

                                print "\n\t =>  Server ssh key known - Proceeding with password authentication"

                                session.sendline("%s" %password)
                                session.expect("%s" %prompt)

                                session.timeout=60

                                commandSet = ['date', 'sudo mv /home/devops/Desktop/dhcpd.conf /etc/dhcp/' ,'date', 'ls -lrt /etc/dhcp/' ,'date', 'sudo service isc-dhcp-server restart', 'date', 'date']

                                for element in commandSet:
                                        session.sendline("\r")
                                        session.expect("%s \r" %prompt)
                                        session.sendline("\r")
                                        session.sendline("%s \r" %element)
                                        session.sendline("\r")





                elif chkKey==2:

                        print "\n\t => Connection timeout"

                        pass



def main():
        import argparse

        parser = argparse.ArgumentParser(description='Copy DHCP config file to remote server')
        parser.add_argument("--host", dest="hostname", default="",metavar="HOST",help="Specify remote host")
        parser.add_argument("--username", dest="username", metavar="USERNAME",help="Specify the username")
        parser.add_argument("--password", dest="password", metavar="PASSWORD",help="Specify the password")
        args = parser.parse_args()

        host = args.hostname
        user = args.username
        password = args.password

        copyDhcp(host, user, password)
        runCmds(host, user, password)


if __name__ == "__main__":
        main()
