# Startup Scripts
Each startup script initializes the appropriate *lowpan0* and *wpan0* devices.

## startCA
usage:

    sudo ./startCA.sh

Instantiates an RPL router listening on the *lowpan0* interface and will join
the first DODAG advertised. At which time a valid IPv6 address (Prefix::Local-Link)
is assigned to the interface.


## startTA
usage:

    sudo ./startTA.sh


The IP of the TA is currently hardcoded to `dead:beef:dead:beef::1/64` and will
propagate the `dead:beef:dead:beef::/32` prefix to each CA within range.
