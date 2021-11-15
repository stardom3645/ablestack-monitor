'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 prometheus.yml, defaults.ini, db 파일 등을 설정하는 프로그램입니다.
최초 작성일 : 2021. 08. 25
'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import yaml
import argparse
import json
from ablestack import *
import configparser
import sqlite3
import pymysql
from sh import cp

# prometheus에서 수집하는 exporter 및 서비스 포트
wall_prometheus_port = ":3001"
libvirt_exporter_port = ":3002"
node_exporter_port = ":3003"
process_exporter_port = ":3004"
blackbox_exporter_port = ":3005"
cube_service_port = ":9090"
mold_service_port = ":8080"
mold_db_port = ":3306"
glue_prometheus_port = ":9095"

'''
함수명 : parseArgs
이 함수는 python library argparse를 시용하여 함수를 실행될 때 필요한 파라미터를 입력받고 파싱하는 역할을 수행합니다.
예를들어 action을 요청하면 해당 action일 때 요구되는 파라미터를 입력받고 해당 코드를 수행합니다.
'''


def parseArgs():
    parser = argparse.ArgumentParser(description='Prometheus Yaml file parsing and replace targets',
                                     epilog='copyrightⓒ 2021 All rights reserved by ABLECLOUD™')

    parser.add_argument('action', choices=[
                        'config'], help='choose one of the actions')
    parser.add_argument('--cube', metavar='name', type=str,
                        nargs='*', help='cube ips')
    parser.add_argument('--scvm', metavar='name', type=str,
                        nargs='*', help='scvm ips')
    parser.add_argument('--ccvm', metavar='name', type=str,
                        nargs='*', help='ccvm ips')

    return parser.parse_args()


def cubeServiceConfig(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + cube_service_port
    return cube


def moldServiceConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + mold_service_port
    return ccvm


def moldDBConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + mold_db_port
    return ccvm


def libvirtConfig(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + libvirt_exporter_port
    return cube


def cubeNodeConfig(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + node_exporter_port
    return cube


def scvmNodeConfig(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i] + node_exporter_port
    return scvm


def ccvmNodeConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + node_exporter_port
    return ccvm


def wallPrometheusConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + wall_prometheus_port
    return ccvm


def gluePrometheusConfig(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i] + glue_prometheus_port
    return scvm


def cubeProcessConfig(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i] + process_exporter_port
    return cube


def scvmProcessConfig(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i] + process_exporter_port
    return scvm


def ccvmProcessConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + process_exporter_port
    return ccvm


def cubeBlackboxConfig(cube_ip):
    cube = cube_ip.copy()
    for i in range(len(cube)):
        cube[i] = cube[i]
    return cube


def scvmBlackboxConfig(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i]
    return scvm

def ccvmBlackboxConfigReplacement(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + blackbox_exporter_port
    return ccvm

def ccvmBlackboxConfigReplacementReplacement(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + blackbox_exporter_port
    return ccvm

# 함수명 : configYaml
# 주요 기능 : 입력 받은 ip를 prometheus.yml 파일의 targets에 설정


def configYaml(cube, scvm, ccvm):
    prometheus_yml_path = '/usr/share/ablestack/ablestack-wall/prometheus/prometheus.yml'

    with open(prometheus_yml_path) as f:
        prometheus_org = yaml.safe_load(f)
    for i in range(len(prometheus_org['scrape_configs'])):

        if prometheus_org['scrape_configs'][i]['job_name'] == 'libvirt':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = libvirtConfig(
                cube)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'cube':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cubeNodeConfig(
                cube)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'scvm':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = scvmNodeConfig(
                scvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'ccvm':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = ccvmNodeConfig(
                ccvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'cube-process-exporter':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cubeProcessConfig(
                cube)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'scvm-process-exporter':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = scvmProcessConfig(
                scvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'ccvm-process-exporter':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = ccvmProcessConfig(
                ccvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'cube-blackbox':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cubeBlackboxConfig(
                cube)
            prometheus_org['scrape_configs'][i]['relabel_configs'][-1]['replacement'] = ccvmBlackboxConfigReplacement(
                ccvm)[0]

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'scvm-blackbox':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = scvmBlackboxConfig(
                scvm)
            prometheus_org['scrape_configs'][i]['relabel_configs'][-1]['replacement'] = ccvmBlackboxConfigReplacement(
                ccvm)[0]

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'ccvm-blackbox':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = ccvmBlackboxConfig(
                ccvm)
            prometheus_org['scrape_configs'][i]['relabel_configs'][-1]['replacement'] = ccvmBlackboxConfigReplacement(
                ccvm)[0]

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'blackbox-tcp':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cubeServiceConfig(cube) + moldServiceConfig(ccvm) + moldDBConfig(ccvm) + libvirtConfig(cube) + cubeNodeConfig(cube) + scvmNodeConfig(scvm) + ccvmNodeConfig(
                ccvm) + cubeProcessConfig(cube) + scvmProcessConfig(scvm) + ccvmProcessConfig(ccvm) + ccvmBlackboxConfigReplacement(ccvm)
            prometheus_org['scrape_configs'][i]['relabel_configs'][-1]['replacement'] = ccvmBlackboxConfigReplacement(
                ccvm)[0]

        with open(prometheus_yml_path, 'w') as yaml_file:
            yaml_file.write(
                yaml.dump(prometheus_org, default_flow_style=False))

# 함수명 : configIni
# 주요 기능 : grafana의 설정 파일에 도메인을 ccvm ip로 설정


def configIni(ccvm):
    ini_file = '/usr/share/ablestack/ablestack-wall/grafana/conf/defaults.ini'
    config = configparser.ConfigParser()

    config.read(ini_file)

    config.set('server', 'domain', ccvm[0])

    with open(ini_file, 'w') as f:
        config.write(f)


def configDS(scvm, ccvm):

    conn = sqlite3.connect(
        "/usr/share/ablestack/ablestack-wall/grafana/data/grafana.db")

    ds_update_query1 = "UPDATE data_source SET url = \'http://" + \
        "localhost:3001' WHERE id = 1"
    ds_update_query2 = "UPDATE data_source SET url = \'http://" + \
        gluePrometheusConfig(scvm)[0] + "' WHERE id = 2"
    ds_update_query3 = "UPDATE data_source SET url = \'" + \
        "localhost:3306' WHERE id = 3"
    ds_update_query4 = "UPDATE data_source SET url = \'http://" + \
        "localhost:3001' WHERE id = 4"

    cur = conn.cursor()
    cur.execute(ds_update_query1)
    cur.execute(ds_update_query2)
    cur.execute(ds_update_query3)
    cur.execute(ds_update_query4)

    conn.commit()
    conn.close()


def configSkydiveLink(ccvm):

    conn = sqlite3.connect(
        "/usr/share/ablestack/ablestack-wall/grafana/data/grafana.db")

    # skydive 링크가 들어가는 대시보드 ip 변경
    link_update_query = "UPDATE dashboard SET data = replace(data, 'http://10.10.1.10:8082', 'http://" + str(ccvm[0]) + ":8082') WHERE org_id = 1 AND folder_id = 0 AND is_folder = 0 AND data like '%http://10.10.1.10:8082%'"

    cur = conn.cursor()
    cur.execute(link_update_query)

    conn.commit()
    conn.close()


def configMoldUserDashboard():

    # grafana.db 에서 사용자 대시보드의 UID 가져오기
    conn = sqlite3.connect(
        "/usr/share/ablestack/ablestack-wall/grafana/data/grafana.db")

    user_dashboard_query = "SELECT uid, slug FROM dashboard WHERE id = 13 AND org_id = 2"

    cur = conn.cursor()
    cur.execute(user_dashboard_query)
    user_dashboard_val = cur.fetchone()

    uri_val = '/d/' + user_dashboard_val[0] + '/' + user_dashboard_val[1]

    conn.close()

    cloud_db = pymysql.connect(
        user='cloud',
        password='Ablecloud1!',
        host='localhost',
        db='cloud',
        charset='utf8'
    )

    cursor = cloud_db.cursor(pymysql.cursors.DictCursor)
    update_user_dashboard_uri_sql = "UPDATE configuration SET value ='" + uri_val + "' WHERE name = 'monitoring.wall.portal.vm.uri'"
    cursor.execute(update_user_dashboard_uri_sql)

    cloud_db.commit()
    cloud_db.close()


# DB 파일 초기화 (기존 초기 파일로 되돌리기)
def initDB():
    cp("-f", "/usr/share/ablestack/ablestack-wall/grafana/data/grafana_org.db",
       "/usr/share/ablestack/ablestack-wall/grafana/data/grafana.db")


def main():
    args = parseArgs()
    initDB()

    if (args.action) == 'config':
        try:
            configYaml(args.cube, args.scvm, args.ccvm)
            configIni(args.ccvm)
            configDS(args.scvm, args.ccvm)
            configSkydiveLink(args.ccvm)
            configMoldUserDashboard()
            ret = createReturn(code=200, val="update wall configuration")
            print(json.dumps(json.loads(ret), indent=4))
        except Exception as e:
            ret = createReturn(code=500, val="fail to update")
            print(json.dumps(json.loads(ret), indent=4))

    return ret


if __name__ == "__main__":
    main()