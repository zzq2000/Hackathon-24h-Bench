### 25.5.6 ndb\_blob\_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables

This tool can be used to check for and remove orphaned BLOB
column parts from [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") tables, as
well as to generate a file listing any orphaned parts. It is
sometimes useful in diagnosing and repairing corrupted or
damaged `NDB` tables containing
[`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") or
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns.

The basic syntax for [**ndb\_blob\_tool**](mysql-cluster-programs-ndb-blob-tool.md "25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables") is shown
here:

```simple
ndb_blob_tool [options] table [column, ...]
```

Unless you use the [`--help`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_help)
option, you must specify an action to be performed by including
one or more of the options
[`--check-orphans`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_check-orphans),
[`--delete-orphans`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_delete-orphans), or
[`--dump-file`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_dump-file). These options
cause [**ndb\_blob\_tool**](mysql-cluster-programs-ndb-blob-tool.md "25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables") to check for orphaned
BLOB parts, remove any orphaned BLOB parts, and generate a dump
file listing orphaned BLOB parts, respectively, and are
described in more detail later in this section.

You must also specify the name of a table when invoking
[**ndb\_blob\_tool**](mysql-cluster-programs-ndb-blob-tool.md "25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables"). In addition, you can
optionally follow the table name with the (comma-separated)
names of one or more [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") or
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns from that table. If
no columns are listed, the tool works on all of the table's
[`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") and
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns. If you need to
specify a database, use the
[`--database`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_database)
(`-d`) option.

The [`--verbose`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_verbose) option
provides additional information in the output about the
tool's progress.

All options that can be used with [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon")
are shown in the following table. Additional descriptions follow
the table.

**Table 25.28 Command-line options used with the program ndb\_blob\_tool**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--add-missing` | Write dummy blob parts to take place of those which are missing | ADDED: NDB 8.0.20 |
| `--character-sets-dir=path` | Directory containing character sets | REMOVED: 8.0.31 |
| `--check-missing` | Check for blobs having inline parts but missing one or more parts from parts table | ADDED: NDB 8.0.20 |
| `--check-orphans` | Check for blob parts having no corresponding inline parts | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retries=#` | Number of times to retry connection before giving up | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retry-delay=#` | Number of seconds to wait between attempts to contact management server | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-string=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--core-file` | Write core file on error; used in debugging | REMOVED: 8.0.31 |
| `--database=name`,  `-d name` | Database to find the table in | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--delete-orphans` | Delete blob parts having no corresponding inline parts | (Supported in all NDB releases based on MySQL 8.0) |
| `--dump-file=file` | Write orphan keys to specified file | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection_string`,  `-c connection_string` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--verbose`,  `-v` | Verbose output | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--add-missing`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_add-missing)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--add-missing` |
  | Introduced | 8.0.20-ndb-8.0.20 |

  For each inline part in NDB Cluster tables which has no
  corresponding BLOB part, write a dummy BLOB part of the
  required length, consisting of spaces.
- [`--character-sets-dir`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`--check-missing`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_check-missing)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--check-missing` |
  | Introduced | 8.0.20-ndb-8.0.20 |

  Check for inline parts in NDB Cluster tables which have no
  corresponding BLOB parts.
- [`--check-orphans`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_check-orphans)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--check-orphans` |

  Check for BLOB parts in NDB Cluster tables which have no
  corresponding inline parts.
- [`--connect-retries`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-connectstring).
- [`--core-file`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--database=db_name`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_database),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--database=name` |
  | Type | String |
  | Default Value | `[none]` |

  Specify the database to find the table in.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--delete-orphans`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_delete-orphans)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--delete-orphans` |

  Remove BLOB parts from NDB Cluster tables which have no
  corresponding inline parts.
- [`--dump-file=file`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_dump-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--dump-file=file` |
  | Type | File name |
  | Default Value | `[none]` |

  Writes a list of orphaned BLOB column parts to
  *`file`*. The information written to
  the file includes the table key and BLOB part number for
  each orphaned BLOB part.
- [`--help`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--login-path`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--ndb-connectstring`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connect string for connecting to ndb\_mgmd. Syntax:
  "[nodeid=id;][host=]hostname[:port]". Overrides entries in
  NDB\_CONNECTSTRING and my.cnf.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as
  [`--ndb-connectstring`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-connectstring).
- [`--ndb-nodeid`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  --ndb-connectstring.
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--no-defaults`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--usage`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as --help.
- [`--verbose`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_verbose)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Provide extra information in the tool's output
  regarding its progress.
- [`--version`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

#### Example

First we create an `NDB` table in the
`test` database, using the
[`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statement shown
here:

```sql
USE test;

CREATE TABLE btest (
    c0 BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    c1 TEXT,
    c2 BLOB
)   ENGINE=NDB;
```

Then we insert a few rows into this table, using a series of
statements similar to this one:

```sql
INSERT INTO btest VALUES (NULL, 'x', REPEAT('x', 1000));
```

When run with
[`--check-orphans`](mysql-cluster-programs-ndb-blob-tool.md#option_ndb_blob_tool_check-orphans) against
this table, [**ndb\_blob\_tool**](mysql-cluster-programs-ndb-blob-tool.md "25.5.6 ndb_blob_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables") generates the
following output:

```terminal
$> ndb_blob_tool --check-orphans --verbose -d test btest
connected
processing 2 blobs
processing blob #0 c1 NDB$BLOB_19_1
NDB$BLOB_19_1: nextResult: res=1
total parts: 0
orphan parts: 0
processing blob #1 c2 NDB$BLOB_19_2
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=0
NDB$BLOB_19_2: nextResult: res=1
total parts: 10
orphan parts: 0
disconnected
```

The tool reports that there are no `NDB` BLOB
column parts associated with column `c1`, even
though `c1` is a
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") column. This is due to the
fact that, in an [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") table, only
the first 256 bytes of a [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") or
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") column value are stored
inline, and only the excess, if any, is stored separately; thus,
if there are no values using more than 256 bytes in a given
column of one of these types, no `BLOB` column
parts are created by `NDB` for this column. See
[Section 13.7, “Data Type Storage Requirements”](storage-requirements.md "13.7 Data Type Storage Requirements"), for more information.
