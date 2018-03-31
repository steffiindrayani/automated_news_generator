# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:42:21 2018

@author: Steffi Indrayani
"""

from document_planning import documentPlanning
from microplanning import microplanning
from input_handler import readQuery
#from microplanning import lexicalisation

query, request = readQuery()
documentPlan = documentPlanning(query, request)
microplanning(documentPlan, request)


#lexicalisation(contents)