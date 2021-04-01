#!/usr/bin/env python
# coding: utf-8

import os
import json
import subprocess

"""
DISPLAY PART
"""
def decrompress_gzip_file():

    json_file = os.popen("cat " + os.getcwd() + "/../output/no_name/all.hijacks.json", "r").read()
    #json_file = os.popen("cat test.json", "r").read()

    json_line = ""
    all_json_line = []

    for element in json_file:
        if element == "\n":
            all_json_line.append(json_line)
            json_line = ""
        else:
            json_line += str(element)

    return all_json_line

def add_space(characteristic_list, current_characteristic):
    max_length = len(max(characteristic_list, key=len))
    space = ""
    for i in range(max_length - len(current_characteristic)):
        space += " "

    return space

def retrieve_characteristic(all_json_line):
    characteristic = []
    random_json_line = json.loads(all_json_line[0])
    for element in random_json_line:
        characteristic.append(element)
    return characteristic

def display_json(all_json_line):
    ret = "-------------------------------------------------\n"
    count = 1
    for line in all_json_line:
        json_line = json.loads(line)
        characteristic_list = retrieve_characteristic(all_json_line)
        ret += "Hijack " + str(count) + " : \n"
        for element in characteristic_list:
            if element in json_line:
                if isinstance(json_line[element], dict):
                    ret += str(element) + add_space(characteristic_list, str(element)) + " : " + "\n"
                    for characteristic, value in json_line[element].items():
                        ret += add_space(characteristic_list, "") + "   " + str(characteristic) + add_space(json_line[element], str(characteristic)) + " : " + str(value) + "\n"
                else:
                    a = str(element)
                    b = str(json_line[element])
                    c = a + add_space(characteristic_list, a) + " : " + b
                    ret += c + "\n"
        count += 1
        ret += "-------------------------------------------------\n"
    return ret

path_result = os. getcwd() + "/../output/result.txt"
fichier = open(path_result, "w")
fichier.write(display_json(decrompress_gzip_file()))
fichier.close()

import discord
import asyncio
from discord.ext.commands import bot
from discord.ext import commands

bot = commands.Bot(command_prefix = "!")
@bot.event
async def on_ready():
    print("Le bot est prêt")
    await bot.get_channel(519597257784557570).send("BGP HIJACK DETECTION BOT is online.\nI am ready to send you some informations.\n\nHere is the 5 minutes update with all hijacks :")
    await bot.get_channel(519597257784557570).send(file=discord.File(path_result))
    await bot.get_channel(519597257784557570).send("Enjoy ;)")

# bgp hijacks all
@bot.command(pass_context = True, help = "Display all the hijacks characteristics detected during a 5 min window")
async def bgpha(ctx):
        await ctx.send(file=discord.File(path_result))

# bgp hijacks one
@bot.command(pass_context = True, help = "Display one hijack characteristics detected during a 5 min window")
async def bgpho(ctx, number_of_hijack:int):
    fichier = open(path_result, "r")
    lines = fichier.readlines()
    bool_value = False
    fine_result_string = ""
    path_fine_result = os.getcwd() + "/../output/fine_result.txt"

    for line in lines:
        if line == "Hijack " + str(number_of_hijack) + " : \n":
            bool_value = True
            fine_result = open(path_fine_result, "w")
            fine_result_string += "-------------------------------------------------\n"

        if bool_value == True:
            fine_result_string += line
            
        if (bool_value == True and line == "-------------------------------------------------\n"):
            fine_result.write(fine_result_string)
            fine_result.close()
            break 
        
    fichier.close()
    await ctx.send(file=discord.File(path_fine_result))

# bgp hijacks number
@bot.command(pass_context = True, help = "Display the number of hijacks detected during a 5 min window")
async def bgphn(ctx):
    print(path_result)
    fichier = open(path_result, "r")
    lines = fichier.readlines()
    i = 1
    for line in lines:
        if line == "Hijack " + str(i) + " : \n":
            i += 1

    fichier.close()

    await ctx.send("There are " + str(i - 1) + " hijacks")
    
token = 'INSERT TOKEN HERE'
bot.run(token)
