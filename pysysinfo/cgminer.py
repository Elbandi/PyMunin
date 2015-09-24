"""Implements CgminerInfo Class for gathering stats from cgminers.

The statistics are obtained by connecting to and querying the api
of local and/or remote cgminer

"""

import re
import util
from pycgminer import CgminerAPI

__author__ = "Elbandi"
__copyright__ = "Copyright 2015, Elbandi"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.20"
__maintainer__ = "elbandi"
__email__ = "elso.andras at gmail.com"
__status__ = "Development"


defaultCGMINERport = "4028"


class CgminerInfo:
    """Class to retrieve stats for cgminer."""

    def __init__(self, host=None, port=None, autoInit=True):
        """Initialize cgminers.
        
        @param host:     Cgminer Api Host. (Default: 127.0.0.1)
        @param port:     Cgminer Api Port. (Default: 4028)
        @param autoInit: If True connect to cgminer on instantiation.
        
        """
        if host is not None:
            self._host = host
        else:
            self._host = '127.0.0.1'
        self._ports = (port or defaultCGMINERport).split(" ")
        self._statusDict = None
        if autoInit:
            self.initStats()

    def initStats(self):
        """Query and parse cgminer device api call."""

        self._statusDict = {}
        for port in self._ports:
            cgminer = CgminerAPI(self._host, int(port))
            self._statusDict[port] = cgminer.command('devs', None)['DEVS']

    def getAcceptedStats(self):
        """Return Accepted Share Stats.
        
        @return: Dictionary of server stats.
        
        """
        acceptedstats = {}
        for port, devs in self._statusDict.iteritems():
            acceptedstats[int(port)] = []
            for g in devs:
                acceptedstats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': g['Difficulty Accepted']})
        return acceptedstats

    def getHardwareErrorsStats(self):
        """Return Hardware Errors Stats.
        
        @return: Dictionary of server stats.
        
        """
        hwerrorsstats = {}
        for port, devs in self._statusDict.iteritems():
            hwerrorsstats[int(port)] = []
            for g in devs:
                hwerrorsstats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': g['Hardware Errors']})
        return hwerrorsstats

    def getFanSpeedStats(self):
        """Return Fan Speed Stats.
        
        @return: Dictionary of server stats.
        
        """
        fanspeedstats = {}
        for port, devs in self._statusDict.iteritems():
            fanspeedstats[int(port)] = []
            for g in devs:
                fanspeedstats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': g['Fan Speed'] if 'Fan Speed' in g else None})
        return fanspeedstats

    def getRateStats(self):
        """Return 5sec Hashrate Stats.
        
        @return: Dictionary of server stats.
        
        """
        hashratestats = {}
        for port, devs in self._statusDict.iteritems():
            hashratestats[int(port)] = []
            for g in devs:
                if 'KHS 5s' in g:
                    value = g['KHS 5s'] * 1e3
                elif 'MHS 5s' in g:
                    value = g['MHS 5s'] * 1e6
                else:
                    value = None
                hashratestats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': value})
        return hashratestats

    def getRateAvStats(self):
        """Return Average Hashrate Stats.
        
        @return: Dictionary of server stats.
        
        """
        hashratestats = {}
        for port, devs in self._statusDict.iteritems():
            hashratestats[int(port)] = []
            for g in devs:
                if 'KHS av' in g:
                    value = g['KHS av'] * 1e3
                elif 'MHS av' in g:
                    value = g['MHS av'] * 1e6
                else:
                    value = None
                hashratestats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': value})
        return hashratestats

    def getRejectedStats(self):
        """Return Rejected Ratio Stats.
        
        @return: Dictionary of server stats.
        
        """
        rejectedstats = {}
        for port, devs in self._statusDict.iteritems():
            rejectedstats[int(port)] = []
            for g in devs:
                rejectedstats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': g['Device Rejected%'] if 'Device Rejected%' in g else None})
        return rejectedstats

    def getTemperatureStats(self):
        """Return Temperature Stats.
        
        @return: Dictionary of server stats.
        
        """
        temperaturestats = {}
        for port, devs in self._statusDict.iteritems():
            temperaturestats[int(port)] = []
            for g in devs:
                temperaturestats[int(port)].append({'ID': g['ID'], 'Name': g['Name'], 'value': g['Temperature']})
        return temperaturestats
