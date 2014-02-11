"""
Created on 8 Feb 2014

@author: AbbyTheRat


"""

from Cli import Cli
from Cli import option
from Cli import CliHelpError
from oauth2client.client import AccessTokenRefreshError
import GoogleServices
import Flags
import CalendarSelection


class MyOptions(object):
    @option(default='localhost')
    def getauth_host_name(self):
        pass

    @option(multiValued=True, default=[8080, 8090])
    def getauth_host_port(self):
        pass

    @option(default='ERROR')
    def getlogging_level(self):
        pass

    @option()
    def isnoauth_local_webserver(self):
        pass

    @option(default='client_secret.json')
    def getclient_secret(self):
        pass



def get_events(services, calendar_id='primary', pageToken=None):
    events = services.events().list(
        calendarId=calendar_id,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2014-01-01T00:00:00-08:00',
        timeMax='2014-10-30T00:00:00-08:00',
        pageToken=pageToken,
    ).execute()

    return events


def main():
    try:
        myoptions = Cli(MyOptions).parseArguments()
    except CliHelpError as helpError:
        print helpError
        return 0

    flags = Flags.Flags(myoptions.getauth_host_name(),
                        myoptions.getauth_host_port(),
                        myoptions.isnoauth_local_webserver(),
                        myoptions.getlogging_level())

    newservices = GoogleServices.GoogleServices(myoptions.getclient_secret(), flags)

    try:
        google_services = newservices.startgoogleservices()
    except AccessTokenRefreshError:
        print("The credentials have been revoked or expired, please re-run the application to re-authorize")
        return 0

    select_calendar = CalendarSelection.calendarlisting(google_services)
    # events = get_events(google_services)
    #
    # while True:
    #     for event in events['items']:
    #         print(event)
    #     page_token = events.get('nextPageToken')
    #     if page_token:
    #         events = get_events(page_token)
    #     else:
    #         print('Nothing left')
    #         break


if __name__ == '__main__':
    main()