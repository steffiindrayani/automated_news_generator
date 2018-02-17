# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 20:02:53 2018

@author: Steffi Indrayani
"""

from input_handler import dataRetrieval

def contentDetermination(query):
    #Retrieve data based on query
    contents = dataRetrieval(query)
    return contents

