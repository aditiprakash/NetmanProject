import json
import csv
with open("interfaces.json","r") as json_file:
    routers = json.load(json_file)
with open('roles/router/vars/main.yaml','a+') as f:
      for i in routers:
        f.write("\n{}_routers:".format(i))
        for x in routers[i]:
            f.write("\n  - hostname: {}\n    username: {}\n    user_priv: {}\n    password: {}\n    ospf_network: {}\n    ospf_mask: {}\n    interfaces:".format(
                routers[i][x]['hostname'],
                routers[i][x]['username'],
                routers[i][x]['user_priv'],
                routers[i][x]['password'],
                routers[i][x]['ospf_network'],
                routers[i][x]['ospf_mask']
                ))
            for interface in routers[i][x]['interfaces']:
                f.write("\n    - interface: {}\n      description: {}\n      v4_address: {}\n      mask: {}".format(interface,
                routers[i][x]['interfaces'][interface]['description'],
                routers[i][x]['interfaces'][interface]['v4_address'],
                routers[i][x]['interfaces'][interface]['mask']))
            
            
            try:
                print(routers[i][x]['bgp_neighbors'])
                f.write("\n    AS_NUMBER: 65001\n    bgp_neighbors:")
                for bgp in routers[i][x]['bgp_neighbors']:
                   f.write("\n    - neighbor: {}\n      remote_as: {}".format(routers[i][x]['bgp_neighbors'][bgp]["ID"],
                    routers[i][x]['bgp_neighbors'][bgp]["AS"])) 
            except:
                pass
