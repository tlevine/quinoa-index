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
    d = _parse_tr(trs[0])

def _parse_tr(tr):
    "Turn a tr lxml element into a zip"
    spans = tr.cssselect('span')

    if len(spans) != 13:
        print(tostring(tr))
        raise ValueError('Wrong number of spans')

    print [span.attrib['id'] for span in spans]
    return [_get_span_tuple(span) for span in spans]

KEYS = []
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
    header = [th.text for th in header_tr.xpath('th')]
    if keys != ['Name', 'Contact', 'Address', 'Registration']
        raise ValueError('The header is wrong; it\'s %s' % keys)
