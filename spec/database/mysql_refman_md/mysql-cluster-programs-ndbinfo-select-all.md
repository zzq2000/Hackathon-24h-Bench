### 25.5.2 ndbinfo\_select\_all — Select From ndbinfo Tables

[**ndbinfo\_select\_all**](mysql-cluster-programs-ndbinfo-select-all.md "25.5.2 ndbinfo_select_all — Select From ndbinfo Tables") is a client program that
selects all rows and columns from one or more tables in the
[`ndbinfo`](mysql-cluster-ndbinfo.md "25.6.16 ndbinfo: The NDB Cluster Information Database") database

Not all `ndbinfo` tables available in the
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client can be read by this program (see
later in this section). In addition,
[**ndbinfo\_select\_all**](mysql-cluster-programs-ndbinfo-select-all.md "25.5.2 ndbinfo_select_all — Select From ndbinfo Tables") can show information about
some tables internal to `ndbinfo` which cannot
be accessed using SQL, including the `tables`
and `columns` metadata tables.

To select from one or more `ndbinfo` tables
using [**ndbinfo\_select\_all**](mysql-cluster-programs-ndbinfo-select-all.md "25.5.2 ndbinfo_select_all — Select From ndbinfo Tables"), it is necessary to
supply the names of the tables when invoking the program as
shown here:

```terminal
$> ndbinfo_select_all table_name1  [table_name2] [...]
```

For example:

```terminal
$> ndbinfo_select_all logbuffers logspaces
== logbuffers ==
node_id log_type        log_id  log_part        total   used    high
5       0       0       0       33554432        262144  0
6       0       0       0       33554432        262144  0
7       0       0       0       33554432        262144  0
8       0       0       0       33554432        262144  0
== logspaces ==
node_id log_type        log_id  log_part        total   used    high
5       0       0       0       268435456       0       0
5       0       0       1       268435456       0       0
5       0       0       2       268435456       0       0
5       0       0       3       268435456       0       0
6       0       0       0       268435456       0       0
6       0       0       1       268435456       0       0
6       0       0       2       268435456       0       0
6       0       0       3       268435456       0       0
7       0       0       0       268435456       0       0
7       0       0       1       268435456       0       0
7       0       0       2       268435456       0       0
7       0       0       3       268435456       0       0
8       0       0       0       268435456       0       0
8       0       0       1       268435456       0       0
8       0       0       2       268435456       0       0
8       0       0       3       268435456       0       0
$>
```

Options that can be used with
[**ndbinfo\_select\_all**](mysql-cluster-programs-ndbinfo-select-all.md "25.5.2 ndbinfo_select_all — Select From ndbinfo Tables") are shown in the following
table. Additional descriptions follow the table.

**Table 25.25 Command-line options used with the program ndbinfo\_select\_all**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--character-sets-dir=path` | Directory containing character sets | REMOVED: 8.0.31 |
| `--connect-retries=#` | Number of times to retry connection before giving up | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retry-delay=#` | Number of seconds to wait between attempts to contact management server | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-string=connection-string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--core-file` | Write core file on error; used in debugging | REMOVED: 8.0.31 |
| `--database=db_name`,  `-d` | Name of database where table is located | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--delay=#` | Set delay in seconds between loops | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--loops=#`,  `-l` | Set number of times to perform select | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection-string`,  `-c` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection-string`,  `-c` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--parallelism=#`,  `-p` | Set degree of parallelism | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--character-sets-dir`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`--core-file`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--connect-retries`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection-string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-connectstring).
- [`--defaults-extra-file`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--delay=seconds`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--delay=#` |
  | Type | Numeric |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `MAX_INT` |

  This option sets the number of seconds to wait between
  executing loops. Has no effect if
  [`--loops`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_loops) is set to
  0 or 1.
- [`--help`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--login-path`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--loops=number`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_loops),
  `-l number`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--loops=#` |
  | Type | Numeric |
  | Default Value | `1` |
  | Minimum Value | `0` |
  | Maximum Value | `MAX_INT` |

  This option sets the number of times to execute the select.
  Use [`--delay`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_delay) to
  set the time between loops.
- [`--ndb-connectstring`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection-string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connect string for connecting to ndb\_mgmd. Syntax:
  "[nodeid=id;][host=]hostname[:port]". Overrides entries in
  NDB\_CONNECTSTRING and my.cnf.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection-string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-connectstring).
- [`--ndb-nodeid`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  --ndb-connectstring.
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--no-defaults`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--usage`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as --help.
- [`--version`](mysql-cluster-programs-ndbinfo-select-all.md#option_ndbinfo_select_all_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

[**ndbinfo\_select\_all**](mysql-cluster-programs-ndbinfo-select-all.md "25.5.2 ndbinfo_select_all — Select From ndbinfo Tables") is unable to read the
following tables:

- [`arbitrator_validity_detail`](mysql-cluster-ndbinfo-arbitrator-validity-detail.md "25.6.16.1 The ndbinfo arbitrator_validity_detail Table")
- [`arbitrator_validity_summary`](mysql-cluster-ndbinfo-arbitrator-validity-summary.md "25.6.16.2 The ndbinfo arbitrator_validity_summary Table")
- [`cluster_locks`](mysql-cluster-ndbinfo-cluster-locks.md "25.6.16.6 The ndbinfo cluster_locks Table")
- [`cluster_operations`](mysql-cluster-ndbinfo-cluster-operations.md "25.6.16.7 The ndbinfo cluster_operations Table")
- [`cluster_transactions`](mysql-cluster-ndbinfo-cluster-transactions.md "25.6.16.8 The ndbinfo cluster_transactions Table")
- [`disk_write_speed_aggregate_node`](mysql-cluster-ndbinfo-disk-write-speed-aggregate-node.md "25.6.16.29 The ndbinfo disk_write_speed_aggregate_node Table")
- [`locks_per_fragment`](mysql-cluster-ndbinfo-locks-per-fragment.md "25.6.16.41 The ndbinfo locks_per_fragment Table")
- [`memory_per_fragment`](mysql-cluster-ndbinfo-memory-per-fragment.md "25.6.16.46 The ndbinfo memory_per_fragment Table")
- [`memoryusage`](mysql-cluster-ndbinfo-memoryusage.md "25.6.16.45 The ndbinfo memoryusage Table")
- [`operations_per_fragment`](mysql-cluster-ndbinfo-operations-per-fragment.md "25.6.16.48 The ndbinfo operations_per_fragment Table")
- [`server_locks`](mysql-cluster-ndbinfo-server-locks.md "25.6.16.53 The ndbinfo server_locks Table")
- [`server_operations`](mysql-cluster-ndbinfo-server-operations.md "25.6.16.54 The ndbinfo server_operations Table")
- [`server_transactions`](mysql-cluster-ndbinfo-server-transactions.md "25.6.16.55 The ndbinfo server_transactions Table")
- [`table_info`](mysql-cluster-ndbinfo-table-info.md "25.6.16.58 The ndbinfo table_info Table")
