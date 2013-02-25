#!/bin/sh

[ -e county-results.json ] || wget -O county-results.json 'http://apps.washingtonpost.com/data/politics/elections/api/v1/results/winners/?format=json&office_name_slug=president&reporting_unit_type=county&polling_date=2012-11-06'

[ -e county-shapes.json ] || wget -O county-shapes.json 'http://www.washingtonpost.com/wp-srv/special/politics/election-map-2012/data/counties.json'
