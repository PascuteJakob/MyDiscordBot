import discord 
import asyncio
from discord.ext import commands
from discord.utils import get
import os
from PIL import Image
from urllib.request import urlopen
import requests
import re
import time
import math
from requests.auth import HTTPBasicAuth
from datetime import datetime

client_id = "d7943f5e28ca44c8b1e4946e44316e1c"
client_secret = "apXdFIJ9u1IskqEDqwAftgntEjsM3ozb"
ustoken = "0"
eutoken = "0"

users = [
    {
        "name": "Rock",
        "pnAddressInternal": "",
        "pnAddressExternal": "",
        "emote": 827679557078220829,
        "seasonal": True,
        "tag":  "",
        "region": "us"
    },
]

class Logging:
    def __init__(self):
        print()
        #placeholder

    def log_data(self, user, paragon):
        dirPath = 'C:/d3_stuff/BotStuff/DiscordBot/'
        currentTime = datetime.now().strftime("%d-%m-%Y %H-%M-%S")
        currentTime = currentTime.split(" ")
        fileName = str(user) + '.png'
        imagePath = dirPath + fileName
        userPath = dirPath + 'UserData/' + user + "/"
        print(userPath)
        print(imagePath)
        print(userPath + fileName)
        if os.path.isdir(userPath) == False:
            print('making folder')
            os.mkdir(userPath)
        try: 
            if not os.path.isfile(userPath + "data.csv"):
                a = open(userPath + "data.csv", "a")
                a.write("date,time,paragon,imgPath \n")
                a.close()
            f = open(userPath + "data.csv", "a")
            f.write(currentTime[0] + "," + currentTime[1] + "," + str(paragon) + "," + userPath + user + '_' + str(paragon) + '_' + currentTime[0] + "_" + currentTime[1] + '.png' + "\n")
            f.close()
        except Exception as e:
            print('------ make csv error ------')
            print(e)
            print('----------------------------')
        try:
            os.replace(imagePath, userPath + user + '_' + str(paragon) + '_' + currentTime[0] +  '_' + currentTime[1] + '.png')
        except Exception as e:
            print(e)
            return
        return

class ApiCommands:
    def __init__(self, cid, csecret, us, eu):
        self.client_id = cid
        self.client_secret = csecret
        self.ustoken = us
        self.eutoken = eu
    def create_access_token(self, id, secret, region):
        url = "https://%s.battle.net/oauth/token" % region
        body = {"grant_type": 'client_credentials'}
        auth = HTTPBasicAuth(id, secret)
        response = requests.post(url, data=body, auth=auth)
        return response.json()

    def query_btag(self, tag, region):
        try:
            if region == "us":
                dataRequest = requests.get("https://" + region + ".api.blizzard.com/d3/profile/ " + tag + "/?locale=en_US&access_token=" + self.ustoken)
                if dataRequest.status_code == 401:
                    self.ustoken = self.create_access_token(self.client_id, self.client_secret, region)['access_token']
                    dataRequest = requests.get("https://" + region + ".api.blizzard.com/d3/profile/ " + tag + "/?locale=en_US&access_token=" + self.ustoken)
            if region == "eu":
                dataRequest = requests.get("https://" + region + ".api.blizzard.com/d3/profile/ " + tag + "/?locale=en_US&access_token=" + self.eutoken)
                if dataRequest.status_code == 401:
                    self.eutoken = self.create_access_token(self.client_id, self.client_secret, region)['access_token']
                    dataRequest = requests.get("https://" + region + ".api.blizzard.com/d3/profile/ " + tag + "/?locale=en_US&access_token=" + self.eutoken)
            print(dataRequest)
            print(dataRequest.status_code)
            playerData = dataRequest.json()
            nsParagon = playerData['paragonLevel']
            sParagon = playerData['paragonLevelSeason']
            return nsParagon, sParagon
        except Exception as e:
            print(e)

log = Logging()
api = ApiCommands(client_id, client_secret, ustoken, eutoken)


def pn(arg):
    try:
        for i in range(len(users)):
            arg = arg.capitalize()
            if users[i]["name"] == arg:
                try:
                    if users[i]["name"] == "Rock" or users[i]["name"] == "Rock2":
                        img = Image.open(urlopen(users[i]["pnAddressInternal"], timeout=1))
                        img.save(users[i]["name"] + ".png")
                        print('image saved')
                    else:
                        img = Image.open(urlopen(users[i]["pnAddressExternal"], timeout=1))
                        img.save(users[i]["name"] + ".png")
                        print('image saved')
                except:
                    print("Unable to retrieve image")
                try:
                    if users[i]["seasonal"] == False:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[0]
                    else:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[1]
                    #print(tag.split('%')[0] + "'s nonseason paragon is " + str(currentParagon))
                    if int(currentParagon) == 0:
                        raise Exception('BOOM!')
                    else:
                        print(users[i]["name"] + "'s paragon is " + str(currentParagon))    
                except Exception as e:
                    print(e)
                    print("Unable to retrieve " + users[i]["name"] + "'s paragon")
                log.log_data(users[i]["name"], currentParagon)
                return
            if i == len(users) - 1:
                raise Exception('BOOM!')
    except Exception as e:
        print(e)
        print("Invalid user")

while True:
    for i in range(len(users)):
        pn(users[i]['name'])
    print('starting sleep')
    time.sleep(1800)
