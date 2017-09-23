#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 16:07:00 2017

@author: sofia
"""
import json

mod1_out_file = './Module1/sample_output.json'
mod2_out_file = './Module2/sample_output.json'

with open(mod1_out_file, 'r') as f:
     mod1_out = json.load(f)

with open(mod2_out_file, 'r') as f:
     mod2_out = json.load(f)


links = []

for orASdata in mod1_out:
    curr_asn = orASdata['Origin-AS']
    for neighbor in orASdata['Neighbours']:
        links.append({"source" : curr_asn, "target" : neighbor, "value" : 1})

output = {"nodes" : mod2_out, "links" : links}

with open('./neighborhood.json', 'w') as f:
    json.dump(output, f)  