'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 skydive.yml 파일을 설정하는 프로그램입니다.
최초 작성일 : 2021. 09. 15
'''

# !/usr/bin/python3
# -*- coding: utf-8 -*-

import yaml
import argparse
import json
from ablestack import *

# skydive analyzer 포트
skydive_analyzer_port = ":8082"

'''
함수명 : parseArgs
이 함수는 python library argparse를 시용하여 함수를 실행될 때 필요한 파라미터를 입력받고 파싱하는 역할을 수행합니다.
예를들어 action을 요청하면 해당 action일 때 요구되는 파라미터를 입력받고 해당 코드를 수행합니다.
'''


def parseArgs():
    parser = argparse.ArgumentParser(description='Skydive Yaml file parsing and replace targets',
                                     epilog='copyrightⓒ 2021 All rights reserved by ABLECLOUD™')

    parser.add_argument('action', choices=[
        'config'], help='choose one of the actions')
    parser.add_argument('--ccvm', metavar='name', type=str,
                        nargs='*', help='ccvm ips')

    return parser.parse_args()


def ccvmSkydiveConfig(ccvm_ip):
    ccvm = ccvm_ip.copy()
    for i in range(len(ccvm)):
        ccvm[i] = ccvm[i] + skydive_analyzer_port
    return ccvm

# 함수명 : configYaml
# 주요 기능 : 입력 받은 ip를 skydive.yml 파일의 analyzers에 설정


def configYaml(ccvm):
    skydive_yml_path = '/usr/share/ablestack/ablestack-skydive/skydive/skydive.yml'

    with open(skydive_yml_path) as f:
        skydive_org = yaml.safe_load(f)

        skydive_org['analyzers'][0] = ccvmSkydiveConfig(ccvm)

        with open(skydive_yml_path, 'w') as yaml_file:
            yaml_file.write(
                yaml.dump(skydive_org, default_flow_style=False))


def main():
    args = parseArgs()

    if (args.action) == 'config':
        try:
            configYaml(args.ccvm)
            ret = createReturn(code=200, val="update skydive configuration")
            print(json.dumps(json.loads(ret), indent=4))
        except Exception as e:
            ret = createReturn(code=500, val="fail to update")
            print(json.dumps(json.loads(ret), indent=4))

    return ret


if __name__ == "__main__":
    main()