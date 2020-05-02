#!/usr/bin/python3

# This program updates the code from the local machine to the host machine

import pexpect

f = open('passwords.txt')
passwords = f.readlines()

# First we need to stop the docker container running the backendserver
print("Trying to stop docker container")
child = pexpect.spawn('ssh taliban@45.76.32.59')
child.expect('taliban@*')
child.sendline(passwords[0])
option = child.expect(['#','Permission denied, please try again.','Connection refused'])

#if password is wrong we cannot do anything so its better to kill the child
if(option == 1 or option==2):
    print("Password Errada")
    child.kill
else:
    child.sendline('cd /home/taliban/cenas')
    child.expect('#')
    child.sendline('docker-compose down')
    option2 = child.expect(['Network cenas_default not found.','Stopping cenas_web_1 ...'])

    if(option2 == 0):
        print("Docker container already down")
    else:
        print("Stopped docker container")
        
    # After the container is stopped we need to update the backendserver with the changes intended
    print("Updating the backendserver with the local changes")
    child2 = pexpect.spawn('rsync -a backendserver/server/ taliban@45.76.32.59:/home/taliban/cenas')
    option3 = child2.expect(["taliban@45.76.32.59's password:","ssh: Could not resolve hostname","Connection refused"])
    if(option3 == 0):
        child2.sendline(passwords[0])
        print("Backend Server Updated, trying to start docker container")
    elif(option3 == 2):
        print("Could not connect to the machine, maybe it is down")
    else:
        print("Wrong hostname or maybe the machine is wrong")

    # Now that the code has been updated, it is time to start the docker containers again
    child3 = pexpect.spawn('ssh taliban@45.76.32.59')
    child3.expect('taliban@*')
    child3.sendline(passwords[0])
    child3.sendline('cd /home/taliban/cenas')
    child3.expect('#')
    child3.sendline('docker-compose up -d')
    child3.expect("#")
    child3.sendline('ls')
    child3.expect("#")
    print("Docker container running, everything should be ok")
    



