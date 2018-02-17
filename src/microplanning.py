# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:04:27 2018

@author: Steffi Indrayani
"""

from input_handler import templateRetrieval

def lexicalisation(contents):
    for data in contents:
        print("data: ", data)
        template = templateRetrieval(data)
        print("template: ", template)
        sentence = template.replace("{{entity}}", data['entity'])
        sentence = sentence.replace("{{location}}", data['location'])
        sentence = sentence.replace("{{location_type}}", data['location_type'])
        sentence = sentence.replace("{{value}}", str(data['value']))
        sentence = sentence.replace("{{event}}", data['event'])
        print("sentence: ", sentence)
        print(" ")