# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:04:27 2018

@author: Steffi Indrayani
"""

from input_handler import templateRetrieval

def microplanning(documentPlan, request):
    print("lexicalising...")
    lexicalisation(documentPlan, request)
    print(documentPlan)
    
def lexicalisation(documentPlan, request):
    for contents in documentPlan:
        couple = 0
        for data in contents:
            id_template, template, couple = getTemplate(data, request["lokasi"], couple)
            data["id_template"] = id_template
            data["template"] = template

#        sentence = template.replace("{{entity}}", data['entity'])
#        sentence = sentence.replace("{{location}}", data['location'])
#        sentence = sentence.replace("{{location_type}}", data['location_type'])
#        sentence = sentence.replace("{{value}}", str(data['value']))
#        sentence = sentence.replace("{{event}}", data['event'])
#        print("sentence: ", sentence)
#        print(" ")

def getTemplate(data, lokasi, id_couple):
    entity_type = data['entity_type'].lower()
    value_type = data['value_type'].lower()
    location = data['location'].lower()
    template = ""
    query = "SELECT id,template, couple FROM template WHERE entity_type='%s' AND value_type='%s'" % (entity_type, value_type)
    
    if location == lokasi:
        query += " AND (location = 'lokasi' OR location IS NULL)"
    else:
        query += " AND location IS NULL"

    if "rank" in data:
        rank = data['rank']
        if rank > 1:
            query += " AND (rank = '%d' OR rank IS NULL OR rank = '2-last')" % (rank)
        else:
            query += " AND (rank = '%d' OR rank IS NULL)" % (rank)
    
    if id_couple != 0:
        query1 = query + " AND id = %d" % (id_couple)
        id_template, template, _ = templateRetrieval(query1)
        couple = 0
    
    query += " ORDER BY number_of_selection LIMIT 1"
    if template == "":
        id_template, template, couple = templateRetrieval(query)
   
    return id_template, template, couple
    