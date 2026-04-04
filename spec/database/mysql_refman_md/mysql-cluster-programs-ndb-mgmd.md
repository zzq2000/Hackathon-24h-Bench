### 25.5.4 ndb\_mgmd — The NDB Cluster Management Server Daemon

The management server is the process that reads the cluster
configuration file and distributes this information to all nodes
in the cluster that request it. It also maintains a log of
cluster activities. Management clients can connect to the
management server and check the cluster's status.

All options that can be used with [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon")
are shown in the following table. Additional descriptions follow
the table.

**Table 25.26 Command-line options used with the program ndb\_mgmd**

| Format | Description | Added, Deprecated, or Removed |
| --- | --- | --- |
| `--bind-address=host` | Local bind address | (Supported in all NDB releases based on MySQL 8.0) |
| `--character-sets-dir=path` | Directory containing character sets | REMOVED: 8.0.31 |
| `--cluster-config-suffix=name` | Override defaults group suffix when reading cluster\_config sections in my.cnf file; used in testing | ADDED: 8.0.24 |
| `--config-cache[=TRUE|FALSE]` | Enable management server configuration cache; true by default | (Supported in all NDB releases based on MySQL 8.0) |
| `--config-file=file`,  `-f file` | Specify cluster configuration file; also specify --reload or --initial to override configuration cache if present | (Supported in all NDB releases based on MySQL 8.0) |
| `--configdir=directory`,  `--config-dir=directory` | Specify cluster management server configuration cache directory | (Supported in all NDB releases based on MySQL 8.0) |
| `--connect-retries=#` | Number of times to retry connection before giving up | REMOVED: 8.0.31 |
| `--connect-retry-delay=#` | Number of seconds to wait between attempts to contact management server | REMOVED: 8.0.31 |
| `--connect-string=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--core-file` | Write core file on error; used in debugging | REMOVED: 8.0.31 |
| `--daemon`,  `-d` | Run ndb\_mgmd in daemon mode (default) | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-extra-file=path` | Read given file after global files are read | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-file=path` | Read default options from given file only | (Supported in all NDB releases based on MySQL 8.0) |
| `--defaults-group-suffix=string` | Also read groups with concat(group, suffix) | (Supported in all NDB releases based on MySQL 8.0) |
| `--help`,  `-?` | Display help text and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--initial` | Causes management server to reload configuration data from configuration file, bypassing configuration cache | (Supported in all NDB releases based on MySQL 8.0) |
| `--install[=name]` | Used to install management server process as Windows service; does not apply on other platforms | (Supported in all NDB releases based on MySQL 8.0) |
| `--interactive` | Run ndb\_mgmd in interactive mode (not officially supported in production; for testing purposes only) | (Supported in all NDB releases based on MySQL 8.0) |
| `--log-name=name` | Name to use when writing cluster log messages applying to this node | (Supported in all NDB releases based on MySQL 8.0) |
| `--login-path=path` | Read given path from login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--mycnf` | Read cluster configuration data from my.cnf file | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-connectstring=connection_string`,  `-c connection_string` | Set connect string for connecting to ndb\_mgmd. Syntax: "[nodeid=id;][host=]hostname[:port]". Overrides entries in NDB\_CONNECTSTRING and my.cnf | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-mgmd-host=connection_string`,  `-c connection_string` | Same as --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-nodeid=#` | Set node ID for this node, overriding any ID set by --ndb-connectstring | (Supported in all NDB releases based on MySQL 8.0) |
| `--ndb-optimized-node-selection` | Enable optimizations for selection of nodes for transactions. Enabled by default; use --skip-ndb-optimized-node-selection to disable | REMOVED: 8.0.31 |
| `--no-defaults` | Do not read default options from any option file other than login file | (Supported in all NDB releases based on MySQL 8.0) |
| `--no-nodeid-checks` | Do not perform any node ID checks | (Supported in all NDB releases based on MySQL 8.0) |
| `--nodaemon` | Do not run ndb\_mgmd as a daemon | (Supported in all NDB releases based on MySQL 8.0) |
| `--nowait-nodes=list` | Do not wait for management nodes specified when starting this management server; requires --ndb-nodeid option | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-defaults` | Print program argument list and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--print-full-config`,  `-P` | Print full configuration and exit | (Supported in all NDB releases based on MySQL 8.0) |
| `--reload` | Causes management server to compare configuration file with configuration cache | (Supported in all NDB releases based on MySQL 8.0) |
| `--remove[=name]` | Used to remove management server process that was previously installed as Windows service, optionally specifying name of service to be removed; does not apply on other platforms | (Supported in all NDB releases based on MySQL 8.0) |
| `--skip-config-file` | Do not use configuration file | (Supported in all NDB releases based on MySQL 8.0) |
| `--usage`,  `-?` | Display help text and exit; same as --help | (Supported in all NDB releases based on MySQL 8.0) |
| `--verbose`,  `-v` | Write additional information to log | (Supported in all NDB releases based on MySQL 8.0) |
| `--version`,  `-V` | Display version information and exit | (Supported in all NDB releases based on MySQL 8.0) |

- [`--bind-address=host`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=host` |
  | Type | String |
  | Default Value | `[none]` |

  Causes the management server to bind to a specific network
  interface (host name or IP address). This option has no
  default value.
- [`--character-sets-dir`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Removed | 8.0.31 |

  Directory containing character sets.
- [`cluster-config-suffix`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_cluster-config-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--cluster-config-suffix=name` |
  | Introduced | 8.0.24 |
  | Type | String |
  | Default Value | `[none]` |

  Override defaults group suffix when reading cluster
  configuration sections in `my.cnf`; used
  in testing.
- [`--config-cache`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-cache)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--config-cache[=TRUE|FALSE]` |
  | Type | Boolean |
  | Default Value | `TRUE` |

  This option, whose default value is `1` (or
  `TRUE`, or `ON`), can be
  used to disable the management server's configuration
  cache, so that it reads its configuration from
  `config.ini` every time it starts (see
  [Section 25.4.3, “NDB Cluster Configuration Files”](mysql-cluster-config-file.md "25.4.3 NDB Cluster Configuration Files")). You can do
  this by starting the [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") process
  with any one of the following options:

  - `--config-cache=0`
  - `--config-cache=FALSE`
  - `--config-cache=OFF`
  - [`--skip-config-cache`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_skip-config-cache)

  Using one of the options just listed is effective only if
  the management server has no stored configuration at the
  time it is started. If the management server finds any
  configuration cache files, then the
  `--config-cache` option or the
  `--skip-config-cache` option is ignored.
  Therefore, to disable configuration caching, the option
  should be used the *first* time that the
  management server is started. Otherwise—that is, if
  you wish to disable configuration caching for a management
  server that has *already* created a
  configuration cache—you must stop the management
  server, delete any existing configuration cache files
  manually, then restart the management server with
  `--skip-config-cache` (or with
  `--config-cache` set equal to 0,
  `OFF`, or `FALSE`).

  Configuration cache files are normally created in a
  directory named `mysql-cluster` under the
  installation directory (unless this location has been
  overridden using the
  [`--configdir`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_configdir) option). Each
  time the management server updates its configuration data,
  it writes a new cache file. The files are named sequentially
  in order of creation using the following format:

  ```simple
  ndb_node-id_config.bin.seq-number
  ```

  *`node-id`* is the management
  server's node ID; *`seq-number`*
  is a sequence number, beginning with 1. For example, if the
  management server's node ID is 5, then the first three
  configuration cache files would, when they are created, be
  named `ndb_5_config.bin.1`,
  `ndb_5_config.bin.2`, and
  `ndb_5_config.bin.3`.

  If your intent is to purge or reload the configuration cache
  without actually disabling caching, you should start
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") with one of the options
  [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload) or
  [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial) instead of
  `--skip-config-cache`.

  To re-enable the configuration cache, simply restart the
  management server, but without the
  `--config-cache` or
  `--skip-config-cache` option that was used
  previously to disable the configuration cache.

  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") does not check for the
  configuration directory
  ([`--configdir`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_configdir)) or attempts
  to create one when `--skip-config-cache` is
  used. (Bug #13428853)
- [`--config-file=filename`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file),
  `-f filename`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--config-file=file` |
  | Disabled by | `skip-config-file` |
  | Type | File name |
  | Default Value | `[none]` |

  Instructs the management server as to which file it should
  use for its configuration file. By default, the management
  server looks for a file named
  `config.ini` in the same directory as the
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") executable; otherwise the file
  name and location must be specified explicitly.

  This option has no default value, and is ignored unless the
  management server is forced to read the configuration file,
  either because [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") was started with
  the [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload) or
  [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial) option, or
  because the management server could not find any
  configuration cache. Beginning with NDB 8.0.26,
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") refuses to start if
  [`--config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file) is specified
  without either of [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial)
  or [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload).

  The [`--config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file) option is
  also read if [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") was started with
  [`--config-cache=OFF`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-cache). See
  [Section 25.4.3, “NDB Cluster Configuration Files”](mysql-cluster-config-file.md "25.4.3 NDB Cluster Configuration Files"), for more
  information.
- [`--configdir=dir_name`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_configdir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--configdir=directory`  `--config-dir=directory` |
  | Type | File name |
  | Default Value | `$INSTALLDIR/mysql-cluster` |

  Specifies the cluster management server's configuration
  cache directory. `--config-dir` is an alias
  for this option.

  In NDB 8.0.27 and later, this must be an absolute path.
  Otherwise, the management server refuses to start.
- [`--connect-retries`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_connect-retries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retries=#` |
  | Removed | 8.0.31 |
  | Type | Integer |
  | Default Value | `12` |
  | Minimum Value | `0` |
  | Maximum Value | `12` |

  Number of times to retry connection before giving up.
- [`--connect-retry-delay`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_connect-retry-delay)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-retry-delay=#` |
  | Removed | 8.0.31 |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `0` |
  | Maximum Value | `5` |

  Number of seconds to wait between attempts to contact
  management server.
- [`--connect-string`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_connect-string)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-string=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as --ndb-connectstring.
- [`--core-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_core-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--core-file` |
  | Removed | 8.0.31 |

  Write core file on error; used in debugging.
- [`--daemon`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_daemon),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--daemon` |

  Instructs [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") to start as a daemon
  process. This is the default behavior.

  This option has no effect when running
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") on Windows platforms.
- [`--defaults-extra-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given file after global files are read.
- [`--defaults-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read default options from given file only.
- [`--defaults-group-suffix`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Also read groups with concat(group, suffix).
- [`--help`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display help text and exit.
- [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--initial` |

  Configuration data is cached internally, rather than being
  read from the cluster global configuration file each time
  the management server is started (see
  [Section 25.4.3, “NDB Cluster Configuration Files”](mysql-cluster-config-file.md "25.4.3 NDB Cluster Configuration Files")). Using the
  `--initial` option overrides this behavior,
  by forcing the management server to delete any existing
  cache files, and then to re-read the configuration data from
  the cluster configuration file and to build a new cache.

  This differs in two ways from the
  [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload) option. First,
  `--reload` forces the server to check the
  configuration file against the cache and reload its data
  only if the contents of the file are different from the
  cache. Second, `--reload` does not delete any
  existing cache files.

  If [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") is invoked with
  `--initial` but cannot find a global
  configuration file, the management server cannot start.

  When a management server starts, it checks for another
  management server in the same NDB Cluster and tries to use
  the other management server's configuration data. This
  behavior has implications when performing a rolling restart
  of an NDB Cluster with multiple management nodes. See
  [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster"), for more
  information.

  When used together with the
  [`--config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file) option, the
  cache is cleared only if the configuration file is actually
  found.
- [`--install[=name]`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_install)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--install[=name]` |
  | Platform Specific | Windows |
  | Type | String |
  | Default Value | `ndb_mgmd` |

  Causes [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") to be installed as a
  Windows service. Optionally, you can specify a name for the
  service; if not set, the service name defaults to
  `ndb_mgmd`. Although it is preferable to
  specify other [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") program options in
  a `my.ini` or `my.cnf`
  configuration file, it is possible to use them together with
  [`--install`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_install). However, in such
  cases, the [`--install`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_install) option
  must be specified first, before any other options are given,
  for the Windows service installation to succeed.

  It is generally not advisable to use this option together
  with the [`--initial`](mysql-cluster-programs-ndbd.md#option_ndbd_initial) option,
  since this causes the configuration cache to be wiped and
  rebuilt every time the service is stopped and started. Care
  should also be taken if you intend to use any other
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") options that affect the starting
  of the management server, and you should make absolutely
  certain you fully understand and allow for any possible
  consequences of doing so.

  The [`--install`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_install) option has no
  effect on non-Windows platforms.
- [`--interactive`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_interactive)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--interactive` |

  Starts [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") in interactive mode; that
  is, an [**ndb\_mgm**](mysql-cluster-programs-ndb-mgm.md "25.5.5 ndb_mgm — The NDB Cluster Management Client") client session is started
  as soon as the management server is running. This option
  does not start any other NDB Cluster nodes.
- [`--log-name=name`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_log-name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--log-name=name` |
  | Type | String |
  | Default Value | `MgmtSrvr` |

  Provides a name to be used for this node in the cluster log.
- [`--login-path`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=path` |
  | Type | String |
  | Default Value | `[none]` |

  Read given path from login file.
- [`--mycnf`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_mycnf)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mycnf` |

  Read configuration data from the `my.cnf`
  file.
- [`--ndb-connectstring`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_ndb-connectstring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-connectstring=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Set connection string. Syntax:
  `[nodeid=id;][host=]hostname[:port]`.
  Overrides entries in `NDB_CONNECTSTRING`
  and `my.cnf`. Ignored if
  [`--config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file) is specified;
  beginning with NDB 8.0.27, a warning is issued when both
  options are used.
- [`--ndb-mgmd-host`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_ndb-mgmd-host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-mgmd-host=connection_string` |
  | Type | String |
  | Default Value | `[none]` |

  Same as --ndb-connectstring.
- [`--ndb-nodeid`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_ndb-nodeid)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-nodeid=#` |
  | Type | Integer |
  | Default Value | `[none]` |

  Set node ID for this node, overriding any ID set by
  --ndb-connectstring.
- [`--ndb-optimized-node-selection`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_ndb-optimized-node-selection)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ndb-optimized-node-selection` |
  | Removed | 8.0.31 |

  Enable optimizations for selection of nodes for
  transactions. Enabled by default; use
  `--skip-ndb-optimized-node-selection` to
  disable.
- [`--no-nodeid-checks`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_no-nodeid-checks)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-nodeid-checks` |

  Do not perform any checks of node IDs.
- [`--nodaemon`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_nodaemon)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--nodaemon` |

  Instructs [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") not to start as a
  daemon process.

  The default behavior for [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") on
  Windows is to run in the foreground, making this option
  unnecessary on Windows platforms.
- [`--no-defaults`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read default options from any option file other than
  login file.
- [`--nowait-nodes`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_nowait-nodes)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--nowait-nodes=list` |
  | Type | Numeric |
  | Default Value | `[none]` |
  | Minimum Value | `1` |
  | Maximum Value | `255` |

  When starting an NDB Cluster is configured with two
  management nodes, each management server normally checks to
  see whether the other [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") is also
  operational and whether the other management server's
  configuration is identical to its own. However, it is
  sometimes desirable to start the cluster with only one
  management node (and perhaps to allow the other
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") to be started later). This
  option causes the management node to bypass any checks for
  any other management nodes whose node IDs are passed to this
  option, permitting the cluster to start as though configured
  to use only the management node that was started.

  For purposes of illustration, consider the following portion
  of a `config.ini` file (where we have
  omitted most of the configuration parameters that are not
  relevant to this example):

  ```ini
  [ndbd]
  NodeId = 1
  HostName = 198.51.100.101

  [ndbd]
  NodeId = 2
  HostName = 198.51.100.102

  [ndbd]
  NodeId = 3
  HostName = 198.51.100.103

  [ndbd]
  NodeId = 4
  HostName = 198.51.100.104

  [ndb_mgmd]
  NodeId = 10
  HostName = 198.51.100.150

  [ndb_mgmd]
  NodeId = 11
  HostName = 198.51.100.151

  [api]
  NodeId = 20
  HostName = 198.51.100.200

  [api]
  NodeId = 21
  HostName = 198.51.100.201
  ```

  Assume that you wish to start this cluster using only the
  management server having node ID `10` and
  running on the host having the IP address 198.51.100.150.
  (Suppose, for example, that the host computer on which you
  intend to the other management server is temporarily
  unavailable due to a hardware failure, and you are waiting
  for it to be repaired.) To start the cluster in this way,
  use a command line on the machine at 198.51.100.150 to enter
  the following command:

  ```terminal
  $> ndb_mgmd --ndb-nodeid=10 --nowait-nodes=11
  ```

  As shown in the preceding example, when using
  [`--nowait-nodes`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_nowait-nodes), you must
  also use the [`--ndb-nodeid`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_ndb-nodeid)
  option to specify the node ID of this
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") process.

  You can then start each of the cluster's data nodes in
  the usual way. If you wish to start and use the second
  management server in addition to the first management server
  at a later time without restarting the data nodes, you must
  start each data node with a connection string that
  references both management servers, like this:

  ```terminal
  $> ndbd -c 198.51.100.150,198.51.100.151
  ```

  The same is true with regard to the connection string used
  with any [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") processes that you wish
  to start as NDB Cluster SQL nodes connected to this cluster.
  See [Section 25.4.3.3, “NDB Cluster Connection Strings”](mysql-cluster-connection-strings.md "25.4.3.3 NDB Cluster Connection Strings"), for
  more information.

  When used with [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon"), this option
  affects the behavior of the management node with regard to
  other management nodes only. Do not confuse it with the
  [`--nowait-nodes`](mysql-cluster-programs-ndbd.md#option_ndbd_nowait-nodes) option used with
  [**ndbd**](mysql-cluster-programs-ndbd.md "25.5.1 ndbd — The NDB Cluster Data Node Daemon") or [**ndbmtd**](mysql-cluster-programs-ndbmtd.md "25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)") to
  permit a cluster to start with fewer than its full
  complement of data nodes; when used with data nodes, this
  option affects their behavior only with regard to other data
  nodes.

  Multiple management node IDs may be passed to this option as
  a comma-separated list. Each node ID must be no less than 1
  and no greater than 255. In practice, it is quite rare to
  use more than two management servers for the same NDB
  Cluster (or to have any need for doing so); in most cases
  you need to pass to this option only the single node ID for
  the one management server that you do not wish to use when
  starting the cluster.

  Note

  When you later start the “missing” management
  server, its configuration must match that of the
  management server that is already in use by the cluster.
  Otherwise, it fails the configuration check performed by
  the existing management server, and does not start.
- [`--print-defaults`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print program argument list and exit.
- [`--print-full-config`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_print-full-config),
  `-P`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-full-config` |

  Shows extended information regarding the configuration of
  the cluster. With this option on the command line the
  [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") process prints information about
  the cluster setup including an extensive list of the cluster
  configuration sections as well as parameters and their
  values. Normally used together with the
  [`--config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_config-file)
  (`-f`) option.
- [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--reload` |

  NDB Cluster configuration data is stored internally rather
  than being read from the cluster global configuration file
  each time the management server is started (see
  [Section 25.4.3, “NDB Cluster Configuration Files”](mysql-cluster-config-file.md "25.4.3 NDB Cluster Configuration Files")). Using this
  option forces the management server to check its internal
  data store against the cluster configuration file and to
  reload the configuration if it finds that the configuration
  file does not match the cache. Existing configuration cache
  files are preserved, but not used.

  This differs in two ways from the
  [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial) option. First,
  `--initial` causes all cache files to be
  deleted. Second, `--initial` forces the
  management server to re-read the global configuration file
  and construct a new cache.

  If the management server cannot find a global configuration
  file, then the `--reload` option is ignored.

  When `--reload` is used, the management
  server must be able to communicate with data nodes and any
  other management servers in the cluster before it attempts
  to read the global configuration file; otherwise, the
  management server fails to start. This can happen due to
  changes in the networking environment, such as new IP
  addresses for nodes or an altered firewall configuration. In
  such cases, you must use
  [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial) instead to force
  the existing cached configuration to be discarded and
  reloaded from the file. See
  [Section 25.6.5, “Performing a Rolling Restart of an NDB Cluster”](mysql-cluster-rolling-restart.md "25.6.5 Performing a Rolling Restart of an NDB Cluster"), for
  additional information.
- [`--remove[=name]`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_remove)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--remove[=name]` |
  | Platform Specific | Windows |
  | Type | String |
  | Default Value | `ndb_mgmd` |

  Remove a management server process that has been installed
  as a Windows service, optionally specifying the name of the
  service to be removed. Applies only to Windows platforms.
- [`--skip-config-file`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_skip-config-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--skip-config-file` |

  Do not read cluster configuration file; ignore
  [`--initial`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_initial) and
  [`--reload`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_reload) options if
  specified.
- [`--usage`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_usage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--usage` |

  Display help text and exit; same as --help.
- [`--verbose`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Remove a management server process that has been installed
  as a Windows service, optionally specifying the name of the
  service to be removed. Applies only to Windows platforms.
- [`--version`](mysql-cluster-programs-ndb-mgmd.md#option_ndb_mgmd_version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.

It is not strictly necessary to specify a connection string when
starting the management server. However, if you are using more
than one management server, a connection string should be
provided and each node in the cluster should specify its node ID
explicitly.

See [Section 25.4.3.3, “NDB Cluster Connection Strings”](mysql-cluster-connection-strings.md "25.4.3.3 NDB Cluster Connection Strings"), for
information about using connection strings.
[Section 25.5.4, “ndb\_mgmd — The NDB Cluster Management Server Daemon”](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon"), describes
other options for [**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon").

The following files are created or used by
[**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon") in its starting directory, and are
placed in the [`DataDir`](mysql-cluster-ndbd-definition.md#ndbparam-ndbd-datadir) as
specified in the `config.ini` configuration
file. In the list that follows,
*`node_id`* is the unique node
identifier.

- `config.ini` is the configuration file
  for the cluster as a whole. This file is created by the user
  and read by the management server.
  [Section 25.4, “Configuration of NDB Cluster”](mysql-cluster-configuration.md "25.4 Configuration of NDB Cluster"), discusses how
  to set up this file.
- `ndb_node_id_cluster.log`
  is the cluster events log file. Examples of such events
  include checkpoint startup and completion, node startup
  events, node failures, and levels of memory usage. A
  complete listing of cluster events with descriptions may be
  found in [Section 25.6, “Management of NDB Cluster”](mysql-cluster-management.md "25.6 Management of NDB Cluster").

  By default, when the size of the cluster log reaches one
  million bytes, the file is renamed to
  `ndb_node_id_cluster.log.seq_id`,
  where *`seq_id`* is the sequence
  number of the cluster log file. (For example: If files with
  the sequence numbers 1, 2, and 3 already exist, the next log
  file is named using the number `4`.) You
  can change the size and number of files, and other
  characteristics of the cluster log, using the
  [`LogDestination`](mysql-cluster-mgm-definition.md#ndbparam-mgmd-logdestination)
  configuration parameter.
- `ndb_node_id_out.log`
  is the file used for `stdout` and
  `stderr` when running the management server
  as a daemon.
- `ndb_node_id.pid`
  is the process ID file used when running the management
  server as a daemon.
