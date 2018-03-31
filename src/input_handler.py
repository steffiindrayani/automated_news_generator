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
    if calon != "":
        query += " AND (entity='%s' OR entity ='pemilih')" % (calon)
    

    query += " AND (location='%s'" % (loc)
    query += " OR location IN (SELECT location FROM location WHERE super_location='%s'))" % (loc)
    
    query += " ORDER BY location, value desc"
    return query, request
    
def readJsonFile(filename):
    data = json.load(open(filename))
    return data

def templateRetrieval(query):
    db, cursor = connectDB(dbname)
    template = ""
    couple = 0
    id_template = 0
    try:
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            id_template = row[0]
            template = row[1]
            if row[2] is None:
                couple = 0
            else:
                couple = row[2]
        templateUpdateNumberofSelection(id_template)
    except:
        print("Error: unable to fetch data")
    db.close()
    return id_template, template, couple
    
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

    

