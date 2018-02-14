# Contents
The **smartgrid-comms** repository contains all the code, scripts, and other resources needed for the actual transfer of usage data over 6LoWPAN. Please note that the goal of this repository *is not* to handle or perform mesh networking, instead [Simple RPL](https://github.com/carleton-smart-grid/simpleRPL) is used to handle data routing for a successful mesh network.

All programs written operate on port 4907. Please ensure no other application is bound to that port *before* running anything.

```
└── .
    ├── mesh-comms
    |   ├── init.sql
    |   ├── packer.py
    |   ├── tcpcomms.py
    |   ├── ta.py
    |   └── packet-format.md
    |
    ├── startup
    |   ├── startCA.sh
    |   └── startTA.sh
    |
    ├── test-util
    |   └── udpping.py
    |
    ├── README.md
    ├── useful-cmds.md
```
### Directory: mesh-comms
The `mesh-comms` directory contains all the relative code/scripts to send, encrypt, pack/unpack, and receive usage data using TCP data transfer. It also contains the main runnables for the **TA** and **CA stub**.

### Directory: startup
The `startup` directory contains scripts used to configure the LoWPAN radios and configure/start Simple RPL routing.

### Directory: test-util
The `test-util` directory contains any auxiliary code used to test the various parameters of the mesh network.



# Usage Instructions
### tcpcomms.py
The server (receiver) should first instantiate a tcpcomms server object `server = tcpcomms.Server()`, which will bind to port 4905 by default. After which, calling `data = server.receive()` will block until a successful TCP transfer has completed, and store the resulting data in `data`. If the data received was packed into an IMF format, calling `data = packer.unpack(data)` will convert the data into XML format.

The client (sender) should first define the data to be sent (either as a byte array or string) in a variable `data`. If the data is encoded as a valid XML, it can be converted into IMF format by calling `data = packer.pack(data)`. Then to send the data the method `tcpcomms.send('dead:beef::1', data)` should be called, in which *dead:beef::1* is the destination address.

### udpping.py
TODO
