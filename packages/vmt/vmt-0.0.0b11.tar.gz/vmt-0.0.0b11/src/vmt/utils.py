#!/usr/bin/env python3
import re
from os.path import join as os_join


def auto_title(dir_name, user_system):
    """
    Generate a title from dir_name
    e.g. /path/to/[Group] Show Season 01 (1080p) [Hash info]
    returns ' - path - to - Show Season 01 (1080p)'
    """

    title = re.sub(r"\s?\[[^]]*\]\s?", "", dir_name)
    if user_system == "Windows":
        title = re.sub("\\\\", " - ", title)
    else:
        title = re.sub(r"/", " - ", title)

    return title


def key_value_list(dic, search_key=None):
    """
    Take a dicionary and return two lists one for keys and one for values
    """
    # While it is easiest if dic is a true dict
    # it need not be. As long as the items in dic
    # _are_ true dicts then we can make do
    def psuedo_dic():
        for item in dic:
            if isinstance(item, dict):
                true_dic(item)

    def true_dic(d=dic):
        if search_key is None:
            keys.extend(d.keys())
            values.extend(d.values())
        else:
            for key, value in d.items():
                if key == search_key:
                    keys.append(key)
                    values.append(value)

    keys = []
    values = []
    if isinstance(dic, dict):
        true_dic()
    else:
        psuedo_dic()

    return keys, values


def join(a, b):
    return os_join(a, b)


def merge_libraries(old_dict, new_dict, interactive=False):
    """Takes two dictionaries and merges them"""
    merged_dict = {}
    # pop_key = None
    for new_key in new_dict:
        match = True if new_key in old_dict else False
        if not match:
            merged_dict[new_key] = new_dict[new_key]
            continue
        else:
            merged_dict[new_key] = old_dict[new_key]
            merged_dict[new_key]["episodes"] = new_dict[new_key]["episodes"]
            old_dict.pop(new_key, None)
    return merged_dict
