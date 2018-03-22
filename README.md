# Contents
The **smartgrid-comms** repository contains all the code, scripts, and other resources needed for the actual transfer of usage data over 6LoWPAN. Please note that the goal of this repository *is not* to handle or perform mesh networking, instead [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is used to handle data routing for a successful mesh network.

All programs written operate on port 4907. Please ensure no other application is bound to that port *before* running anything.

```
└── .
    ├──cliReporter
    |   └── cliReporter.py
    |
    ├── mesh-comms
    |   ├── init.sql
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
    |   └── udpping.py
    |
    ├── README.md
    └── useful-cmds.md
```
### Directory: mesh-comms
The `mesh-comms` directory contains all the relative code/scripts to send, encrypt, pack/unpack, and receive usage data using TCP data transfer. It also contains the main runnables for the **TA** and **CA stub**.

### Directory: startup
The `startup` directory contains scripts used to configure the LoWPAN radios and configure/start Simple RPL routing.

### Directory: test-util
The `test-util` directory contains any auxiliary code used to test the various parameters of the mesh network.

### Directory: cliReporter
This contains the CLI reporter python script which reports the status of a 6LoWPAN RPL node to a [lowpan-visualizer](https://github.com/carleton-smart-grid/lowpan-visualizer) via WiFi connection.



# Usage Instructions
### startCA.sh
Configuring the 6LoWPAN (as `lowpan0`) interface for a **CA**, and starting [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is done trivially through: `sudo ./startCA.sh`.

It should be noted that in order to use the [cliRPL.py](https://github.com/carleton-smart-grid/simpleRPL#getting-information-on-a-running-instance) tool to discern node information or to run administration functions, `./startCA.sh` should be run in the root directory of `simpleRPL` (ie the directory containing the files `cliRPL.py` and `simpleRPL.py`).

### startTA.sh
Configuring the 6LoWPAN (as `lowpan0`) interface for a **TA**, and starting [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is done trivially through: `sudo ./startTA.sh`.

It should be noted that in order to use the [cliRPL.py](https://github.com/carleton-smart-grid/simpleRPL#getting-information-on-a-running-instance) tool to discern node information or to run administration functions, `./startTA.sh` should be run in the root directory of `simpleRPL` (ie the directory containing the files `cliRPL.py` and `simpleRPL.py`).

### cliReporter.py
This script should be run from a RPi that already has [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) running (using the [startCA script](#startCA.sh) preferably).

This script should be run in the directory that Simple RPL was started in, as it contains the sockets that are required to access the RPL metadata.
```
sudo python [full path]/cliReporter/cliReporter.py [prefix] [host_ip]
```
Where `prefix` is everything after the `fe80::` on the `lowpan0` interface and `host_ip` is the IP address of the server running the visualizer

### tcpcomms.py
The server (receiver) should first instantiate a tcpcomms server object `server = tcpcomms.Server()`, which will bind to port 4905 by default. After which, calling `packet = server.receive()` will block until a successful TCP transfer has completed, and store the resulting data and source IP address in `packet`. If the data received was packed into an IMF format, calling `data = packer.unpack(data)` will convert the data into XML format.

The client (sender) should first define the data to be sent (either as a byte array or string) in a variable `data`. If the data is encoded as a valid XML, it can be converted into IMF format by calling `data = packer.pack(data)`. Then to send the data the method `tcpcomms.send('dead:beef::1', data)` should be called, in which *dead:beef::1* is the destination address.

### ca.py
Provides a runnable **CA stub** that generates a pseudorandom _currentload_ and _forecastload_ which is subsequently sent via the `tcpcomms.py` library to the TA.

| CLI parameters | Description |
| --- | --- |
| `-c` | Enables XML to IMF compression |
| `-v`| Enable verbose mode |
| `-e`| Enable encryption mode |
| `-t [n]` | Sends usage data every _n_ seconds |
| `-r [k]` | Attempts _k_ retransmissions |
| `-a [ta_ip]` | Defines target TA IPv6 address |
| `-h [j]` | Specifies the spoofed _Home ID_ |

#### General Usage
`sudo python3 ca.py -v -c -h 1 -r 5 -t 10 -a dead:beef::1`

### ta.py

This is the script that should be running on the TA to receive information and put it in the database

| CLI parameters | Description |
| --- | --- |
| `-v`| Enable verbose mode |
| `-e`| Enable encryption mode |

#### General Usage
`sudo python3 ta.py -v [-e] -d database.db`

Ta.py handles interrupts gracefully, SIGKILL (2, ^C) will kill the program and close any open sockets. SIGQUIT (3, ^\\) will break the current iteration of the loop, this is useful for when SYNACKs are lost in the mesh and the receive socket livelocks (this appears to be a TCP 'bug' of sorts). Of course, any data currently in the socket will be lost.

### udpping.py
TODO

### Packer.py
Packer.py is a library for packing and unpacking XML to IMF and vice versa. It contains two main functions: `pack()` and `unpack(xml)`.

The `pack(xml)` function should be used to convert valid XML-formated usage data to an IMF format. To use, simply call as `imf = packer.pack(xml)`, in which xml is a valid XML-formated string. The function will return a *bytearray* type object.

The `unpack()` function takes a valid IMF *bytearray* object as input and returns the usage data as an XML formated string. If an XML formated string is given as an input, the returned XML will simply be the given XML such that: `(xml → xml) ∧ (¬xml → unpack xml)`. Calling the unpack function _**may throw exceptions: `indexException` or `etree.ElementTree.ParseError`**_.

### aestools.py
Contains three functions that are used by `ca.py` and `encryptiontool.py`, `key = aestools.generateKey()` which returns a 16 byte random key to use for AES encryption. The other two functions `data = aestools.encryptAES(data, key)` and `data = aestools.decryptAES(data, key)` both do exactly as the name implies. Encrypt takes unencrypted data and an AES key and returns encrypted data, the other takes encrypted data and a key to return usable data.

### rsatools.py
Contains three functions that are used by `ca.py` and `encryptiontool.py`, `rsatools.generateKey()` which saves both a full key pair and a public key to a specific directory (currently the current directory). The other two functions `data = rsatools.encryptRSA(data, key)` and `data = rsatools.decryptRSA(data, key)` both do exactly as the name implies. Encrypt takes unencrypted data and an public RSA key and returns encrypted data, the other takes encrypted data and a private RSA key to return usable data.

### encryptiontool.py
TODO
