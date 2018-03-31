# Contents
The **smartgrid-comms** repository contains all the code, scripts, and other resources needed for the actual transfer of usage data over 6LoWPAN. Please note that the goal of this repository *is not* to handle or perform mesh networking, instead [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is used to handle data routing for a successful mesh network.

All programs written operate on port 4907. Please ensure no other application is bound to that port *before* running anything.

```
└── .
    ├──cliReporter
    |   └── cliReporter.py
    |
    ├── mesh-comms
    |   ├── packer.py
    |   ├── tcpcomms.py
    |   ├── ta.py
    |   ├── ca.py
    |   ├── encryptiontool.py
    |   ├── aestools.py
    |   ├── rsatools.py
    |   └── packet-format.md
    |
    ├── startup
    |   ├── startCA.sh
    |   ├── startTA.sh
    |   └── README.md
    |
    ├── test-util
    |   ├── init.sql
    |   └── udpping.py
    |
    ├── README.md
    └── useful-cmds.md
```
## Directory: mesh-comms
The `mesh-comms` directory contains all the relative code/scripts to send, encrypt, pack/unpack, and receive usage data using TCP data transfer. It also contains the main runnables for the **TA** and **CA stub**.

## Directory: startup
The `startup` directory contains scripts used to configure the LoWPAN radios and configure/start Simple RPL routing. It also contains any additional setup files.

## Directory: test-util
The `test-util` directory contains any auxiliary code used to test the various parameters of the mesh network.

## Directory: cliReporter
This contains the CLI reporter python script which reports the status of a 6LoWPAN RPL node to a [lowpan-visualizer](https://github.com/carleton-smart-grid/lowpan-visualizer) via WiFi connection.



# Usage Instructions for Runnables
## startCA.sh
Configuring the 6LoWPAN (as `lowpan0`) interface for a **CA**, and starting [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is done trivially through:
```
sudo ./startCA.sh
```

It should be noted that in order to use the [cliRPL.py](https://github.com/carleton-smart-grid/simpleRPL#getting-information-on-a-running-instance) tool to discern node information or to run administration functions, `./startCA.sh` should be run in the root directory of `simpleRPL` (ie the directory containing the files `cliRPL.py` and `simpleRPL.py`).


## startTA.sh
Configuring the 6LoWPAN (as `lowpan0`) interface for a **TA**, and starting [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is done trivially through:
```
sudo ./startTA.sh
```

It should be noted that in order to use the [cliRPL.py](https://github.com/carleton-smart-grid/simpleRPL#getting-information-on-a-running-instance) tool to discern node information or to run administration functions, `./startTA.sh` should be run in the root directory of `simpleRPL` (ie the directory containing the files `cliRPL.py` and `simpleRPL.py`).


## ca.py
Provides a runnable **CA stub** that generates a pseudorandom _currentload_ and _forecastload_ which is subsequently sent via the `tcpcomms.py` library to the TA.

| CLI Parameters | Description |
| --- | --- |
| `-c` | Enables XML to IMF compression |
| `-v`| Enable verbose mode |
| `-e`| Enable encryption mode |
| `-t [n]` | Sends usage data every *n* seconds |
| `-r [k]` | Attempts *k* retransmissions |
| `-a [ta_ip]` | Defines target TA IPv6 address |
| `-h [j]` | Specifies the spoofed *house_id* value |

General Usage:
```
sudo python3 ca.py -v -c -h 1 -r 5 -t 10 -a dead:beef::1
```

## ta.py
This program provides full TA functionality for the node. This program should only be run on the designated DODAG node of the system (normally IPv6 address dead:beef::1 by convention). The program is generally executed as:
```
sudo python3 ta.py -e -d [D]
```
| CLI Parameters | Description |
|----------------|-------------|
| `-e` | Enable AES encryption on packets |
| `-d` | Relative path from the calling directory to the SQLite3 database containing the `usages` table, in which the TA will store received usage data

If not explicitly set using the CLI parameters, the database used is set to `dat/power-usages.db` (relative to the directory `ta.py` is called from). The sqlite3 database used by the TA **must** contain a table entitled "usages" which conforms to a predefined schema, given in [init.sql](https://github.com/carleton-smart-grid/smartgrid-comms/blob/master/startup/init.sql). Initial setup of the database can be done trivially using the provide `init.sql` file, given as:
```
sqlite3 database.db < init.sql
```

It is also of interest to note that the `init.sql` file can be used to reset/clear the saved usage values.


## cliReporter.py
This program communicates a node's rank and parent to a [lowpan-visualiser](https://github.com/carleton-smart-grid/lowpan-visualiser) program using UDP over WiFi. This script should be run from a RPi that already has simpleRPL running (using the [startCA script](#startCA.sh) preferably).

The cliReporter must be run from the same directory that RPL is run from (so that it can connect to the *RPL_CLI* socket) The program is run such that:
```
sudo python2 cliReporter.py [IID] [host_ip]
```

Where `IID` is the partial IPv6 address of the node, specifically the section after the initial double colon `dead:beef::`. The parameter `host_ip` is the full IP address of the server running the visualizer. For example, running the cliReporter program on a node with an IPv6 address of `dead:beef::0:1:2:3`, with the lowpan-visualizer program running on host with address 192.168.1.50 would be called as:
```
sudo python cliReporter.py 0:1:2:3 192.168.1.50
```


## udpping.py
TODO





# Usage Instructions for Libraries
## tcpcomms.py
The tcpcomms library contains all the necessary tools needed to send data over the IPv6 6LoWPAN network. Although this **is not** a runnable, the library is built such that it can by used easily from the python console for debugging and demoing purposed. Instructions for using the library are given as follows.

The server (receiver) should first instantiate a tcpcomms server object `server = tcpcomms.Server()`, which will bind to port 4905 by default. After which, calling `packet = server.receive()` will block until a successful TCP transfer has completed, and store the resulting data and source IP address in `packet`. If the data received was packed into an IMF format, calling `data = packer.unpack(data)` will convert the data into XML format.

Sample code for receiving a single data transfer from the python console is given below.
```python
> import tcpcomms as comms    # imports the library
> server = comms.Server()     # creates a server, binding to port 4905
> data = server.receive()     # blocks for data
> print(data)
  'hello world'
>
```

The client (sender) should first define the data to be sent (either as a byte array or string) in a variable `data`. If the data is encoded as a valid XML, it can be converted into IMF format by calling `data = packer.pack(data)`. Then to send the data the method `tcpcomms.send('dead:beef::1', data)` should be called, in which *dead:beef::1* is the destination address.
Sample code for receiving a single data transfer from the python console is given below.

Sample code for sending a single data transfer from the python console is given below.
```python
> import tcpcomms as comms    # imports the library
> addr = 'dead:beef::1'
> data = 'hello world'
> comms.send(addr, data)      # sends data to addr
>
```
The full set of function calls for the tcpcomms library can be found below. It should be noted *additional* exceptions may be raised if the preconditions are not met.

Function Call | Precondition(s) | Postcondition(s)
--------------|---------------|---------------
`send(dest, data)` | <ol> <li> `dest` is a valid IPv6 address, given as type `str` </li> <li> `data` is either of type `str` or `bytearray` </li> </ol> | <ol> <li> `data` is sent to the given `dest` address if reachable </li> <li> An exception is raised if the socket timeouts, or, if the address is unreachable </li> </ol>
`Sever()` | <ol> <li> Port 4905 is free </li> </ol> | <ol> <li> A `Server` type object is returned </li> <li> Port 4905 is bound </li> </ol>
`Server.setup()` | <ol> <li> Port 4905 is free </li> <li> The Server object is not currently setup | <ol> <li> Port 4905 is bound </li> </ol>
`Server.teardown()` | None | <ol> <li> `Server.serversocket` is unbound </li> </ol>
`Server.receive()` | <ol> <li> Server is setup </li> </ol> | <ol> <li> The received data is returned as type `bytearray` </li> </ol>



## packer.py
`packer.py` is a library for packing and unpacking XML to IMF and vice versa. It contains two main functions: `pack()` and `unpack(xml)`.

The `pack(xml)` function should be used to convert valid XML-formated usage data to an IMF format. To use, simply call as `imf = packer.pack(xml)`, in which xml is a valid XML-formated string. The function will return a *bytearray* type object.

The `unpack()` function takes a valid IMF *bytearray* object as input and returns the usage data as an XML formated string. If an XML formated string is given as an input, the returned XML will simply be the given XML such that: **(xml → xml) ∧ (¬xml → unpack xml)**. Calling the unpack function may throw exceptions: `indexException` or `etree.ElementTree.ParseError`.

The full set of function calls for the packer library can be found below. It should be noted *additional* exceptions may be raised if the preconditions are not met.

Function Call | Precondition(s) | Postcondition(s)
--------------|-----------------|---------------
`pack(xmlContents)` | <ol> <li> `xmlContents` is given as type `str` </li> <li> `xmlContents` matches the expected XML tag/attribute/element structure, refer to [packet-format.md](https://github.com/carleton-smart-grid/smartgrid-comms/blob/master/mesh-comms/packet-format.md) </li> </ol> | <ol> <li> Returns the contents of `xmlContents` as a valid IMF of type `bytearray` (length of 14 bytes) </li> </ol>
`unpack(packetContents)` | <ol> <li> `packetContents` is a valid IMF of type `bytearray`, and is the expected length of 14 Bytes </li> <li> `packetContents` is of type `str` and matches the expect XML tag/attribute/element structure </li> </ol> | <ol> <li> Returns an XML formated representation of `packetContents` of type `str` (if `packetContents` was given as an XML, merely returns `packetContents`) </li> <li> Throws `indexException` if `packetContents` is not expected length of 14 Bytes AND `packetContents` is of type `bytearray` </li> <li> Throws `xml.etree.ElementTree.ParseError` if `packetContents` is not a valid XML AND `packetContents` is of type `str` </li> </ol>
`floatToBytes(num)` | <ol> <li> `num` is of type `float` </li> </ol> | <ol> <li> Returns an IEEE-754 floating point encoded as type `bytearray`, of length 4 </li> <li> Returned `bytearray` is encoded using *little endian* schema (LSB at 0) </li> </ol>
`bytesToFloat(bytes)` | <ol> <li> `bytes` is of type `bytearray` with a length of 4 <li> <li> `bytes` is an IEEE-754 floating point encoded as little endian (LSB at 0) </li> </ol> | <ol> <li> Returns a `float` type representation </li> </ol>
`intToBits(num, minLength)` | <ol> <li> `num` and `minLength` are of type `int` </li> </ol> | <ol> <li> Returns type `str` equal to `num` as a binary string (ie a string of only 1 and 0 characters) </li> <li> Returned string is guaranteed to be at least `minLength` in length. Resulting string will be 0 padded to satisfy this condition </li> </ol>
`bytesToInt(bytes)` | <ol> <li> `bytes` of of type `bytearray` or `bytes` </li> <li> `bytes` is encoded using little endian schema (LSB at 0)</li> </ol> | <ol> <li> Returns type `int` equal to the value of all entries in `bytes` read as one unsigned integer </li> </ol>
`printableByteArray(arr)` | <ol> <li> `arr` is given as type `bytearray` </li> </ol> | <ol> <li> Returns a human-readable string (type `str`) of the hex values in `arr` (ie 0x03 0xF3 0x4D) </li> </ol>



## aestools.py
Contains three functions that are used by `ca.py` and `encryptiontool.py`, `key = aestools.generateKey()` which returns a 16 byte random key to use for AES encryption. The other two functions `data = aestools.encryptAES(data, key)` and `data = aestools.decryptAES(data, key)` both do exactly as the name implies. Encrypt takes unencrypted data and an AES key and returns encrypted data, the other takes encrypted data and a key to return usable data.


## rsatools.py
Contains three functions that are used by `ca.py` and `encryptiontool.py`, `rsatools.generateKey()` which saves both a full key pair and a public key to a specific directory (currently the current directory). The other two functions `data = rsatools.encryptRSA(data, key)` and `data = rsatools.decryptRSA(data, key)` both do exactly as the name implies. Encrypt takes unencrypted data and an public RSA key and returns encrypted data, the other takes encrypted data and a private RSA key to return usable data.


## encryptiontool.py
TODO
