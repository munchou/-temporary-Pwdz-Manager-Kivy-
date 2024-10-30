import string, hashlib
import plyer
from random import choice, shuffle, randint
import json
from os.path import exists
import platform
import configparser
import bcrypt
from configparser import ConfigParser

from kivy.uix.popup import Popup
from kivy.uix.label import Label


FILENAME = "config.ini"


def show_message(title, message):
    message = message.replace("\n", " [returnz] ")
    height = 1
    if len(message) > 35:
        message = message.split(" ")
        sentence = ""
        long_message = ""
        for u in range(len(message)):
            word = message[u]
            word = word.strip()
            if word == "[returnz]":
                word = ""
            else:
                if len(sentence + word) <= 35:
                    sentence += f"{word} "
                    if u == len(message):
                        height += 1
                        break
                    continue
            long_message += f"{sentence.strip()}\n"
            height += 1
            sentence = f"{word} "
        long_message += f"{sentence.strip()}"
        message = long_message

    popup = Popup(
        title=title,
        content=Label(text=message),
        size_hint=(None, None),
        size=("350dp", f"{80 + 20*height}dp"),
    )
    popup.open()


def hasher(word, salt):
    sha256 = hashlib.sha256()
    sha256.update((word + salt).encode())
    return sha256.hexdigest()
    # word = bytes(word, "utf-8")
    # return bcrypt.hashpw(word, salt)


def generate_salt():
    return bcrypt.gensalt()


def create_ini(
    username,
    salt,
    device_id,
    filename=FILENAME,
):
    """Create the config INI file after having filled in
    the fields."""
    # print("salt CREATE INI:", salt)
    parser = ConfigParser()
    parser.add_section(username)
    parser.set(username, "salt", salt)
    parser.set(username, "device id", device_id)

    with open(filename, "w") as configfile:
        parser.write(configfile)


def check_input(word):
    if " " not in word or word == "":
        if word.isascii():
            return word
    return False


def add_user(
    username,
    password,
    device_id,
    filename=FILENAME,
):
    """Update the config INI file after having filled in
    the fields."""

    parser = ConfigParser()
    parser.read(filename)
    try:
        parser.add_section(username)
    except configparser.DuplicateSectionError:
        print("Section already exists, skipping that step.")

    parser.set(username, "password", password)
    parser.set(username, "device id", device_id)

    with open(filename, "w") as configfile:
        parser.write(configfile)


def load_config_info(filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    # for item in parser.items():
    #     if item[0] == "autologin":
    #         print("AUTOLOGIN FOUND")
    params = parser.items(hasher("user_test", ""))
    print("Config file loaded")
    for param in params:
        print(param, param[0], param[1])


def list_users(username, password, filename=FILENAME):
    parser = ConfigParser()
    parser.read(filename)
    # for item in parser.items():
    return [item[0] for item in parser.items()]

    print(list(parser.items()))


def auto_login(filename=FILENAME):
    autologin = False
    parser = ConfigParser()
    parser.read(filename)
    for item in parser.items():
        if item[0] == "autologin":
            autologin = True
            break
    return autologin


def get_sys_info():
    system_info = platform.uname()

    print("System Information:")
    print(f"System: {system_info.system}")
    print(f"Node Name: {system_info.node}")
    print(f"Release: {system_info.release}")
    print(f"Version: {system_info.version}")
    print(f"Machine: {system_info.machine}")
    print(f"Processor: {system_info.processor.replace(' ', '')}")

    device_id = plyer.uniqueid.id
    print(f"Device unique ID: {device_id}")
