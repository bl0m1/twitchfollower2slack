#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Docstring """

import json
import time
import requests
import logging
from twitchchannelquery import twitchchannelquery

# pylint: disable=invalid-name,global-statement

CONFIG_FILE = "config.json"
TIME_FILE = "time.json"
SAVE_CONFIG = True
new_followers = 0
message = ""
Start = 0

def save_json(f, cfg):
    """ Save JSON-formatted file """
    try:
        with open(f, 'w') as configfile:
            json.dump(cfg, configfile)
    except:
        return False
    return True

def read_json(f):
    """ Read JSON-formatted file """
    data = []
    try:
        with open(f, 'r') as configfile:
            data = json.load(configfile)
    except (FileNotFoundError, PermissionError):
        pass
    return data

def default_json(flag):
    if flag is 'config':
        return {"channel": "swectv", "webhook": "", "username": "twitch", "slack-channel": "#webhook-test", "get_followers": "100"}
    if flag is 'time':
        return {"time": "0"}
    else:
        return {}

if not 'oldtime' in locals():
    oldtime = 1

def get_date(list, nr):
    time = list.get_follower_list()[nr]['created_at']
    time_fixed = time_to_nummeric(time)
    return int(time_fixed)


def time_to_nummeric(time):
    return time.replace("-", "").replace(":", "").replace("T", "").replace("Z", "")

def get_follower_name(list, nr):
    return list.get_follower_list()[int(nr)-1]['user']['display_name']


def has_new_follower(list):
    global follower_oldtime
    follower_oldtime = int(TIME['time'])
    global new_followers

    newtime = get_date(list, 0)
    if newtime > follower_oldtime:
        new_followers = 1

        while int(get_date(list, new_followers)) > int(TIME['time']):
            new_followers += 1
            if new_followers >= int(CONFIG["get_followers"]):
                break
        save_json(TIME_FILE, {"time": str(newtime)})
        return new_followers
    else:
        return 0

def generate_message(channel):
    """ Docstring """
    if has_new_follower(channel) > 0:
        if new_followers == 1:
            message = "1 new follower: " + get_follower_name(channel, 1)
            logger.info(message)
            if CONFIG["webhook"]:
                send_message(CONFIG["webhook"], CONFIG["username"], CONFIG["slack-channel"], message)
        else:
            message = "New followers (" + str(new_followers) + ")"
            new_followers_int = (int(new_followers))
            while (new_followers_int > 0):
                message += "\n" + str(new_followers_int) + ": " + get_follower_name(channel, new_followers_int)
                new_followers_int -= 1
            logger.info(message)
            if CONFIG["webhook"]:
                send_message(CONFIG["webhook"], CONFIG["username"], CONFIG["slack-channel"], message)
    else:
        logger.info("no new followers this time.")

def send_message(url, username, channel, string):
    """ Docstring """
    payload = {"username": username, "channel": channel, "text": string}
    requests.post(url, json=payload)

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO,
                    filename='twitch.log',
                    format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)

CONFIG = read_json(CONFIG_FILE)
TIME = read_json(TIME_FILE)
if not CONFIG:
    CONFIG = default_json('config')
    if SAVE_CONFIG is True:
        save_json(CONFIG_FILE, CONFIG)
if not TIME:
    CONFIG = default_json('time')
    if SAVE_CONFIG is True:
        save_json(TIME_FILE, CONFIG)

channel = twitchchannelquery()
channel.setup(CONFIG["channel"], CONFIG["get_followers"])

if (Start == 0):
    logger.info("Started!")
    channel.query_follower_list()
    TIME = read_json(TIME_FILE)
    generate_message(channel)
    Start = 1
    logger.info("Done!")
