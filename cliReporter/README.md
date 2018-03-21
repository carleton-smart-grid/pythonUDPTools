# CLIReporter

This reports to a lowpan-visualiser instance running on a server.

##Usage

The cliReporter must be run from the same directory that RPL is run from (so that it can connect to the RPL_CLI socket)

    sudo python ../cliReporter/cliReporter.py [IID] [host_ip]

Where `IID` is everything **after** the `fe80::` (or `dead::beef::`), *not including the ::* and `host_ip` is the IP of the server running the visualizer

