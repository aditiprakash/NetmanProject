# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.home.routerconfig import * 
import pandas

@blueprint.route('/index')
@login_required
def index():
    devstatus = checkHealth()
    R1status = devstatus[0]
    R2status = devstatus[1]
    R3status = devstatus[2]
    R4status = devstatus[3]
    R5status = devstatus[4]
    return render_template(
      'index.html', 
      segment='index',
      R1status=R1status, 
      R2status=R2status, 
      R3status=R3status, 
      R4status=R4status, 
      R5status=R5status, 
    )

# @blueprint.route('/bgtest')
# def bgtest():
#     testthis()
#     return render_template("index.html", segment='index')


@blueprint.route('/<router>/<template>')
@login_required
def route_template(router,template):

    try:

        if "basic-table" in template:
            test = ['test', 'test', 'test', 'test', 'test', 'test']
            intList = list() 
            oneighborList = list() 
            bneighborList = list() 

            interfaces = getInterfaces(router)
            if not bool(interfaces):
              intList = [test, test, test]
            for iface in interfaces.keys():
              tempList = list()
              tempList.append(iface)
              tempList.append(list(interfaces[iface]['ipv4'].keys())[0])
              tempList.append(list(list(interfaces[iface]['ipv4'].values())[0].values())[0])
              intList.append(tempList)
           

            try:
              oneighborList = getOspfNeighbors(router)
            except Exception as e:
              print(f'Unable to fetch ospf neighbors: \n{e}')

            try:
              bneighborList = getBgpNeighbors(router)
            except Exception as e:
              print(f'Unable to fetch ospf neighbors: \n{e}')

            return render_template(
                "basic-table.html", 
                interfaces=intList, 
                oneighbors=oneighborList,
                bneighbors=bneighborList,
            )

        if "typography" in template:
            config = 'Unable to fetch config'
            diff = 'Unable to fetch diff'
            try:
              config = getConfig(router) 
              diff = getDiff(router)
            except:
              pass
            return render_template("typography.html", config=config, diff=diff, router = router)


        if "chartjs" in template:
            # print(router, type(router))
            index = int(router[1])
            # print(index)
            colnames = ['R1','R2','R3','R4','R5']
            data = pandas.read_csv('app/home/cpu.csv',header=1,names=colnames)
              
            list_cpu_list = list()
            list_cpu_list.append(data.R1.tolist())
            list_cpu_list.append(data.R2.tolist())
            list_cpu_list.append(data.R3.tolist())
            list_cpu_list.append(data.R4.tolist())
            list_cpu_list.append(data.R5.tolist())
            # replace with list for R6 -> temporary list is R1
            list_cpu_list.append(data.R1.tolist())

            data = list_cpu_list[index-1]
            x_max = len(data)
            time = list(range(x_max))
            time = [ele * 5 for ele in time]
            # print(type(data))
            return render_template("chartjs.html", info=data, labels=time)


        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


@blueprint.route('/<router>/bgtest')
def bgtest(router):
    diff = commitDiff(router)
    return render_template("page-500.html")

@blueprint.route('/deploy')
def deploy():
    diff = commit_all()
    return render_template("page-500.html")
# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  


