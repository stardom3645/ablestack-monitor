'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 grafana.ini 파일의 smtp를 설정하는 프로그램입니다.
최초 작성일 : 2021. 08. 26
'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import argparse

'''
함수명: parseArgs
이 함수는 python library argparse를 시용하여 함수를 실행될 때 필요한 파라미터를 입력받고 파싱하는 역할을 수행합니다.
예를들어 action을 요청하면 해당 action일 때 요구되는 파라미터를 입력받고 해당 코드를 수행합니다.
'''


def parseArgs():
    parser = argparse.ArgumentParser(description='Prometheus Yaml file parsing and replace targets',
                                     epilog='copyrightⓒ 2021 All rights reserved by ABLECLOUD™')

    parser.add_argument('action', choices=[
                        'config'], help='choose one of the actions')
    parser.add_argument('--host', metavar='name', type=str,
                        help='host_ip:port')
    parser.add_argument('--user', metavar='name', type=str,
                        help='admin email address')
    parser.add_argument('--password', metavar='name', type=str,
                        help='admin email password')

    return parser.parse_args()


def configSmtp(host, user, password):
    ini_file = '/usr/share/ablestack/ablestack-wall/grafana/conf'
    config = configparser.ConfigParser()

    config.read(ini_file)
    smtp_enabled = config['smtp']['enabled']

    config.set('smtp', 'enabled', 'true')
    config.set('smtp', 'host', host)
    config.set('smtp', 'user', user)
    config.set('smtp', 'password', '"""' + password + '"""')
    config.set('smtp', 'from_address', user)

    with open(ini_file, 'w') as f:
        config.write(f)


def main():
    args = parseArgs()

    if (args.action) == 'config':
        configSmtp(args.host, args.user, args.password)


if __name__ == "__main__":
    main()
