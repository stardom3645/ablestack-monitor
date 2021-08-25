#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys

'''
함수명 : updateJson
이 함수는 notification channel을 업데이트 하기 전 실행되어야 합니다. ';'으로 구분한 이메일 인자 값을 받아 json 파일을 구성합니다.
실행 예시 : python3 update_noti_channel.py "ablestack@ablecloud.io; ablestack2@ablecloud.io"
'''


def updateJson():

    with open("../properties/notification.json", "r") as notificationJsonFile:
        data = json.load(notificationJsonFile)

    data["settings"]["addresses"] = sys.argv[1]

    with open("../properties/notification.json", "w") as notificationJsonFile:
        json.dump(data, notificationJsonFile)


def main():
    updateJson()


if __name__ == "__main__":
    main()
