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

filenames = {
    'R1': "Core_1.txt",
    'R2': "Internal_1.txt",
    'R3': "Internal_2.txt",
    'R4': "Edge_1.txt",
    'R5': "Edge_2.txt",
}

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

def getConfig(routerName):
    config = f'Unable to fetch config for router {routerName}'
    try:
      dev = getCredentials()[routerName]
      dev.open()
      config = dev.get_config()['running'].replace('\n', '<br />')
      #response += f"<p style='color:red;'>{config}</p>"
      dev.close()
    except: 
      print('Unable to fetch config')
      pass  
    return config 

def getDiff(routerName):
    diff = f'Unable to fetch diff for router {routerName}'
    config_file = f"../{filenames[routerName]}" 
    try:
      dev = getCredentials()[routerName]
      dev.open()
      if not (os.path.exists(config_file) and os.path.isfile(config_file)):
        diff = diff + f"\nMissing or invalid golden config file" 
        print('Missing or invalid golden config file')
        return diff
      dev.load_replace_candidate(filename=config_file)
      diff = dev.compare_config().replace('\n', '<br />')
      #response += f"<p style='color:red;'>{diff}</p>"
      dev.discard_config()
      dev.close()
    except OSError:
      pass
    except Exception as e: 
      print(f'Unable to fetch diff: \n{e}')
      pass  
    return diff 

def getOspfNeighbors(routerName):
    nList = list()
    errormsg = f'Unable to fetch OSPF Neighbors for router {routerName}'
    try:
      dev = getCredentials()[routerName]
      dev.open()

      ospfstr = dev.cli(['show ip ospf neighbor'])['show ip ospf neighbor']
      tlist = ospfstr.split('\n')
      tmmlist = list()
      for t in tlist[1:]:
          tmlist = list()
          for tm in t.split(' '):
              if not tm == '':
                  tmlist.append(tm)
          tmmlist.append(tmlist)
      nList = tmmlist    
      dev.close()
    except OSError:
      pass
      dev.close()
    except Exception as e: 
      print(f'{errormsg} \n{e}')
      pass  
    return nList 
    
def getBgpNeighbors(routerName):
    nList = list()
    errormsg = f'Unable to fetch BGP Neighbors for router {routerName}'
    try:
      dev = getCredentials()[routerName]
      dev.open()

      bgpstr = dev.get_bgp_neighbors_detail()
      for b in bgpstr.keys():
        print(b)
        print(bgbstr[b])

      dev.close()
    except OSError:
      pass
      dev.close()
    except Exception as e: 
      print(f'{errormsg} \n{e}')
      dev.close()
      pass  
    return nList 
