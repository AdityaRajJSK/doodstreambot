from os import environ
import os
import time
from unshortenit import UnshortenIt
from urllib.request import urlopen
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from pyshorteners import Shortener
from bs4 import BeautifulSoup
#from doodstream import DoodStream
import requests
import re

import pyrogram
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#from telethon.sessions import StringSession
#from telethon.sync import TelegramClient
#from decouple import config
import logging, sys
import threading
from doodstream import DoodStream

API_ID = environ.get('API_ID', 24748535)
API_HASH = environ.get('API_HASH', '7600412f97699a960c218fa1240a0822')
BOT_TOKEN = environ.get('BOT_TOKEN', '6005978396:AAF8v6xZwtmM0CBgDwy_DlYW9quk2czF8ws')
SESSION = environ.get('SESSION', 'AQBhPFxrmxMjobupLs54ZaLmwCv3IDGjiSOZS9CSoUenH-DfNUjZnXamwZ5vabZMAeJDaKM-gaCpf0_fWBiuAPBh1CWno2ICXBkpLmUd6BADn3kx3cjAOCbranR1BntU46ryLdK-qf08rELhYIT7LQnnj-U6HQ3qaOkfethlR7eweDNOZepijU0SEhxO-qfJiGT4uKwNdSxBKlNuSizYD29j3is7ceEl0K-SMvVo3h3OmG8UUzNh-QkSC6LsvYPdUc1dxOsvd4VTeqQiJZcarnPRegtutLAqTOAX5zIKlcvR9T1YspzpW3d2xHJN9KHIZ0hvZo0UY2XGrtDEZDJvnAxnAAAAAVbqnxYA')
DOODSTREAM_API_KEY = environ.get('DOODSTREAM_API_KEY', '201988m9954bb5is552b0r')
BITLY_KEY = environ.get('BITLY_KEY', 'ca51d2eba85e838eb65650ff14abc4310ff98ce7')
CHANNEL = environ.get('CHANNEL', 'https://google.com')
HOWTO = environ.get('HOWTO', 'https://google.com')
base_url = "https://doodapi.com/api/"
api = os.environ.get('DOODSTREAM_API', '201988m9954bb5is552b0r')
d = DoodStream(api)
bot = Client('Doodstream bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)
             
if SESSION is not None:
    acc = Client(
    session_name=SESSION, 
    api_hash=API_HASH, 
    api_id=API_ID)
    
    try:
            acc.start()
    except BaseException:
            print("Userbot Error ! Have you added SESSION while deploying??")
            sys.exit(1)
        
else: acc = None

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.message_id, f"__Downloaded__ : **{txt}**")
			time.sleep(2)
		except:
			time.sleep(2)
			
# upload status
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.message_id, f"__Uploaded__ : **{txt}**")
			time.sleep(2)
		except:
			time.sleep(2)
			
# progress writter
def progress(current, total, message, type):
	with open(f'{message.chat.id}{message.message_id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")
		
# dood stream upload
class DoodStream:
    def __init__(self, api_key):
        """init doodstream
        Args:
            api_key (str): api key from doodstream"""
        self.api_key = api_key

    def req(self, url):
        """requests to api

        Args:
            url (str): api url

        Return:
            (dict): output dic from requests url"""
        try:
            r = requests.get(url)
            response = r.json()
            if response["msg"] == "Wrong Auth":
                sys.exit("Invalid API key, please check your API key")
            else:
                return response
        except ConnectionError as e:
            sys.exit(f"ERROR : {e}")

    def account_info(self):
        """Get basic info of your account"""
        url = f"{self.base_url}account/info?key={self.api_key}"
        return self.req(url)

    def account_reports(self):
        """Get reports of your account"""
        url = f"{self.base_url}account/stats?key={self.api_key}"
        return self.req(url)

    def local_upload(self, path):
        """Upload from local storage

        Args:
            path (str): path to file
        """
        url = f"{self.base_url}upload/server?key={self.api_key}"
        url_for_upload = self.req(url)["result"]
        post_data = {"api_key": self.api_key}
        filename = path.split("/")[-1]
        post_files = {"file": (filename, open(path, "rb"))}
        res = requests.post(url_for_upload, data=post_data, files=post_files).json()
        if res["msg"] == "OK":
            return res
        else:
            raise TypeError(
                f"unsupported video format {filename}, please upload video with mkv, mp4, wmv, avi, mpeg4, mpegps, flv, 3gp, webm, mov, mpg & m4v format"
            )


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**I am a Doodstream post convertor bot and i am able to upload all direct links to Doodstream,just send me link or telegram link of any video**")
        
@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):

	# joining chats
	if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:

		if acc is None:
			bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
			return

		try:
			try: acc.join_chat(message.text)
			except Exception as e: 
				bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
				return
			bot.send_message(message.chat.id,"**Chat Joined**", reply_to_message_id=message.message_id)
		except UserAlreadyParticipant:
			bot.send_message(message.chat.id,"**Chat alredy Joined**", reply_to_message_id=message.message_id)
		except InviteHashExpired:
			bot.send_message(message.chat.id,"**Invalid Link**", reply_to_message_id=message.message_id)
	
	# getting message
	elif "https://t.me/" in message.text:

		datas = message.text.split("/")
		msgid = int(datas[-1].split("?")[0])

		# private
		if "https://t.me/c/" in message.text:
			chatid = int("-100" + datas[-2])
			if acc is None:
				bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
				return
			try: handle_private(message,chatid,msgid)
			except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
		
		# public
		else:
			username = datas[-2]
			msg  = bot.get_messages(username,msgid)
			try: bot.copy_message(message.chat.id, msg.chat.id, msg.id)
			except:
				if acc is None:
					bot.send_message(message.chat.id,f"**String Session is not Set**", reply_to_message_id=message.message_id)
					return
				try: handle_private(message,username,msgid)
				except Exception as e: bot.send_message(message.chat.id,f"**Error** : __{e}__", reply_to_message_id=message.message_id)
	
	
# handle private
def handle_private(message,chatid,msgid):
		msg  = acc.get_messages(chatid,msgid)

		if "text" in str(msg):
			bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.message_id)
			return

		smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.message_id)
		dosta = threading.Thread(target=lambda:downstatus(f'{message.chat.id}{message.message_id}downstatus.txt',smsg),daemon=True)
		dosta.start()
		file = acc.download_media(msg, progress=progress, progress_args=[message,"down"])
		os.remove(f'{message.chat.id}{message.message_id}downstatus.txt')
		"""upsta = threading.Thread(target=lambda:upstatus(f'{message.chat.id}{message.message_id}upstatus.txt',smsg),daemon=True)
		upsta.start()"""
		bot.edit_message_text(message.chat.id,[smsg.message_id], "__Uploading Please Wait...__")
		
		path=file
		if "Document" or "Video" in str(msg):
			try:
				u = d.local_upload(path)
				print("#" * 10 + " Local Upload " + "#" * 10)
				print(f"Status : {u['status']}")
				print(f"Video ID : {u['result'][0]['filecode']}")
				print(f"Video Url : {u['result'][0]['download_url']}")
				print(f"Protected DL : {u['result'][0]['protected_dl']}")
				print(f"Protected Embed : {u['result'][0]['protected_embed']}")
				print("#" * 40)
				bot.delete_messages(message.chat.id,[smsg.message_id])
				smsg = bot.send_message(message.chat.id, f"**Status :** {u['status']}\n\n**Video ID :** {u['result'][0]['filecode']}\n\n**Download Url :** {u['result'][0]['download_url']}\n\n**Protected DL :** {u['result'][0]['protected_dl']}\n\n**Protected Embed :** {u['result'][0]['protected_embed']}\n\n ", reply_to_message_id=message.message_id)
			except: 
			    pass
		os.remove(file)
		if os.path.exists(f'{message.chat.id}{message.message_id}upstatus.txt'): os.remove(f'{message.chat.id}{message.message_id}upstatus.txt')


@bot.on_message(filters.video)
async def vdood_upload(bot, message):
    smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.message_id)
    dosta = threading.Thread(target=lambda:downstatus(f'{message.chat.id}{message.message_id}downstatus.txt',smsg),daemon=True)
    dosta.start()
    file = bot.download_media(message, progress=progress, progress_args=[message,"down"])
    #os.remove(f'{message.chat.id}{message.message_id}downstatus.txt')
    """upsta = threading.Thread(target=lambda:upstatus(f'{message.chat.id}{message.message_id}upstatus.txt',smsg),daemon=True)
    upsta.start()"""


@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Doodstream Links, texts & images... Than I'll convert & replace all Doodstream links with your Doodstream links \nMessage me @kamdev07 For more help-**")

@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @kamdev07 or for more join @Doodstream_Admins**")
    
@bot.on_message(filters.text & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{Doodstream_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        if(len(Doodstream_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{Doodstream_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{Doodstream_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


'''async def get_ptitle(url):
    if ('bit' in url or 'gplink' in url ):
      url = urlopen(url).geturl()
      
      
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for title in soup.find_all('title'):
        pass
    title = list(title.get_text())
    title = title[8:]
    str = 't.me/' + CHANNEL + ' '
    for i in title:
        str = str + i
    lst = list(html_text.split(","))
    c = 0
    for i in lst:
        if ("""/e/""" in i):
            found = lst[c]
            break
        c += 1

    # Doodstream.com link
    Doodstream_video_id = list(found.split(":"))
    video_id = Doodstream_video_id[2]
    video_id = list(video_id.split(","))
    v_id = video_id[0]
    #v_len = len(v_id)
    #v_id = v_id[1:v_len - 2]

    v_url = 'https://dood.ws/d/' + v_id
    v_url = url
    res = [str, v_url]
    return res'''


async def Doodstream_up(link):
    if ('bit' in link):
        #link = urlopen(link).geturl()
        unshortener = UnshortenIt()
        link = unshortener.unshorten(link)
    
    title_new = urlparse(link)
    title_new = os.path.basename(title_new.path)
    title_Doodstream = '@' + CHANNEL + title_new
    res = requests.get(
         f'https://doodapi.com/api/upload/url?key={DOODSTREAM_API_KEY}&url={link}&new_title={title_Doodstream}')
         
    data = res.json()
    data = dict(data)
    print(data)
    v_id = data['result']['filecode']
    #bot.delete_messages(con)
    v_url = 'https://dood.ws/d/' + v_id
    s = Shortener(api_key=BITLY_KEY)
    v_url = s.bitly.short(v_url)
    return (v_url)


async def multi_Doodstream_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_Doodstream_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)


async def new_Doodstream_url(urls):
    new_urls = []
    for i in urls:
        time.sleep(0.2)
        new_urls.append(await Doodstream_up(i))
    return new_urls


async def remove_username(new_List):
    for i in new_List:
        if('@' in i or 't.me' in i or 'https://bit.ly/abcd' in i or 'https://bit.ly/123abcd' in i or 'telegra.ph' in i):
            new_List.remove(i)
    return new_List

async def addFooter(str):
    footer = """
    ━━━━━━━━━━━━━━━
⚙️ How to Download / Watch Online :""" + HOWTO + """
━━━━━━━━━━━━━━━
⭐️JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer

bot.run()
