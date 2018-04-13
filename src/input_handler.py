# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:59:51 2018

@author: Steffi Indrayani
"""

import MySQLdb
import json

dbname = "automated_news_generator"


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
    print("Pembangkit Berita Pemilihan Kepala Daerah di Indonesia")
    tahun = input("Tahun: ")
    fokus = input("Fokus (Pemilih/Partai/Pasangan Calon): ")
    tingkat = input("Tingkat (Walikota/Bupati/Gubernur/Presiden): ")
    daerah = input("Nama Daerah: ")
    calon = input("Pasangan Calon: ")
    lokasi = input("Lokasi Pencoblosan: ")
    value_type = input("Informasi: ")
    event = "Pemilihan " + tingkat + " " + daerah + " " + tahun

    request = dict()
    loc = ""
    if lokasi != "":
        loc = lokasi
    else:
        loc = daerah
    request["loc"] = loc
    request["event"] = event
    request["fokus"] = fokus
    request["daerah"] = daerah
    request["calon"] = calon
    request["lokasi"] = lokasi
    request["value_type"] = value_type

    query = "SELECT * FROM input_data WHERE event = '%s'" % (event)
    if fokus != "":
        if fokus == "Pasangan Calon":
            query += " AND (entity_type='pemilih' OR entity_type='%s')" % (fokus)
        else:
            query += " AND entity_type='%s'" % (fokus)
        
    if calon != "":
        query += " AND (entity='%s' OR entity_type ='pemilih')" % (calon)        

    query += " AND (location='%s'" % (loc)
    query += " OR location IN (SELECT location FROM location WHERE super_location='%s'))" % (loc)
    
    query += " ORDER BY location, value desc"
    return query, request
    
def readJsonFile(filename):
    data = json.load(open(filename))
    return data

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

