#!/usr/bin/env python2
from dumptruck import DumpTruck
from lxml.html import fromstring
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from random import normalvariate
from time import sleep

url = 'https://secure.yogaalliance.org/IMISPublic/Registration/Teachers/teacherdirectory.aspx'

def randomsleep():
    seconds=normalvariate(9, 3)
    if seconds>0:
        sleep(seconds)

def _driver_setup():
    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
    desired_capabilities['name'] = 'Yoga'
    driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor="http://localhost:4444/wd/hub")
    return driver

def main():
    dt = DumpTruck(dbname='somatic.sqlite')
    dt.execute('''
CREATE TABLE IF NOT EXISTS page_source (
  page_number INTEGER NOT NULL,
  page_source TEXT NOT NULL,
  UNIQUE(page_number)
)''')

    print('Running the search')
    # Get the search page
    driver = _driver_setup()
    driver.get(url)

    # 100 per page
    option = driver.find_elements_by_xpath('id("ctl00_TemplateBody_ucTeacherDirectory_ddhowmany")/option[@value="100"]')[0]
    option.click()

    # Search
    button = driver.find_elements_by_id('ctl00_TemplateBody_ucTeacherDirectory_imgSearch')[0]
    button.click()

    while True:
        print('Pausing for a few seconds to let the page load and be polite')
        sleep(8)
        randomsleep()

        # Current page number
        page_numbers = driver.find_elements_by_css_selector('#ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory tr td tr span')]

        # Fast forward to new pages: Ellipsis
        ellipses = driver.find_element_by_xpath('//a[text()="..."]')

        # Fast forward to new pages: Maximum page
        max_page_numbers = driver.find_element_by_xpath('//td[a[text()="..."]]/preceding-sibling::td[position()=1]')

        for nodes in [page_numbers, ellipses, max_page_numbers]:
            if len(nodes) == 1:
                raise ValueError('Only one navigation row')
            elif nodes.text[0] != nodes.text[1]:
                raise ValueError('Page navigation rows don\'t match.')

        page_number = int(page_numbers[0].text)
        ellipsis = ellipses[0]
        max_page_number = int(max_page_numbers[0].text)

        previous_page_saved = dt.execute('select max(page_number) as "m" from page_source')[0]['m']

        print('On page %d' % page_number)
        if previous_page_saved == page_number:
            # If we're up to this page, save it.
            pass
        elif previous_page_saved < max_page_number:
            # If we're not up to this page but the appropriate page is visible,
            # click to the right page.
            print('Skipping a little bit ahead')
            xpath = 'id("ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory")' +
                '/descendant::tr/descendant::a[text()="%d"]' % (previous_page_saved + 1)
            a = driver.find_elements_by_xpath(xpath)[0]
            a.click()
            continue
        elif previous_page_saved > max_page_number:
            # If we're not up to this page and the appropriate page is not visible,
            # click the ellipsis.
            print('Skipping a big bit ahead')
            ellipsis.click()
            continue

        print('Saving page %d' % page_number)
        dt.insert({'page_number': page_number, 'page_source': driver.page_source}, 'page_source')
        try:
            a = spans[0].find_element_by_xpath('../following-sibling::td[position()=1]/a')
        except NoSuchElementException:
            print('We appear to have reached the end at page %d. Please confirm that this is correct.' % page_number)
            break
        else:
            a.click()

main()
