"""
Created on 9 Feb 2014

@author: AbbyTheRat

Store thes options flags for Googles AP Client Library

"""


class Flags(object):
    """
    Holds data for Googles API Client Library
    """
    auth_host_name = ''
    auth_host_port = ''
    noauth_local_webserver = ''
    logging_level = ''

    def __init__(self, auth_host_name, auth_host_port, noauth_local_webserver, logging_level):
        self.auth_host_name = auth_host_name
        self.auth_host_port = auth_host_port
        self.noauth_local_webserver = noauth_local_webserver
        self.logging_level = logging_level
        #TODO - Data check