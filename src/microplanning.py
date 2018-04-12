# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:04:27 2018

@author: Steffi Indrayani
"""

from input_handler import templateRetrieval, aggregationTemplateRetrieval

def microplanning(documentPlan, request):
    print("lexicalising...")
    lexicalisation(documentPlan, request)
    print(documentPlan)
 #   print("aggregating...")
    #aggregation(documentPlan)
#    print("assigning REG..")
#    assignREG(documentPlan)
    return documentPlan
    
# def lexicalisation(documentPlan, request):
#     for contents in documentPlan:
#         couple = 0
#         for data in contents:
#             id_template, template, couple = getTemplate(data, request["lokasi"], couple)
#             data["id_template"] = id_template
#             data["template"] = template

def lexicalisation(documentPlan, request):
    for contents in documentPlan:
        couple = 0
        existingTemplates = []
        for data in contents:
            id_template, template, couple = searchExistingTemplate(data, existingTemplates, couple)
            if id_template != 0:
                data["id_template"] = id_template
                data["template"] = template
            else:
                template,couple = getTemplate(data, request["lokasi"], couple)
                data["id_template"] = template["id"]
                data["template"] = template["template"]
                template["prevlocation_type"] = data["location_type"]
                existingTemplates.append(template)

                
def assignREG(documentPlan):
    for contents in documentPlan:
        for i in range (0, len(contents) - 1):
            if (contents[i]["entity"] == contents[i+1]["entity"]):
                contents[i+1]["REG"] = "True"

# def aggregation(documentPlan):
#     for contents in documentPlan:
#         for i in range (0, len(contents) - 1):
#             if contents[i]["id_template"] != 0:
#                 idtemp, template = getAggregationTemplate(contents[i],contents[i+1])
#                 if template != "":
#                     contents[i]["id_template"] = idtemp
#                     contents[i]["template"] = template
#                     contents[i+1]["id_template"] = 0
#                     contents[i+1]["template"] = ""
                
# def getTemplate(data, lokasi, id_couple):
#     entity_type = data['entity_type'].lower()
#     value_type = data['value_type'].lower()
#     location = data['location'].lower()
#     template = ""
#     query = "SELECT id,template, couple FROM template WHERE entity_type='%s' AND value_type='%s'" % (entity_type, value_type)
    
#     if location == lokasi:
#         query += " AND (location = 'lokasi' OR location IS NULL)"
#     else:
#         query += " AND location IS NULL"

#     if "rank" in data:
#         rank = data['rank']
#         if rank > 1:
#             query += " AND (rank = '%d' OR rank IS NULL OR rank = '2-last')" % (rank)
#         else:
#             query += " AND (rank = '%d' OR rank IS NULL)" % (rank)
    
#     if id_couple != 0:
#         query1 = query + " AND id = %d" % (id_couple)
#         id_template, template, _ = templateRetrieval(query1)
#         couple = 0
    
#     query += " ORDER BY number_of_selection LIMIT 1"
#     if template == "":
#         id_template, template, couple = templateRetrieval(query)
   
#     return id_template, template, couple

def getTemplate(data, lokasi, id_couple):
    entity_type = data['entity_type'].lower()
    value_type = data['value_type'].lower()
    location = data['location'].lower()
    template = ""
    query = "SELECT id,template, entity_type, value_type, couple, location, rank FROM template WHERE entity_type='%s' AND value_type='%s'" % (entity_type, value_type)
    
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
        template = templateRetrieval(query1)
        couple = 0
    
    query += " ORDER BY number_of_selection LIMIT 1"
    if not template:
        template = templateRetrieval(query)
        couple = template["couple"]
    return template, couple

def searchExistingTemplate(data, existingTemplates, couple):
    for template in existingTemplates:
        if template["value_type"] == data["value_type"].lower() and template["entity_type"] == data["entity_type"].lower() and template["prevlocation_type"] == data["location_type"] and ("rank" not in data or template["rank"] is None or template["rank"] == data["rank"] or (template["rank"] == "2-last" and data["rank"] != 1)):
            return template["id"], template["template"], template["couple"]
    return 0, "", couple
   
def getAggregationTemplate(data1, data2):
    id1 = data1["id_template"]
    id2 = data2["id_template"]
    query = "SELECT value_type1, template FROM aggregation_template WHERE (id1 = %d AND id2 = %d) OR (id1 = %d AND id2 = %d)" % (id1, id2, id2, id1)
    value_type, template = aggregationTemplateRetrieval(query)
    if value_type == data1["value_type"].lower():
        template = template.replace("{{value1}}", "{{value}}")
    else:
        template = template.replace("{{value2}}", "{{value}}")
    return str(id1) + ", " + str(id2), template