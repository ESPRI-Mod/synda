#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 2.8=>2.9 upgrade procedure."""

import os
import re
import sys
import sqlite3 # this is to create a second database connection 
import argparse
import sdapp
import sdlog
from sdprogress import SDProgressDotAuto
import sdconfig
from sdexception import SDException
import sdtools
import sdparam

# this is just to create tables & indexes
import sddb
sddb.disconnect()

templates={
    'CMIP5'   :{ 
                    9:'cmip5.%(product)s.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s'
               },
    'GeoMIP'  :{ 
                    8:'GeoMIP.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s',
                    9:'GeoMIP.%(product)s.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s'
               },
    'obs4MIPs':{ 
                    4:'%(project)s.%(institute)s.%(source_id)s.%(time_frequency)s',
                    5:'%(project)s.%(institute)s.%(source_id)s.%(realm)s.%(time_frequency)s'
               },
    'EUCLIPSE':{ 
                    5:'euclipse.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s',
                    8:'euclipse.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s'
               },
    'PMIP3'   :{
                    9:'pmip3.%(product)s.%(institute)s.%(model)s.%(experiment)s.%(time_frequency)s.%(realm)s.%(cmor_table)s.%(ensemble)s'
               },
    'CORDEX'  :{
                    10:'cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(model)s.%(time_frequency)s.%(variable)s',
                    11:'cordex.%(product)s.%(domain)s.%(institute)s.%(driving_model)s.%(experiment)s.%(ensemble)s.%(model)s.%(rcm_version)s.%(time_frequency)s.%(variable)s'
               }
}

def run(dbfile_28):
    transfer_metadata(dbfile_28)

def extract_filename(local_image):
    m=re.search("/([^/]*)$",local_image)
    if m!=None:
        filename=m.group(1)
    else:
        raise SDException('SD28TO29-001','Incorrect value (local_image=%s)'%local_image)
    return filename

def projectid2project(conn,project_id):

    if project_cache_28 is None:
        c=conn.cursor()
        c.execute('select id,name from project where id in (select distinct project_id from dataset)')
        rs=c.fetchone()
        while rs!=None:
            id_=rs['id']
            name=rs['name']

            project_cache_28[id_]=name

            rs=c.fetchone()

        c.close()

    if project_id in project_cache_28:
        project=project_cache_28[project_id]
    else:
        raise SDException('SD28TO29-002','Incorrect value (project_id=%i)'%project_id)

    return project

def extract_dataset_path(local_image,project,product):
    # returns dataset path (version included)

    m=re.search("(.*)/([^/]*)$",local_image)
    if m!=None:
        dataset_path=m.group(1)
    else:
        raise SDException('SD28TO29-003','Incorrect value (local_image=%s)'%local_image)

    if project in ('CMIP5','GeoMIP'):

        # IPSLONLY: only fit non-merged product (i.e. output{1,2} kept separated)
        # (for merged product, force product to 'output' in line below)

        if product is None:
            sdlog.info("SD28TO29-018","Product is None (dataset_path=%s)"%dataset_path)

            # BEWARE
            # this case if for the 24 GeoMIP without product (select local_image from transfert where product_xml_tag is NULL and project_id=2;)

            dataset_path="{0}/{1}".format(project,dataset_path)
        else:
            dataset_path="{0}/{1}/{2}".format(project,product,dataset_path)

    elif project in ('CORDEX'):
        if 'output/' not in dataset_path:
            # for some dataset, product is missing for this project, so we add it (it's always 'output' for this project)

            # remove project (so we can add product in-between in the next step)
            dataset_path=re.sub('^[^/]+/','',dataset_path)

            # add output and re-add project
            dataset_path="{0}/{1}/{2}".format(project,'output',dataset_path)
        else:
            # if product is present, nothing to do

            pass
    else:
        # all other project have complete path in local_image

        pass

    return dataset_path

def extract_datanode(url):
    m=re.search("^http://([^/]*)/",url)
    if m!=None:
        data_node=m.group(1)
    else:
        raise SDException('SD28TO29-004','Incorrect value (url=%s)'%url)
    return data_node

def get_template(project,fields_number):
    # IPSLONLY

    # WARNING: this code may contain some bugs, as I considere that for the same project and the same fields count, exists only one DRS. This may not be true.

    try:
        template=templates[project][fields_number]
    except:
        raise

    return template

def rebuild_template(dataset_functional_id,project,old_dataset_id):

    # count how many fields in the id
    count=dataset_functional_id.count(".")+1 # compute number of fields(field delimiter occurence number + 1)
    count-=1                                 # last field doesn't count (i.e. dataset version is not part of DRS)

    try:
        template=get_template(project,count)
    except:
        sdlog.info("SD28TO29-012","Un-referenced template (dataset_functional_id=%s,project=%s,fields_number=%i,old_dataset_id=%i)"%(dataset_functional_id,project,count,old_dataset_id))
        raise

    return template

def get_dataset_distinct_products(conn,dataset_id):
    c=conn.cursor()
    c.execute('select distinct product_xml_tag from transfert where dataset_id = ?',(dataset_id,))
    li=[]
    rs=c.fetchone()
    while rs!=None:
        li.append(rs['product_xml_tag'])
        rs=c.fetchone()
    c.close()
    return li

def fix_B0034(conn):
    """
    Replace path style model name with non-normalized model name.

    Note
        - There are 3 differents model name styles: normalized, non-normalized and path
            - non-normalized is the one used in the search-API model facet.
            - path is the one used in the dataset path
            - normalized, which is very similar to path style.
        - Both normalized and non-normalized are supported in Synchro-data selection file.
        - Path style and can't normalized style can't be used in search-API
    """
    c=conn.cursor()

    c.execute("update file set model='BCC-CSM1.1' where model='bcc-csm1-1'")
    c.execute("update dataset set model='BCC-CSM1.1' where model='bcc-csm1-1'")

    c.execute("update file set model='BCC-CSM1.1(m)' where model='bcc-csm1-1-m'")
    c.execute("update dataset set model='BCC-CSM1.1(m)' where model='bcc-csm1-1-m'")

    c.execute("update dataset set model='INM-CM4' where model='inmcm4'")
    c.execute("update file set model='INM-CM4' where model='inmcm4'")

    c.execute("update file set model='GFDL-CM2.1' where model='GFDL-CM2p1'")
    c.execute("update dateset set model='GFDL-CM2.1' where model='GFDL-CM2p1'")

    c.close()

def switch_model_naming_to_non_normalized(conn):
    for normalized_mode_name,non_normalized_mode_name in sdparam.models.iteritems():
        if normalized_mode_name!=non_normalized_mode_name:

            c=conn.cursor()
            c.execute("update dataset set model=? where model=?",(non_normalized_mode_name,normalized_mode_name))
            sdlog.info("SD28TO29-110","%i model switched from normalized to non-normalized (normalized_mode_name=%s,non_normalized_mode_name=%s)"%(c.rowcount,non_normalized_mode_name,normalized_mode_name))
            c.close()

            c=conn.cursor()
            c.execute("update file set model=? where model=?",(non_normalized_mode_name,normalized_mode_name))
            sdlog.info("SD28TO29-120","%i model switched from normalized to non-normalized (normalized_mode_name=%s,non_normalized_mode_name=%s)"%(c.rowcount,non_normalized_mode_name,normalized_mode_name))
            c.close()

def fix_project_name(path):
    if 'CMIP5' in path:
        return path.replace('CMIP5','cmip5')
    elif 'PMIP3' in path:
        return path.replace('PMIP3','pmip3')
    elif 'EUCLIPSE' in path:
        return path.replace('EUCLIPSE','euclipse')
    elif 'CORDEX' in path:
        return path.replace('CORDEX','cordex')
    else:
        return path

def build_path(name,product,project):
    if project in ('CMIP5','GeoMIP'):
        
        if product is None:
            sdlog.info("SD28TO29-011","Product is None (name=%s)"%name)

            # BEWARE
            # this case if for the 24 GeoMIP without product (select local_image from transfert where product_xml_tag is NULL and project_id=2;)

            path="{0}/{1}".format(project,name)
        else:
            path="{0}/{1}/{2}".format(project,product,name)
    elif project in ('CORDEX'):

        if 'output/' in name:
            # add project
            path="{0}/{1}".format(project,name)

        else:
            # for some datasets of CORDEX project, project and product are missing, so we add it (it's always 'output' for this project)

            # add output and project
            path="{0}/{1}/{2}".format(project,'output',name)
    else:
        # project is missing

        path="{0}/{1}".format(project,name)

    path=fix_project_name(path) # project name in 28 have been transformed in many columns (in 29, only local_path should have transformed fields)

    return path

def build_file_functional_id(dataset_path,filename,project):
    dataset_path=fix_project_name(dataset_path) # project name in 28 have been transformed in many columns (in 29, only local_path should have transformed fields)

    # In 28, for some project, varname have been added at the end of the dataset path.
    # Let's remove it.
    if project in ('CMIP5','GeoMIP'):
        dataset_path=re.sub('/[^/]+$','',dataset_path)

    file_functional_id="{0}.{1}".format(dataset_path.replace("/","."),filename)
    return file_functional_id

def populate_datasets_local_path(conn):

    # retrieve dataset list
    li=[]
    c=conn.cursor()
    c.execute("select dataset_id from dataset")
    rs=c.fetchone()
    while rs!=None:
        li.append(rs['dataset_id'])

        rs=c.fetchone()
    c.close()

    # retrieve file local path and transform it into dataset local path
    SDProgressDotAuto.reset(500)
    datasets=[]
    for dataset_id in li:
        c=conn.cursor()
        c.execute("select local_path,project from file where dataset_id=? limit 1",(dataset_id,))
        rs=c.fetchone()
        if rs is not None:
            file_local_path=rs['local_path']
            project=rs['project']
        else:
            raise SDException("SD28TO29-016","Empty dataset (dataset_id=%i)"%dataset_id)

        c.close()

        dataset_local_path=file_local_path_2_dataset_local_path(file_local_path,project)

        t=(dataset_local_path,dataset_id)
        datasets.append(t)

        SDProgressDotAuto.print_char('x')

    # final update
    SDProgressDotAuto.reset(500)
    for d in datasets:
        conn.execute("update dataset set local_path=? where dataset_id=?",d)
        SDProgressDotAuto.print_char('y')

def file_local_path_2_dataset_local_path(file_local_path,project):
    if project in ('CMIP5','GeoMIP'):
        m=re.search("(.+)/[^/]+/[^/]+$",file_local_path) # remove variable_folder+filename 
        dataset_local_path=m.group(1)
    else:
        m=re.search("(.+)/[^/]+$",file_local_path) # remove filename 
        dataset_local_path=m.group(1)

    return dataset_local_path

def transfer_metadata(dbfile_28):
    """This func migrate Synchro-data 2.8 metadata into Synchro-data 2.9."""

    conn_28=sqlite3.connect(dbfile_28)
    conn_28.row_factory=sqlite3.Row # this is for "by name" colums indexing

    conn_29=sqlite3.connect(sdconfig.db_file)
    conn_29.row_factory=sqlite3.Row # this is for "by name" colums indexing


    # dataset table
    SDProgressDotAuto.reset(75)
    dataset_id_mapping={}
    c1=conn_28.cursor()
    c1.execute('select * from dataset')
    rs=c1.fetchone()
    while rs!=None:
        project=projectid2project(conn_28,rs['project_id'])
        old_dataset_id=rs['dataset_id']

        """BEWARE: This code transforms 'mono product' datasets into many datasets with different product.
        I.e. in 28, there is only one dataset for output, output1 and output2.
        In 29, when create a dataset for each product.
        """

        products=get_dataset_distinct_products(conn_28,old_dataset_id) # this is because dataset with different product are merged in dataset table in 28 !!!

        if len(products)>1:
            sdlog.info("SD28TO29-009","Exploded dataset (old_dataset_id=%i,products_count=%i)"%(old_dataset_id,len(products)))

        for product in products:
            path=build_path(rs['name'],product,project) # WARNING: in Synchro-data 2.8, name and name_without_version doesn't contain project field (nor the product for CMIP5 and GeoMIP !!!)
            path_without_version=re.sub('/[^/]+$','',path)
            dataset_functional_id=path.replace('/','.')
            template=rebuild_template(dataset_functional_id,project,old_dataset_id)
            model=rs['model'] if rs['model']!='n/a' else None

            c2=conn_29.cursor()
            c2.execute(     """insert into dataset 
                                   (dataset_functional_id, status, crea_date, path, 
                                    path_without_version, version, last_mod_date, latest, latest_date, 
                                    last_done_transfer_date, model, project, template)
                               values (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                   (dataset_functional_id, rs['status'], rs['crea_date'], path, 
                                    path_without_version, rs['version'], rs['last_mod_date'], rs['latest'], rs['latest_date'], 
                                    rs['last_done_transfer_date'], model, project, template))
            new_dataset_id=c2.lastrowid
            c2.close()

            # old/new dataset mapping
            if old_dataset_id not in dataset_id_mapping:
                dataset_id_mapping[old_dataset_id]=[]
            dataset_id_mapping[old_dataset_id].append((new_dataset_id,product))
        
        SDProgressDotAuto.print_char('d')

        rs=c1.fetchone()
    conn_29.commit()
    c1.close()


    # transfer table
    files=[]
    SDProgressDotAuto.reset(3000)
    c=conn_28.cursor()
    c.execute('select * from transfert')
    rs=c.fetchone()
    while rs!=None:
        project=projectid2project(conn_28,rs['project_id'])
        product=rs['product_xml_tag']
        filename=extract_filename(rs['local_image'])
        dataset_path=extract_dataset_path(rs['local_image'],project,product)
        file_functional_id=build_file_functional_id(dataset_path,filename,project)
        local_path="{0}/{1}".format(dataset_path,filename)
        model=rs['model'] if rs['model']!='n/a' else None

        # IPSLONLY
        if project=="CORDEX":
            local_path=local_path.replace("/output/","/")

        url=rs['location']
        data_node=extract_datanode(url) # not sure if reliable but other no choice
        
        c2=conn_29.cursor()
        try:
            c2.execute("""insert into file 
                                   (url, file_functional_id, filename, local_path, data_node, 
                                    checksum, checksum_type, duration, size, rate, 
                                    start_date, end_date, crea_date, status, error_msg, sdget_status, 
                                    sdget_error_msg, priority, tracking_id, model, project, variable, 
                                    last_access_date, dataset_id, insertion_group_id, file_id)
                               values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                   (url,file_functional_id,filename,local_path,
                                    data_node,rs['checksum'],rs['checksum_type'],
                                    rs['duration'],rs['size_xml_tag'],rs['rate'], rs['start_date'],rs['end_date'],
                                    rs['crea_date'],rs['status'],rs['error_msg'],None,None,
                                    rs['priority'],rs['tracking_id'],model,project, rs['variable'], 
                                    rs['last_access_date'], rs['dataset_id'], 1,rs['transfert_id']))
        except:
            sdtools.print_stderr("tracking_id=%s"%rs['tracking_id'])
            raise

        file_id=c2.lastrowid
        c2.close()
        files.append((file_id,rs['dataset_id'],product)) # store some info for downstream steps

        SDProgressDotAuto.print_char('f')

        rs=c.fetchone()
    c.close()
    conn_29.commit()


    # update dataset_id in 'transfer' table
    SDProgressDotAuto.reset(3000)
    for f in files:
        file_id=f[0]
        old_dataset_id=f[1]

        # choose new dataset_id using 'product'
        new_dataset_id=None
        for dataset_id,dataset_product in dataset_id_mapping[old_dataset_id]:
            if dataset_product==f[2]:
                new_dataset_id=dataset_id
                break
        if new_dataset_id is None:
            raise SDException('SD28TO29-008','Product not found (file_id=%i)'%file_id)

        sdlog.info("SD28TO29-019","New dataset_id set (file_id=%i,old_dataset_id=%i,new_dataset_id=%i)"%(file_id,old_dataset_id,new_dataset_id))
        conn_29.execute('update file set dataset_id=? where file_id=?',(new_dataset_id,file_id))

        SDProgressDotAuto.print_char('u')
    conn_29.commit()

    # update local_path in dataset table
    populate_datasets_local_path(conn_29)
    conn_29.commit()

    # migrate daily_export table
    SDProgressDotAuto.reset(100)
    c=conn_28.cursor()
    c.execute('select * from daily_export')
    rs=c.fetchone()
    while rs!=None:
        old_dataset_id=rs['dataset_id']
        for new_dataset_id,product in dataset_id_mapping[old_dataset_id]:
            conn_29.execute('insert into export (dataset_id,export_date) values (?,?)',(new_dataset_id,rs['export_date']))
        rs=c.fetchone()
        SDProgressDotAuto.print_char('e')
    conn_29.commit()
    c.close()






    # project table
    # => obsolete

    # model table
    # => obsolete

    # version table
    # => from scratch

    # selection__transfer table
    # => from scratch

    # selection table
    # => from scratch

    # transfer_without_selection table
    # => from scratch

    # transfer_without_dataset table
    # => from scratch

    # param table
    # => from scratch

    # non_matching_us_deleted_transfers table
    # => from scratch

    fix_B0034(conn_29)
    conn_29.commit()

    switch_model_naming_to_non_normalized(conn_29)
    conn_29.commit()

    conn_28.close()
    conn_29.close()

# module init.

project_cache_28=None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dbfile',required=True,help='2.8 database file')
    args = parser.parse_args()

    run(args.dbfile)
