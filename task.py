#!/usr/bin/python3

Dict1 ={"Product Name": "Samsung", "color": "Red"}
Dict2 ={"Product Name": "Nokia", "Year": 2022, "color": "white", "car": "BMW"}

def MergeDictionary(Dict1, Dict2):
    Dict3 = {**Dict1, **Dict2}
    for key, value in Dict3.items():
        if key in Dict1 and key in Dict2:
            Dict3[key]= [value, Dict1[key]]
    return Dict3

Dict3 = MergeDictionary(Dict1, Dict2)

print(Dict3)
