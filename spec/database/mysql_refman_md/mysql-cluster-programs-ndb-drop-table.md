### 25.5.11 ndb\_drop\_table — Drop an NDB Table

[**ndb\_drop\_table**](mysql-cluster-programs-ndb-drop-table.md "25.5.11 ndb_drop_table — Drop an NDB Table") drops the specified
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") table. (If you try to use this
on a table created with a storage engine other than
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0"), the attempt fails with the
error 723: No such table exists.) This
operation is extremely fast; in some cases, it can be an order
of magnitude faster than using a MySQL [`DROP
TABLE`](drop-table.md "15.1.32 DROP TABLE Statement") statement on an [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")
table.

#### Usage

```terminal
ndb_drop_table -c connection_string tbl_name -d db_name
```

Options that can be used with [**ndb\_drop\_table**](mysql-cluster-programs-ndb-drop-table.md "25.5.11 ndb_drop_table — Drop an NDB Table")
are shown in the following table. Additional descriptions follow
the table.

**Table 25.33 Command-line options used with the program ndb\_drop\_table**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--character-sets-dir=path` | Directory containing character sets | REMOVED: 8.0.31 |
| `--connect-retries=#` | Number of times to retry connection before giving up | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retry-delay=#` | Number of seconds to wait between attempts to contact management server | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-string=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--core-file` | Write core file on error; used in debugging | REMOVED: 8.0.31 |
| `--database=name`,  `-d name` | Name of database in which table is found | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection_string`,  `-c connection_string` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--character-sets-dir`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`--connect-retries`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-connectstring).
- [`--core-file`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--database`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_database),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--database=name` |
  | Type | String |
  | Default Value | `TEST_DB` |

  Name of the database in which the table resides.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--help`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--login-path`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--ndb-connectstring`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connect string for connecting to ndb\_mgmd. Syntax:
  "[nodeid=id;][host=]hostname[:port]". Overrides entries in
  NDB\_CONNECTSTRING and my.cnf.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-connectstring).
- [`--ndb-nodeid`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-connectstring).
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--no-defaults`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--usage`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as
  [`--help`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_help).
- [`--version`](mysql-cluster-programs-ndb-drop-table.md#option_ndb_drop_table_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
