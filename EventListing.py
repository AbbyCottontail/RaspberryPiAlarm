"""
Created on 8 Feb 2014

@author: AbbyTheRat

Fetch events from google calendar and caches the wanted events.

IDEA: Maybe also do some parsing on the event for special keyword in here
Possible offloading caching functions to a separate file and class, as
I can see some of these functions being shared across the program.
Cache things like current weather data, calendar selection

"""

import datetime


class event_listing:
    calendarid = None
    page_token = None

    def __init__(self, services, calendarid='primary', pageToken=None):
        """
            Fetch list of events for the next 24 hours, plus separate list for the next week after.
            :type self: object
        """

        if calendarid is None:
            self.calendarid = 'primary'
        else:
            self.calendarid = calendarid

        self.page_token = None

        self.get_events(services, self.calendarid, self.page_token)
        pass

    def get_events(self, services, calendar_id=calendarid, pagetoken=page_token):

        #Pull UTC time
        dt = datetime.datetime.utcnow()

        start_time = dt

        #Select a week of events
        end_time = start_time + datetime.timedelta(7)
        #Remove any microseconds from ISOformat, (google doesn't want it) then add Z to denote UTC datetime.
        #googles wants rfc3339 format for datetime.
        start_time = start_time.isoformat()[:19] + 'Z'
        end_time = end_time.isoformat()[:19] + 'Z'


        print start_time + ' ' + end_time

        events = services.events().list(
            calendarId=calendar_id,
            singleEvents=True,
            maxResults=1000,
            orderBy='startTime',
            timeMin=start_time,
            timeMax=end_time,
            pageToken=pagetoken,
        ).execute()

        #Test to see if there's any events to list.
        event_item = events.get('items', None)

        if event_item is not None:
            while True:
                for event in events['items']:
                    print 'Title: ' + event['summary']
                    if 'description' in event:
                        print 'Description: "' + event['description'] + '"'
                    print "-"*60
                    pagetoken = events.get('nextPageToken')

                if not pagetoken:
                    break




                    #self.print_events_list(events)

    def print_events_list(self, events):
        page_token = self.page_token
        while True:
            for event in events['items']:
                print event['summary']
                page_token = events.get('nextPageToken')
            if not page_token:
                break

        print events