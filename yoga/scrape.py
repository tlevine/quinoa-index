from dumptruck import DumpTruck
import requests

class SearchPage:
    def __init__(self, page_number):
        self.page_number = page_number

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
            'ctl00$TemplateBody$ucTeacherDirectory$ddhowmany': '25',
            'ctl00$TemplateBody$ucTeacherDirectory$ddlSortBy': 'Last Name',
            'ctl00_GenericWindow_ClientState': '',
            'ctl00_ObjectBrowser_ClientState': '',
            'ctl00_ObjectBrowserDialog_ClientState': '',
            'ctl00_ctl28_ClientState': '',
            '__EVENTTARGET': 'ctl00$TemplateBody$ucTeacherDirectory$gvTeacherDirectory',
            '__EVENTARGUMENT': 'Page$8',
            'TemplateUserMessagesID': 'ctl00_TemplateUserMessages_ctl00_Messages',
            'PageIsDirty': 'true',
            '__ASYNCPOST': 'true',
            '': '',
        }
        

        'ctl00_TemplateBody_ucTeacherDirectory_gvTeacherDirectory'
