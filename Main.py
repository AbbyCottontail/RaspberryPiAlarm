'''
Created on 8 Feb 2014

@author: AbbyTheRat
'''


from Cli import Cli
from Cli import option
from Cli import CliHelpError
import GoogleServices
import Flags

class MyOptions(object):
    
    @option(default='localhost')
    def getAuth_host_name(self):
        pass
    
    @option(multiValued=True, default=[8080,8090])
    def getAuth_host_port(self):
        pass
    
    @option(default='ERROR')
    def getLogging_level(self):
        pass
    
    @option()
    def isNoauth_local_webserver(self):
        pass
    
    @option(default='client_secret.json')
    def getClientSecret(self):
        pass
       
def getEvents(services, calendarId='primary', pageToken=None):
    events = services.events().list(
        calendarId=calendarId,
        singleEvents=True,
        maxResults=1000,
        orderBy='startTime',
        timeMin='2014-01-01T00:00:00-08:00',
        timeMax='2014-10-30T00:00:00-08:00',
        pageToken=pageToken,
        ).execute()
        
    return events
'''TODO rebuild Flags from Cli instead of parsing.
'''

def main():
    try:
        myOptions = Cli(MyOptions).parseArguments()
    except CliHelpError as helpError:
        print helpError
        return 1
    
    flags = Flags.Flags(myOptions.getAuth_host_name(),
                  myOptions.getAuth_host_port(),
                  myOptions.isNoauth_local_webserver(),
                  myOptions.getLogging_level()
                  )
    
    NewServices = GoogleServices.GoogleServices(myOptions.getClientSecret(), flags) 
    '''Flags'''
    services = NewServices.startGoogleServices()    
    events =getEvents(services)
    
    while True:
        for event in events['items']:
            print(event)
        page_token = events.get('nextPageToken')
        if page_token:
            events = getEvents(page_token)
        else:
            print('Nothing left')
            break
        
    

if __name__ == '__main__':
    main()