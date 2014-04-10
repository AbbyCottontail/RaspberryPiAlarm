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
import EventListing
from twisted.internet import reactor
from twisted.web.client import getPage
import WeatherParser
import xml.etree.ElementTree as et
import traceback

import sys

WEATHER_COM_URL = 'http://wxdata.weather.com/wxdata/weather/local/%s?unit=%s&cc=*'


def get_weather(location_id, units = 'metric'):
    """Fetch weather report from Weather.com

    Parameters:
        location_id: A location ID or 5 digit US zip code.

        units: type of units. 'metric' for metric and 'imperial' for non-metric.
        Note that choosing metric units changes all the weather units to metric.
        For example, wind speed will be reported as kilometers per hour and
        barometric pressure as millibars.

    """

    if units == 'm':
        unit = 'm'
    elif units == 'i' or units == '':    # for backwards compatibility
        unit = ''
    else:
        unit = 'm'      # fallback to metric
    url = WEATHER_COM_URL % (location_id, unit)

    #set up a callback for weather data
    getPage(url).addCallbacks(
        callback=fetch_xml_data,
        errback=fetch_error)

def fetch_xml_data(data):
    """
        this pulls the data from twisted once it has fetched the XML data
    """

    xml_root = et.fromstring(data)

    try:
        #Attempt to parse the xml data into English instead of short tags.
        wp = WeatherParser.weather_parser(xml_root)
        #For some reasons that I have yet to learn. Twisted likes to get stuck in a loop if there's an error in the code
        # unless exceptions are caught outside. Hence the current broad catch.
    except:
        traceback.print_exc()

    #done! Close down twisted event loop
    shutdownwebapp()


def fetch_error(err):
    print "error ", err
    #found an error, shutdown the event loop to avoid app hanging.
    shutdownwebapp()


def shutdownwebapp():
    reactor.stop()


class MyOptions(object):
    """
    Define options for command line parameters.
    """
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

    @option(default='CAXX0343:1:CA')
    def getweather_location(self):
        pass

    @option(default='m')
    def getmetric_unit(self):
        pass


def main():
    try:
        #parse the commandline
        myoptions = Cli(MyOptions).parseArguments()
    except CliHelpError as helpError:
        print helpError
        return 0

    #weather functions
    get_weather(myoptions.getweather_location(), myoptions.getmetric_unit())

    #create flags for Google Services
    flags = Flags.Flags(myoptions.getauth_host_name(),
                        myoptions.getauth_host_port(),
                        myoptions.isnoauth_local_webserver(),
                        myoptions.getlogging_level())

    #Create google services object. This get carried around for google api functions.
    google_services = GoogleServices.GoogleServices(myoptions.getclient_secret(), flags)

    try:
        #connect, auth and return a connected service object
        google_services = google_services.startgoogleservices()
    except AccessTokenRefreshError:
        print("The credentials have been revoked or expired, please re-run the application to re-authorize")
        return 0

    #returns a selected calendar - either from one stored in user file or return an option
    select_calendar = CalendarSelection.calendarlisting(google_services)
    calendarid = select_calendar.return_calendar_id()


    EventListing.event_listing(google_services, calendarid)

    #start twisted event loop for fetching weather data.
    reactor.run()


if __name__ == '__main__':
    main()