"""
Created on 8 Feb 2014

@author: AbbyTheRat

Manage events and store on file

"""



class event_listing:

    calendarid = None
    page_token = None

    def __init__(self, services, calendarid='primary', pageToken = None):
        """

        :type self: object
        """

        if calendarid is None:
            self.calendarid='primary'
        else:
            self.calendarid = calendarid

        self.page_token=None

        self.get_events(services, self.calendarid, self.page_token)
        pass

    def get_events(self, services, calendar_id=calendarid, pagetoken=page_token):
        events = services.events().list(
            calendarId=calendar_id,
            singleEvents=True,
            maxResults=1000,
            orderBy='startTime',
            timeMin='2014-01-01T00:00:00-08:00',
            timeMax='2014-10-30T00:00:00-08:00',
            pageToken=pagetoken,
        ).execute()

        self.print_events_list(events)

    def print_events_list(self, events):
        page_token = self.page_token
        while True:
            for event in events['items']:
                print event['summary']
                page_token = events.get('nextPageToken')
            if not page_token:
                break

        print events