from transitions.extensions import GraphMachine
from pymongo import MongoClient, errors
from bson import ObjectId

import json
import pprint
import sys
import telegram

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
        return text == '中文'

    def is_going_to_state2(self, update, bot):
        text = update.message.text
        text = text.replace("台", "臺")
        if text.find("連江縣") != -1:
            text = text.replace("連江縣", "連江縣(馬祖)")
        elif text.find("馬祖") != -1:
            text = text.replace("馬祖", "連江縣(馬祖)")
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

    def is_going_to_state8(self, update, bot):
        text = update.message.text
        return text == 'English'

    def is_going_to_state9(self, update, bot):
        text = update.message.text
        if text.find("Lienchiang County") != -1:
            text = text.replace("Lienchiang County", "Lienchiang County (Matzu)")
        elif text.find("Matzu") != -1:
            text = text.replace("Matzu", "Lienchiang County (Matzu)")

        found = 0
        for post in collect.find():
            if post['city'] == text:
                found = 1
                storecity(text)
                break
        
        if found == 0:
            update.message.reply_text("Cannot find this city\nPlease submit again")
        return found

    def is_going_to_state10(self, update, bot):
        text = update.message.text
        found = 0
        for post in collect.find():
            if post['name'] == text:
                found = 1
                storeloc(text)
                break
        
        if found == 0:
            update.message.reply_text("Cannot find this scenic attraction\nPlease submit again")
        return found
    
    def is_going_to_state11(self, update, bot):
        text = update.message.text
        text = text.lower()
        return text == 'yes'

    def is_going_to_state12(self, update, bot):
        text = update.message.text
        text = text.lower()
        return text == 'drive'

    def is_going_to_state13(self, update, bot):
        text = update.message.text
        text = text.lower()
        return text == 'public transportation'

    def is_going_to_state14(self, update, bot):
        text = update.message.text
        return text == 'Not interested anymore'

    def not_interested(selt, update, bot):
        text = update.message.text
        return text == '沒有'

    def not_interested_eng(selt, update, bot):
        text = update.message.text
        return text == 'No'
    
    def about_me(selt, update, bot):
        found = 0
        text = update.message.text
        if text.lower() == 'about me':
            found = 1
        elif text == '關於我':
            found = 1
        return found

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

    def on_exit_state8(self, update, bot):
        print('Leaving state8')
    
    def on_exit_state9(self, update, bot):
        print('Leaving state9')

    def on_exit_state10(self, update, bot):
        print('Leaving state10')

    def on_exit_state11(self, update, bot):
        print('Leaving state11')

    def on_exit_state12(self, update, bot):
        print('Leaving state12')

    def on_exit_state13(self, update, bot):
        print('Leaving state13')
    
    def on_exit_state14(self, update, bot):
        print('Leaving state14')
    
    def on_exit_state15(self, update, bot):
        print('Leaving state15')

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
        self.go_back(update, bot)

    def on_enter_state6(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['trans'] + '\n'
        update.message.reply_text("以下是搭乘大眾運輸工具去該景點的方法：")
        update.message.reply_text(out)
        update.message.reply_text("祝你玩得開心～")
        self.go_back(update, bot)
    
    def on_enter_state7(self, update, bot):
        update.message.reply_text("好吧 TT\n有需要再跟我說")
        self.go_back(update, bot)

    def on_enter_state8(self, update, bot):
        chat_id = update.message.chat_id
        bot.send_photo(chat_id, photo='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Taiwan_ROC_political_divisions_labeled.svg/850px-Taiwan_ROC_political_divisions_labeled.svg.png')
        update.message.reply_text("Which city / county do you want to go to?")

    def on_enter_state9(self, update, bot):
        cityname = getcity()
        print(cityname)
        out = ""
        for post in collect.find({'city': cityname}):
            out = out + post['name'] + '\n'
        print(out)
        update.message.reply_text("These are the scenic attraction in that city / county:")
        update.message.reply_text(out)
        update.message.reply_text("Which scenic attraction would you like to further understand?")

    
    def on_enter_state10(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['info'] + '\n'
        update.message.reply_text("This is the introduction of that scenic attraction: ")
        update.message.reply_text(out)
        update.message.reply_text("Are you interested in going there?")

    def on_enter_state11(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = 'Name: ' + post['name'] + '\n'
            out = out + 'Telephone number: ' + post['phone'] + '\n'
            out = out + 'Address: ' + post['address'] + '\n'
            out = out + 'Longitude/Latitude：： ' + post['geo'] + '\n'
            out = out + 'Official Website ' + post['web'] + '\n'
        update.message.reply_text("This is the information of that scenic attraction: ")
        update.message.reply_text(out)
        update.message.reply_text("How would you like to get there?\n(Drive / Public transportation / Not interested anymore)")

    def on_enter_state12(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['drive'] + '\n'
        update.message.reply_text("This is how you get there by driving:")
        update.message.reply_text(out)
        update.message.reply_text("Have fun～")
        self.go_back(update, bot)

    def on_enter_state13(self, update, bot):
        locname = getloc()
        print(locname)
        out = ""
        for post in collect.find({'name': locname}):
            out = post['trans'] + '\n'
        update.message.reply_text("This is how you get there by public transportation:")
        update.message.reply_text(out)
        update.message.reply_text("Have fun～")
        self.go_back(update, bot)
    
    def on_enter_state14(self, update, bot):
        update.message.reply_text("Alright TT\nTell me again if you still need me")
        self.go_back(update, bot)
    
    def on_enter_state15(self, update, bot):
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, 
                        text="Hi! I'm TravelTaiwan. I am a telegram bot based on a finite state machine.\nI can help you with planning your trips in Taiwan by giving you a list of places to visit, as well as the information of that scenic attraction provided by [Tourism Bureau, Republic of China (Taiwan).](http://eng.taiwan.net.tw/)\nI am created by [Kathy](https://github.com/katherine0504).\nYou can find out more about me [here](https://github.com/katherine0504/ChatBot).", 
                        parse_mode=telegram.ParseMode.MARKDOWN)
        self.go_back(update, bot)
