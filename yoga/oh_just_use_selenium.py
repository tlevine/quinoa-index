from dumptruck import DumpTruck
from lxml.html import fromstring
from selenium import webdriver
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
    driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor="http://thomaslevine.com:4444/wd/hub")
    return driver

def _search_setup():
    # Get the search page
    driver = _driver_setup()
    driver.get(url)

    # 100 per page
    option = driver.find_elements_by_xpath('id("ctl00_TemplateBody_ucTeacherDirectory_ddhowmany")/option[@value="100"]')[0]
    option.click()

    # Search
    button = driver.find_elements_by_id('ctl00_TemplateBody_ucTeacherDirectory_imgSearch')[0]
    button.click()

    return driver

def main():
    dt = DumpTruck(dbname='somatic.sqlite')
    dt.create_index('page_source', ['page_number'], if_not_exists = True, unique = True)

    driver = _search_setup()

    while True:
        spans = driver.find_elements_by_css_selector('#ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory tr td tr span')
        if spans[0].text != spans[1].text:
            raise ValueError('Page navigation rows don\'t match.')

        page_number = int(spans[0].text)
        dt.insert({'page_number': page_number, 'page_source': driver.page_source}, 'page_source')
        try:
            a = span[0].find_element_by_xpath('../following-sibling::td[position()=1]/a')
        except NoSuchElementException:
            print('We appear to have reached the end at page %d. Please confirm that this is correct.' % page_number)
            break
        else:
            a.click()
        randomsleep()
