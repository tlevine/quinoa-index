#!/usr/bin/env python2
import json

# Load the two tables
county_shapes = json.load(open('county-shapes.json'))
county_results = json.load(open('county-results.json'))

# Which keys are missing from one of the tables?
shape_ids = set([o['pr']['f'] for o in county_shapes['objects']])
result_ids = set(county_results['objects']['president'].keys())
missing = shape_ids.symmetric_difference(result_ids)

print('Data are missing for these counties, so I am skipping them.')
print(', '.join(missing))

for o in county_shapes['objects']:
    shape_id = o['pr']['f']

    # Skipp the missing ones.
    if shape_id in missing:
        continue

    o['results'] = county_results['objects']['president'][shape_id]

json.dump(county_shapes['objects'], open('county.json', 'w'))
