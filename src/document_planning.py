# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:02:53 2018

@author: Steffi Indrayani
"""

from input_handler import dataRetrieval, readJsonFile
import re 
import collections
import operator
from collections import OrderedDict
from operator import itemgetter

summarizationConfig = "../data/summarizationconfigforpilkada"
value_type_groups = "../data/value_type_groups.json"


def documentPlanning(query, request):
    print("determining content...")
    contents = contentDetermination(query, request)
    print("structuring document...")
    documentPlan = documentStructuring(contents, request)
    # print(documentPlan)
    for contents in documentPlan:
        for content in contents:
            content["value"] = str(content["value"])
    return documentPlan

def contentDetermination(query,request):
    #Retrieve data based on query
    contents = dataRetrieval(query)
    # print("panjang konten", len(contents))
    derivedContents = generateDerivedContents(request)
    # print("panjang konten turunan", len(derivedContents))
    contents.extend(derivedContents)
    if request["entity"] == "":
        contents = dataRankSummarization(contents)
    # print("panjang konten total", len(contents))
    return contents
    
def documentStructuring(structuredContents, request):
    factOrderStructuring = ["entity_type", "location_type", "value_type_group", "location", "rank"]
    # factOrderStructuring = ["value_type", "value"]
    # factOrderStructuring = ["entity_type", "entity"]
    for fact in factOrderStructuring:
        structuredContents = ordering(structuredContents, request, fact)
    return structuredContents
    
def ordering(contents, request, fact):
    if fact == "entity_type":
        contents = orderContentByEntityType(contents,request["entity_type"])
    elif fact == "location_type":
        contents = orderContentByLocationType(contents)
    elif fact == "value_type_group":
        contents = orderContentByValueTypeGroup(contents) 
    elif fact == "value_type":
        contents = orderContentByValueType(contents) 
    elif fact == "location":
        contents = orderContentByLocation(contents)
    elif fact == "entity":
        contents = orderContentByEntity(contents)
    elif fact == "rank":
        contents = sortContentByRank(contents)
    return contents

def generateDerivedContents(request):
    rules = readJsonFile(summarizationConfig)
    derivedContents = []
    for rule in rules:
        if (rule["new_value_type"] in request["value_type"]):
            query = generateSummarizationQuery(rule,request)
            contents = dataRetrieval(query)
            for content in contents:
                content["value_type"] = rule["new_value_type"]
            derivedContents.extend(contents)
    return derivedContents
    
def dataRankSummarization(contents):
    value_types = ["Persentase Suara", "Jumlah Suara", "Total Kemenangan", "Jumlah Kemenangan Tingkat Gubernur", "Jumlah Kemenangan Tingkat Walikota", "Jumlah Kemenangan Tingkat Bupati"]
    for value_type in value_types:
        content = [item for item in contents if item["value_type"] == value_type]
        contents = [item for item in contents if item not in content]
        location = ""
        #content = sorted(content, key=itemgetter('location', 'value'), reverse=True)
        for item in content:
            if item["location"] != location:
                location = item["location"]
                rank = 1
            else:
                rank +=1
            item["rank"] = rank
        contents.extend(content)
    # value_types = ["Persentase Partisipasi Pemilih"]
    # for value_type in value_types:
    #     content = [item for item in contents if item["value_type"] == value_type]
    #     contents = [item for item in contents if item not in content]
    #     content = sorted(content, key=operator.itemgetter('location_type','value'), reverse=True)
    #     location_type = ""
    #     for item in content:
    #         if item["location_type"] != location_type:
    #             location_type = item["location_type"]
    #             rank = 1
    #         else:
    #             rank +=1
    #         item["rank"] = rank
    #     contents.extend(content)
    return contents
            
def generateSummarizationQuery(rule, request):
        #new_value_type = rule["new_value_type"]
        operation = re.split("([+-/*])", rule["operation"])
        operands = operation[0::2]
        operands = [x.lower() for x in operands if not x.isnumeric()]
        #generate query
        query = "SELECT table0.entity_type, table0.entity, table0.location_type, table0.location, table0.value_type, round(%s,0) as value, table0.event_type, table0.event FROM" % (rule["operation"].lower().replace(" ", ""))
        i = 0 
        for operand in operands:
            if i > 0:
                query += ","
            query += " (SELECT entity_type, entity, location_type, location, value_type, value as %s, event_type, event FROM input_data WHERE value_type = '%s') as %s" % (operands[i].replace(" ",""), operands[i], "table" + str(i))
            i += 1
        query += " WHERE"
        query += " (table0.location = '{}' OR table0.location IN (SELECT location FROM location WHERE super_location='{}'))".format(request["location"], request["location"])
        query += " AND table0.event = '%s'" % (request["event"])
        if (request["entity"] != ""):
            query += " AND (table0.entity='%s' OR table0.entity_type ='pemilih')" % (request["entity"])
        for idx in range(i):
            if idx > 0:
                query += " AND table" + str(idx - 1) + ".location = table" + str(idx) + ".location"
        query += " AND (table0.entity = table1.entity OR table1.entity_type = 'pemilih')"        
        query += " ORDER BY location, value desc"
        return query

def orderContentByEntityType(contents, focus):
    result = collections.defaultdict(list)
    for content in contents:
        result[content['entity_type']].append(content)
    if focus != "":
        result = OrderedDict(sorted(result.items(), key=lambda key:(key!='focus', key)))
    return result.values()
    
def orderContentByLocationType(contentsList):
    results = []
    for contents in contentsList:
        result = collections.defaultdict(list)        
        for content in contents:
            result[content['location_type']].append(content)
        location_type = ['Negara', 'Provinsi', 'Kabupaten', 'Kota', 'Kecamatan', 'Kelurahan', 'Kelurahan']
        index_map = {v: i for i, v in enumerate(location_type)}
        result = OrderedDict(sorted(result.items(), key=lambda pair: index_map[pair[0]]))
        results.extend(result.values())
    return results

def orderContentByValueType(contents):
    results = []
    result = collections.defaultdict(list)
    for content in contents:
        result[content['value_type']].append(content)
    value_type = ['Cuaca Pagi', 'Cuaca Siang', 'Cuaca Malam', 'Cuaca Dini Hari', 'Suhu', 'Kelembaban']
    index_map = {v: i for i, v in enumerate(value_type)}
    result = OrderedDict(sorted(result.items(), key=lambda pair: index_map[pair[0]]))
    results.extend(result.values())
    return results

def orderContentByValue(contents):
    results = []
    for contents in contentsList:
        contents = sorted(contents, key=itemgetter('value'))
        results.append(contents)
    return results
    
def orderContentByValueTypeGroup(contentsList):
    groups = readJsonFile(value_type_groups)
    results = []
    for contents in contentsList:
        result = collections.defaultdict(list)
        result1 = collections.defaultdict(list)
        for content in contents:
            result[content['value_type']].append(content)
        computed_key = []
        for key in result:
            if key not in computed_key:
                computed_key.append(key)
                result1[key].extend(result[key])
                value_types = [v for k, v in groups.items() if key in v]
                if len(value_types) > 0:
                    for t in value_types[0]:
                        if t not in computed_key and t in result:
                            result1[key].extend(result[t])
                            computed_key.append(t)
        results.extend(result1.values())
    return results
            
def orderContentByLocation(contentsList):
    results = []
    for contents in contentsList:
        #result = collections.defaultdict(list)        
        #for content in contents:
            #result[content['location']].append(content)
        #results.extend(result.values())
        contents = sorted(contents, key=itemgetter('location'))
        results.append(contents)
    return results

def orderContentByEntity(contentsList):
    results = []
    for contents in contentsList:
        result = collections.defaultdict(list)        
        for content in contents:
            result[content['entity']].append(content)
        results.extend(result.values())
    return results
        
def sortContentByRank(contentsList):
    results = []
    for contents in contentsList:
        if "rank" in contents[0]:
            contents = sorted(contents, key=operator.itemgetter('location','rank'))
        results.append(contents)
    return results
