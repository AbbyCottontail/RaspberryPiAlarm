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

    getPage(url).addCallbacks(
        callback=fetch_xml_data,
        errback=fetch_error)

def fetch_xml_data(data):
    xml_root = et.fromstring(data)

    try:
        wp = WeatherParser.weather_parser(xml_root)
    except:
        traceback.print_exc()

    shutdownwebapp()

def fetch_error(err):
    print "error ", err
    shutdownwebapp()

def shutdownwebapp():
    reactor.stop()

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

    @option(default='CAXX0343:1:CA')
    def getweather_location(self):
        pass

    @option(default='m')
    def getmetric_unit(self):
        pass


def main():
    try:
        myoptions = Cli(MyOptions).parseArguments()
    except CliHelpError as helpError:
        print helpError
        return 0

    get_weather(myoptions.getweather_location(), myoptions.getmetric_unit())

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

    calendarid = select_calendar.return_calendar_id()
    EventListing.event_listing(google_services, calendarid)


    reactor.run()


if __name__ == '__main__':
    main()