import asynckivy

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import Screen, MDScreen
from kivymd.uix.screenmanager import ScreenManager

# from kivymd.uix.list import (
#     TwoLineIconListItem,
#     IconLeftWidget,
#     ImageLeftWidgetWithoutTouch,
# )
# from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.list import MDList
from kivymd.uix.textfield import MDTextField
from kivymd.uix.appbar import MDActionBottomAppBarButton

from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import ScreenManager  # , Screen
from kivy.properties import (
    ObjectProperty,
    StringProperty,
    ListProperty,
    BooleanProperty,
)
import string
from random import choice, shuffle, randint
import json, os, time
from os.path import exists
import platform
import plyer
import pwd_manager_utils

Window.size = 414, 736


class ListItems(RecycleDataViewBehavior, MDBoxLayout):
    id = StringProperty()
    icon = StringProperty()
    text = StringProperty()
    callback = ObjectProperty(lambda x: x)

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    deselect = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ListItems, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(ListItems, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        # if super().on_touch_down(touch):
        #     return True
        if self.collide_point(*touch.pos) and self.selectable and not self.selected:
            self.deselect = False
            Clock.schedule_once(self.callback)
            return self.parent.select_with_touch(self.index, touch)
        if self.collide_point(*touch.pos) and self.selectable and self.selected:
            self.deselect = True
            self.selected = False
            Clock.schedule_once(self.callback)
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        if self.deselect:
            self.deselect = True
            rv.data[index]["selected"] = False
        else:
            self.deselect = False
            self.selected = is_selected
            rv.data[index]["selected"] = is_selected


class SelectableRecycleGridLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    pass


class BottomAppBarButton(MDActionBottomAppBarButton):
    theme_icon_color = "Custom"
    icon_color = "#8A8D79"


class ListScreen(MDScreen, RecycleView):
    selected_entry = False

    def __init__(self, **kwargs):
        super(ListScreen, self).__init__(**kwargs)

    def tap_entry(self, *args):
        testu = "1"
        items = [data["selected"] for data in self.ids.entries_list.data]
        for u in self.ids.entries_list.data:
            print("entry", u, "-", u["text"])
        if True in items and not self.selected_entry and items.count(True) == 1:
            self.ids.bottom_appbar.action_items = [
                BottomAppBarButton(
                    icon="open-in-new",
                    on_release=lambda x: (
                        pwd_manager_utils.show_message(
                            f"Info about {x.text}",
                            f"username: Blablabloup\nPassword: DECRYPTING FUNCTION HERE",
                        )
                        if testu == "1"
                        else pwd_manager_utils.show_message(
                            "ERROR",
                            "The current user does not match the database",
                        )
                    ),
                ),
                BottomAppBarButton(icon="pencil"),
            ]
            self.selected_entry = True
            self.ids.fab_button.icon = "trash-can-outline"

        else:
            if len(list(set(items))) == 1 and not list(set(items))[0]:
                self.selected_entry = False
            if not self.selected_entry:
                self.ids.bottom_appbar.action_items = [""]
                self.ids.fab_button.icon = "plus"

    def add_entry(self):
        self.ids.entries_list.data.append(
            {
                "icon": "icon",
                "text": "item",
                "selected": False,
                "callback": self.tap_entry,
            }
        )
        self.ids.entries_list.data = sorted(
            self.ids.entries_list.data, key=lambda x: x["text"].casefold()
        )
        print("new list:", self.ids.entries_list.data)

    def on_enter(self):
        # def on_start(self):
        current_user = os.environ["pwdzmanuser"]
        print("Connected user:", current_user)
        print(pwd_manager_utils.hasher(current_user, ""))

        if exists(f'{pwd_manager_utils.hasher(current_user, "")}.json'):
            print("FILE EXISTS")
        else:
            print("FILE DOESN'T EXIST")

        async def generate_card():
            dico = {
                "Amazon": "gAAAAABm_oy-UpMRzvruCEZiAHp8J7SEzGL7FmiILS5IHvqzJfcYHDXTLu2wNPl85EMRcvkunlwXlVOsWpJiMGPE0DtXfrfTuA==",
                "Netflix": "gAAAAABm_o0Op_Wn8q2blNMdRrTt4AxM8jFdSuq1LZYvG1O49x1hxCq-pry_KNnnUQlQ9lP6cP3t1cf5ghDzxWsomX8bSUJoPA==",
            }

            for item in dico:
                await asynckivy.sleep(0)
                if exists(f"apps_icons/{item.casefold()}.png"):
                    icon = f"apps_icons/{item.casefold()}.png"
                else:
                    print(f"App icon doesn't exit for {item}, using default icon.")
                    icon = "pencil"
                self.ids.entries_list.data.append(
                    {
                        "icon": icon,
                        "text": item,
                        "selected": False,
                        "callback": self.tap_entry,
                    }
                )
                print("self.ids 0:", self.ids.entries_list.data)
            self.ids.entries_list.data = sorted(
                self.ids.entries_list.data, key=lambda x: x["text"].casefold()
            )

        self.tap_entry()
        Clock.schedule_once(lambda x: asynckivy.start(generate_card()))

    # def on_leave(self, *args):
    # print("self.ids 1:", self.ids.entries_list.data)
    # self.ids.entries_list.data = []
    # self.selected_entry = False
    # print("self.ids 2:", self.ids.entries_list.data)

    def logout(self):
        os.environ["pwdzmanuser"] = ""
        # print("current_user after logout:", os.environ.get("pwdzmanuser"))
        test = self.ids.entries_list
        print("current list:", test.data)
        print("self.selected_entry", self.selected_entry)
        self.ids.entries_list.data = []
        print("logout list:", self.ids.entries_list.data)
        self.selected_entry = False
        print("self.selected_entry", self.selected_entry)

        self.manager.current = "loginscreen"


class LoginScreen(MDScreen):
    username_input = ObjectProperty(None)
    password_input_login = ObjectProperty(None)
    username_input_reg = ObjectProperty(None)
    password_input_reg = ObjectProperty(None)
    password_input_confirm = ObjectProperty(None)

    # info_box = StringProperty("")
    info_box = Label(size_hint_y=1, text="asd")
    new_data = None
    file = None
    file_exists = None
    path = "log.json"
    input_color = 0, 0.2, 0, 0.5
    btn_color = 0.2, 0, 0, 0.2
    white = 1, 1, 1, 0.5

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        device_id = plyer.uniqueid.id
        salt = pwd_manager_utils.generate_salt().decode()
        hashed_id = pwd_manager_utils.hasher(device_id, salt)

        path = "config.ini"
        check_file = exists(path)
        if not check_file:
            pwd_manager_utils.create_ini(
                pwd_manager_utils.hasher("user_test", ""),
                salt,
                hashed_id,
            )
            print("CONFIG FILE created")
        else:
            print("CONFIG FILE already exists")
            pwd_manager_utils.load_config_info()

        pwd_manager_utils.add_user(
            pwd_manager_utils.hasher("user_test2", ""), "pwd", "device_ID", path
        )

    def on_leave(self, *args):
        self.username_input.text = ""
        self.password_input_login.text = ""
        self.username_input_reg.text = ""
        self.password_input_reg.text = ""
        self.password_input_confirm.text = ""

    def user_login(self):
        username_text = self.username_input.text
        current_user = pwd_manager_utils.hasher(username_text, "")
        password_text = self.password_input_login.text
        users = pwd_manager_utils.list_users(username_text, password_text)
        if current_user in users:
            print(f"{username_text} exists in DB")
            self.manager.current = "testscreen"
        else:
            pwd_manager_utils.show_message(
                "ERROR", "username does not exist or wrong password"
            )
            self.username_input.text = ""
            self.password_input_login.text = ""
        os.environ["pwdzmanuser"] = username_text
        os.environ["pwdzmanpwd"] = password_text
        current_user_env = os.environ["pwdzmanuser"]
        print("current_user:", current_user_env)
        print(f"{current_user_env}'s password:", os.environ["pwdzmanpwd"])

    def new_user(self):
        username_text = self.username_input_reg.text
        password_text = self.password_input_reg.text
        password_confirm_text = self.password_input_confirm.text

        if not pwd_manager_utils.check_input(username_text):
            pwd_manager_utils.show_message(
                "ERROR",
                "Invalid characters in the username 123490 Invalid characters\nin the username 123490 Invalid\ncharacters in \n the username 123490",
            )
        else:
            if len(password_text) >= 8:
                if not pwd_manager_utils.check_input(password_text):
                    pwd_manager_utils.show_message(
                        "ERROR", "Invalid characters in the password"
                    )
                elif password_text != password_confirm_text:
                    pwd_manager_utils.show_message("ERROR", "Passwords don't match")
            else:
                pwd_manager_utils.show_message(
                    "ERROR",
                    "Password must be at least 8 characters",
                )

    def save_profile(self):
        website_text = self.website_input.text
        email_text = self.email_input.text
        password_text = self.password_input_reg.text
        if email_text != "" and website_text != "" and password_text != "":
            self.new_data = {
                website_text: {"email": email_text, "password": password_text}
            }
            self.save_to_file()

    def create_file(self):
        self.file = open(self.path, "x")

    def load_file(self):
        self.file_exists = exists(self.path)
        if not self.file_exists:
            self.create_file()

    def save_to_file(self):
        self.load_file()
        self.file = open(self.path, "r")
        try:
            data = json.load(self.file)
        except json.decoder.JSONDecodeError:
            self.file = open(self.path, "w")
            json.dump(self.new_data, self.file, indent=4)
        else:
            self.file = open(self.path, "w")
            data.update(self.new_data)
            json.dump(data, self.file, indent=4)
        finally:
            self.file.close()

    def load_profile(self):
        self.load_file()
        keyword = self.website_input.text
        if keyword != "":
            self.file = open(self.path, "r")
            try:
                data = json.load(self.file)
            except json.decoder.JSONDecodeError:
                exit()
            else:
                if keyword in data:
                    self.email_input.text = data[keyword]["email"]
                    self.password_input.text = data[keyword]["password"]
                else:
                    print("keyword is not in the log")


class PassManagerApp(MDApp):
    screenmanager = ScreenManager()

    def build(self):
        # self.theme_cls.theme_style = "Dark"
        # self.theme_cls.primary_palette = "Orange"
        # screenmanager = ScreenManager()
        self.screenmanager.add_widget(LoginScreen(name="loginscreen"))
        self.screenmanager.add_widget(ListScreen(name="testscreen"))
        return self.screenmanager

    def restart(self):
        self.screenmanager.clear_widgets()
        self.stop()
        return PassManagerApp().run()


# if __name__ == "__main__":
PassManagerApp().run()
