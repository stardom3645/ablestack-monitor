'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 prometheus.yml 파일의 tartget ip 및 port를 설정하는 프로그램입니다.
최초 작성일 : 2021. 08. 25
'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import yaml
import argparse


# prometheus에서 수집하는 exporter 및 서비스 포트
# prometheus_port = ":3001"
libvirt_exporter_port = ":3002"
node_exporter_port = ":3003"
process_exporter_port = ":3004"
blackbox_exporter_port = ":3005"
cube_service_port = ":9090"
mold_service_port = ":8080"
mold_db_port = ":3306"

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


# def prometheusConfig(ccvm_ip):
#     ccvm = ccvm_ip.copy()
#     for i in range(len(ccvm)):
#         ccvm[i] = ccvm[i] + prometheus_port
#     return ccvm

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
        cube[i] = cube[i] + blackbox_exporter_port
    return cube


def scvmBlackboxConfig(scvm_ip):
    scvm = scvm_ip.copy()
    for i in range(len(scvm)):
        scvm[i] = scvm[i] + blackbox_exporter_port
    return scvm


def ccvmBlackboxConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + blackbox_exporter_port
    return ccvm

# 함수명 : configYaml
# 주요 기능 : 입력 받은 ip를 prometheus.yml 파일의 targets에 설정


def configYaml(cube, scvm, ccvm):
    prometheus_yml_path = '/usr/share/ablestack/ablestack-wall/prometheus/prometheus.yml'
    with open(prometheus_yml_path) as f:
        prometheus_org = yaml.load(f, Loader=yaml.FullLoader)
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

        # elif prometheus_org['scrape_configs'][i]['job_name'] == 'prometheus':
        #     prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = prometheusConfig(
        #         ccvm)

        #     print(prometheus_org['scrape_configs'][4]
        #           ['static_configs'][0]['targets'])

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

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'scvm-blackbox':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = scvmBlackboxConfig(
                scvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'ccvm-blackbox':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = ccvmBlackboxConfig(
                ccvm)

        elif prometheus_org['scrape_configs'][i]['job_name'] == 'blackbox-tcp':
            prometheus_org['scrape_configs'][i]['static_configs'][0]['targets'] = cubeServiceConfig(cube) + moldServiceConfig(ccvm) + moldDBConfig(ccvm) + libvirtConfig(cube) + cubeNodeConfig(cube) + scvmNodeConfig(scvm) + ccvmNodeConfig(
                ccvm) + cubeProcessConfig(cube) + scvmProcessConfig(scvm) + ccvmProcessConfig(ccvm) + cubeBlackboxConfig(cube) + scvmBlackboxConfig(scvm) + ccvmBlackboxConfig(ccvm)

        with open(prometheus_yml_path, 'w') as yaml_file:
            yaml_file.write(
                yaml.dump(prometheus_org, default_flow_style=False))


def main():
    args = parseArgs()

    if (args.action) == 'config':
        configYaml(args.cube, args.scvm, args.ccvm)


if __name__ == "__main__":
    main()
