
## Format Flow

The purpose of adding an intermediate format...

```
(XML format)                                     (XML format)
     |                                                 |
     |                                                 |
     |                                                 |
(IMF format)                                     (IMF format)
     |                                                 |
     |                                                 |
     |                                                 |
     └── [node 1] ──────── ..... ────────── [node n] ──┘

```

## XML Format

The XML format used is assumed to be of the format:

```xml
<usagedata>
 <homeid> 01 </homeid>
 <time> 01-01-15 15:00 </time>
 <currentload> 1.608475556 </currentload>
 <forecastload> 2.5 </forecastload>
 <negociate> Yes </negociate>
 <negociateload> Full </negociateload>
 <greenenergy> 1 </greenenergy>
</usagedata>
```

Each child of the root `usagedata` is given in full, even if the entry is empty. For instance, if there is no value for `currentload`, `currentload` is to be given simple as `<currentload></currentload>`.


## IMF Format

The **Intra-Mesh Format** (IMF) is solely used while data is traveling from source to destination over the mesh network.

Due to small packet sizes and the lossy nature of 6LoWPAN mesh networks, minimalization of packets is crucial. By removing all the overhead from the desired XML format, packet size can be shrunk significantly.

It should be noted at all words and double-words are encoded using the **litle endian** schema (ie. the *least* significant byte is given first).

The structure of an IMF formated packet is as follows:

Value | Byte Number | Bit Range | Total Bits | Encoded As
----- | ----------- | --------- | ---------- | ----------
Home ID | 0 | 0 - 7 | 8 | Unsigned Int
Time | 1 - 4 | 8 - 39 | 32 | UNIX timestamp
Current Load | 5 - 8 | 40 - 71 | 32 | IEEE-754 Float
Forecast Load | 9 - 12 | 72 - 103 | 32 | IEEE-754 Float
Negociate | 13 | 104 | 1 | Boolean
Negociate Load | 13 | 105 - 107 | 3 | Unsigned Int
Green Energy | 13 | 108 - 111 | 4 | Unsigned Int

Using this format, the total data can be reduced from 241B to a mere 14B.
