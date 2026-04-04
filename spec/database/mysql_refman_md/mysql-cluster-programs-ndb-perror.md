### 25.5.16 ndb\_perror — Obtain NDB Error Message Information

[**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") shows information about an NDB
error, given its error code. This includes the error message,
the type of error, and whether the error is permanent or
temporary. This is intended as a drop-in replacement for
[**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information") [`--ndb`](perror.md#option_perror_ndb),
which is no longer supported.

#### Usage

```terminal
ndb_perror [options] error_code
```

[**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") does not need to access a running
NDB Cluster, or any nodes (including SQL nodes). To view
information about a given NDB error, invoke the program, using
the error code as an argument, like this:

```terminal
$> ndb_perror 323
NDB error code 323: Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

To display only the error message, invoke
[**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") with the
[`--silent`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_silent) option (short form
`-s`), as shown here:

```terminal
$> ndb_perror -s 323
Invalid nodegroup id, nodegroup already existing: Permanent error: Application error
```

Like [**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information"), [**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information")
accepts multiple error codes:

```terminal
$> ndb_perror 321 1001
NDB error code 321: Invalid nodegroup id: Permanent error: Application error
NDB error code 1001: Illegal connect string
```

Additional program options for [**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") are
described later in this section.

[**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") replaces [**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information")
`--ndb`, which is no longer supported by NDB
Cluster. To make substitution easier in scripts and other
applications that might depend on [**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information") for
obtaining NDB error information, [**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information")
supports its own “dummy”
[`--ndb`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_ndb) option, which does
nothing.

The following table includes all options that are specific to
the NDB Cluster program [**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information").
Additional descriptions follow the table.

**Table 25.38 Command-line options used with the program ndb\_perror**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb` | For compatibility with applications depending on old versions of perror; does nothing | (Supported in all NDB releases based on MySQL 8.0) |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--silent`,  `-s` | Show error message only | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Print program version information and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--verbose`,  `-v` | Verbose output; disable with --silent | (Supported in all NDB releases based on MySQL 8.0) |

#### Additional Options

- [`--defaults-extra-file`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--help`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display program help text and exit.
- [`--login-path`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--ndb`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_ndb)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb` |

  For compatibility with applications depending on old
  versions of [**perror**](perror.md "6.8.2 perror — Display MySQL Error Message Information") that use that
  program's [`--ndb`](perror.md#option_perror_ndb) option.
  The option when used with [**ndb\_perror**](mysql-cluster-programs-ndb-perror.md "25.5.16 ndb_perror — Obtain NDB Error Message Information") does
  nothing, and is ignored by it.
- [`--no-defaults`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--print-defaults`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--silent`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_silent),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--silent` |

  Show error message only.
- [`--version`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Print program version information and exit.
- [`--verbose`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose output; disable with
  [`--silent`](mysql-cluster-programs-ndb-perror.md#option_ndb_perror_silent).
