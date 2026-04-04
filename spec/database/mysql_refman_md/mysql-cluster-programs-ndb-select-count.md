### 25.5.26 ndb\_select\_count — Print Row Counts for NDB Tables

[**ndb\_select\_count**](mysql-cluster-programs-ndb-select-count.md "25.5.26 ndb_select_count — Print Row Counts for NDB Tables") prints the number of rows in
one or more [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") tables. With a
single table, the result is equivalent to that obtained by using
the MySQL statement `SELECT COUNT(*) FROM
tbl_name`.

#### Usage

```terminal
ndb_select_count [-c connection_string] -ddb_name tbl_name[, tbl_name2[, ...]]
```

Options that can be used with
[**ndb\_select\_count**](mysql-cluster-programs-ndb-select-count.md "25.5.26 ndb_select_count — Print Row Counts for NDB Tables") are shown in the following
table. Additional descriptions follow the table.

**Table 25.47 Command-line options used with the program ndb\_select\_count**

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
| `--lock=#`,  `-l #` | Lock type | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection_string`,  `-c connection_string` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--parallelism=#`,  `-p #` | Degree of parallelism | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--character-sets-dir`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`--connect-retries`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-connectstring).
- [`--core-file`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--defaults-file`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--login-path`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--help`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--ndb-connectstring`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connect string for connecting to ndb\_mgmd. Syntax:
  "[nodeid=id;][host=]hostname[:port]". Overrides entries in
  NDB\_CONNECTSTRING and my.cnf.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-connectstring).
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--ndb-nodeid`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_ndb-connectstring).
- [`--no-defaults`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--usage`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as
  [`--help`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_help).
- [`--version`](mysql-cluster-programs-ndb-select-count.md#option_ndb_select_count_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

You can obtain row counts from multiple tables in the same
database by listing the table names separated by spaces when
invoking this command, as shown under
**Sample Output**.

#### Sample Output

```terminal
$> ./ndb_select_count -c localhost -d ctest1 fish dogs
6 records in table fish
4 records in table dogs
```
