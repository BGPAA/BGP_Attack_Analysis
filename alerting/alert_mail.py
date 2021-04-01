#!/usr/bin/env python
# coding: utf-8
import os
import glob
import gzip
import pytz
import shutil
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta



def unzip(now_str):
    files = glob.glob("archives/" + now_str + "*_hijacks.json.gz")
    for f in files:
        with gzip.open(f, 'rb') as f_in:
            with open(f.split(".gz")[0], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def concat(now_str):
    files_in = glob.glob("archives/"+now_str+"*_hijacks.json")
    file_out = "archives/"+now_str+"hijacks.json"
    with open(file_out, 'w') as f_out :
        for f_in in files_in:
            with open(f_in) as infile:
                f_out.write(infile.read())
            os.remove(f_in))
    with open(file_out, 'rb') as f_in, gzip.open(file_out + '.gz', 'wb') as f_out:
        f_out.writelines(f_in)

"""
DISPLAY PART
"""
def decrompress_gzip_file():
    json_file = os.popen("cat " + os.getcwd() + "/archives/"+now_str+"hijacks.json", "r").read()

    json_line = ""
    all_json_line = []

    for element in json_file:
        if element == "\n":
            all_json_line.append(json_line)
            json_line = ""
        else:
            json_line += str(element)

    return all_json_line

"""
ASCII
"""
# def add_space(characteristic_list, current_characteristic):
#     max_length = len(max(characteristic_list, key=len))
#     space = ""
#     for i in range(max_length - len(current_characteristic)):
#         space += " "

#     return space

"""
HTML
"""
def add_space(characteristic_list, current_characteristic):
    max_length = len(max(characteristic_list, key=len))
    space = ""
    for i in range(max_length - len(current_characteristic)):
        space += "&nbsp;"

    return space

def retrieve_characteristic(all_json_line):
    characteristic = []
    random_json_line = json.loads(all_json_line[0])
    for element in random_json_line:
        characteristic.append(element)
    return characteristic

"""
ASCII
"""
# def display_json(all_json_line):
#     ret = ""
#     for line in all_json_line:
#         json_line = json.loads(line)
#         characteristic_list = retrieve_characteristic(all_json_line)
#         for element in characteristic_list:
#             if isinstance(json_line[element], dict):
#                 ret += str(element) + add_space(characteristic_list, str(element)) + " : " + "\n"
#                 for characteristic, value in json_line[element].items():
#                     ret += add_space(characteristic_list, "") + "   " + str(characteristic) + add_space(json_line[element], str(characteristic)) + " : " + str(value) + "\n"
#             else:
#                 a = str(element)
#                 b = str(json_line[element])
#                 c = a + add_space(characteristic_list, a) + " : " + b
#                 ret += c + "\n"
        
#         ret += "\n"

#     return ret


"""
HTML
"""
def display_json(all_json_line):
    ret = "<pre>-------------------------------------------------<br />"
    count = 1
    for line in all_json_line:
        json_line = json.loads(line)
        characteristic_list = retrieve_characteristic(all_json_line)
        ret += "<strong>Hijack " + str(count) + "</strong> : <br />"
        for element in characteristic_list:
            if element in json_line:
                if isinstance(json_line[element], dict):
                    ret += str(element) + add_space(characteristic_list, str(element)) + "&nbsp;:&nbsp;" + "<br />"
                    for characteristic, value in json_line[element].items():
                        ret += add_space(characteristic_list, "") + "&nbsp;&nbsp;&nbsp;" + str(characteristic) + add_space(json_line[element], str(characteristic)) + "&nbsp;:&nbsp;" + str(value) + "<br />"
                else:
                    a = str(element)
                    b = str(json_line[element])
                    c = a + add_space(characteristic_list, a) + "&nbsp;:&nbsp;" + b
                    ret += c + "<br />"
        count += 1
        ret += "-------------------------------------------------<br />"
    ret += "</pre>"
    return ret


now = datetime.now(pytz.utc)
now_str = now.strftime("%Y-%m-%d")

unzip(now_str)
concat(now_str)

print(display_json(decrompress_gzip_file()))   
"""
MAIL PART
"""

message = display_json(decrompress_gzip_file())
address_list = ['INSERT MAILING LIST HERE'] 
sender_address = 'INSERT YOUR SENDER ADDRESS'
password = 'INSERT YOUR SENDER PASSWORD'
server_smtp = 'INSERT YOUR SMTP SERVER'

for address in address_list: 
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = address
    msg['Subject'] = 'Le sujet de mon mail' 
    msg.attach(MIMEText(message, 'html'))
    mailserver = smtplib.SMTP(server_smtp, 465)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(sender_address, password)
    mailserver.sendmail(sender_address, address, msg.as_string())
    mailserver.quit()
os.remove("archives/"+now_str+"hijacks.json")

