# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:42:21 2018

@author: Steffi Indrayani
"""

from document_planning import documentPlanning
from microplanning import microplanning
from input_handler import readQuery
from realisation import realisation
from datetime import datetime
#from microplanning import lexicalisation

query, request = readQuery()
documentPlan = documentPlanning(query, request)
textSpecification = microplanning(documentPlan, request)
article = realisation(textSpecification)

city = "Bandung"
time = datetime.now().strftime('%Y-%m-%d,%H:%M:%S')

filename = "../results/article.txt" 

f = open(filename,'w')
f.write(time)
f.write("\n\n")
f.write(city + " - " + article)
f.close()