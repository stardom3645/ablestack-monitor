#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
from ablestack import *

WALL_GRAFANA_PORT = "19400"
ROOT_CA_CERT_PATH = "/usr/share/ablestack/ablestack-wall/grafana/tls/rootCA.crt"


'''
함수명 : updateNotification
이 함수는 notification.json 파일을 이용하여 새로운 notification channel을 생성합니다.
이 함수가 정상적으로 실행되기 위해서는 /usr/share/ablestack/ablestack-wall/properties/notification.json 파일이 생성되어 있어야합니다.
'''


def updateNotification():
    with open("/usr/share/ablestack/ablestack-wall/properties/api.key") as apikey:
        key = apikey.readline()

    wall_ip = sys.argv[1]
    url = 'https://admin:admin@' + wall_ip + \
        ':' + WALL_GRAFANA_PORT + '/api/alert-notifications'

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer' + key}

    with open("/usr/share/ablestack/ablestack-wall/properties/notification.json", "r") as notificationJsonFile:
        data = json.load(notificationJsonFile)

    res = requests.post(url, data=json.dumps(data), headers=headers, verify=ROOT_CA_CERT_PATH)
    # print(str(res.status_code) + "|" + res.text)

    ret = createReturn(code=res.status_code, val=res.text)
    print(json.dumps(json.loads(ret), indent=4))

    return ret


def main():
    if len(sys.argv) == 2:
        try:
            updateNotification()
        except Exception as e:
            print('Update failed', e)

    else:
        print("One parameter(wallvm_ip) is required.")
        sys.exit()


if __name__ == "__main__":
    main()
