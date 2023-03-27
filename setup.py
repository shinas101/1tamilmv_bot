from asyncio import events
import telebot
from telebot import types
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
import requests
import re
from bs4 import BeautifulSoup
import asyncio

TOKEN = 'YOUR_BOT_TOKEN_HERE'

bot = telebot.TeleBot(TOKEN)

button1 = telebot.types.InlineKeyboardButton(text="⚡Powered by ",url='https://t.me/heyboy2004')
button2 = telebot.types.InlineKeyboardButton(text="🔗 Gdrive channel ",url='https://t.me/GdtotLinkz')
button3 = telebot.types.InlineKeyboardButton(text="📜 Status channel ",url='https://t.me/TmvStatus')
keyboard = telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('👨‍💻 Developed by', url='github.com/shinas101')).add(button1).add(button2).add(button3)
keyboard2 = telebot.types.InlineKeyboardMarkup().add(button2).add(button3)

@bot.message_handler(commands=['start'])
def random_answer(message):
    bot.send_message(chat_id=message.chat.id,text=f"Hello👋 \n\n🗳Get latest Movies from 1Tamilmv\n\n⚙️*How to use me??*🤔\n\n✯ Please Enter */view* command and you'll get magnet link as well as link to torrent file 😌\n\nShare and Support💝",parse_mode='Markdown',reply_markup=keyboard)

@bot.message_handler(commands=['view'])
def start(message):
  bot.send_message(message.chat.id,text="*Please wait for 10 seconds*",parse_mode='Markdown')
  tamilmv()
  bot.send_message(chat_id=message.chat.id,
                text="Select a Movie from the list 🙂 : ",
                reply_markup=makeKeyboard(),
                parse_mode='HTML')

@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    bot.send_message(call.message.chat.id,text=f"Here's your Movie links 🎥 ",parse_mode='markdown')
    for key , value in enumerate(movie_list):
        if call.data == f"{key}":
            print("HI")
            if movie_list[int(call.data)] in real_dict.keys():
                for i in real_dict[movie_list[int(call.data)]]:                  
                  bot.send_message(call.message.chat.id,text=f"{i}\n\n🤖 @Tamilmv\_movie\_bot",parse_mode='markdown')
                  print(real_dict[movie_list[int(call.data)]])
    bot.send_message(call.message.chat.id,text=f"🌐 Please Join Our Status Channel",parse_mode='markdown',reply_markup=keyboard2)
      
def makeKeyboard():
    markup = types.InlineKeyboardMarkup()

    for key,value in enumerate(movie_list):
        markup.add(types.InlineKeyboardButton(text=value,callback_data=f"{key}"))

    return markup

def tamilmv():
    mainUrl = 'https://www.1tamilmv.tips/'
    mainlink = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Connection':'Keep-alive',
        'sec-ch-ua-platform': '"Windows"',
    }

    global movie_dict 
    movie_dict = {}
    global real_dict
    real_dict  = {}
    web = requests.request("GET",mainUrl,headers=headers)
    soup = BeautifulSoup(web.text,'lxml')
    linker = []
    magre = []
    badtitles = []
    realtitles = []
    global movie_list
    movie_list = []

    num = 0
    
    temps = soup.find_all('div',{'class' : 'ipsType_break ipsContained'})

    for i in range(21):
        title = temps[i].findAll('a')[0].text
        badtitles.append(title)
        links = temps[i].find('a')['href']
        content = str(links)
        linker.append(content)
        
    for element in badtitles:
        realtitles.append(element.strip())
        movie_dict[element.strip()] = None
    print(badtitles)
    movie_list = list(movie_dict)
        
    for url in linker:

        html = requests.request("GET",url)
        soup = BeautifulSoup(html.text,'lxml')
        pattern=re.compile(r"magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{40}")
        bigtitle = soup.find_all('a')
        alltitles = []
        filelink = []
        mag = []
        for i in soup.find_all('a', href=True):
            if i['href'].startswith('magnet'):
                mag.append(i['href'])
                
        for a in soup.findAll('a',{"data-fileext":"torrent",'href':True}):
            filelink.append(a['href'])

        for title in bigtitle:
            if title.find('span') == None:
                pass
            else:
                if title.find('span').text.endswith('torrent'):
                    alltitles.append(title.find('span').text[19:-8])

        for p in range(0,len(mag)):
#             print(f"*{alltitles[p]}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({filelink[p]})")
            try:
              real_dict.setdefault(movie_list[num],[])
              real_dict[movie_list[num]].append((f"*{alltitles[p]}* -->\n🧲 `{mag[p]}`\n🗒️->[Torrent file]({filelink[p]})"))
            except:
              pass
            
        num = num + 1


    
def main():
     bot.infinity_polling(timeout=10, long_polling_timeout = 5)
#     bot.polling() # looking for message
      

if __name__ == '__main__':
    main() 
   
#shinas101
