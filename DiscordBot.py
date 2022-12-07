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
import json
from bs4 import BeautifulSoup

client_id = ""
client_secret = ""
ustoken = "0"
eutoken = "0"

client = discord.Client()
bot = commands.Bot(command_prefix='!')

users = []
dirPath = 'C:/d3_stuff/BotStuff/DiscordBot/'
userslist = []
for i in userslist:
    with open(dirPath + 'UserData/' + i + '/' + i + '_info.json', 'r') as f:
        js = json.load(f)
        users.append(js)

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

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# emoting when user's name is sent
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    msgItems = message.content.split()
    for i in msgItems:
        for x in range(len(users)):
            if "emote" in users[x]:
                if i == (users[x]["name"]).lower() or i == (users[x]["name"]).capitalize():
                    emoji = bot.get_emoji(users[x]['emote'])
                    await message.add_reaction(emoji)

    await bot.process_commands(message)

# sends userlist to discord chat
@bot.command()
async def userlist(ctx):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    userlist = []
    for i in range(len(users)):
        userlist.append(users[i]['name'])
    await ctx.send(userlist)
 

@bot.command()
@commands.dm_only()
async def quit(ctx):
    if ctx.author.id == 219579010361982976:
        try:
            exit()
        except Exception as e:
            print(e)
    else:
        await ctx.send("Your cock isn't long enough, sorry :(")
@bot.command()
@commands.dm_only()
async def dataChange(ctx, user, key, data):
    if ctx.author.id == 219579010361982976 or ctx.author.id == 123820105032269824:
        try:
            global userlist
            global dirPath
            counter = 0
            user = user.capitalize()
            for i in userslist:
                if i == user:
                    print(i)
                    if key == 'emote':
                        newData = {key: int(data)}
                    elif key == 'seasonal':
                        if data == 'True':
                            data = True 
                            newData = {key: data}
                        else:
                            data = False
                            newData = {key: data}
                    elif key == 'timestamp':
                        newData = {key: int(data)}
                    else:
                        newData = {key: data}
                    users[counter].update(newData)
                    userJson = users[counter]
                    print(userJson)
                counter += 1
            with open(dirPath + 'UserData/' + user + '/' + user + '_info.json', 'w') as f:
                json.dump(userJson, f)
            await ctx.send('```' + str(userJson) + '```')
        except Exception as e:
            print(e)
    else:
        await ctx.send("You lack adequate permissions")

@bot.command()
@commands.dm_only()
async def data(ctx, user):
    if ctx.author.id == 219579010361982976 or ctx.author.id == 123820105032269824:
        try:
            global userlist
            global dirPath
            counter = 0
            user = user.capitalize()
            for i in userslist:
                if i == user:
                    userJson = users[counter]
                    await ctx.send('```' + str(userJson) + '```')
                    print(userJson)
                counter += 1
        except Exception as e:
            print(e)
    else:
        await ctx.send("You lack adequate permissions")

#sends PN and paragon to chat   
@bot.command()
async def pn(ctx, arg):
    global userlist
    global dirPath
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    try:
        if arg == 'prophet' or arg == 'proph' or arg == 'bighandsomegermandude' or arg == 'shithead':
            arg = 'proph3t'
        for i in range(len(users)):
            arg = arg.capitalize()
            if users[i]["name"] == arg:
            #    try:
            #        userJson = users[i]
            #        if 'timeStamp' in userJson:
            #            if not isinstance(ctx.channel, discord.channel.DMChannel):
            #                currentTime = int(time.time())
            #                timeDifference = currentTime - userJson['timeStamp']
            #                if timeDifference <= 600:
            #                    await ctx.send("You've used this command too often, please wait " + str(int((600 - timeDifference)/60)) + " minutes and " + str((600 - timeDifference)%60) + " seconds" + "\nYou can use this command in DMs without cooldown :)")
            #                    break
            #                else:
            #                    newData = {'timeStamp': int(time.time())}
            #                    users[i].update(newData)
            #                    userJson = users[i]
            #                    with open(dirPath + 'UserData/' + arg + '/' + arg + '_info.json', 'w') as f:
            #                        json.dump(userJson, f) 
            #        else:
            #            print('No timeStamp, creating one')
            #            newData = {'timeStamp': int(time.time())}
            #            users[i].update(newData)
            #            userJson = users[i]
            #            with open(dirPath + 'UserData/' + arg + '/' + arg + '_info.json', 'w') as f:
            #                json.dump(userJson, f)        
            #    except Exception as e:
            #        print(e)
                try:
                    if users[i]["name"] == "Rock" or users[i]["name"] == "Rock2":
                        img = Image.open(urlopen(users[i]["pnAddressInternal"], timeout=1))
                        img.save(users[i]["name"] + ".png")
                        await ctx.send(file=discord.File(users[i]["name"] + '.png'))
                    else:
                        img = Image.open(urlopen(users[i]["pnAddressExternal"], timeout=1))
                        img.save(users[i]["name"] + ".png")
                        await ctx.send(file=discord.File(users[i]["name"] + '.png'))
                except:
                    await ctx.send("Unable to retrieve image, stopping function")
                    break
                try:
                    if users[i]["seasonal"] == False:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[0]
                    else:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[1]
                    #print(tag.split('%')[0] + "'s nonseason paragon is " + str(currentParagon))
                    if int(currentParagon) == 0:
                        raise Exception('BOOM!')
                    else:
                        await ctx.send(users[i]["name"] + "'s paragon is " + str(currentParagon))    
                except Exception as e:
                    print(e)
                    await ctx.send("Unable to retrieve " + users[i]["name"] + "'s paragon")
                log.log_data(users[i]["name"], currentParagon)
                return
            if i == len(users) - 1:
                raise Exception('BOOM!')
                break
    except Exception as e:
        print(e)
        await ctx.send("Invalid user")

# sends para to chat
@bot.command()
async def para(ctx, arg):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    try:
        for i in range(len(users)):
            arg = arg.capitalize()
            if users[i]["name"] == arg:
                try:
                    if users[i]["seasonal"] == False:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[0]
                    else:
                        currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[1]
                    #print(tag.split('%')[0] + "'s nonseason paragon is " + str(currentParagon))
                    if int(currentParagon) == 0:
                        raise Exception('BOOM!')
                    else:
                        await ctx.send(users[i]["name"] + "'s paragon is " + str(currentParagon))    
                except:
                    await ctx.send("Unable to retrieve " + users[i]["name"] + "'s paragon")
                return
            if i == len(users) - 1:
                raise Exception('BOOM!')
    except:
        await ctx.send("Invalid user")

# Calculates time needed to reach certain paragon
@bot.command()
async def paracalc(ctx, name, goalLevel, BilEph):
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    username = name.capitalize()
    for i in range(len(users)):
        if username == users[i]["name"]:
            if users[i]["seasonal"] == False:
                currentLevel = api.query_btag(users[i]["tag"], users[i]["region"])[0]
                break
            else: 
                currentLevel = api.query_btag(users[i]["tag"], users[i]["region"])[1]
                break
   # if "k" in currentLevel:
   #     currentLevel = currentLevel.replace("k", "000")
    if "k" in goalLevel:
        goalLevel = goalLevel.replace("k", "000")
    def millify(n):
        millnames = ['',' Thousand',' Million',' Billion',' Trillion']
        n = float(n)
        millidx = max(0,min(len(millnames)-1,
                            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

        return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
    def getParaLevelXp(level):
        c1 = 166105421028000
        c2 = 201211626000
        c3 = 229704000
        c4 = 102000
        half = 0.5
        six = 6

        x = int(level) - 2252
        xp1 = int(level) - 2251
        xp2 = int(level) - 2250
        xpVar = c1 + (c2 * x + (c3 * (x * xp1 * half) + (x * xp1 * xp2 / six) * c4))
        return xpVar

    def DiffParagon(a, b):
        current = b
        goal = a
        xpDifVar = getParaLevelXp(current) - getParaLevelXp(goal)
        return xpDifVar
    try:
        xpReq = DiffParagon(currentLevel, goalLevel)
        timeReq = xpReq/float(int(BilEph) * pow(10,9))
        await ctx.send("Current Paragon: " + str(currentLevel) + '\n' + "Goal Paragon: " + str(goalLevel) + '\n' + "EPH: " + str(BilEph) + ' Billion' + '\n' + "XP Required: " + str(millify(xpReq)) + '\n' + "Hours Required: " + str(int(timeReq)) + '\n' + "Days Required: " + str(round(int(timeReq)/24, 1)))
    except:
        await ctx.send("its fucking broken idk man")

# pretty table for "leaderboard"
@bot.command()
async def gons(ctx):
    seasonlist = [] 
    nonseasonlist = []
    seasonlist2 = []
    nonseasonlist2 = []
    if not isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.message.delete()
    for i in range(len(users)):
        try:
            if users[i]["seasonal"] == False:
                if users[i]["name"] == "Proph3t2":
                    continue
                else:
                    currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[0]
                    nonseasonlist.append(users[i]["name"] + " " + str(currentParagon))
                    print(users[i]["name"])
            elif users[i]["seasonal"] == True:
                if users[i]["name"] == "Proph3t2":
                    continue
                else:
                    currentParagon = api.query_btag(users[i]["tag"], users[i]["region"])[1]
                    seasonlist.append(users[i]["name"] + " " + str(currentParagon))
                    print(users[i]["name"])
        except Exception as e:
            print(e)
            continue

    seasonlist = sorted(seasonlist, key=lambda x: int(re.search(r'\d+$',x).group()), reverse=True)
    for i in range(len(seasonlist)):
        #seasonlist2.append(str(i + 1) + ". " + seasonlist[i])
        seasonlist2.append(seasonlist[i])

    nonseasonlist = sorted(nonseasonlist, key=lambda x: int(re.search(r'\d+$',x).group()), reverse=True)
    for i in range(len(nonseasonlist)):
        #nonseasonlist2.append(str(i + 1) + ". " + nonseasonlist[i])
        nonseasonlist2.append(nonseasonlist[i])

    embed = discord.Embed(title="Paragon Ranking")
    newseasonlist2 = ('\n'.join(seasonlist2))
    newnonseasonlist2 = ('\n'.join(nonseasonlist2))

    namenonseasonlist2 = [i.split(" ")[0] for i in nonseasonlist2]
    gonnonseasonlist2 = [i.split(" ")[1] for i in nonseasonlist2]
    namenonseasonlist2 = ('\n'.join(namenonseasonlist2))
    gonnonseasonlist2 = ('\n'.join(gonnonseasonlist2))

    nameseasonlist2 = [i.split(" ")[0] for i in seasonlist2]
    gonseasonlist2 = [i.split(" ")[1] for i in seasonlist2]
    nameseasonlist2 = ('\n'.join(nameseasonlist2))
    gonseasonlist2 = ('\n'.join(gonseasonlist2))

    embed.add_field(name="Seasonal", value="** **", inline=False)
    embed.add_field(name="User", value=nameseasonlist2, inline = True)
    embed.add_field(name="Gons", value=gonseasonlist2, inline = True)

    embed.add_field(name="Non Seasonal", value="** **", inline=False)
    embed.add_field(name="User", value=namenonseasonlist2, inline = True)
    embed.add_field(name="Gons", value=gonnonseasonlist2, inline = True)
    await ctx.send(embed=embed)

@bot.command()
@commands.dm_only()
async def scraper(ctx, minimum, maximum, iterator, secondsToRun=None):
    print(ctx.author.name, "using scraper")
    if ctx.author.id == 219579010361982976 or ctx.author.id == 191025633365590026 or ctx.author.id == 789168743321829405:
        startTime = int(time.time())
        for i in range(int(minimum), int(maximum), int(iterator)):
            if secondsToRun == None:
                if startTime + 30 <= int(time.time()):
                    await ctx.send("ending")
                    return
            else:
                if startTime + int(secondsToRun) <= int(time.time()):
                    await ctx.send("ending")
                    return           
            try:
                response = requests.get("https://ros-bot.com/node/" + str(i))
                if response.status_code == 429:
                    await ctx.send("too many queries")
                    return
                data = response.text
                soup = BeautifulSoup(data, 'html.parser')
                title = soup.find("meta", property="og:title")
                url = soup.find("meta", property="og:url")
                name = soup.find("span", class_="username")
                if "custom-script" in str(url):
                    await ctx.send("SCRIPT, " + str(title) + ", " + str(url) + ", " + str(name.text) + "\n")
                elif "bot-settings" in str(url):
                    await ctx.send("SETTINGS, " + str(title) + ", " + str(url) + ", " + str(name.text) + "\n")
                elif "fast-mode" in str(url):
                    await ctx.send("FM, " + str(title) + ", " + str(url) + ", " + str(name.text) + "\n")    
                elif "master-profiles" in str(url):
                    await ctx.send("MP, " + str(title) + ", " + str(url) + ", " + str(name.text) + "\n")               
                else:
                    await ctx.send("OTHER, "+ str(title) + ", " + str(url) + ", " + str(name.text) + "\n")
            except Exception as e:
                await ctx.send(e)
                continue
bot.run()//TOKEN HERE
