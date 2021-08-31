'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 wall 대시보드의 admin api key를 생성하는 프로그램입니다.
최초 작성일 : 2021. 08. 25
'''

#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import json
import sys
from ablestack import *


'''
함수명 : createApiKey
이 함수는 wallvm의 ip와 api key 이름을 입력받아 api key를 생성합니다.
'''


def createApiKey():
    wall_ip = sys.argv[1]
    key_name = sys.argv[2]
    url = 'http://admin:admin@' + wall_ip + \
        ':3000/api/auth/keys'

    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    data = '{"name":' + '"'+key_name+'"' + ', "role": "Admin"}'

    res = requests.post(url, data=data, headers=headers)
    # print(str(res.status_code) + "|" + res.text)
    ret = createReturn(code=res.status_code, val=res.text)
    print(json.dumps(json.loads(ret), indent=4))
    if str(res.status_code) == '200':

        with open("../properties/api.json", "w") as apiJsonFile:
            apiJsonFile.write(res.text)

    with open("../properties/api.json", "r") as apiJsonFile:
        data = json.load(apiJsonFile)
        key = data["key"]
        with open("../properties/api.key", "w") as apiKey:
            apiKey.write(key)
    return ret


def main():
    if len(sys.argv) == 3:
        try:
            createApiKey()

        except Exception as e:
            print('Update failed', e)

    else:
        print("wallvm_ip, apikey_name are required.")
        sys.exit()


if __name__ == "__main__":
    main()
