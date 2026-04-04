### 25.5.12 ndb\_error\_reporter — NDB Error-Reporting Utility

[**ndb\_error\_reporter**](mysql-cluster-programs-ndb-error-reporter.md "25.5.12 ndb_error_reporter — NDB Error-Reporting Utility") creates an archive from
data node and management node log files that can be used to help
diagnose bugs or other problems with a cluster. *It is
highly recommended that you make use of this utility when filing
reports of bugs in NDB Cluster*.

Options that can be used with
[**ndb\_error\_reporter**](mysql-cluster-programs-ndb-error-reporter.md "25.5.12 ndb_error_reporter — NDB Error-Reporting Utility") are shown in the following
table. Additional descriptions follow the table.

**Table 25.34 Command-line options used with the program ndb\_error\_reporter**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--connection-timeout=#` | Number of seconds to wait when connecting to nodes before timing out | (Supported in all NDB releases based on MySQL 8.0) |
| `--dry-scp` | Disable scp with remote hosts; used in testing only | (Supported in all NDB releases based on MySQL 8.0) |
| `--fs` | Include file system data in error report; can use a large amount of disk space | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--skip-nodegroup=#` | Skip all nodes in the node group having this ID | (Supported in all NDB releases based on MySQL 8.0) |

#### Usage

```terminal
ndb_error_reporter path/to/config-file [username] [options]
```

This utility is intended for use on a management node host, and
requires the path to the management host configuration file
(usually named `config.ini`). Optionally, you
can supply the name of a user that is able to access the
cluster's data nodes using SSH, to copy the data node log files.
[**ndb\_error\_reporter**](mysql-cluster-programs-ndb-error-reporter.md "25.5.12 ndb_error_reporter — NDB Error-Reporting Utility") then includes all of these
files in archive that is created in the same directory in which
it is run. The archive is named
`ndb_error_report_YYYYMMDDhhmmss.tar.bz2`,
where *`YYYYMMDDhhmmss`* is a datetime
string.

[**ndb\_error\_reporter**](mysql-cluster-programs-ndb-error-reporter.md "25.5.12 ndb_error_reporter — NDB Error-Reporting Utility") also accepts the options
listed here:

- [`--connection-timeout=timeout`](mysql-cluster-programs-ndb-error-reporter.md#option_ndb_error_reporter_connection-timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connection-timeout=#` |
  | Type | Integer |
  | Default Value | `0` |

  Wait this many seconds when trying to connect to nodes
  before timing out.
- [`--dry-scp`](mysql-cluster-programs-ndb-error-reporter.md#option_ndb_error_reporter_dry-scp)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--dry-scp` |

  Run [**ndb\_error\_reporter**](mysql-cluster-programs-ndb-error-reporter.md "25.5.12 ndb_error_reporter — NDB Error-Reporting Utility") without using scp
  from remote hosts. Used for testing only.
- [`--help`](mysql-cluster-programs-ndb-error-reporter.md#option_ndb_error_reporter_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--fs`](mysql-cluster-programs-ndb-error-reporter.md#option_ndb_error_reporter_fs)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fs` |

  Copy the data node file systems to the management host and
  include them in the archive.

  Because data node file systems can be extremely large, even
  after being compressed, we ask that you please do
  *not* send archives created using this
  option to Oracle unless you are specifically requested to do
  so.
- [`--skip-nodegroup=nodegroup_id`](mysql-cluster-programs-ndb-error-reporter.md#option_ndb_error_reporter_skip-nodegroup)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connection-timeout=#` |
  | Type | Integer |
  | Default Value | `0` |

  Skip all nodes belong to the node group having the supplied
  node group ID.
