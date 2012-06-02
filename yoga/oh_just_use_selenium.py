from dumptruck import DumpTruck
from lxml.html import fromstring
from selenium import webdriver

url = 'https://secure.yogaalliance.org/IMISPublic/Registration/Teachers/teacherdirectory.aspx'

def driver_setup():
    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
    desired_capabilities['name'] = 'Yoga'
    driver = webdriver.Remote(desired_capabilities=desired_capabilities,command_executor="http://thomaslevine.com:4444/wd/hub")
    return driver

dt = DumpTruck(dbname='somatic.sqlite')

# Get the search page
driver = driver_setup()
driver.get(url)

# 100 per page
option = driver.find_elements_by_xpath('id("ctl00_TemplateBody_ucTeacherDirectory_ddhowmany")/option[@value="100"]')[0]
option.click()
