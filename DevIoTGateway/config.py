__author__ = 'tingxxu'

import json
import os


class ConfigDict(dict):

    def __init__(self, *args):
        dict.__init__(self, args)

    def get_info(self, key, default_value):
        if key in self:
            info = self[key]
            return info
        return default_value

    def get_string(self, key, default_value):
        if key in self:
            info = self[key]
            if info:
                return info
        return default_value

    def get_int(self, key, default_value):
        if key in self:
            info = self[key]
            try:
                return int(info)
            except:
                return default_value
            return default_value

config = ConfigDict()

current_folder = os.getcwd()

PATH = current_folder + "/setting.cfg"

if os.path.isfile(PATH) and os.access(PATH, os.R_OK):

    __config_file__ = open("setting.cfg", 'r')
    __content__ = []

    __line__ = __config_file__.readline()
    while __line__:
        start_comment = __line__.find("#")
        if start_comment >= 0:
            raw_content = __line__[0:start_comment]
        else:
            raw_content = __line__
        __content__.append(raw_content)
        __line__ = __config_file__.readline()
    __all_content__ = ''.join([str(x) for x in __content__])
    try:
        json_dic = json.loads(__all_content__)
        for item in json_dic:
            config[item] = json_dic[item]

    except:
        print("the content of setting should be json format, please check it(remove the comments)"
              " in here:https://jsonformatter.curiousconcept.com/")

    __config_file__.close()



