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
STATES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
  

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

    # Schema
    _schema(_parse_tr(trs[0]))

    # Body
    d = [dict(_parse_tr(tr)) for tr in trs]

    # Clean and check
    for row in d:
        if row['State'] not in STATES:
            raise ValueError('This is an odd state: %s.' % row['State'])

        # Remove trailing hyphens
        if row['Zip'][-1] == '-':
            row['Zip'] = row['Zip'][0:-1]

        # Check that it's five long
        if len(row) != 5:
            raise ValueError('Zip code %s is not five characters long.' % row['Zip'])

        # Check that it's five _digits_
        for digit in row:
            int(digit)

        # Country should be 'USA'
        if row['Country'] != 'USA':
            raise ValueError('Wrong country: %s' % row['Country'])

    return d

def _schema(data_row):
    dt.create_table(data_row, 'teacher', if_not_exists = True, structure=zip)

    dt.create_index(['City'], 'teacher')
    dt.create_index(['State'], 'teacher')
    dt.create_index(['Zip'], 'teacher')
    dt.create_index(['Style'], 'teacher')

    # Not country because they're all USA
    # dt.create_index('teacher', ['Country'])

def _parse_tr(tr):
    "Turn a tr lxml element into a zip"
    spans = tr.cssselect('span')

    rightnumber = 15
    if len(spans) != rightnumber:
        print(tostring(tr))
        msg = 'Wrong number of spans (%d instead of %d)'
        params = (len(spans), rightnumber)
        raise ValueError(msg % params)

    return [_get_span_tuple(span) for span in spans]

def _get_span_tuple(span):
    """
    Return a tuple of data key and value for a span inside the table.
    Before returning, check that the key is valid.
    """
    key = span.attrib['id'].split('_lbl')[-1]
    if key not in SPAN_KEYS:
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
