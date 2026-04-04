#### 25.4.3.4 Defining Computers in an NDB Cluster

The `[computer]` section has no real
significance other than serving as a way to avoid the need of
defining host names for each node in the system. All parameters
mentioned here are required.

- `Id`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | string |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Initial System Restart:**Requires a complete shutdown of the cluster, wiping and restoring the cluster file system from a [backup](mysql-cluster-backup.md "25.6.8 Online Backup of NDB Cluster"), and then restarting the cluster. (NDB 8.0.13) |

  This is a unique identifier, used to refer to the host
  computer elsewhere in the configuration file.

  Important

  The computer ID is *not* the same as
  the node ID used for a management, API, or data node.
  Unlike the case with node IDs, you cannot use
  `NodeId` in place of
  `Id` in the `[computer]`
  section of the `config.ini` file.
- `HostName`

  |  |  |
  | --- | --- |
  | Version (or later) | NDB 8.0.13 |
  | Type or units | name or IP address |
  | Default | [...] |
  | Range | ... |
  | Restart Type | **Node Restart:**Requires a [rolling restart](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster") of the cluster. (NDB 8.0.13) |

  This is the computer's hostname or IP address.

**Restart types.**
Information about the restart types used by the parameter
descriptions in this section is shown in the following table:

**Table 25.8 NDB Cluster restart types**

| Symbol | Restart Type | Description |
| --- | --- | --- |
| N | Node | The parameter can be updated using a rolling restart (see [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster")) |
| S | System | All cluster nodes must be shut down completely, then restarted, to effect a change in this parameter |
| I | Initial | Data nodes must be restarted using the [`--initial`](mysql-cluster-programs-ndbd.md#option_ndbd_initial) option |
