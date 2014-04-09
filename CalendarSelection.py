"""
Created on 8 Feb 2014

@author: AbbyTheRat

Select a calendar if it has not been selected before hand.

Allow new selection to be made.
"""


class calendarlisting(object):

    calendarIDlist = list()
    calendarid = None
    google_service = None

    def __init__(self, google_service):

        #TODO Store selected CalendarID to file
        #TODO Test calendarID stored on file to make sure it's still valid otherwise request a new selection

        self.google_service = google_service
        if self.calendarid is None:
            self.select_calendar()

    def return_calendar_id(self):
        return self.calendarid

    def select_calendar(self):
        page_token = None

        while True:
            calendar_list = self.google_service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'owner' == calendar_list_entry['accessRole']:
                    self.calendarIDlist.append(calendar_list_entry['id'])
                    count = str(len(self.calendarIDlist))
                    if 'primary' in calendar_list_entry and calendar_list_entry['primary']:
                        print str(count) + ': primary - name: ' + calendar_list_entry['summary']
                        if 'description' in calendar_list_entry:
                            print str(count) + ': description:', calendar_list_entry['description']
                    else:
                        print str(count) + ': name:' + calendar_list_entry['summary']
                        if 'description' in calendar_list_entry:
                            print str(count) + ': description:', calendar_list_entry['description']
                    page_token = calendar_list.get('nextPageToken')

            if not page_token:
                break

        page_token = None

        if len(self.calendarIDlist) > 1:
            try:
                inputselection = input("Select Calendar: ")
                if inputselection < 1 or inputselection > len(self.calendarIDlist):
                    raise SyntaxError

                self.calendarid = self.calendarIDlist[inputselection -1]
            except SyntaxError:
                print 'Select only a number between 1 and ' + str(len(self.calendarIDlist))


    def print_calendar_list(self, calendar_list):

        count = 1
        for calendar_list_tag in calendar_list['items']:
            for celendar_list_entry in calendar_list_tag:
                print str(count) + ':- ' + celendar_list_entry + ': ' + str(calendar_list_tag[celendar_list_entry])
            count += 1