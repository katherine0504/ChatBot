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

city = None
loc = None

def storecity(cityname):
    global city
    city = cityname
    print(city)

def storeloc(locname):
    global loc
    loc = locname
    print(loc)

def getcity():
    global city
    return city

def getloc():
    global loc
    return loc

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

    def is_going_to_state1(self, update, bot):
        text = update.message.text
        return text == '想旅行'

    def is_going_to_state2(self, update, bot):
        text = update.message.text
        text = text.replace("台", "臺")
        found = 0
        for post in collect.find():
            if post['city'] == text:
                found = 1
                storecity(text)
                break
        
        if found == 0:
            update.message.reply_text("找不到這個縣市唷\n請你再輸入一次")
        return found

    def is_going_to_state3(self, update, bot):
        text = update.message.text
        found = 0
        for post in collect.find():
            if post['name'] == text:
                found = 1
                storeloc(text)
                break
        
        if found == 0:
            update.message.reply_text("找不到這個景點唷\n請你再輸入一次")
        return found
    
    def is_going_to_state4(self, update, bot):
        text = update.message.text
        return text == '有'

    def is_going_to_state5(self, update, bot):
        text = update.message.text
        return text == '開車'

    def is_going_to_state6(self, update, bot):
        text = update.message.text
        return text == '大眾運輸'

    def is_going_to_state7(self, update, bot):
        text = update.message.text
        return text == '不想去了'

    def not_interested(selt, update, bot):
        text = update.message.text
        return text == '沒有'

    def on_exit_state1(self, update, bot):
        print('Leaving state1')
    
    def on_exit_state2(self, update, bot):
        print('Leaving state2')

    def on_exit_state3(self, update, bot):
        print('Leaving state3')

    def on_exit_state4(self, update, bot):
        print('Leaving state4')

    def on_exit_state5(self, update, bot):
        print('Leaving state5')

    def on_exit_state6(self, update, bot):
        print('Leaving state6')
    
    def on_exit_state7(self, update, bot):
        print('Leaving state7')    

    def on_enter_state1(self, update, bot):
        chat_id = update.message.chat_id
        bot.send_photo(chat_id, photo='http://www.shining.org.tw/uploads/taiwan-map-wt-2013.gif')
        update.message.reply_text("想去哪個縣市呢？")

    def on_enter_state2(self, update, bot):
        cityname = getcity()
        print(cityname)
        out = ""
        for post in collect.find({'city': cityname}):
            out = out + post['name'] + '\n'
        print(out)
        update.message.reply_text("以下是該縣市的景點：")
        update.message.reply_text(out)
        update.message.reply_text("你想更深入知道哪個景點呢？")

    
    def on_enter_state3(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['info'] + '\n'
        update.message.reply_text("以下是該景點的介紹：")
        update.message.reply_text(out)
        update.message.reply_text("對這個景點有興趣嗎？")

    def on_enter_state4(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = '景點名稱： ' + post['name'] + '\n'
            out = out + '電話： ' + post['phone'] + '\n'
            out = out + '地址： ' + post['address'] + '\n'
            out = out + '經緯度： ' + post['geo'] + '\n'
            out = out + '官方網站： ' + post['web'] + '\n'
        update.message.reply_text("以下是該景點的詳細資訊：")
        update.message.reply_text(out)
        update.message.reply_text("你想怎麼去？\n(開車 / 大眾運輸 / 不想去了)")

    def on_enter_state5(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['drive'] + '\n'
        update.message.reply_text("以下是開車去該景點的方法：")
        update.message.reply_text(out)
        update.message.reply_text("祝你玩得開心～")
        self.go_back(update)

    def on_enter_state6(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['trans'] + '\n'
        update.message.reply_text("以下是搭乘大眾運輸工具去該景點的方法：")
        update.message.reply_text(out)
        update.message.reply_text("祝你玩得開心～")
        self.go_back(update)
    
    def on_enter_state7(self, update, bot):
        update.message.reply_text("好吧 TT\n有需要再跟我說")
        self.go_back(update)