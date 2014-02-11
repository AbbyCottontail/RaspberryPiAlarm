"""
Created on 8 Feb 2014

@author: AbbyTheRat

Select a calendar if it has not been selected before hand.

Allow new selection to be made.
"""


class calendarlisting(object):

    def __init__(self, google_service):
        page_token = None
        while True:
            calendar_list = google_service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if 'owner' == calendar_list_entry['accessRole']:
                    if 'primary' in calendar_list_entry and calendar_list_entry['primary']:
                        print'primary - name:', calendar_list_entry['summary']
                        if 'description' in calendar_list_entry:
                            print'description:', calendar_list_entry['description']
                    else:
                        print'name:', calendar_list_entry['summary']
                        if 'description' in calendar_list_entry:
                            print'description:', calendar_list_entry['description']
                    page_token = calendar_list.get('nextPageToken')

            if not page_token:
                break

        page_token = None
        # while True:
        #     calendar_list = google_service.calendarList().list(pageToken=page_token).execute()
        #     for calendar_list_entry in calendar_list['items']:
        #         print calendar_list_entry['summary']
        #         page_token = calendar_list.get('nextPageToken')
        #     if not page_token:
        #         break
        print calendar_list