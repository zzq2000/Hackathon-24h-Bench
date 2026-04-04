#### 25.4.3.8 Defining the System

The `[system]` section is used for parameters
applying to the cluster as a whole. The
[`Name`](mysql-cluster-system-definition.md#ndbparam-system-name) system parameter
is used with MySQL Enterprise Monitor;
[`ConfigGenerationNumber`](mysql-cluster-system-definition.md#ndbparam-system-configgenerationnumber)
and [`PrimaryMGMNode`](mysql-cluster-system-definition.md#ndbparam-system-primarymgmnode) are
not used in production environments. Except when using NDB
Cluster with MySQL Enterprise Monitor, is not necessary to have a
`[system]` section in the
`config.ini` file.

More information about these parameters can be found in the
following list:

- [`ConfigGenerationNumber`](mysql-cluster-system-definition.md#ndbparam-system-configgenerationnumber)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Configuration generation number. This parameter is currently
  unused.
- [`Name`](mysql-cluster-system-definition.md#ndbparam-system-name)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | string |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Set a name for the cluster. This parameter is required for
  deployments with MySQL Enterprise Monitor; it is otherwise unused.

  You can obtain the value of this parameter by checking the
  [`Ndb_system_name`](mysql-cluster-options-variables.md#statvar_Ndb_system_name) status
  variable. In NDB API applications, you can also retrieve it
  using
  [`get_system_name()`](https://dev.mysql.com/doc/ndbapi/en/ndb-ndb-cluster-connection.html#ndb-ndb-cluster-connection-get-system-name).
- [`PrimaryMGMNode`](mysql-cluster-system-definition.md#ndbparam-system-primarymgmnode)

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | unsigned |
  | Default | 0 |
  | Range | 0 - 4294967039 (0xFFFFFEFF) |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  Node ID of the primary management node. This parameter is
  currently unused.

**Restart types.**
Information about the restart types used by the parameter
descriptions in this section is shown in the following table:

**Table 25.19 NDB Cluster restart types**

| Symbol | Restart Type | Description |
| --- | --- | --- |
| N | Node | The parameter can be updated using a rolling restart (see [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster")) |
| S | System | All cluster nodes must be shut down completely, then restarted, to effect a change in this parameter |
| I | Initial | Data nodes must be restarted using the [`--initial`](mysql-cluster-programs-ndbd.md#option_ndbd_initial) option |
