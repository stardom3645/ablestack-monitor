'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 grafana.ini 파일의 smtp를 설정하는 프로그램입니다.
최초 작성일 : 2021. 08. 26
'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import configparser
import argparse
import json
from ablestack import *
from sh import systemctl
import pymysql

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


def configWallSmtp(host, user, password):
    ini_file = '/usr/share/ablestack/ablestack-wall/grafana/conf/defaults.ini'
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

    systemctl('restart', 'grafana-server')


def configMoldSmtp(host, user, password):
    cloud_db = pymysql.connect(
        user='cloud',
        password='Ablecloud1!',
        host='localhost',
        db='cloud',
        charset='utf8'
    )
    smtp_server = host.split(':')[0]
    smtp_port = host.split(':')[1]

    cursor = cloud_db.cursor(pymysql.cursors.DictCursor)
    update_email_sender_sql = "UPDATE configuration SET value ='" + user + "' WHERE name = 'alert.email.sender'"
    cursor.execute(update_email_sender_sql)
    update_smtp_host_sql = "UPDATE configuration SET value ='" + smtp_server + "' WHERE name = 'alert.smtp.host'"
    cursor.execute(update_smtp_host_sql)
    update_smtp_port_sql = "UPDATE configuration SET value ='" + smtp_port + "' WHERE name = 'alert.smtp.port'"
    cursor.execute(update_smtp_port_sql)

    with open("/usr/share/ablestack/ablestack-wall/properties/notification.json", "r") as notificationJsonFile:
        data = json.load(notificationJsonFile)
        # print(str(data['settings']['addresses']).replace(";",","))
        smtp_addresses = str(data['settings']['addresses']).replace(";", ",")
        update_email_addresses_sql = "UPDATE configuration SET value ='" + \
            smtp_addresses + "' WHERE name = 'alert.email.addresses'"
        cursor.execute(update_email_addresses_sql)

    # result = cursor.fetchall()
    # print(result)
    cloud_db.commit()
    cloud_db.close()

    systemctl('restart', 'cloudstack-management')


def main():
    args = parseArgs()

    if (args.action) == 'config':
        configWallSmtp(args.host, args.user, args.password)
        configMoldSmtp(args.host, args.user, args.password)

        ret = createReturn(code=200, val="update smtp")
        print(json.dumps(json.loads(ret), indent=4))

    return ret


if __name__ == "__main__":
    main()
