"""
Created on 8 Feb 2014

@author: AbbyTheRat

Loads the google services and setup oAuth. Cache valid credentials.
"""

import httplib2
import os

from apiclient.discovery import build
from oauth2client import file
from oauth2client import client
from oauth2client import tools


class GoogleServices(object):
    """
        Performs OAuth 2 checks. If there's no key, it'll requests permission to use the users' google services and store
        for later user.
    """

    ClientSecrets = None
    flags = None
    flow = None
    parser = None

    def __init__(self, client_secrets, flags):
        """
            This is doing so many things via in API library, Abby only understands about half the things it's doing
            The main function is to authorize itself with the google services. First checking to see if there's any stored
            from an old request, check to make sure it's still valid and haven't been revoked or create a request URL
            for user to give this app permission and store credentials.


            :rtype : object
        """
        self.__flags = flags
        self.__ClientSecrets = os.path.join(os.path.dirname(__file__), client_secrets)
        #TODO - file path check - make sure the file is valid
        self.set_flags(flags)
        self.set_client_secrets(client_secrets)

        self.flow = client.flow_from_clientsecrets(
            self.get_client_secrets(),
            scope=[
                'https://www.googleapis.com/auth/calendar.readonly',
            ],
            message=tools.message_if_missing(self.get_client_secrets())
        )

    def startgoogleservices(self):
        storage = file.Storage('credStore.dat')
        creds = storage.get()
        #If there is no credentials stored in file, then create a new flow. Whatever flow means.
        if creds is None or creds.invalid:
            #This function creates a request URL for the user to use in their browser, (or use web server if available
            #which I won't use due to the nature of this app
            creds = tools.run_flow(self.flow, storage, self.getFlags())



        http = httplib2.Http()
        http = creds.authorize(http)

        #attempts to create the accepted services.
        service = build(serviceName='calendar', version='v3', http=http)

        try:
            return service
        except client.AccessTokenRefreshError:
            return None

    def get_flags(self):
        return self.__flags

    def get_client_secrets(self):
        return self.__ClientSecrets

    def set_client_secrets(self, value):
        pass

    def set_flags(self, value):
        pass
