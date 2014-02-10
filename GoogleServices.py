'''
Created on 8 Feb 2014

@author: AbbyTheRat

Contains classes
'''

import httplib2
import os

from apiclient.discovery import build
from oauth2client import file
from oauth2client import client
from oauth2client import tools




class GoogleServices(object):
    '''
    classdocs
    '''

    ClientSecrets = None
    flags = None
    flow = None
    parser = None
    
    def __init__(self, ClientSecrets, flags):
        self.setFlags(flags)
        self.setClientSecrets(ClientSecrets)
        
        self.flow = client.flow_from_clientsecrets(
                                                   self.getClientSecrets(),
                                                   scope=[
                                                          'https://www.googleapis.com/auth/calendar.readonly',
                                                          ], 
                                                   message=tools.message_if_missing(self.getClientSecrets())
                                                   )
    
    def startGoogleServices(self):
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
            print ("The credentials have been revoked or expired, please re-run"
                    "the application to re-authorize")
            return None
        
        
    '''setters/getters methods'''

    def getFlags(self):
        return self.__flags
    
    def getClientSecrets(self):
        return self.__ClientSecrets
    

    def setClientSecrets(self, value):
        self.__ClientSecrets = os.path.join(os.path.dirname(__file__), value)
        
    def setFlags(self, value):
        self.__flags = value
    

    
    