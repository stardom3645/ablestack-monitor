#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import sys

'''
함수명 : testNotification
이 함수는 wallvm의 ip를 입력 받아 notification.json 파일을 참조하여
notification channel을 통한 알람 메시지 송신 여부를 체크합니다.
'''


def testNotification():
    with open("../properties/api.key") as apikey:
        key = apikey.readline()

    wall_ip = sys.argv[1]
    url = 'http://admin:admin@' + wall_ip + \
        ':3000/api/alert-notifications/test'

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer' + key}
    with open("../properties/notification.json", "r") as notificationJsonFile:
        data = json.load(notificationJsonFile)

    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(str(res.status_code) + "|" + res.text)


def main():
    if len(sys.argv) == 2:
        try:
            testNotification()
        except Exception as e:
            print('Update failed', e)

    else:
        print(len(sys.argv))
        print("One parameter(wallvm_ip) is required.")
        sys.exit()


if __name__ == "__main__":
    main()
