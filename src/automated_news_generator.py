# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 15:42:21 2018

@author: Steffi Indrayani
"""

from document_planning import contentDetermination
from input_handler import readQuery
from microplanning import lexicalisation

query = readQuery()
contents = contentDetermination(query)
lexicalisation(contents)