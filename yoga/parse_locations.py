from dumptruck import DumpTruck
from lxml.html import fromstring, tostring

DB = '/tmp/yoga.sqlite'
SPAN_KEYS = ['LAST_NAME',
    'FIRST_NAME',
    'Style',
    'Designation',
    'Phone',
    'Email',
    'Website',
    'Address',
    'City',
    'State',
    'Zip',
    'Country',
    'Reg',
    'Languages',
    'ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory_ctl03_Label2'
]
HEADER_KEYS = ['Name', 'Contact', 'Address', 'Registration']

# Open the database
dt = DumpTruck(DB) 

def parse(page_number):
    sql = 'select page_source from page_source where page_number = %d'
    page_source = dt.execute(sql % page_number)[0]['page_source']
    html = fromstring(page_source)
    table = html.get_element_by_id('ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory')
    trs = table.xpath('tbody/tr')[1:-1]

    # Remove the header, check it, and don't use it.
    _check_header(trs.pop(0))

    # Body
    d = _parse_tr(trs[0])

def _parse_tr(tr):
    "Turn a tr lxml element into a zip"
    spans = tr.cssselect('span')

    rightnumber = 15
    if len(spans) != rightnumber:
        print(tostring(tr))
        msg = 'Wrong number of spans (%d instead of %d)'
        params = (len(spans), rightnumber)
        raise ValueError(msg % params)

    print [span.attrib['id'] for span in spans]
    return [_get_span_tuple(span) for span in spans]

def _get_span_tuple(span):
    """
    Return a tuple of data key and value for a span inside the table.
    Before returning, check that the key is valid.
    """
    key = span.attrib['id'].split('_lbl')[-1]
    if key not in KEYS:
        raise ValueError('Key %s is not among the expected keys.' % key)

    # .text_content rather than .text in case one of them is weird.
    # links, inside of a tags, are an example of such weirdness.
    value = span.text_content()

    return (key, value)

def _check_header(tr):
    header_tr = tr
    header_keys = [th.text for th in header_tr.xpath('th')]
    if header_keys != HEADER_KEYS:
        raise ValueError('The header is wrong; it\'s %s' % header_keys)
