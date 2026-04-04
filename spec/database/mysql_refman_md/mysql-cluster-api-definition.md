#### 25.4.3.7 Defining SQL and Other API Nodes in an NDB Cluster

The `[mysqld]` and `[api]`
sections in the `config.ini` file define the
behavior of the MySQL servers (SQL nodes) and other applications
(API nodes) used to access cluster data. None of the parameters
shown is required. If no computer or host name is provided, any
host can use this SQL or API node.

Generally speaking, a `[mysqld]` section is
used to indicate a MySQL server providing an SQL interface to
the cluster, and an `[api]` section is used for
applications other than [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") processes
accessing cluster data, but the two designations are actually
synonymous; you can, for instance, list parameters for a MySQL
server acting as an SQL node in an `[api]`
section.

Note

For a discussion of MySQL server options for NDB Cluster, see
[Section 25.4.3.9.1, “MySQL Server Options for NDB Cluster”](mysql-cluster-options-variables.md#mysql-cluster-program-options-mysqld "25.4.3.9.1 MySQL Server Options for NDB Cluster"). For
information about MySQL server system variables relating to
NDB Cluster, see
[Section 25.4.3.9.2, “NDB Cluster System Variables”](mysql-cluster-options-variables.md#mysql-cluster-system-variables "25.4.3.9.2 NDB Cluster System Variables").

- `Id`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | [...] |
  | Range | 1 - 255 |
  | Restart Type | **Initial System Restart:**Requires a complete shutdown of the cluster, wiping and restoring the cluster file system from a [backup](mysql-cluster-backup.md "25.6.8 Online Backup of NDB Cluster"), and then restarting the cluster. (NDB 8.0.13) |

  The `Id` is an integer value used to
  identify the node in all cluster internal messages. The
  permitted range of values is 1 to 255 inclusive. This value
  must be unique for each node in the cluster, regardless of
  the type of node.

  Note

  In NDB 8.0, data node IDs must be less than 145. If you
  plan to deploy a large number of data nodes, it is a good
  idea to limit the node IDs for API nodes (and management
  nodes) to values greater than 144. (Previously, the
  maximum supported value for a data node ID was 48.)

  [`NodeId`](mysql-cluster-api-definition.md#ndbparam-api-nodeid) is the
  preferred parameter name to use when identifying API nodes.
  (`Id` continues to be supported for
  backward compatibility, but is now deprecated and generates
  a warning when used. It is also subject to future removal.)
- `ConnectionMap`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | string |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Specifies which data nodes to connect.
- `NodeId`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | [...] |
  | Range | 1 - 255 |
  | Restart Type | **Initial System Restart:**Requires a complete shutdown of the cluster, wiping and restoring the cluster file system from a [backup](mysql-cluster-backup.md "25.6.8 Online Backup of NDB Cluster"), and then restarting the cluster. (NDB 8.0.13) |

  The `NodeId` is an integer value used to
  identify the node in all cluster internal messages. The
  permitted range of values is 1 to 255 inclusive. This value
  must be unique for each node in the cluster, regardless of
  the type of node.

  Note

  In NDB 8.0, data node IDs must be less than 145. If you
  plan to deploy a large number of data nodes, it is a good
  idea to limit the node IDs for API nodes (and management
  nodes) to values greater than 144. (Previously, the
  maximum supported value for a data node ID was 48.)

  [`NodeId`](mysql-cluster-api-definition.md#ndbparam-api-nodeid) is the
  preferred parameter name to use when identifying management
  nodes. An alias, `Id`, was used for this
  purpose in very old versions of NDB Cluster, and continues
  to be supported for backward compatibility; it is now
  deprecated and generates a warning when used, and is subject
  to removal in a future release of NDB Cluster.
- `ExecuteOnComputer`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | name |
  | Default | [...] |
  | Range | ... |
  | Deprecated | Yes (in NDB 7.5) |
  | Restart Type | **System Restart:**Requires a complete shutdown and restart of the cluster. (NDB 8.0.13) |

  This refers to the `Id` set for one of the
  computers (hosts) defined in a `[computer]`
  section of the configuration file.

  Important

  This parameter is deprecated, and is subject to removal in
  a future release. Use the
  [`HostName`](mysql-cluster-api-definition.md#ndbparam-api-hostname) parameter
  instead.
- The node ID for this node can be given out only to
  connections that explicitly request it. A management server
  that requests “any” node ID cannot use this
  one. This parameter can be used when running multiple
  management servers on the same host, and
  [`HostName`](mysql-cluster-api-definition.md#ndbparam-api-hostname) is not
  sufficient for distinguishing among processes.
- `HostName`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | name or IP address |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Specifying this parameter defines the hostname of the
  computer on which the SQL node (API node) is to reside.

  If no `HostName` is specified in a given
  `[mysql]` or `[api]`
  section of the `config.ini` file, then an
  SQL or API node may connect using the corresponding
  “slot” from any host which can establish a
  network connection to the management server host machine.
  *This differs from the default behavior for data
  nodes, where `localhost` is assumed for
  `HostName` unless otherwise
  specified*.
- [`LocationDomainId`](mysql-cluster-api-definition.md#ndbparam-api-locationdomainid)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | integer |
  | Default | 0 |
  | Range | 0 - 16 |
  | Restart Type | **System Restart:**Requires a complete shutdown and restart of the cluster. (NDB 8.0.13) |

  Assigns an SQL or other API node to a specific
  [availability
  domain](https://docs.us-phoenix-1.oraclecloud.com/Content/General/Concepts/regions.htm) (also known as an availability zone) within a
  cloud. By informing `NDB` which nodes are
  in which availability domains, performance can be improved
  in a cloud environment in the following ways:

  - If requested data is not found on the same node, reads
    can be directed to another node in the same availability
    domain.
  - Communication between nodes in different availability
    domains are guaranteed to use `NDB`
    transporters' WAN support without any further
    manual intervention.
  - The transporter's group number can be based on
    which availability domain is used, such that also SQL
    and other API nodes communicate with local data nodes in
    the same availability domain whenever possible.
  - The arbitrator can be selected from an availability
    domain in which no data nodes are present, or, if no
    such availability domain can be found, from a third
    availability domain.

  `LocationDomainId` takes an integer value
  between 0 and 16 inclusive, with 0 being the default; using
  0 is the same as leaving the parameter unset.
- `ArbitrationRank`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | 0-2 |
  | Default | 0 |
  | Range | 0 - 2 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter defines which nodes can act as arbitrators.
  Both management nodes and SQL nodes can be arbitrators. A
  value of 0 means that the given node is never used as an
  arbitrator, a value of 1 gives the node high priority as an
  arbitrator, and a value of 2 gives it low priority. A normal
  configuration uses the management server as arbitrator,
  setting its `ArbitrationRank` to 1 (the
  default for management nodes) and those for all SQL nodes to
  0 (the default for SQL nodes).

  By setting `ArbitrationRank` to 0 on all
  management and SQL nodes, you can disable arbitration
  completely. You can also control arbitration by overriding
  this parameter; to do so, set the
  [`Arbitration`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-arbitration)
  parameter in the `[ndbd default]` section
  of the `config.ini` global configuration
  file.
- `ArbitrationDelay`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | milliseconds |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Setting this parameter to any other value than 0 (the
  default) means that responses by the arbitrator to
  arbitration requests are delayed by the stated number of
  milliseconds. It is usually not necessary to change this
  value.
- [`BatchByteSize`](mysql-cluster-api-definition.md#ndbparam-api-batchbytesize)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 16K |
  | Range | 1K - 1M |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  For queries that are translated into full table scans or
  range scans on indexes, it is important for best performance
  to fetch records in properly sized batches. It is possible
  to set the proper size both in terms of number of records
  ([`BatchSize`](mysql-cluster-api-definition.md#ndbparam-api-batchsize)) and in
  terms of bytes (`BatchByteSize`). The
  actual batch size is limited by both parameters.

  The speed at which queries are performed can vary by more
  than 40% depending upon how this parameter is set.

  This parameter is measured in bytes. The default value is
  16K.
- [`BatchSize`](mysql-cluster-api-definition.md#ndbparam-api-batchsize)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | records |
  | Default | 256 |
  | Range | 1 - 992 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter is measured in number of records and is by
  default set to 256. The maximum size is 992.
- [`ExtraSendBufferMemory`](mysql-cluster-api-definition.md#ndbparam-api-extrasendbuffermemory)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter specifies the amount of transporter send
  buffer memory to allocate in addition to any that has been
  set using
  [`TotalSendBufferMemory`](mysql-cluster-api-definition.md#ndbparam-api-totalsendbuffermemory),
  [`SendBufferMemory`](mysql-cluster-tcp-definition.md#ndbparam-tcp-sendbuffermemory), or
  both.
- [`HeartbeatThreadPriority`](mysql-cluster-api-definition.md#ndbparam-api-heartbeatthreadpriority)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | string |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Use this parameter to set the scheduling policy and priority
  of heartbeat threads for management and API nodes. The
  syntax for setting this parameter is shown here:

  ```simple
  HeartbeatThreadPriority = policy[, priority]

  policy:
    {FIFO | RR}
  ```

  When setting this parameter, you must specify a policy. This
  is one of `FIFO` (first in, first in) or
  `RR` (round robin). This followed
  optionally by the priority (an integer).
- [`MaxScanBatchSize`](mysql-cluster-api-definition.md#ndbparam-api-maxscanbatchsize)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 256K |
  | Range | 32K - 16M |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  The batch size is the size of each batch sent from each data
  node. Most scans are performed in parallel to protect the
  MySQL Server from receiving too much data from many nodes in
  parallel; this parameter sets a limit to the total batch
  size over all nodes.

  The default value of this parameter is set to 256KB. Its
  maximum size is 16MB.
- `TotalSendBufferMemory`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | bytes |
  | Default | 0 |
  | Range | 256K - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter is used to determine the total amount of
  memory to allocate on this node for shared send buffer
  memory among all configured transporters.

  If this parameter is set, its minimum permitted value is
  256KB; 0 indicates that the parameter has not been set. For
  more detailed information, see
  [Section 25.4.3.14, “Configuring NDB Cluster Send Buffer Parameters”](mysql-cluster-config-send-buffers.md "25.4.3.14 Configuring NDB Cluster Send Buffer Parameters").
- [`AutoReconnect`](mysql-cluster-api-definition.md#ndbparam-api-autoreconnect)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | boolean |
  | Default | false |
  | Range | true, false |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter is `false` by default. This
  forces disconnected API nodes (including MySQL Servers
  acting as SQL nodes) to use a new connection to the cluster
  rather than attempting to re-use an existing one, as re-use
  of connections can cause problems when using
  dynamically-allocated node IDs. (Bug #45921)

  Note

  This parameter can be overridden using the NDB API. For
  more information, see
  [Ndb\_cluster\_connection::set\_auto\_reconnect()](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.html#ndb-ndb-cluster-connection-set-auto-reconnect),
  and
  [Ndb\_cluster\_connection::get\_auto\_reconnect()](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.html#ndb-ndb-cluster-connection-get-auto-reconnect).
- [`DefaultOperationRedoProblemAction`](mysql-cluster-api-definition.md#ndbparam-api-defaultoperationredoproblemaction)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | enumeration |
  | Default | QUEUE |
  | Range | ABORT, QUEUE |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This parameter (along with
  [`RedoOverCommitLimit`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-redoovercommitlimit)
  and
  [`RedoOverCommitCounter`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-redoovercommitcounter))
  controls the data node's handling of operations when
  too much time is taken flushing redo logs to disk. This
  occurs when a given redo log flush takes longer than
  [`RedoOverCommitLimit`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-redoovercommitlimit)
  seconds, more than
  [`RedoOverCommitCounter`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-redoovercommitcounter)
  times, causing any pending transactions to be aborted.

  When this happens, the node can respond in either of two
  ways, according to the value of
  `DefaultOperationRedoProblemAction`, listed
  here:

  - `ABORT`: Any pending operations from
    aborted transactions are also aborted.
  - `QUEUE`: Pending operations from
    transactions that were aborted are queued up to be
    re-tried. This the default. Pending operations are still
    aborted when the redo log runs out of space—that
    is, when P\_TAIL\_PROBLEM errors
    occur.
- [`DefaultHashMapSize`](mysql-cluster-api-definition.md#ndbparam-api-defaulthashmapsize)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | buckets |
  | Default | 3840 |
  | Range | 0 - 3840 |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  The size of the table hash maps used by
  [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") is configurable using this
  parameter. `DefaultHashMapSize` can take
  any of three possible values (0, 240, 3840). These values
  and their effects are described in the following table.

  **Table 25.17 DefaultHashMapSize parameter values**

  | Value | Description / Effect |
  | --- | --- |
  | `0` | Use the lowest value set, if any, for this parameter among all data nodes and API nodes in the cluster; if it is not set on any data or API node, use the default value. |
  | `240` | Old default hash map size |
  | `3840` | Hash map size used by default in NDB 8.0 |

  The original intended use for this parameter was to
  facilitate upgrades and downgrades to and from older NDB
  Cluster versions, in which the hash map size differed, due
  to the fact that this change was not otherwise backward
  compatible. This is not an issue when upgrading to or
  downgrading from NDB Cluster 8.0.
- [`Wan`](mysql-cluster-api-definition.md#ndbparam-api-wan)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | boolean |
  | Default | false |
  | Range | true, false |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Use WAN TCP setting as default.
- [`ConnectBackoffMaxTime`](mysql-cluster-api-definition.md#ndbparam-api-connectbackoffmaxtime)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | integer |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  In an NDB Cluster with many unstarted data nodes, the value
  of this parameter can be raised to circumvent connection
  attempts to data nodes which have not yet begun to function
  in the cluster, as well as moderate high traffic to
  management nodes. As long as the API node is not connected
  to any new data nodes, the value of the
  [`StartConnectBackoffMaxTime`](mysql-cluster-api-definition.md#ndbparam-api-startconnectbackoffmaxtime)
  parameter is applied; otherwise,
  `ConnectBackoffMaxTime` is used to
  determine the length of time in milliseconds to wait between
  connection attempts.

  Time elapsed *during* node connection
  attempts is not taken into account when calculating elapsed
  time for this parameter. The timeout is applied with
  approximately 100 ms resolution, starting with a 100 ms
  delay; for each subsequent attempt, the length of this
  period is doubled until it reaches
  `ConnectBackoffMaxTime` milliseconds, up to
  a maximum of 100000 ms (100s).

  Once the API node is connected to a data node and that node
  reports (in a heartbeat message) that it has connected to
  other data nodes, connection attempts to those data nodes
  are no longer affected by this parameter, and are made every
  100 ms thereafter until connected. Once a data node has
  started, it can take up
  [`HeartbeatIntervalDbApi`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-heartbeatintervaldbapi)
  for the API node to be notified that this has occurred.
- [`StartConnectBackoffMaxTime`](mysql-cluster-api-definition.md#ndbparam-api-startconnectbackoffmaxtime)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | integer |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  In an NDB Cluster with many unstarted data nodes, the value
  of this parameter can be raised to circumvent connection
  attempts to data nodes which have not yet begun to function
  in the cluster, as well as moderate high traffic to
  management nodes. As long as the API node is not connected
  to any new data nodes, the value of the
  `StartConnectBackoffMaxTime` parameter is
  applied; otherwise,
  [`ConnectBackoffMaxTime`](mysql-cluster-api-definition.md#ndbparam-api-connectbackoffmaxtime)
  is used to determine the length of time in milliseconds to
  wait between connection attempts.

  Time elapsed *during* node connection
  attempts is not taken into account when calculating elapsed
  time for this parameter. The timeout is applied with
  approximately 100 ms resolution, starting with a 100 ms
  delay; for each subsequent attempt, the length of this
  period is doubled until it reaches
  `StartConnectBackoffMaxTime` milliseconds,
  up to a maximum of 100000 ms (100s).

  Once the API node is connected to a data node and that node
  reports (in a heartbeat message) that it has connected to
  other data nodes, connection attempts to those data nodes
  are no longer affected by this parameter, and are made every
  100 ms thereafter until connected. Once a data node has
  started, it can take up
  [`HeartbeatIntervalDbApi`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-heartbeatintervaldbapi)
  for the API node to be notified that this has occurred.

**API Node Debugging Parameters.**
You can use the `ApiVerbose` configuration
parameter to enable debugging output from a given API node.
This parameter takes an integer value. 0 is the default, and
disables such debugging; 1 enables debugging output to the
cluster log; 2 adds [`DBDICT`](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-kernel-blocks-dbdict.html)
debugging output as well. (Bug #20638450) See also
[DUMP 1229](https://dev.mysql.com/doc/ndb-internals/en/dump-command-1229.html).

You can also obtain information from a MySQL server running as
an NDB Cluster SQL node using [`SHOW
STATUS`](show-status.md "15.7.7.37 SHOW STATUS Statement") in the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client, as
shown here:

```sql
mysql> SHOW STATUS LIKE 'ndb%';
+-----------------------------+----------------+
| Variable_name               | Value          |
+-----------------------------+----------------+
| Ndb_cluster_node_id         | 5              |
| Ndb_config_from_host        | 198.51.100.112 |
| Ndb_config_from_port        | 1186           |
| Ndb_number_of_storage_nodes | 4              |
+-----------------------------+----------------+
4 rows in set (0.02 sec)
```

For information about the status variables appearing in the
output from this statement, see
[Section 25.4.3.9.3, “NDB Cluster Status Variables”](mysql-cluster-options-variables.md#mysql-cluster-status-variables "25.4.3.9.3 NDB Cluster Status Variables").

Note

To add new SQL or API nodes to the configuration of a running
NDB Cluster, it is necessary to perform a rolling restart of
all cluster nodes after adding new `[mysqld]`
or `[api]` sections to the
`config.ini` file (or files, if you are
using more than one management server). This must be done
before the new SQL or API nodes can connect to the cluster.

It is *not* necessary to perform any
restart of the cluster if new SQL or API nodes can employ
previously unused API slots in the cluster configuration to
connect to the cluster.

**Restart types.**
Information about the restart types used by the parameter
descriptions in this section is shown in the following table:

**Table 25.18 NDB Cluster restart types**

| Symbol | Restart Type | Description |
| --- | --- | --- |
| N | Node | The parameter can be updated using a rolling restart (see [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster")) |
| S | System | All cluster nodes must be shut down completely, then restarted, to effect a change in this parameter |
| I | Initial | Data nodes must be restarted using the [`--initial`](mysql-cluster-programs-ndbd.md#option_ndbd_initial) option |
