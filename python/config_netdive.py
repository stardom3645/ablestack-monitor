#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Copyright (c) 2021 ABLECLOUD Co. Ltd
이 파일은 Wall VM을 구성할 때 Netdive 서비스를 기동하는 프로그램입니다.
최초 작성일 : 2021. 09. 15
수정일 : 2026. 03. 16
수정 내용 :
- analyzer 실패를 삼키지 않도록 수정
- analyzer 준비 완료 확인 후 agent 재시작하도록 수정
- sys.stderr.write 제거
'''

import os
import argparse
import json
import time
from subprocess import call
from ablestack import *
from sh import systemctl


env = os.environ.copy()
env['LANG'] = "en_US.utf-8"
env['LANGUAGE'] = "en"

SSH_COMMON_OPTS = "-o BatchMode=yes -o StrictHostKeyChecking=no -o ConnectTimeout=5"

ANALYZER_HEALTH_URL = "https://localhost:19500/api/capture"


def parseArgs():
    parser = argparse.ArgumentParser(
        description='Start netdive analyzer on ccvm and netdive agent on cubes',
        epilog='copyrightⓒ 2021 All rights reserved by ABLECLOUD™'
    )

    parser.add_argument('action', choices=['config'], help='choose one of the actions')
    parser.add_argument('--cube', metavar='name', type=str, nargs='*', help='cube ips')
    parser.add_argument('--ccvm', metavar='name', type=str, nargs='*', help='ccvm ips')

    return parser.parse_args()


def StartAnalyzer():
    """
    ccvm에서 netdive-analyzer를 enable/restart 합니다.
    실패 시 예외를 그대로 올립니다.
    """
    systemctl("enable", "netdive-analyzer")
    systemctl("restart", "netdive-analyzer")


def WaitAnalyzerReady():
    """
    analyzer HTTPS endpoint 준비 완료를 확인합니다.
    """
    tries = 30

    for _ in range(tries):
        rc = call(
            [f"curl -sfk {ANALYZER_HEALTH_URL} > /dev/null 2>&1"],
            universal_newlines=True,
            shell=True,
            env=env
        )

        if rc == 0:
            return 200

        time.sleep(1)

    return 500


def SendCommandToHost(cube):
    """
    입력 받은 cube ip 주소에서 netdive-agent.service를 재시작합니다.
    3회 재시도 후에도 실패하면 500을 반환합니다.
    """
    tries = 3

    for _ in range(tries):
        result_code_list = []

        for i in range(len(cube)):
            stringCube = cube[i]

            ssh_cmd = (
                    "ssh " + SSH_COMMON_OPTS + " root@" + stringCube +
                    " 'systemctl reset-failed netdive-agent.service || true; "
                    "systemctl restart netdive-agent.service'"
            )

            rc = call(
                [ssh_cmd],
                universal_newlines=True,
                shell=True,
                env=env
            )

            result_code_list.append(rc)

        if all(x == 0 for x in result_code_list):
            return 200

    return 500


def main():
    args = parseArgs()
    ret = createReturn(code=500, val="fail to update netdive configuration")

    if args.action == 'config':
        try:
            StartAnalyzer()

            analyzer_ready = WaitAnalyzerReady()
            if analyzer_ready != 200:
                ret = createReturn(code=500, val="fail to start netdive analyzer")
                print(json.dumps(json.loads(ret), indent=4))
                return ret

            result = SendCommandToHost(args.cube)

            if result == 200:
                ret = createReturn(code=200, val="update netdive configuration")
            else:
                ret = createReturn(code=500, val="fail to update netdive configuration")

        except Exception as e:
            ret = createReturn(code=500, val="fail to update netdive configuration : " + str(e))

        print(json.dumps(json.loads(ret), indent=4))
        return ret


if __name__ == "__main__":
    main()