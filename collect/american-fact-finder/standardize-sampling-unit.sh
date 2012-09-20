#!/bin/sh

# Remove rows that aren't at the zip code level.
sed -n -e 2p -e /ZCTA/p DEC_10_SF1_GCTP2.ST09.csv | wc -l
