#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
import sys


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
