#!/usr/bin/env python2
import json

f = open('county.json')
county = json.load(f)
f.close()
del(f)

# county['objects']['president']
