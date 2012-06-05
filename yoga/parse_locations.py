from dumptruck import DumpTruck
from lxml.html import fromstring, tostring

dt = DumpTruck('/tmp/yoga.sqlite') 

def parse(page_number):
    sql = 'select page_source from page_source where page_number = %d'
    page_source = dt.execute(sql % page_number)[0]['page_source']
    html = fromstring(page_source)
    table = html.get_element_by_id('ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory')
    trs = table.xpath('tbody/tr')[1:-1]

    # Remove the header, check it, and don't use it.
    _check_header(trs.pop(0))

    # Body
    print tostring(trs[0])
    #.text_content()

def _check_header(tr)
    header_tr = tr
    header = [th.text for th in header_tr.xpath('th')]
    if keys != ['Name', 'Contact', 'Address', 'Registration']
        raise ValueError('The header is wrong; it\'s %s' % keys)
