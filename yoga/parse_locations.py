from dumptruck import DumpTruck
from lxml.html import fromstring

dt = DumpTruck('/tmp/somatic.sqlite') 

def parse(page_number):
    sql = 'select page_source from page_source where page_number = %d'
    page_source = dt.execute(sql % page_number)[0]['page_source']
    html = fromstring(page_source)
    return html
