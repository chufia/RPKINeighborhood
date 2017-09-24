#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 16:20:09 2017

@author: jexus
"""

import json
import sys
import radix
import csv
from netaddr import IPSet

rt_prefijos = radix.Radix()

with open('roas_export.csv', 'rb') as csvfile:
    aslines = csv.reader(csvfile, delimiter=',')
    for row in aslines:
        rt_prefijos.add(row[1])



with open("module_out.json", "r") as f: #genera el archivo de salida .json
    listas = json.load(f)
    
for origin_as_data in listas:
    denom = 0.0
    coverage = 0.0
    for prefix in origin_as_data["prefixes"]:
        bgp_pref_len= int(prefix.split("/")[1])
        #TODO IMPLEMENTAR
        covering_prefixes = rt_prefijos.search_covering(prefix)
        if len(covering_prefixes) > 0:
            coverage += pow(2,32-bgp_pref_len)
            denom += pow(2,32-bgp_pref_len)
            continue
        covered_prefixes  = rt_prefijos.search_covered(prefix)
        if len(covered_prefixes) == 0:
            coverage += 0
        else:
            covered_prefixes_str = []
            for node in covered_prefixes:
                covered_prefixes_str.append(node.prefix)
            covered_prefixes_comp = IPSet(covered_prefixes_str) 
            #coverage=0
            for covered in covered_prefixes_comp.iter_cidrs():
                coverage+=pow((2),-(covered.prefixlen-bgp_pref_len))*pow(2,32-bgp_pref_len)
                denom += pow(2,32-bgp_pref_len)
    coverage = coverage/denom        
    print coverage*100
#with open("module_out.json", "w") as f: #genera el archivo de salida .json
   # json.dump(listas,f)