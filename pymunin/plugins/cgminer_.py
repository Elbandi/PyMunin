#!/usr/bin/env python
"""cgminer_ - Munin Plugin to monitor cgminer.


Requirements

  - Requires ntpd running on remote host and access to NTP on remote host.
  - Requires ntpdate utility on local host.

Wild Card Plugin

  Symlink indicates IP of remote host (or group name) to be monitored:
  Ex: cgminer_groupname -> /usr/shar/munin/plugins/cgminer_


Multigraph Plugin - Graph Structure

   - accept_shares
   - hwerrors
   - fan_speed
   - hashrate
   - hashrate_av
   - rejected


Environment Variables

  include_graphs: Comma separated list of enabled graphs.
                  (All graphs enabled by default.)
  exclude_graphs: Comma separated list of disabled graphs.

Environment Variables for Multiple Instances of Plugin (Omitted by default.)
  instance_name:         Name of instance.
  instance_label:        Graph title label for instance.
                         (Default is the same as instance name.)
  instance_label_format: One of the following values:
                         - suffix (Default)
                         - prefix
                         - none 

  Example:
    [cgminer_group1]
       env.host 127.0.0.1
       env.ports 4020 4021
       env.exclude_graphs accept_shares

"""
# Munin  - Magic Markers
#%# family=manual
#%# capabilities=noautoconf nosuggest

import sys
from pymunin import MuninGraph, MuninPlugin, muninMain
from pysysinfo.cgminer import CgminerInfo

__author__ = "Elbandi"
__copyright__ = "Copyright 2015, Elbandi"
__credits__ = []
__license__ = "GPL"
__version__ = "0.9.20"
__maintainer__ = "elbandi"
__email__ = "elso.andras at gmail.com"
__status__ = "Development"


class MuninCgminerPlugin(MuninPlugin):
    """Multigraph Munin Plugin for monitoring cgminer.

    """
    plugin_name = 'cgminer_'
    isMultigraph = True
    isMultiInstance = True

    def __init__(self, argv=(), env=None, debug=False):
        """Populate Munin Plugin with MuninGraph instances.
        
        @param argv:  List of command line arguments.
        @param env:   Dictionary of environment variables.
        @param debug: Print debugging messages if True. (Default: False)
        
        """
        MuninPlugin.__init__(self, argv, env, debug)
        self._category = 'cgminer'

        if self.arg0 is None:
            raise Exception("Group cannot be determined.")
        else:
            self._group = self.arg0

        self._host = self.envGet('host')
        self._ports = self.envGet('ports', "4028")

        self._cgminerInfo = CgminerInfo(self._host, self._ports)

        if self.graphEnabled('accept_shares'):
            graphName = 'accept_shares_%s' % self._group
            graph = MuninGraph('Accepted shares on %s' % self._group,
                self._category,
                vlabel="Shares/second",
                info='This graph shows the accepted shares rate as reported by cgminer.',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getAcceptedStats().iteritems():
                for g in devs:
                    fname = "accept_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'DERIVE', 'AREASTACK',
                                   min=0, max=10000,
                                   info="Accepted shares")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('hwerrors'):
            graphName = 'hwerrors_%s' % self._group
            graph = MuninGraph('Hardware Error on %s' % self._group,
                self._category,
                info='This graph shows the amount of errors on the devices',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getHardwareErrorsStats().iteritems():
                for g in devs:
                    fname = "error_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'DERIVE', 'AREASTACK',
                                   min=0, max=10000,
                               info="Hardware Error")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('fan_speed'):
            graphName = 'fan_speed_%s' % self._group
            graph = MuninGraph('Fan speed on %s' % self._group,
                self._category,
                vlabel="RPM",
                info='This graph shows the rounds per minute of the fans in the devices.',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getFanSpeedStats().iteritems():
                for g in devs:
                    fname = "fan_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'GAUGE', draw='LINE2',
                                   min=0,
                                   info="Current fan speed")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('hashrate'):
            graphName = 'hashrate_%s' % self._group
            graph = MuninGraph('5sec hashrate on %s' % self._group,
                self._category,
                vlabel="hash/s",
                info='This graph shows the accepted hash rate as reported by cgminer.',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getRateStats().iteritems():
                for g in devs:
                    fname = "hashrate_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'GAUGE', 'AREASTACK',
                                   min=0,
                                   info="Current mining speed (5s)")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('hashrate_av'):
            graphName = 'hashrate_av_%s' % self._group
            graph = MuninGraph('Avg hashrate on %s' % self._group,
                self._category,
                vlabel="hash/s",
                info='This graph shows the avg hash rate as reported by cgminer.',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getRateAvStats().iteritems():
                for g in devs:
                    fname = "hashrate_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'GAUGE', 'AREASTACK',
                                   min=0,
                                   info="Current mining speed (5s)")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('rejected'):
            graphName = 'rejected_%s' % self._group
            graph = MuninGraph('Rejected percent on %s' % self._group,
                self._category,
                vlabel="%",
                info='This graph shows the rejected shares percentage',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getRejectedStats().iteritems():
                for g in devs:
                    fname = "reject_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'GAUGE',
                                   min=0,
                                   info="Reject %")
            self.appendGraph(graphName, graph)

        if self.graphEnabled('temperature'):
            graphName = 'temperature_%s' % self._group
            graph = MuninGraph('Temperature on %s' % self._group,
                self._category,
                vlabel="Degrees C",
                info='This graph shows the temperatures',
                args='--base 1000 --lower-limit 0')
            for port, devs in self._cgminerInfo.getTemperatureStats().iteritems():
                for g in devs:
                    fname = "temp_%s_%s" % (port, g['ID'])
                    graph.addField(fname, "%s %d" % (g['Name'], g['ID']), 'GAUGE',
                                   min=0,
                                   info="temperature")
            self.appendGraph(graphName, graph)

    def _fetchAllValue(self, graphname, fieldname, stats, func = None):
        graph_name = '%s_%s' % (graphname, self._group)
        if self.hasGraph(graph_name):
            for port, devs in stats.iteritems():
                for g in devs:
                    fname = "%s_%s_%s" % (fieldname, port, g['ID'])
                    self.setGraphVal(graph_name, fname, func(g['value']) if func is not None else g['value'])

    def retrieveVals(self):
        """Retrieve values for graphs."""
        self._fetchAllValue('accept_shares', 'accept', self._cgminerInfo.getAcceptedStats(), int)
        self._fetchAllValue('hwerrors', 'error', self._cgminerInfo.getHardwareErrorsStats())
        self._fetchAllValue('fan_speed', 'fan', self._cgminerInfo.getFanSpeedStats())
        self._fetchAllValue('hashrate', 'hashrate', self._cgminerInfo.getRateStats(), int)
        self._fetchAllValue('hashrate_av', 'hashrate', self._cgminerInfo.getRateAvStats(), int)
        self._fetchAllValue('rejected', 'reject', self._cgminerInfo.getRejectedStats())
        self._fetchAllValue('temperature', 'temp', self._cgminerInfo.getTemperatureStats())


    def autoconf(self):
        """Implements Munin Plugin Auto-Configuration Option.

        @return: True if plugin can be  auto-configured, False otherwise.

        """
        return self._cgminerInfo is not None

def main():
    sys.exit(muninMain(MuninCgminerPlugin))


if __name__ == "__main__":
    main()
