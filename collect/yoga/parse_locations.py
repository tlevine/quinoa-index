#!/usr/bin/env python
from collections import OrderedDict
import re
from lxml.html import fromstring, tostring
from dumptruck import DumpTruck

DB = '/tmp/yoga.db'
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
    'Label2',
]
HEADER_KEYS = ['Name', 'Contact', 'Address', 'Registration']
STATES = [
    # States
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',

    # Other territories
    'DC', 'INTL',
]
  

# Open the database
dt = DumpTruck(DB) 

def main():
    query = dt.execute('select page_number from page_source')
    page_numbers = [row['page_number'] for row in query]
    for page_number in page_numbers:
        d = parse(page_number)
        dt.insert(d)

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

        row['Errors'] = u''
        # Ugh. Replace this with withs or something.
        try:
            if row['State'] not in STATES:
                raise ValueError('This is an odd state: %s.' % row['State'])
        except ValueError, msg:
            row['State'] = u''
            row['Errors'] += unicode(msg) + u'\n'
 
        try:
            row['Zip'] = _clean_zip_code(row['Zip'])
        except ValueError, msg:
            row['Zip'] = u''
            row['Errors'] += unicode(msg) + u'\n'
 
        try:
            # Country should be 'USA'
            if row['Country'] != 'USA':
                raise ValueError('Wrong country: %s' % row['Country'])
        except ValueError, msg:
            row['Country'] = u''
            row['Errors'] += unicode(msg) + u'\n'

    return d

def _clean_zip_code(zipcode):
    if zipcode == u'':
        return None

    # Remove trailing hyphens from zip code.
    if zipcode[-1] == '-':
        zipcode = zipcode[0:-1]

    # It should be five characters long.
    if len(zipcode) == 5:
        pass

    # Or it should be ten characters, with the sixth being a hyphen.
    elif len(zipcode) == 10 and zipcode[5] == '-':
        pass

    # If it isn't raise an error.
    else:
        raise ValueError('%s doesn\'t look like a zip code.' % zipcode)

    # Check that it's five _digits_
    for i, digit in enumerate(zipcode):
        if i == 5 and digit == '-':
            pass
        else:
            int(digit)
    return zipcode

def _schema(data_row):
    data_row['Errors'] = u''
    dt.create_table(data_row, 'teacher', if_not_exists = True)

    dt.create_index(['City'], 'teacher')
    dt.create_index(['State'], 'teacher')
    dt.create_index(['Zip'], 'teacher')
    dt.create_index(['Style'], 'teacher')

    # Not country because they're all USA
    # dt.create_index('teacher', ['Country'])

def _parse_tr(tr):
    "Turn a tr lxml element into an OrderedDict"
    spans = tr.cssselect('span')

    rightnumber = 15
    if len(spans) != rightnumber:
        print(tostring(tr))
        msg = 'Wrong number of spans (%d instead of %d)'
        params = (len(spans), rightnumber)
        raise ValueError(msg % params)

    return OrderedDict([_get_span_tuple(span) for span in spans])

def _get_span_tuple(span):
    """
    Return a tuple of data key and value for a span inside the table.
    Before returning, check that the key is valid.
    """
    id = span.attrib['id']
    if '_lbl' in id:
        key = id.split('_lbl')[-1]
    else:
        key = re.split(r'_ctl\d{2,3}_', id)[-1]

    if key not in SPAN_KEYS:
        raise ValueError('Key %s is not among the expected keys.' % key)

    # .text_content rather than .text in case one of them is weird.
    # links, inside of a tags, are an example of such weirdness.
    value = span.text_content()

    return (unicode(key), unicode(value))

def _check_header(tr):
    header_tr = tr
    header_keys = [th.text for th in header_tr.xpath('th')]
    if header_keys != HEADER_KEYS:
        raise ValueError('The header is wrong; it\'s %s' % header_keys)

if __name__ == '__main__':
    main()
