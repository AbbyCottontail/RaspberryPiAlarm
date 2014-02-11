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
    classdocs
    """

    ClientSecrets = None
    flags = None
    flow = None
    parser = None

    def __init__(self, client_secrets, flags):
        """

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
        if creds is None or creds.invalid:
            creds = tools.run_flow(self.flow, storage, self.getFlags())

        http = httplib2.Http()
        http = creds.authorize(http)

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
