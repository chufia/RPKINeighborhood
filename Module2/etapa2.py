#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 16:20:09 2017

@author: jexus
"""

import json
import radix
import csv
from netaddr import IPSet

rt_prefixes = radix.Radix()
output=[] #lista de diccionarios


#load the roas list
with open('roas_export.csv', 'rb') as csvfile:
    aslines = csv.reader(csvfile, delimiter=',')
    for row in aslines:
        #we just load the prefixes variable into the radix tree
        rt_prefixes.add(row[1])


#load the json exported from module 1
with open("module_out.json", "r") as f:
    listas = json.load(f)


#we run the loop for EACH AS
for origin_as_data in listas:
    denom = 0.0
    coverage = 0.0
    
    bgp_prefixes_comp = IPSet(origin_as_data["prefixes"]) 
    
    for prefix in bgp_prefixes_comp.iter_cidrs():
        prefix_str = str(prefix)
        
        covering_prefixes = rt_prefixes.search_covering(prefix_str)
        if len(covering_prefixes) > 0:
            #if covering_prefixes > 0 then everything is covered and the fraction
            #is 1/1 then we add all the ips both to the denom and the num
            coverage += pow(2,32-prefix.prefixlen)
            denom += pow(2,32-prefix.prefixlen)
            continue
        covered_prefixes  = rt_prefixes.search_covered(prefix_str)
        if len(covered_prefixes) == 0:
            #if covered_prefixes == 0 then no ip is covered 
            #then the fraction to add is 0/1 and we only add to the denom
            coverage += 0
            denom += pow(2,32-prefix.prefixlen)
        else:
            #otherwise the num is neither 0 nor 1 so we must calculate
            covered_prefixes_str = []
            
            #here we compact the nodes so as to avoid overlapping adresses
            for node in covered_prefixes:
                covered_prefixes_str.append(node.prefix)
            covered_prefixes_comp = IPSet(covered_prefixes_str) 
            
            #now we calculate the coverage for every prefix and accumulate
            for covered in covered_prefixes_comp.iter_cidrs():
                coverage+=pow((2),-(covered.prefixlen-prefix.prefixlen))*pow(2,32-prefix.prefixlen)
                denom += pow(2,32-prefix.prefixlen)
    #here we write coverage as a percentage for the json file
    coverage = 100*(coverage/denom)        
    
       
    output.append({ # here we create the json dictionary
        'id':origin_as_data["Origin-AS"],
        'rpki':coverage
        })
with open("module_salida.json", "w") as f: #here we dump the file
    json.dump(output,f)