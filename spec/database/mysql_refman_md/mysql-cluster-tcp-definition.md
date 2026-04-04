#### 25.4.3.10 NDB Cluster TCP/IP Connections

TCP/IP is the default transport mechanism for all connections
between nodes in an NDB Cluster. Normally it is not necessary to
define TCP/IP connections; NDB Cluster automatically sets up
such connections for all data nodes, management nodes, and SQL
or API nodes.

Note

For an exception to this rule, see
[Section 25.4.3.11, “NDB Cluster TCP/IP Connections Using Direct Connections”](mysql-cluster-tcp-definition-direct.md "25.4.3.11 NDB Cluster TCP/IP Connections Using Direct Connections").

To override the default connection parameters, it is necessary
to define a connection using one or more
`[tcp]` sections in the
`config.ini` file. Each
`[tcp]` section explicitly defines a TCP/IP
connection between two NDB Cluster nodes, and must contain at a
minimum the parameters
[`NodeId1`](mysql-cluster-tcp-definition.md#ndbparam-tcp-nodeid1) and
[`NodeId2`](mysql-cluster-tcp-definition.md#ndbparam-tcp-nodeid2), as well as any
connection parameters to override.

It is also possible to change the default values for these
parameters by setting them in the `[tcp
default]` section.

Important

Any `[tcp]` sections in the
`config.ini` file should be listed
*last*, following all other sections in the
file. However, this is not required for a `[tcp
default]` section. This requirement is a known issue
with the way in which the `config.ini` file
is read by the NDB Cluster management server.

Connection parameters which can be set in
`[tcp]` and `[tcp default]`
sections of the `config.ini` file are listed
here:

- `AllowUnresolvedHostNames`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.22 |
  | Type or units | boolean |
  | Default | false |
  | Range | true, false |
  | Added | NDB 8.0.22 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  By default, when a management node fails to resolve a host
  name while trying to connect, this results in a fatal error.
  This behavior can be overridden by setting
  `AllowUnresolvedHostNames` to
  `true` in the `[tcp
  default]` section of the global configuration file
  (usually named `config.ini`), in which
  case failure to resolve a host name is treated as a warning
  and [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") startup continues
  uninterrupted.
- `Checksum`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | boolean |
  | Default | false |
  | Range | true, false |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter is disabled by default. When it is enabled
  (set to `Y` or `1`),
  checksums for all messages are calculated before they placed
  in the send buffer. This feature ensures that messages are
  not corrupted while waiting in the send buffer, or by the
  transport mechanism.
- `Group`

  When
  [`ndb_optimized_node_selection`](mysql-cluster-options-variables.md#sysvar_ndb_optimized_node_selection)
  is enabled, node proximity is used in some cases to select
  which node to connect to. This parameter can be used to
  influence proximity by setting it to a lower value, which is
  interpreted as “closer”. See the description of
  the system variable for more information.
- `HostName1`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | name or IP address |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  The `HostName1` and
  [`HostName2`](mysql-cluster-tcp-definition.md#ndbparam-tcp-hostname2) parameters
  can be used to specify specific network interfaces to be
  used for a given TCP connection between two nodes. The
  values used for these parameters can be host names or IP
  addresses.
- `HostName2`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | name or IP address |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  The [`HostName1`](mysql-cluster-tcp-definition.md#ndbparam-tcp-hostname1) and
  `HostName2` parameters can be used to
  specify specific network interfaces to be used for a given
  TCP connection between two nodes. The values used for these
  parameters can be host names or IP addresses.
- `NodeId1`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | numeric |
  | Default | [none] |
  | Range | 1 - 255 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  To identify a connection between two nodes it is necessary
  to provide their node IDs in the `[tcp]`
  section of the configuration file as the values of
  `NodeId1` and
  [`NodeId2`](mysql-cluster-tcp-definition.md#ndbparam-tcp-nodeid2). These are
  the same unique `Id` values for each of
  these nodes as described in
  [Section 25.4.3.7, “Defining SQL and Other API Nodes in an NDB Cluster”](mysql-cluster-api-definition.md "25.4.3.7 Defining SQL and Other API Nodes in an NDB Cluster").
- `NodeId2`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | numeric |
  | Default | [none] |
  | Range | 1 - 255 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  To identify a connection between two nodes it is necessary
  to provide their node IDs in the `[tcp]`
  section of the configuration file as the values of
  [`NodeId1`](mysql-cluster-tcp-definition.md#ndbparam-tcp-nodeid1) and
  `NodeId2`. These are the same unique
  `Id` values for each of these nodes as
  described in [Section 25.4.3.7, “Defining SQL and Other API Nodes in an NDB Cluster”](mysql-cluster-api-definition.md "25.4.3.7 Defining SQL and Other API Nodes in an NDB Cluster").
- [`NodeIdServer`](mysql-cluster-tcp-definition.md#ndbparam-tcp-nodeidserver)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | numeric |
  | Default | [none] |
  | Range | 1 - 63 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Set the server side of a TCP connection.
- `OverloadLimit`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  When more than this many unsent bytes are in the send
  buffer, the connection is considered overloaded.

  This parameter can be used to determine the amount of unsent
  data that must be present in the send buffer before the
  connection is considered overloaded. See
  [Section 25.4.3.14, “Configuring NDB Cluster Send Buffer Parameters”](mysql-cluster-config-send-buffers.md "25.4.3.14 Configuring NDB Cluster Send Buffer Parameters"), for
  more information.
- [`PreferIPVersion`](mysql-cluster-tcp-definition.md#ndbparam-tcp-preferipversion)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.26 |
  | Type or units | enumeration |
  | Default | 4 |
  | Range | 4, 6 |
  | Added | NDB 8.0.26 |
  | Restart Type | **Initial System Restart:**Requires a complete shutdown of the cluster, wiping and restoring the cluster file system from a [backup](mysql-cluster-backup.md "25.6.8 Online Backup of NDB Cluster"), and then restarting the cluster. (NDB 8.0.13) |

  Determines the preference of DNS resolution for IP version 4
  or version 6. Because the configuration retrieval mechanism
  employed by NDB Cluster requires that all connections use
  the same preference, this parameter should be set in the
  `[tcp default]` of the
  `config.ini` global configuration file.
- [`PreSendChecksum`](mysql-cluster-tcp-definition.md#ndbparam-tcp-presendchecksum)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | boolean |
  | Default | false |
  | Range | true, false |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  If this parameter and
  [`Checksum`](mysql-cluster-tcp-definition.md#ndbparam-tcp-checksum) are both
  enabled, perform pre-send checksum checks, and check all TCP
  signals between nodes for errors. Has no effect if
  `Checksum` is not also enabled.
- [`Proxy`](mysql-cluster-tcp-definition.md#ndbparam-tcp-proxy)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | string |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Set a proxy for the TCP connection.
- [`ReceiveBufferMemory`](mysql-cluster-tcp-definition.md#ndbparam-tcp-receivebuffermemory)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 2M |
  | Range | 16K - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Specifies the size of the buffer used when receiving data
  from the TCP/IP socket.

  The default value of this parameter is 2MB. The minimum
  possible value is 16KB; the theoretical maximum is 4GB.
- [`SendBufferMemory`](mysql-cluster-tcp-definition.md#ndbparam-tcp-sendbuffermemory)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 2M |
  | Range | 256K - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  TCP transporters use a buffer to store all messages before
  performing the send call to the operating system. When this
  buffer reaches 64KB its contents are sent; these are also
  sent when a round of messages have been executed. To handle
  temporary overload situations it is also possible to define
  a bigger send buffer.

  If this parameter is set explicitly, then the memory is not
  dedicated to each transporter; instead, the value used
  denotes the hard limit for how much memory (out of the total
  available memory—that is,
  `TotalSendBufferMemory`) that may be used
  by a single transporter. For more information about
  configuring dynamic transporter send buffer memory
  allocation in NDB Cluster, see
  [Section 25.4.3.14, “Configuring NDB Cluster Send Buffer Parameters”](mysql-cluster-config-send-buffers.md "25.4.3.14 Configuring NDB Cluster Send Buffer Parameters").

  The default size of the send buffer is 2MB, which is the
  size recommended in most situations. The minimum size is 64
  KB; the theoretical maximum is 4 GB.
- `SendSignalId`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | boolean |
  | Default | false (debug builds: true) |
  | Range | true, false |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  To be able to retrace a distributed message datagram, it is
  necessary to identify each message. When this parameter is
  set to `Y`, message IDs are transported
  over the network. This feature is disabled by default in
  production builds, and enabled in `-debug`
  builds.
- `TcpBind_INADDR_ANY`

  Setting this parameter to `TRUE` or
  `1` binds `IP_ADDR_ANY` so
  that connections can be made from anywhere (for
  autogenerated connections). The default is
  `FALSE` (`0`).
- [`TcpSpinTime`](mysql-cluster-tcp-definition.md#ndbparam-tcp-tcpspintime)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.20 |
  | Type or units | µsec |
  | Default | 0 |
  | Range | 0 - 2000 |
  | Added | NDB 8.0.20 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Controls spin for a TCP transporter; no enable, set to a
  nonzero value. This works for both the data node and
  management or SQL node side of the connection.
- [`TCP_MAXSEG_SIZE`](mysql-cluster-tcp-definition.md#ndbparam-tcp-tcp_maxseg_size)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 0 |
  | Range | 0 - 2G |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Determines the size of the memory set during TCP transporter
  initialization. The default is recommended for most common
  usage cases.
- [`TCP_RCV_BUF_SIZE`](mysql-cluster-tcp-definition.md#ndbparam-tcp-tcp_rcv_buf_size)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 0 |
  | Range | 0 - 2G |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Determines the size of the receive buffer set during TCP
  transporter initialization. The default and minimum value is
  0, which allows the operating system or platform to set this
  value. The default is recommended for most common usage
  cases.
- [`TCP_SND_BUF_SIZE`](mysql-cluster-tcp-definition.md#ndbparam-tcp-tcp_snd_buf_size)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 0 |
  | Range | 0 - 2G |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Determines the size of the send buffer set during TCP
  transporter initialization. The default and minimum value is
  0, which allows the operating system or platform to set this
  value. The default is recommended for most common usage
  cases.

**Restart types.**
Information about the restart types used by the parameter
descriptions in this section is shown in the following table:

**Table 25.21 NDB Cluster restart types**

| Symbol | Restart Type | Description |
| --- | --- | --- |
| N | Node | The parameter can be updated using a rolling restart (see [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster")) |
| S | System | All cluster nodes must be shut down completely, then restarted, to effect a change in this parameter |
| I | Initial | Data nodes must be restarted using the [`--initial`](mysql-cluster-programs-ndbd.md#option_ndbd_initial) option |
