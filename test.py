#!/usr/bin/python3

dictionary1 = {"product": "Nokia", "colors": "Red", "price": "10 000 TND"}
dictionary2 = {"product": "Samsung", "colors": "yellow", "year": 2022, "Tax": "10%"}
"""
def MergeDictionary(Dict1, Dict2):
    Dict3 = {**Dict1, **Dict2}
    for key, value in Dict3.items():
         if key in Dict1 and key in Dict2:
             Dict3[key] = [value, Dict2[key]]
    return Dict3
"""


def merge_two_dicts(dictionary1, dictionary2):
    if isinstance(dictionary1, list) and isinstance(dictionary2,list):
        return dictionary1 + dictionary2
    elif isinstance(dictionary1, dict) and isinstance(dictionary2, dict):
        return dict(list(dictionary1.items()) + list(dictionary2.items()))
    return False



Dict3 =  merge_two_dicts(dictionary1, dictionary2)
print(Dict3)
