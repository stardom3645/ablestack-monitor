#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import sys


def updateNotification():
    with open("../properties/api.key") as apikey:
        key = apikey.readline()

    wall_ip = sys.argv[1]
    url = 'http://admin:admin@' + wall_ip + \
        ':3000/api/alert-notifications'

    headers = {'Accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': 'Bearer' + key}

    with open("../properties/notification.json", "r") as notificationJsonFile:
        data = json.load(notificationJsonFile)

    res = requests.post(url, data=json.dumps(data), headers=headers)
    print(str(res.status_code) + "|" + res.text)


def main():
    if len(sys.argv) == 2:
        try:
            updateNotification()
        except Exception as e:
            print('Update failed', e)

    else:
        print(len(sys.argv))
        print("One parameter(wallvm_ip) is required.")
        sys.exit()


if __name__ == "__main__":
    main()
