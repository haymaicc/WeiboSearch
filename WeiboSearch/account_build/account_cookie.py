#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author : haymai
import os

import pymongo
from pymongo.errors import DuplicateKeyError

"""
保存cookie到db
"""
if __name__ == '__main__':
    file_path = os.getcwd() + '/account.txt'
    with open(file_path, 'r') as f:
        lines = f.readlines()
    mongo_client = pymongo.MongoClient("127.0.0.1", 27017)
    collection = mongo_client["weibosearch"]["account"]
    collection.remove()
    for line in lines:
        cookie_str = line.strip()
        username = line.split('----')[0]
        cookie_str = line.split('----')[1]
        print('=' * 10 + username + '=' * 10)
        print('Cookie:', cookie_str)
        try:
            collection.insert(
                {"_id": username, "password": "", "cookie": cookie_str, "status": "success"})
        except DuplicateKeyError as e:
            collection.find_one_and_update({'_id': username}, {'$set': {'cookie': cookie_str, "status": "success"}})
