from dumptruck import DumpTruck
import requests
import sqlite3dbm


VIEWSTATE = None

class SearchPage:
#   def __init__(self, pagenum = 1, howmany = 25):
#       self.pagenum = pagenum
#       self.howmany = howmany

    def load(self):
        url = 'https://secure.yogaalliance.org/IMISPublic/Registration/Teachers/teacherdirectory.aspx'
        params = {
            'ctl00$ScriptManager1': 'ctl00$TemplateBody$UpdatePanel1|ctl00$TemplateBody$ucTeacherDirectory$gvTeacherDirectory',
            'ctl00$TemplateBody$ucTeacherDirectory$ddDCountry': 'USA',
            'ctl00$TemplateBody$ucTeacherDirectory$txtDLastName': '',
            'ctl00$TemplateBody$ucTeacherDirectory$txtDFirstName': '',
            'ctl00$TemplateBody$ucTeacherDirectory$txtDCity': '',
            'ctl00$TemplateBody$ucTeacherDirectory$txtDZip': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddDStyle': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddDDesignation': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddDState': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddDSpecialities': '',
            'ctl00$TemplateBody$ucTeacherDirectory$txtDWebsite': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddLanguages': '',
            'ctl00$TemplateBody$ucTeacherDirectory$ddhowmany': '%d' % howmany,
            'ctl00$TemplateBody$ucTeacherDirectory$ddlSortBy': 'Last Name',
            'ctl00_GenericWindow_ClientState': '',
            'ctl00_ObjectBrowser_ClientState': '',
            'ctl00_ObjectBrowserDialog_ClientState': '',
            'ctl00_ctl28_ClientState': '',
            '__EVENTTARGET': 'ctl00$TemplateBody$ucTeacherDirectory$gvTeacherDirectory',
            '__EVENTARGUMENT': 'Page$%d' % pagenum,
            '__VIEWSTATE': VIEWSTATE,
            'TemplateUserMessagesID': 'ctl00_TemplateUserMessages_ctl00_Messages',
            'PageIsDirty': 'true',
            '__ASYNCPOST': 'true',
            '': '',
        }
        headers = {
            'Host': 'secure.yogaalliance.org',
            'Origin': 'https://secure.yogaalliance.org',
            'Referer': 'https://secure.yogaalliance.org/IMISPublic/Registration/Teachers/teacherdirectory.aspx',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
            'X-MicrosoftAjax': 'Delta=true',
        }
   def parse(self, text):
        html = fromstring(text)
        table = html.get_element_by_id('ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory')
        print table.text_content()

bucket_types = {
  'SearchPage': SearchPage,
}
