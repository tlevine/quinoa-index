from lxml.html import parse
from dumptruck import DumpTruck

dt = DumpTruck(dbname = 'alexander.sqlite')

def main():
    html = parse('http://www.alexandertechnique.com/teacher/northamerica').getroot()
    states = html.xpath('//tr[td/font/a[@name]]')

    data = []
    for state in states:
        name = state.text_content().strip()
        teachers = state.xpath('following-sibling::tr[position()=1]/descendant::a[@href]')
        for teacher in teachers:
            city = teacher.text_content().strip()
            link = teacher.attrib['href']
            if link[0] != '#':
                data.append({
                    'state': name,
                    'city': city,
                    'teacher_url': link,
                })
    dt.create_table(data[0], 'alexander_teachers')
    dt.create_index('alexander_teachers',
        ['state', 'city', 'teacher_url'],
        unique = True, if_not_exists = True,
    )
    dt.insert(data, 'alexander_teachers')

if __name__ == '__main__':
    main()
