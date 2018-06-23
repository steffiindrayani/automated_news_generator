# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:59:51 2018

@author: Steffi Indrayani
"""

import MySQLdb
import json

dbname = "automated_news_generator"
queryfile = "../data/query"


def connectDB(dbName):
    host = "localhost"
    username = "root"
    password = "1234"
    db = MySQLdb.connect(host, username, password, dbName)
    cursor = db.cursor()
    return db, cursor
    
def dataRetrieval(query):
    db, cursor = connectDB(dbname)
    contents = []
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            data = dict()
            data['entity_type'] = row[0]
            data['entity'] = row[1]
            data['location_type'] = row[2]
            data['location'] = row[3]
            data['value_type'] = row[4]
            data['value'] = row[5]
            data['event_type'] = row[6]
            data['event'] = row[7]
            contents.append(data)
    except:
        print("Error: unable to fetch data")
    db.close()
    return contents
    
def readQuery():
    event = ""
    entity = ""
    entity_type = ""
    location = ""
    userquery = readTextFile(queryfile)
    userquery = compile(userquery, 'sumstring', 'exec')
    q = locals()
    exec(userquery)
    request = dict()
    q["value_type"] = [x.strip() for x in q["value_type"].split(',')]
    request["event"] = q["event"]
    request["entity_type"] = q["entity_type"]
    request["entity"] = q["entity"]
    request["location"] = q["location"]
    request["value_type"] = q["value_type"]

    query = "SELECT * FROM input_data WHERE ("
    for i in range(0, len(q["value_type"])):
        if i != 0:
            query += " OR"
        query += " value_type = '%s'" % (q["value_type"][i]) 
    query += ")"
    if q["entity_type"] != "":
        if q["entity_type"] == "Pasangan Calon":
            query += " AND (entity_type='pemilih' OR entity_type='%s')" % (q["entity_type"])
            if q["entity"] != "":
                query += " AND (entity='%s' OR entity_type ='pemilih')" % (q["entity"])     
        else:
            query += " AND entity_type='%s'" % (q["entity_type"])
            if q["entity"] != "":
                query += " AND (entity='%s')" % (q["entity"])     
    if q["location"] != "":  
        query += " AND (location='%s'" % (q["location"])
        query += " OR location IN (SELECT location FROM location WHERE super_location='%s'))" % (q["location"])
    
    if q["event"] != "":
        query += " AND event='%s'" % (q["event"])

    query += " ORDER BY location, value desc"
    print(query)
    return query, request
    
def readJsonFile(filename):
    data = json.load(open(filename))
    return data

def readTextFile(filename):
    with open(filename) as f:
        contents = f.read()
    return contents

def templateRetrieval(query):
    db, cursor = connectDB(dbname)
    template = dict()
    try:
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            template["id"] = row[0]
            template["template"] = row[1]
            template["entity_type"] = row[2]
            template["value_type"] = row[3]
            if row[4] is None:
                template["couple"] = 0
            else:
                template["couple"] = row[4]
            template["location"] = row[5]
            template["rank"] = row[6]
        templateUpdateNumberofSelection(template["id"])
    except:
        print("")
    db.close()
    return template
    
def templateUpdateNumberofSelection(idtemp):
    db, cursor = connectDB(dbname)
    query = "UPDATE template SET number_of_selection = number_of_selection + 1 WHERE id = '%d'" % (idtemp)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()    

def aggregationTemplateRetrieval(query):
    db, cursor = connectDB(dbname)
    template = ""
    value_type1 = ""
    try:
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            value_type1 = row[0]
            template = row[1]
    except:
        print("Error: unable to fetch data")
    db.close()
    return value_type1, template

def entityFactRetrieval(query):
    db, cursor = connectDB(dbname)
    entity_type = ""
    value_type = ""
    value = ""
    try:
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            idfact = row[0]
            entity_type = row[1]
            value_type = row[2]
            value = row[3]
        factUpdateNumberofSelection(idfact)
    except:
        return ""
    db.close()
    if value_type == "Alias":
        return value
    return entity_type + " dengan " + value_type + " " + value   
    
def factUpdateNumberofSelection(idfact):
    db, cursor = connectDB(dbname)
    query = "UPDATE entity_fact SET number_of_selection = number_of_selection + 1 WHERE id = '%d'" % (idfact)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()    

