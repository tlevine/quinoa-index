#!/bin/sh

[ -e county.json ] || wget -O county.json 'http://apps.washingtonpost.com/data/politics/elections/api/v1/results/winners/?format=json&office_name_slug=president&reporting_unit_type=county&polling_date=2012-11-06'
