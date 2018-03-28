# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:02:53 2018

@author: Steffi Indrayani
"""

from input_handler import dataRetrieval, getSummarizationRule
import re 

def contentDetermination(query,request):
    #Retrieve data based on query
    contents = dataRetrieval(query)
    derivedContents = generateDerivedContents(request)
    contents.extend(derivedContents)
    print(contents)
    
def generateDerivedContents(request):
    rules = getSummarizationRule()
    derivedContents = []
    for rule in rules:
        query = generateSummarizationQuery(rule,request)
        contents = dataRetrieval(query)
        for content in contents:
            content["value_type"] = rule["new_value_type"]
        derivedContents.extend(contents)
    return derivedContents

def generateSummarizationQuery(rule, request):
        #new_value_type = rule["new_value_type"]
        operation = re.split("([+-/*])", rule["operation"])
        operands = operation[0::2]
        operands = [x.lower() for x in operands if not x.isnumeric()]
        #generate query
        query = "SELECT table0.entity_type, table0.entity, table0.location_type, table0.location, table0.value_type, round(%s,2) as value, table0.event_type, table0.event FROM" % (rule["operation"].lower().replace(" ", ""))
        i = 0 
        for operand in operands:
            if i > 0:
                query += ","
            query += " (SELECT entity_type, entity, location_type, location, value_type, value as %s, event_type, event FROM input_data WHERE value_type = '%s') as %s" % (operands[i].replace(" ",""), operands[i], "table" + str(i))
            i += 1
        query += " WHERE"
        query += " (table0.location = '{}' OR table0.location IN (SELECT location FROM location WHERE super_location='{}'))".format(request["loc"], request["loc"])
        query += " AND table0.event = '%s'" % (request["event"])
        if (request["calon"] != ""):
            query += " AND (entity='%s' OR entity ='pemilih')" % (request["calon"])
        for idx in range(i):
            if idx > 0:
                query += " AND table" + str(idx - 1) + ".location = table" + str(idx) + ".location"
        query += " ORDER BY location, value desc"
        return query
            