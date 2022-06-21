#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:13:26 2022

@author: noboru
"""

from telnetlib import Telnet
from socket import socket,AF_INET,SOCK_STREAM

#You might want to edit this variable if ever the BE fanless
#computer change hostname.
hostname = "wnidcs"

def check_connection():
    '''
    Check if nidcsHxRG is running on wnidcs server.

    Returns
    -------
    bool
        Will return True if we are able to connect to wnidcs on port 5555.
        Otherwise it return False.

    '''
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(10) #we will wait 10 seconds before cloising connection
    try:
        ret = sock.connect_ex((hostname,5555)) 
    except :
        sock.close()
        print("Unable to reach hostname wnidcs.")
        return False
    if ret!=0:
        sock.close()
        print("!!! Warning !!!")
        print("we are able to connect to wnidcs, but nidcsHxRG seems to be not running or busy")
        return False
    else:
        sock.close()
        return True
#check the connection to the server
if not check_connection():
    exit(0)
#connection is ok we will attempt to send the closeMacie command
tn = Telnet()
tn.open(hostname,5555)
#check if we receive the ECHO daemon form nidcsHxRG
echo = tn.read_until(b'\n',timeout=5)
if 'ECHO' not in echo.decode():
    print("We are not sure where we are connected, exiting ...")
    tn.close()
    exit(0)
#write closeMacie
tn.write(b"closeMacie")
ret = tn.read_until(b'\n',timeout=15)
ret = ret.decode()
if ret=='' or 'NOK' in ret:
    print("NOK")
    tn.close()
    exit(0)
print(ret.strip())
print("done!")
    