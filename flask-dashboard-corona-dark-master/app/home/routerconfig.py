import os
import sys
import csv
import json
import time
import napalm
import pickle
import ipaddress
import threading
import subprocess
import multiprocessing

from ctypes import c_uint
from datetime import datetime
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from flask import render_template, redirect, url_for, request

num_threads = multiprocessing.cpu_count()
print_lock = threading.Lock()


driver = napalm.get_network_driver("ios")

filenames = {
    'R1': "Core_1.txt",
    'R2': "Internal_1.txt",
    'R3': "Internal_2.txt",
    'R4': "Edge_1.txt",
    'R5': "Edge_2.txt",
}

def Is_connected(dev, conn):
    try:
      conn.open()
      conn.close()
      now = datetime.now()
      timestr = now.strftime("%c")
    except:
      return {
        dev:'Offline',
        'time': timestr,
      }
    return {
      dev:'Active',
      'time': timestr,
    }
   
def checkHealth():
  devstat = ['Offline', 'Offline', 'Offline', 'Offline', 'Offline']
  devstatus = list() 
  devices = getCredentials()
  try:
    with ThreadPoolExecutor(max_workers=num_threads) as thread:
      exe = {
        thread.submit(
          Is_connected, 
          dev,
          devices[dev] 
        ): dev for dev in devices
      } 
      for item in as_completed(exe):
        if item.result():
          devstatus.append(item.result())
  except Exception as e:
    print(f"Ooops!! Something went wrong while checking router health\n{e}")
  for d in devstatus:
    if list(d.keys())[0] == 'R1':
      devstat[0] = [d['R1'], d['time']] 
    if list(d.keys())[0] == 'R2':
      devstat[1] = [d['R2'], d['time']] 
    if list(d.keys())[0] == 'R3':
      devstat[2] = [d['R3'], d['time']] 
    if list(d.keys())[0] == 'R4':
      devstat[3] = [d['R4'], d['time']] 
    if list(d.keys())[0] == 'R5':
      devstat[4] = [d['R5'], d['time']] 
  return devstat 

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
      dev.load_merge_candidate(filename=config_file)
      diff = dev.compare_config().replace('\n', '<br />')
      #response += f"<p style='color:red;'>{diff}</p>"
      dev.discard_config()
      dev.close()
    except OSError:
      dev.close()
      pass
    except Exception as e: 
      print(f'Unable to fetch diff: \n{e}')
      pass  
    return diff 

def commitDiff(routerName):
    diff_comm = f'Unable to Commit router {routerName}'
    config_file = f"../{filenames[routerName]}" 
    try:
      dev = getCredentials()[routerName]
      dev.open()
      if not (os.path.exists(config_file) and os.path.isfile(config_file)):
        diff_comm = diff_comm + f"\nMissing or invalid golden config file" 
        print('Missing or invalid golden config file')
        return diff_comm
      dev.load_merge_candidate(filename=config_file)
      dev.commit_config()
      dev.close()
    except OSError:
      print(f"OSERROR: {routerName}")
      dev.close()
      pass
    except Exception as e: 
      print(f'Unable to Commit diff: \n{e}')
      return {routerName:0}
    return {routerName:1}

def commit_all():
    commitstatus = list()
    try:
      with ThreadPoolExecutor(max_workers=num_threads) as thread:
        exe = {
          thread.submit(
            commitDiff, 
            routerName,
          ): routerName for routerName in filenames.keys()
        } 
        for item in as_completed(exe):
          if item.result():
            commitstatus.append(item.result())
    except Exception as e:
      print(f"Ooops!! Something went wrong committing all diffs:\n{e}")
    print(commitstatus)
    return commitstatus 
    

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
      for b in bgpstr['global']:
        tlist = list()
        currdict = bgpstr['global'][b][0]
        tlist.append(currdict['local_as'])
        tlist.append(currdict['remote_as'])
        tlist.append(currdict['remote_address'])
        tlist.append(currdict['connection_state'])
        nList.append(tlist)
        
      dev.close()
    except OSError:
      pass
      dev.close()
    except Exception as e: 
      print(f'{errormsg} \n{e}')
      dev.close()
      pass  
    return nList 
