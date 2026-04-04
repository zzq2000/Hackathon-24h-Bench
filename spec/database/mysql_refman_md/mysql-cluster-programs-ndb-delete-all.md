### 25.5.8 ndb\_delete\_all — Delete All Rows from an NDB Table

[**ndb\_delete\_all**](mysql-cluster-programs-ndb-delete-all.md "25.5.8 ndb_delete_all — Delete All Rows from an NDB Table") deletes all rows from the
given [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") table. In some cases,
this can be much faster than
[`DELETE`](delete.md "15.2.2 DELETE Statement") or even
[`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement").

#### Usage

```terminal
ndb_delete_all -c connection_string tbl_name -d db_name
```

This deletes all rows from the table named
*`tbl_name`* in the database named
*`db_name`*. It is exactly equivalent to
executing `TRUNCATE
db_name.tbl_name`
in MySQL.

Options that can be used with [**ndb\_delete\_all**](mysql-cluster-programs-ndb-delete-all.md "25.5.8 ndb_delete_all — Delete All Rows from an NDB Table")
are shown in the following table. Additional descriptions follow
the table.

**Table 25.30 Command-line options used with the program ndb\_delete\_all**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--character-sets-dir=path` | Directory containing character sets | REMOVED: 8.0.31 |
| `--connect-retries=#` | Number of times to retry connection before giving up | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retry-delay=#` | Number of seconds to wait between attempts to contact management server | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-string=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--core-file` | Write core file on error; used in debugging | REMOVED: 8.0.31 |
| `--database=name`,  `-d name` | Name of the database in which the table is found | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--diskscan` | Perform disk scan | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection_string`,  `-c connection_string` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--transactional`,  `-t` | Perform delete in one single transaction; possible to run out of operations when used | (Supported in all NDB releases based on MySQL 8.0) |
| `--tupscan` | Perform tuple scan | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--character-sets-dir`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`--connect-retries`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-connectstring).
- [`--core-file`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--database`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_database),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--database=name` |
  | Type | String |
  | Default Value | `TEST_DB` |

  Name of the database containing the table to delete from.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--diskscan`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_diskscan)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--diskscan` |

  Run a disk scan.
- [`--help`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--login-path`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--ndb-connectstring`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connect string for connecting to ndb\_mgmd. Syntax:
  "[nodeid=id;][host=]hostname[:port]". Overrides entries in
  NDB\_CONNECTSTRING and my.cnf.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-connectstring).
- [`--ndb-nodeid`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-connectstring).
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--no-defaults`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--transactional`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_transactional),
  `-t`

  Use of this option causes the delete operation to be
  performed as a single transaction.

  Warning

  With very large tables, using this option may cause the
  number of operations available to the cluster to be
  exceeded.
- [`--tupscan`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_tupscan)

  Run a tuple scan.
- [`--usage`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as
  [`--help`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_help).
- [`--version`](mysql-cluster-programs-ndb-delete-all.md#option_ndb_delete_all_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

In NDB 7.6 and earlier, this program printed
`NDBT_ProgramExit -
status` upon completion of
its run, due to an unnecessary dependency on the
`NDBT` testing library. This dependency has
been removed in NDB 8.0, eliminating the extraneous output.
