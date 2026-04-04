### 25.5.22 ndb\_redo\_log\_reader — Check and Print Content of Cluster Redo Log

Reads a redo log file, checking it for errors, printing its
contents in a human-readable format, or both.
[**ndb\_redo\_log\_reader**](mysql-cluster-programs-ndb-redo-log-reader.md "25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log") is intended for use
primarily by NDB Cluster developers and Support personnel in
debugging and diagnosing problems.

This utility remains under development, and its syntax and
behavior are subject to change in future NDB Cluster releases.

The C++ source files for [**ndb\_redo\_log\_reader**](mysql-cluster-programs-ndb-redo-log-reader.md "25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log")
can be found in the directory
`/storage/ndb/src/kernel/blocks/dblqh/redoLogReader`.

Options that can be used with
[**ndb\_redo\_log\_reader**](mysql-cluster-programs-ndb-redo-log-reader.md "25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log") are shown in the
following table. Additional descriptions follow the table.

**Table 25.41 Command-line options used with the program ndb\_redo\_log\_reader**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `-dump` | Print dump info | (Supported in all NDB releases based on MySQL 8.0) |
| `--file-key=key`,  `-K key` | Supply decryption key | ADDED: NDB 8.0.31 |
| `--file-key-from-stdin` | Supply decryption key using stdin | ADDED: NDB 8.0.31 |
| `-filedescriptors` | Print file descriptors only | (Supported in all NDB releases based on MySQL 8.0) |
| `--help` | Print usage information (has no short form) | (Supported in all NDB releases based on MySQL 8.0) |
| `-lap` | Provide lap info, with max GCI started and completed | (Supported in all NDB releases based on MySQL 8.0) |
| `-mbyte #` | Starting megabyte | (Supported in all NDB releases based on MySQL 8.0) |
| `-mbyteheaders` | Show only first page header of each megabyte in file | (Supported in all NDB releases based on MySQL 8.0) |
| `-nocheck` | Do not check records for errors | (Supported in all NDB releases based on MySQL 8.0) |
| `-noprint` | Do not print records | (Supported in all NDB releases based on MySQL 8.0) |
| `-page #` | Start with this page | (Supported in all NDB releases based on MySQL 8.0) |
| `-pageheaders` | Show page headers only | (Supported in all NDB releases based on MySQL 8.0) |
| `-pageindex #` | Start with this page index | (Supported in all NDB releases based on MySQL 8.0) |
| `-twiddle` | Bit-shifted dump | (Supported in all NDB releases based on MySQL 8.0) |

#### Usage

```terminal
ndb_redo_log_reader file_name [options]
```

*`file_name`* is the name of a cluster
redo log file. redo log files are located in the numbered
directories under the data node's data directory
([`DataDir`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-datadir)); the path
under this directory to the redo log files matches the pattern
`ndb_nodeid_fs/D#/DBLQH/S#.FragLog`.
*`nodeid`* is the data node's node
ID. The two instances of *`#`* each
represent a number (not necessarily the same number); the number
following `D` is in the range 8-39 inclusive;
the range of the number following `S` varies
according to the value of the
[`NoOfFragmentLogFiles`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-nooffragmentlogfiles)
configuration parameter, whose default value is 16; thus, the
default range of the number in the file name is 0-15 inclusive.
For more information, see
[NDB Cluster Data Node File System Directory](https://dev.mysql.com/doc/ndb-internals/en/ndb-internals-ndbd-filesystemdir-files.html).

The name of the file to be read may be followed by one or more
of the options listed here:

- [`-dump`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_dump)

  |  |  |
  | --- | --- |
  | Command-Line Format | `-dump` |

  Print dump info.
- [`--file-key`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_file-key),
  `-K`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--file-key=key` |
  | Introduced | 8.0.31-ndb-8.0.31 |

  Supply file decryption key using `stdin`,
  `tty`, or a `my.cnf`
  file.
- [`--file-key-from-stdin`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_file-key-from-stdin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--file-key-from-stdin` |
  | Introduced | 8.0.31-ndb-8.0.31 |

  Supply file decryption key using `stdin`.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-filedescriptors` |

  [`-filedescriptors`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_filedescriptors):
  Print file descriptors only.
- |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  [`--help`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_help): Print
  usage information.
- [`-lap`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_lap)

  |  |  |
  | --- | --- |
  | Command-Line Format | `-lap` |

  Provide lap info, with max GCI started and completed.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-mbyte #` |
  | Type | Numeric |
  | Default Value | `0` |
  | Minimum Value | `0` |
  | Maximum Value | `15` |

  [`-mbyte
  #`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_mbyte): Starting megabyte.

  *`#`* is an integer in the range 0 to
  15, inclusive.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-mbyteheaders` |

  [`-mbyteheaders`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_mbyteheaders):
  Show only the first page header of every megabyte in the
  file.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-noprint` |

  [`-noprint`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_noprint): Do not
  print the contents of the log file.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-nocheck` |

  [`-nocheck`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_nocheck): Do not
  check the log file for errors.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-page #` |
  | Type | Integer |
  | Default Value | `0` |
  | Minimum Value | `0` |
  | Maximum Value | `31` |

  [`-page
  #`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_page): Start at this page.

  *`#`* is an integer in the range 0 to
  31, inclusive.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-pageheaders` |

  [`-pageheaders`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_pageheaders):
  Show page headers only.
- |  |  |
  | --- | --- |
  | Command-Line Format | `-pageindex #` |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `12` |
  | Maximum Value | `8191` |

  [`-pageindex
  #`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_pageindex): Start at this page
  index.

  *`#`* is an integer between 12 and
  8191, inclusive.
- [`-twiddle`](mysql-cluster-programs-ndb-redo-log-reader.md#option_ndb_redo_log_reader_twiddle)

  |  |  |
  | --- | --- |
  | Command-Line Format | `-twiddle` |

  Bit-shifted dump.

Like [**ndb\_print\_backup\_file**](mysql-cluster-programs-ndb-print-backup-file.md "25.5.17 ndb_print_backup_file — Print NDB Backup File Contents") and
[**ndb\_print\_schema\_file**](mysql-cluster-programs-ndb-print-schema-file.md "25.5.20 ndb_print_schema_file — Print NDB Schema File Contents") (and unlike most of the
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") utilities that are intended to
be run on a management server host or to connect to a management
server) [**ndb\_redo\_log\_reader**](mysql-cluster-programs-ndb-redo-log-reader.md "25.5.22 ndb_redo_log_reader — Check and Print Content of Cluster Redo Log") must be run on a
cluster data node, since it accesses the data node file system
directly. Because it does not make use of the management server,
this utility can be used when the management server is not
running, and even when the cluster has been completely shut
down.
