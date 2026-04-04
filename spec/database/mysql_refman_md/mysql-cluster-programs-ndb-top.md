### 25.5.29 ndb\_top — View CPU usage information for NDB threads

[**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") displays running information in the
terminal about CPU usage by NDB threads on an NDB Cluster data
node. Each thread is represented by two rows in the output, the
first showing system statistics, the second showing the measured
statistics for the thread.

[**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") is available beginning with MySQL NDB
Cluster 7.6.3.

#### Usage

```terminal
ndb_top [-h hostname] [-t port] [-u user] [-p pass] [-n node_id]
```

[**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") connects to a MySQL Server running as
an SQL node of the cluster. By default, it attempts to connect
to a [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") running on
`localhost` and port 3306, as the MySQL
`root` user with no password specified. You can
override the default host and port using, respectively,
[`--host`](mysql-cluster-programs-ndb-top.md#option_ndb_top_host) (`-h`) and
[`--port`](mysql-cluster-programs-ndb-top.md#option_ndb_top_port) (`-t`). To
specify a MySQL user and password, use the
[`--user`](mysql-cluster-programs-ndb-top.md#option_ndb_top_user) (`-u`) and
[`--passwd`](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-programs-ndb-top.html#option_ndb_top_passwd) (`-p`)
options. This user must be able to read tables in the
[`ndbinfo`](mysql-cluster-ndbinfo.md "25.6.16 ndbinfo: The NDB Cluster Information Database") database
([**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") uses information from
[`ndbinfo.cpustat`](mysql-cluster-ndbinfo-cpustat.md "25.6.16.18 The ndbinfo cpustat Table") and related
tables).

For more information about MySQL user accounts and passwords,
see [Section 8.2, “Access Control and Account Management”](access-control.md "8.2 Access Control and Account Management").

Output is available as plain text or an ASCII graph; you can
specify this using the [`--text`](mysql-cluster-programs-ndb-top.md#option_ndb_top_text)
(`-x`) and
[`--graph`](mysql-cluster-programs-ndb-top.md#option_ndb_top_graph) (`-g`)
options, respectively. These two display modes provide the same
information; they can be used concurrently. At least one display
mode must be in use.

Color display of the graph is supported and enabled by default
([`--color`](mysql-cluster-programs-ndb-top.md#option_ndb_top_color) or `-c`
option). With color support enabled, the graph display shows OS
user time in blue, OS system time in green, and idle time as
blank. For measured load, blue is used for execution time,
yellow for send time, red for time spent in send buffer full
waits, and blank spaces for idle time. The percentage shown in
the graph display is the sum of percentages for all threads
which are not idle. Colors are not currently configurable; you
can use grayscale instead by using
`--skip-color`.

The sorted view ([`--sort`](mysql-cluster-programs-ndb-top.md#option_ndb_top_sort),
`-r`) is based on the maximum of the measured
load and the load reported by the OS. Display of these can be
enabled and disabled using the
[`--measured-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_measured-load)
(`-m`) and
[`--os-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_os-load) (`-o`)
options. Display of at least one of these loads must be enabled.

The program tries to obtain statistics from a data node having
the node ID given by the
[`--node-id`](mysql-cluster-programs-ndb-top.md#option_ndb_top_node-id) (`-n`)
option; if unspecified, this is 1. [**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads")
cannot provide information about other types of nodes.

The view adjusts itself to the height and width of the terminal
window; the minimum supported width is 76 characters.

Once started, [**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") runs continuously until
forced to exit; you can quit the program using
`Ctrl-C`. The display updates once per second;
to set a different delay interval, use
[`--sleep-time`](mysql-cluster-programs-ndb-top.md#option_ndb_top_sleep-time)
(`-s`).

Note

[**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") is available on macOS, Linux, and
Solaris. It is not currently supported on Windows platforms.

The following table includes all options that are specific to
the NDB Cluster program [**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads"). Additional
descriptions follow the table.

**Table 25.50 Command-line options used with the program ndb\_top**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--color`,  `-c` | Show ASCII graphs in color; use --skip-colors to disable | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--graph`,  `-g` | Display data using graphs; use --skip-graphs to disable | (Supported in all NDB releases based on MySQL 8.0) |
| `--help` | Show program usage information | (Supported in all NDB releases based on MySQL 8.0) |
| `--host=string`,  `-h string` | Host name or IP address of MySQL Server to connect to | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--measured-load`,  `-m` | Show measured load by thread | (Supported in all NDB releases based on MySQL 8.0) |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--node-id=#`,  `-n #` | Watch node having this node ID | (Supported in all NDB releases based on MySQL 8.0) |
| `--os-load`,  `-o` | Show load measured by operating system | (Supported in all NDB releases based on MySQL 8.0) |
| `--password=password`,  `-p password` | Connect using this password | (Supported in all NDB releases based on MySQL 8.0) |
| `--port=#`,  `-P #` (>=7.6.6) | Port number to use when connecting to MySQL Server | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--sleep-time=#`,  `-s #` | Time to wait between display refreshes, in seconds | (Supported in all NDB releases based on MySQL 8.0) |
| `--socket=path`,  `-S path` | Socket file to use for connection | (Supported in all NDB releases based on MySQL 8.0) |
| `--sort`,  `-r` | Sort threads by usage; use --skip-sort to disable | (Supported in all NDB releases based on MySQL 8.0) |
| `--text`,  `-t` (>=7.6.6) | Display data using text | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage` | Show program usage information; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--user=name`,  `-u name` | Connect as this MySQL user | (Supported in all NDB releases based on MySQL 8.0) |

#### Additional Options

- [`--color`](mysql-cluster-programs-ndb-top.md#option_ndb_top_color), `-c`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--color` |

  Show ASCII graphs in color; use
  `--skip-colors` to disable.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-top.md#option_ndb_top_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-top.md#option_ndb_top_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-top.md#option_ndb_top_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--graph`](mysql-cluster-programs-ndb-top.md#option_ndb_top_graph), `-g`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--graph` |

  Display data using graphs; use
  `--skip-graphs` to disable. This option or
  [`--text`](mysql-cluster-programs-ndb-top.md#option_ndb_top_text) must be true; both
  options may be true.
- [`--help`](mysql-cluster-programs-ndb-top.md#option_ndb_top_help), `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Show program usage information.
- [`--host[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_host)=*`name]`*,
  `-h`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=string` |
  | Type | String |
  | Default Value | `localhost` |

  Host name or IP address of MySQL Server to connect to.
- [`--login-path`](mysql-cluster-programs-ndb-top.md#option_ndb_top_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--measured-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_measured-load),
  `-m`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--measured-load` |

  Show measured load by thread. This option or
  [`--os-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_os-load) must be true; both
  options may be true.
- [`--no-defaults`](mysql-cluster-programs-ndb-top.md#option_ndb_top_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--node-id[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_node-id)=*`#]`*,
  `-n`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--node-id=#` |
  | Type | Integer |
  | Default Value | `1` |

  Watch the data node having this node ID.
- [`--os-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_os-load),
  `-o`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--os-load` |

  Show load measured by operating system. This option or
  [`--measured-load`](mysql-cluster-programs-ndb-top.md#option_ndb_top_measured-load) must be
  true; both options may be true.
- [`--password[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_password)=*`password]`*,
  `-p`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password=password` |
  | Type | String |
  | Default Value | `NULL` |

  Connect to a MySQL Server using this password and the MySQL
  user specified by [`--user`](mysql-cluster-programs-ndb-top.md#option_ndb_top_user).

  This password is associated with a MySQL user account only,
  and is not related in any way to the password used with
  encrypted `NDB` backups.
- [`--port[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_port)=*`#]`*,
  `-P`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=#` |
  | Type | Integer |
  | Default Value | `3306` |

  Port number to use when connecting to MySQL Server.

  (Formerly, the short form for this option was
  `-t`, which was repurposed as the short form
  of [`--text`](mysql-cluster-programs-ndb-top.md#option_ndb_top_text).)
- [`--print-defaults`](mysql-cluster-programs-ndb-top.md#option_ndb_top_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--sleep-time[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_sleep-time)=*`seconds]`*,
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sleep-time=#` |
  | Type | Integer |
  | Default Value | `1` |

  Time to wait between display refreshes, in seconds.
- [`--socket=path/to/file`](mysql-cluster-programs-ndb-top.md#option_ndb_top_socket),
  `-S`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--socket=path` |
  | Type | Path name |
  | Default Value | `[none]` |

  Use the specified socket file for the connection.
- [`--sort`](mysql-cluster-programs-ndb-top.md#option_ndb_top_sort), `-r`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sort` |

  Sort threads by usage; use `--skip-sort` to
  disable.
- [`--text`](mysql-cluster-programs-ndb-top.md#option_ndb_top_text), `-t`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--text` |

  Display data using text. This option or
  [`--graph`](mysql-cluster-programs-ndb-top.md#option_ndb_top_graph) must be true; both
  options may be true.

  (The short form for this option was `-x` in
  previous versions of NDB Cluster, but this is no longer
  supported.)
- [`--usage`](mysql-cluster-programs-ndb-top.md#option_ndb_top_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as
  [`--help`](mysql-cluster-programs-ndb-top.md#option_ndb_top_help).
- [`--user[`](mysql-cluster-programs-ndb-top.md#option_ndb_top_user)=*`name]`*,
  `-u`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=name` |
  | Type | String |
  | Default Value | `root` |

  Connect as this MySQL user. Normally requires a password
  supplied by the [`--password`](mysql-cluster-programs-ndb-top.md#option_ndb_top_password)
  option.

**Sample Output.**
The next figure shows [**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") running in a
terminal window on a Linux system with an
[**ndbmtd**](mysql-cluster-programs-ndbmtd.md "25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)") data node under a moderate load.
Here, the program has been invoked using
[**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads")
[`-n8`](mysql-cluster-programs-ndb-top.md#option_ndb_top_node-id)
[`-x`](mysql-cluster-programs-ndb-top.md#option_ndb_top_text) to provide
both text and graph output:

**Figure 25.5 ndb\_top Running in Terminal**

![Display from ndb_top, running in a terminal window. Shows information for each node, including the utilized resources.](images/ndb-top-1.png)

Beginning with NDB 8.0.20, [**ndb\_top**](mysql-cluster-programs-ndb-top.md "25.5.29 ndb_top — View CPU usage information for NDB threads") also shows
spin times for threads, displayed in green.
