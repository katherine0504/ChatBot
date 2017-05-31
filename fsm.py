from transitions.extensions import GraphMachine
from pymongo import MongoClient, errors
from bson import ObjectId

import json
import pprint
import sys

uri = "mongodb://kathy:kathy@ds141960.mlab.com:41960/kathytest"
client = MongoClient(uri)
db = client['kathytest']
collect = db['travel']

city = "blank"

def storecity(cityname):
    city = cityname

def getcity(cityname):
    return city

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state1(self, update):
        text = update.message.text
        return text == '想旅行'

    def is_going_to_state2(self, update):
        text = update.message.text
        found = 0
        for post in collect.find():
            print(post['city'])
            if post['city'] == text:
                found = 1
                break
        
        if found == 0:
            update.message.reply_text("找不到這個縣市唷")
        return found == 1

    def on_enter_state1(self, update):
        update.message.reply_text("想去哪個縣市呢？")
        self.go_back(update)

    def on_exit_state1(self, update):
        print('Leaving state1')

    def on_enter_state2(self, update):
        update.message.reply_text("以下是該縣市的景點：")
        update.message.reply_text("你想更深入知道哪些景點呢？")
        self.go_back(update)

    def on_exit_state2(self, update):
        print('Leaving state2')
    