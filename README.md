Quinoa index
===========================

The Quinoa index combines strange properties of municipalities in order to find peculiar municipalities.

## Running the Yoga script
Start selenium.

    java -jar bin/selenium-server-standalone-2.21.0.jar

Run the downloader script.

    yoga/oh_just_use_selenium.py

This results in a `yoga/yoga.sqlite`. Copy this to `/tmp/yoga.sqlite`, then
parse the raw html downloads with

    parse_locations.py

Results will be in `/tmp/yoga.sqlite`; move that wherever you want to keep it.

## American FactFinder
I downloaded that stuff from [here](http://factfinder2.census.gov/faces/tableservices/jsf/pages/productview.xhtml?pid=DEC_10_SF1_GCTP2.ST09&prodType=table).

## More ideas

* [Ikaria](http://www.nytimes.com/2012/10/28/magazine/the-island-where-people-forget-to-die.html)