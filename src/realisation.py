# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 16:47:32 2018

@author: User
"""

import re
import locale
from input_handler import entityFactRetrieval

def realisation(textSpecification):
    print("linguistic realisation...")
    linguisticRealisation(textSpecification)
    print("structure realisation...")
    article = structureRealisation(textSpecification)
    return article
    
def linguisticRealisation(textSpecification):
    for contents in textSpecification:
        for i in range (0, len(contents)):
            if (contents[i]["id_template"] != 0):
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

                if "REG" in contents[i]:
                    r1 = re.compile(re.escape("pasangan"), re.IGNORECASE)
                    r2 = re.compile(re.escape("calon"), re.IGNORECASE)
                    sentence = r1.sub("", sentence)
                    sentence = r2.sub("", sentence)
                    sentence = sentence.replace("{{entity}}", generateRE(contents[i]["entity_type"], contents[i]["entity"]))
                else:
                    sentence = sentence.replace("{{entity}}", contents[i]['entity'].title())        
                #validation
                if sentence.endswith(".") == False and "aggregated" not in contents[i]:
                    sentence += '.'
                contents[i]['sentence'] = sentence

                

def structureRealisation(textSpecification):
    article = ""
    for contents in textSpecification:
        for content in contents:
            if "sentence" in content:
                article += content["sentence"] + " "
        article += "\n\n"
    return article
                
def generateValue(value):    
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    if isinstance(value, float):
        value = locale.format("%.*f", (2, value), True)
    elif value.isnumeric():
        value = int(value)
        value = locale.format("%.*f", (0, value), True)
    return str(value)
    
def generateRE(entity_type, entity):
    query = "SELECT id, entity_type, value_type, value FROM entity_fact WHERE entity = %s ORDER BY number_of_selection DESC LIMIT 1" % (entity)
    re = entityFactRetrieval(query)
    if re == "":
        return entity_type + " tersebut"
    else:
        return re
            
