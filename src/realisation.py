# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:47:32 2018

@author: User
"""

import re
import locale

def realisation(textSpecification):
    print("linguistic realisation...")
    linguisticRealisation(textSpecification)
    print("structure realisation...")
    structureRealisation(textSpecification)

    
def linguisticRealisation(textSpecification):
    for contents in textSpecification:
        for i in range (0, len(contents)):
            #generation
            sentence = re.sub(' +',' ', contents[i]["template"])
            sentence = sentence.replace("{{location_type}}", contents[i]['location_type'].title())
            sentence = sentence.replace("{{location}}", contents[i]['location'].title())
            sentence = sentence.replace("{{event}}", contents[i]['event'].title())
            
            if "rank" in contents[i]:
                sentence = sentence.replace("{{rank}}", "ke-" + str(contents[i]['rank']))
            
            if i + 1 < len(contents):            
                sentence = sentence.replace("{{value1}}", generateValue(contents[i+1]['value']))
                sentence = sentence.replace("{{value2}}", generateValue(contents[i+1]['value']))
            sentence = sentence.replace("{{value}}", generateValue(contents[i]['value']))
                        
            #validation
            if sentence != "" and sentence.endswith(".") == False:
                sentence += '.'
            contents[i]['sentence'] = sentence

def structureRealisation(textSpecification):
    article = ""
    for contents in textSpecification:
        for content in contents:
            article += content["sentence"]
        article += "\n\n"
    print(article)
                
def generateValue(value):    
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    if isinstance(value, float):
        value = locale.format("%.*f", (2, value), True)
    elif value.isnumeric():
        value = int(value)
        value = locale.format("%.*f", (0, value), True)
    return str(value)
            
