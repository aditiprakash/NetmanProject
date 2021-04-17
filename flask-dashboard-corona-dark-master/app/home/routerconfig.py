import os
import sys
import csv
import json
import time
import napalm
import pickle
import ipaddress


from ctypes import c_uint
from datetime import datetime
from flask import render_template, redirect, url_for, request

driver = napalm.get_network_driver("ios")


def getCredentials():
  cred = dict()
  filename = 'app/home/SSHCred.csv'
  try:
    with open(filename) as csvfile:
      reader = csv.DictReader(csvfile)
      for row in reader:
        tempDict = dict(row)
        cred[tempDict['router']] = driver(
          hostname=tempDict['ip'],
          username=tempDict['username'],
          password=tempDict['password'],  
          optional_args={
            'dest_file_system': 'disk0:',
            'secret': tempDict['password'],
            'global_delay_factor': 2,
          }
        )
      return cred
  except Exception as e:
    print(f"File not found: \n{e}")
    # raise e
    return cred

def getInterfaces(routerName):
    interfaces = None
    try:
      dev = getCredentials()[routerName]
      dev.open()
      interfaces = dev.get_interfaces_ip()
      dev.close()
    
    except KeyError:
      pass

    except Exception as e:
      print(f"Unable to fetch interfaces: \n{e}")
      pass
    return interfaces




