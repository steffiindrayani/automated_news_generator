# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 19:59:51 2018

@author: Steffi Indrayani
"""

import MySQLdb

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
            print(data)
    except:
        print("Error: unable to fetch data")
    db.close()
    return contents
    
def templateRetrieval(data):
    entity_type = data['entity_type'].lower()
    value_type = data['value_type'].lower()
    query = """SELECT id,template FROM template WHERE entity_type='%s' AND value_type='%s' ORDER BY number_of_selection LIMIT 1""" % (entity_type, value_type)
    db, cursor = connectDB(dbname)
    sentence = ""
    try:
        cursor.execute(query)
        results = cursor.fetchall()        
        for row in results:
            id_template = row[0]
            sentence = row[1]
        templateUpdateNumberofSelection(id_template)
    except:
        print("Error: unable to fetch data")
    db.close()
    return sentence
    
def templateUpdateNumberofSelection(idtemp):
    db, cursor = connectDB(dbname)
    query = "UPDATE template SET number_of_selection = number_of_selection + 1 WHERE id = '%d'" % (idtemp)
    try:
        cursor.execute(query)
        db.commit()
    except:
        db.rollback()
    db.close()    

def readQuery():
    print("Pembangkit Berita Pemilihan Kepala Daerah di Indonesia")
    tahun = input("Tahun: ")
    tingkat = input("Tingkat (Walikota/Bupati/Gubernur/Presiden): ")
    daerah = input("Nama Daerah: ")
    calon = input("Pasangan Calon: ")
    lokasi = input("Lokasi Pencoblosan: ")
    
    event = "Pemilihan " + tingkat + " " + daerah + " " + tahun
    query = "SELECT * FROM input_data WHERE event = '%s'" % (event)
    if calon != "":
        query += " AND entity='%s'" % (calon)
    if lokasi != "":
        query += " AND location='%s'" % (lokasi)
    return query