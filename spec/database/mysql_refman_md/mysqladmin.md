### 6.5.2 mysqladmin — A MySQL Server Administration Program

[**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") is a client for performing
administrative operations. You can use it to check the server's
configuration and current status, to create and drop databases,
and more.

Invoke [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") like this:

```terminal
mysqladmin [options] command [command-arg] [command [command-arg]] ...
```

[**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") supports the following commands.
Some of the commands take an argument following the command
name.

- `create db_name`

  Create a new database named
  *`db_name`*.
- `debug`

  Prior to MySQL 8.0.20, tell the server to write debug
  information to the error log. The connected user must have
  the [`SUPER`](privileges-provided.md#priv_super) privilege. Format
  and content of this information is subject to change.

  This includes information about the Event Scheduler. See
  [Section 27.4.5, “Event Scheduler Status”](events-status-info.md "27.4.5 Event Scheduler Status").
- `drop db_name`

  Delete the database named *`db_name`*
  and all its tables.
- `extended-status`

  Display the server status variables and their values.
- `flush-hosts`

  Flush all information in the host cache. See
  [Section 7.1.12.3, “DNS Lookups and the Host Cache”](host-cache.md "7.1.12.3 DNS Lookups and the Host Cache").
- `flush-logs [log_type
  ...]`

  Flush all logs.

  The [**mysqladmin flush-logs**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") command permits
  optional log types to be given, to specify which logs to
  flush. Following the `flush-logs` command,
  you can provide a space-separated list of one or more of the
  following log types: `binary`,
  `engine`, `error`,
  `general`, `relay`,
  `slow`. These correspond to the log types
  that can be specified for the [`FLUSH
  LOGS`](flush.md#flush-logs) SQL statement.
- `flush-privileges`

  Reload the grant tables (same as `reload`).
- `flush-status`

  Clear status variables.
- `flush-tables`

  Flush all tables.
- `flush-threads`

  Flush the thread cache.
- `kill
  id,id,...`

  Kill server threads. If multiple thread ID values are given,
  there must be no spaces in the list.

  To kill threads belonging to other users, the connected user
  must have the
  [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) privilege
  (or the deprecated [`SUPER`](privileges-provided.md#priv_super)
  privilege).
- `password
  new_password`

  Set a new password. This changes the password to
  *`new_password`* for the account that
  you use with [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") for connecting to
  the server. Thus, the next time you invoke
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") (or any other client program)
  using the same account, you must specify the new password.

  Warning

  Setting a password using [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program")
  should be considered *insecure*. On
  some systems, your password becomes visible to system
  status programs such as **ps** that may be
  invoked by other users to display command lines. MySQL
  clients typically overwrite the command-line password
  argument with zeros during their initialization sequence.
  However, there is still a brief interval during which the
  value is visible. Also, on some systems this overwriting
  strategy is ineffective and the password remains visible
  to **ps**. (SystemV Unix systems and
  perhaps others are subject to this problem.)

  If the *`new_password`* value
  contains spaces or other characters that are special to your
  command interpreter, you need to enclose it within quotation
  marks. On Windows, be sure to use double quotation marks
  rather than single quotation marks; single quotation marks
  are not stripped from the password, but rather are
  interpreted as part of the password. For example:

  ```terminal
  mysqladmin password "my new password"
  ```

  The new password can be omitted following the
  `password` command. In this case,
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") prompts for the password
  value, which enables you to avoid specifying the password on
  the command line. Omitting the password value should be done
  only if `password` is the final command on
  the [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") command line. Otherwise,
  the next argument is taken as the password.

  Caution

  Do not use this command used if the server was started
  with the
  [`--skip-grant-tables`](server-options.md#option_mysqld_skip-grant-tables) option.
  No password change is applied. This is true even if you
  precede the `password` command with
  `flush-privileges` on the same command
  line to re-enable the grant tables because the flush
  operation occurs after you connect. However, you can use
  [**mysqladmin flush-privileges**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") to
  re-enable the grant tables and then use a separate
  [**mysqladmin password**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") command to change
  the password.
- `ping`

  Check whether the server is available. The return status
  from [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") is 0 if the server is
  running, 1 if it is not. This is 0 even in case of an error
  such as `Access denied`, because this means
  that the server is running but refused the connection, which
  is different from the server not running.
- `processlist`

  Show a list of active server threads. This is like the
  output of the [`SHOW
  PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement") statement. If the
  [`--verbose`](mysqladmin.md#option_mysqladmin_verbose) option is
  given, the output is like that of
  [`SHOW FULL
  PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement"). (See
  [Section 15.7.7.29, “SHOW PROCESSLIST Statement”](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement").)
- `reload`

  Reload the grant tables.
- `refresh`

  Flush all tables and close and open log files.
- `shutdown`

  Stop the server.
- `start-replica`

  Start replication on a replica server. Use this command from
  MySQL 8.0.26.
- `start-slave`

  Start replication on a replica server. Use this command
  before MySQL 8.0.26.
- `status`

  Display a short server status message.
- `stop-replica`

  Stop replication on a replica server. Use this command from
  MySQL 8.0.26.
- `stop-slave`

  Stop replication on a replica server. Use this command
  before MySQL 8.0.26.
- `variables`

  Display the server system variables and their values.
- `version`

  Display version information from the server.

All commands can be shortened to any unique prefix. For example:

```terminal
$> mysqladmin proc stat
+----+-------+-----------+----+---------+------+-------+------------------+
| Id | User  | Host      | db | Command | Time | State | Info             |
+----+-------+-----------+----+---------+------+-------+------------------+
| 51 | jones | localhost |    | Query   | 0    |       | show processlist |
+----+-------+-----------+----+---------+------+-------+------------------+
Uptime: 1473624  Threads: 1  Questions: 39487
Slow queries: 0  Opens: 541  Flush tables: 1
Open tables: 19  Queries per second avg: 0.0268
```

The [**mysqladmin status**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") command result displays
the following values:

- [`Uptime`](server-status-variables.md#statvar_Uptime)

  The number of seconds the MySQL server has been running.
- `Threads`

  The number of active threads (clients).
- [`Questions`](server-status-variables.md#statvar_Questions)

  The number of questions (queries) from clients since the
  server was started.
- `Slow queries`

  The number of queries that have taken more than
  [`long_query_time`](server-system-variables.md#sysvar_long_query_time) seconds.
  See [Section 7.4.5, “The Slow Query Log”](slow-query-log.md "7.4.5 The Slow Query Log").
- `Opens`

  The number of tables the server has opened.
- `Flush tables`

  The number of `flush-*`,
  `refresh`, and `reload`
  commands the server has executed.
- `Open tables`

  The number of tables that currently are open.

If you execute [**mysqladmin shutdown**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") when
connecting to a local server using a Unix socket file,
[**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") waits until the server's process
ID file has been removed, to ensure that the server has stopped
properly.

[**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") supports the following options,
which can be specified on the command line or in the
`[mysqladmin]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.13 mysqladmin Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--bind-address](mysqladmin.md#option_mysqladmin_bind-address) | Use specified network interface to connect to MySQL Server |  |  |
| [--character-sets-dir](mysqladmin.md#option_mysqladmin_character-sets-dir) | Directory where character sets can be found |  |  |
| [--compress](mysqladmin.md#option_mysqladmin_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](mysqladmin.md#option_mysqladmin_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--connect-timeout](mysqladmin.md#option_mysqladmin_connect-timeout) | Number of seconds before connection timeout |  |  |
| [--count](mysqladmin.md#option_mysqladmin_count) | Number of iterations to make for repeated command execution |  |  |
| [--debug](mysqladmin.md#option_mysqladmin_debug) | Write debugging log |  |  |
| [--debug-check](mysqladmin.md#option_mysqladmin_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysqladmin.md#option_mysqladmin_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysqladmin.md#option_mysqladmin_default-auth) | Authentication plugin to use |  |  |
| [--default-character-set](mysqladmin.md#option_mysqladmin_default-character-set) | Specify default character set |  |  |
| [--defaults-extra-file](mysqladmin.md#option_mysqladmin_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysqladmin.md#option_mysqladmin_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysqladmin.md#option_mysqladmin_defaults-group-suffix) | Option group suffix value |  |  |
| [--enable-cleartext-plugin](mysqladmin.md#option_mysqladmin_enable-cleartext-plugin) | Enable cleartext authentication plugin |  |  |
| [--force](mysqladmin.md#option_mysqladmin_force) | Continue even if an SQL error occurs |  |  |
| [--get-server-public-key](mysqladmin.md#option_mysqladmin_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysqladmin.md#option_mysqladmin_help) | Display help message and exit |  |  |
| [--host](mysqladmin.md#option_mysqladmin_host) | Host on which MySQL server is located |  |  |
| [--login-path](mysqladmin.md#option_mysqladmin_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--no-beep](mysqladmin.md#option_mysqladmin_no-beep) | Do not beep when errors occur |  |  |
| [--no-defaults](mysqladmin.md#option_mysqladmin_no-defaults) | Read no option files |  |  |
| [--password](mysqladmin.md#option_mysqladmin_password) | Password to use when connecting to server |  |  |
| [--password1](mysqladmin.md#option_mysqladmin_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password2](mysqladmin.md#option_mysqladmin_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password3](mysqladmin.md#option_mysqladmin_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--pipe](mysqladmin.md#option_mysqladmin_pipe) | Connect to server using named pipe (Windows only) |  |  |
| [--plugin-dir](mysqladmin.md#option_mysqladmin_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysqladmin.md#option_mysqladmin_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysqladmin.md#option_mysqladmin_print-defaults) | Print default options |  |  |
| [--protocol](mysqladmin.md#option_mysqladmin_protocol) | Transport protocol to use |  |  |
| [--relative](mysqladmin.md#option_mysqladmin_relative) | Show the difference between the current and previous values when used with the --sleep option |  |  |
| [--server-public-key-path](mysqladmin.md#option_mysqladmin_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--shared-memory-base-name](mysqladmin.md#option_mysqladmin_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--show-warnings](mysqladmin.md#option_mysqladmin_show-warnings) | Show warnings after statement execution |  |  |
| [--shutdown-timeout](mysqladmin.md#option_mysqladmin_shutdown-timeout) | The maximum number of seconds to wait for server shutdown |  |  |
| [--silent](mysqladmin.md#option_mysqladmin_silent) | Silent mode |  |  |
| [--sleep](mysqladmin.md#option_mysqladmin_sleep) | Execute commands repeatedly, sleeping for delay seconds in between |  |  |
| [--socket](mysqladmin.md#option_mysqladmin_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysqladmin.md#option_mysqladmin_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysqladmin.md#option_mysqladmin_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysqladmin.md#option_mysqladmin_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysqladmin.md#option_mysqladmin_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysqladmin.md#option_mysqladmin_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysqladmin.md#option_mysqladmin_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysqladmin.md#option_mysqladmin_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysqladmin.md#option_mysqladmin_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysqladmin.md#option_mysqladmin_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysqladmin.md#option_mysqladmin_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysqladmin.md#option_mysqladmin_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](mysqladmin.md#option_mysqladmin_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysqladmin.md#option_mysqladmin_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--user](mysqladmin.md#option_mysqladmin_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysqladmin.md#option_mysqladmin_verbose) | Verbose mode |  |  |
| [--version](mysqladmin.md#option_mysqladmin_version) | Display version information and exit |  |  |
| [--vertical](mysqladmin.md#option_mysqladmin_vertical) | Print query output rows vertically (one line per column value) |  |  |
| [--wait](mysqladmin.md#option_mysqladmin_wait) | If the connection cannot be established, wait and retry instead of aborting |  |  |
| [--zstd-compression-level](mysqladmin.md#option_mysqladmin_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysqladmin.md#option_mysqladmin_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--bind-address=ip_address`](mysqladmin.md#option_mysqladmin_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=ip_address` |

  On a computer having multiple network interfaces, use this
  option to select which interface to use for connecting to
  the MySQL server.
- [`--character-sets-dir=dir_name`](mysqladmin.md#option_mysqladmin_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Type | String |
  | Default Value | `[none]` |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--compress`](mysqladmin.md#option_mysqladmin_compress),
  `-C`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--compress[={OFF|ON}]` |
  | Deprecated | 8.0.18 |
  | Type | Boolean |
  | Default Value | `OFF` |

  Compress all information sent between the client and the
  server if possible. See
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  As of MySQL 8.0.18, this option is deprecated. Expect it to
  be removed in a future version of MySQL. See
  [Configuring Legacy Connection Compression](connection-compression-control.md#connection-compression-legacy-configuration "Configuring Legacy Connection Compression").
- [`--compression-algorithms=value`](mysqladmin.md#option_mysqladmin_compression-algorithms)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--compression-algorithms=value` |
  | Introduced | 8.0.18 |
  | Type | Set |
  | Default Value | `uncompressed` |
  | Valid Values | `zlib`  `zstd`  `uncompressed` |

  The permitted compression algorithms for connections to the
  server. The available algorithms are the same as for the
  [`protocol_compression_algorithms`](server-system-variables.md#sysvar_protocol_compression_algorithms)
  system variable. The default value is
  `uncompressed`.

  For more information, see
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  This option was added in MySQL 8.0.18.
- [`--connect-timeout=value`](mysqladmin.md#option_mysqladmin_connect-timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-timeout=value` |
  | Type | Numeric |
  | Default Value | `43200` |

  The maximum number of seconds before connection timeout. The
  default value is 43200 (12 hours).
- [`--count=N`](mysqladmin.md#option_mysqladmin_count),
  `-c N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--count=#` |

  The number of iterations to make for repeated command
  execution if the [`--sleep`](mysqladmin.md#option_mysqladmin_sleep)
  option is given.
- [`--debug[=debug_options]`](mysqladmin.md#option_mysqladmin_debug),
  `-#
  [debug_options]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug[=debug_options]` |
  | Type | String |
  | Default Value | `d:t:o,/tmp/mysqladmin.trace` |

  Write a debugging log. A typical
  *`debug_options`* string is
  `d:t:o,file_name`.
  The default is
  `d:t:o,/tmp/mysqladmin.trace`.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-check`](mysqladmin.md#option_mysqladmin_debug-check)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug-check` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Print some debugging information when the program exits.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-info`](mysqladmin.md#option_mysqladmin_debug-info)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug-info` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Print debugging information and memory and CPU usage
  statistics when the program exits.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--default-auth=plugin`](mysqladmin.md#option_mysqladmin_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--default-character-set=charset_name`](mysqladmin.md#option_mysqladmin_default-character-set)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-character-set=charset_name` |
  | Type | String |

  Use *`charset_name`* as the default
  character set. See [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--defaults-extra-file=file_name`](mysqladmin.md#option_mysqladmin_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=file_name` |
  | Type | File name |

  Read this option file after the global option file but (on
  Unix) before the user option file. If the file does not
  exist or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--defaults-file=file_name`](mysqladmin.md#option_mysqladmin_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=file_name` |
  | Type | File name |

  Use only the given option file. If the file does not exist
  or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  Exception: Even with
  [`--defaults-file`](option-file-options.md#option_general_defaults-file), client
  programs read `.mylogin.cnf`.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--defaults-group-suffix=str`](mysqladmin.md#option_mysqladmin_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") normally reads the
  `[client]` and
  `[mysqladmin]` groups. If this option is
  given as
  [`--defaults-group-suffix=_other`](mysqladmin.md#option_mysqladmin_defaults-group-suffix),
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") also reads the
  `[client_other]` and
  `[mysqladmin_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--enable-cleartext-plugin`](mysqladmin.md#option_mysqladmin_enable-cleartext-plugin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--enable-cleartext-plugin` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Enable the `mysql_clear_password` cleartext
  authentication plugin. (See
  [Section 8.4.1.4, “Client-Side Cleartext Pluggable Authentication”](cleartext-pluggable-authentication.md "8.4.1.4 Client-Side Cleartext Pluggable Authentication").)
- [`--force`](mysqladmin.md#option_mysqladmin_force),
  `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force` |

  Do not ask for confirmation for the `drop
  db_name` command. With
  multiple commands, continue even if an error occurs.
- [`--get-server-public-key`](mysqladmin.md#option_mysqladmin_get-server-public-key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--get-server-public-key` |
  | Type | Boolean |

  Request from the server the public key required for RSA key
  pair-based password exchange. This option applies to clients
  that authenticate with the
  `caching_sha2_password` authentication
  plugin. For that plugin, the server does not send the public
  key unless requested. This option is ignored for accounts
  that do not authenticate with that plugin. It is also
  ignored if RSA-based password exchange is not used, as is
  the case when the client connects to the server using a
  secure connection.

  If
  [`--server-public-key-path=file_name`](mysqladmin.md#option_mysqladmin_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqladmin.md#option_mysqladmin_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--host=host_name`](mysqladmin.md#option_mysqladmin_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Connect to the MySQL server on the given host.
- [`--login-path=name`](mysqladmin.md#option_mysqladmin_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=name` |
  | Type | String |

  Read options from the named login path in the
  `.mylogin.cnf` login path file. A
  “login path” is an option group containing
  options that specify which MySQL server to connect to and
  which account to authenticate as. To create or modify a
  login path file, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--no-beep`](mysqladmin.md#option_mysqladmin_no-beep),
  `-b`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-beep` |

  Suppress the warning beep that is emitted by default for
  errors such as a failure to connect to the server.
- [`--no-defaults`](mysqladmin.md#option_mysqladmin_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysqladmin.md#option_mysqladmin_no-defaults) can be used
  to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysqladmin.md#option_mysqladmin_no-defaults) is used. To
  create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--password[=password]`](mysqladmin.md#option_mysqladmin_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") prompts for one. If given,
  there must be *no space* between
  [`--password=`](mysqladmin.md#option_mysqladmin_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") should not prompt for one, use
  the
  [`--skip-password`](mysqladmin.md#option_mysqladmin_password)
  option.
- [`--password1[=pass_val]`](mysqladmin.md#option_mysqladmin_password1)

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") prompts for one. If given, there
  must be *no space* between
  [`--password1=`](mysqladmin.md#option_mysqladmin_password1) and the
  password following it. If no password option is specified,
  the default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") should not prompt for one, use
  the
  [`--skip-password1`](mysqladmin.md#option_mysqladmin_password1)
  option.

  [`--password1`](mysqladmin.md#option_mysqladmin_password1) and
  [`--password`](mysqladmin.md#option_mysqladmin_password) are
  synonymous, as are
  [`--skip-password1`](mysql-command-options.md#option_mysql_password1)
  and
  [`--skip-password`](mysql-command-options.md#option_mysql_password).
- [`--password2[=pass_val]`](mysqladmin.md#option_mysqladmin_password2)

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqladmin.md#option_mysqladmin_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](mysqladmin.md#option_mysqladmin_password3)

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqladmin.md#option_mysqladmin_password1); see the
  description of that option for details.
- [`--pipe`](mysqladmin.md#option_mysqladmin_pipe),
  `-W`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--pipe` |
  | Type | String |

  On Windows, connect to the server using a named pipe. This
  option applies only if the server was started with the
  [`named_pipe`](server-system-variables.md#sysvar_named_pipe) system variable
  enabled to support named-pipe connections. In addition, the
  user making the connection must be a member of the Windows
  group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- [`--plugin-dir=dir_name`](mysqladmin.md#option_mysqladmin_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the
  [`--default-auth`](mysqladmin.md#option_mysqladmin_default-auth) option is
  used to specify an authentication plugin but
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysqladmin.md#option_mysqladmin_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--print-defaults`](mysqladmin.md#option_mysqladmin_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysqladmin.md#option_mysqladmin_protocol)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--protocol=type` |
  | Type | String |
  | Default Value | `[see text]` |
  | Valid Values | `TCP`  `SOCKET`  `PIPE`  `MEMORY` |

  The transport protocol to use for connecting to the server.
  It is useful when the other connection parameters normally
  result in use of a protocol other than the one you want. For
  details on the permissible values, see
  [Section 6.2.7, “Connection Transport Protocols”](transport-protocols.md "6.2.7 Connection Transport Protocols").
- [`--relative`](mysqladmin.md#option_mysqladmin_relative),
  `-r`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--relative` |

  Show the difference between the current and previous values
  when used with the
  [`--sleep`](mysqladmin.md#option_mysqladmin_sleep) option. This
  option works only with the
  `extended-status` command.
- [`--server-public-key-path=file_name`](mysqladmin.md#option_mysqladmin_server-public-key-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--server-public-key-path=file_name` |
  | Type | File name |

  The path name to a file in PEM format containing a
  client-side copy of the public key required by the server
  for RSA key pair-based password exchange. This option
  applies to clients that authenticate with the
  `sha256_password` or
  `caching_sha2_password` authentication
  plugin. This option is ignored for accounts that do not
  authenticate with one of those plugins. It is also ignored
  if RSA-based password exchange is not used, as is the case
  when the client connects to the server using a secure
  connection.

  If
  [`--server-public-key-path=file_name`](mysqladmin.md#option_mysqladmin_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqladmin.md#option_mysqladmin_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--shared-memory-base-name=name`](mysqladmin.md#option_mysqladmin_shared-memory-base-name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--shared-memory-base-name=name` |
  | Platform Specific | Windows |

  On Windows, the shared-memory name to use for connections
  made using shared memory to a local server. The default
  value is `MYSQL`. The shared-memory name is
  case-sensitive.

  This option applies only if the server was started with the
  [`shared_memory`](server-system-variables.md#sysvar_shared_memory) system
  variable enabled to support shared-memory connections.
- [`--show-warnings`](mysqladmin.md#option_mysqladmin_show-warnings)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--show-warnings` |

  Show warnings resulting from execution of statements sent to
  the server.
- [`--shutdown-timeout=value`](mysqladmin.md#option_mysqladmin_shutdown-timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--shutdown-timeout=seconds` |
  | Type | Numeric |
  | Default Value | `3600` |

  The maximum number of seconds to wait for server shutdown.
  The default value is 3600 (1 hour).
- [`--silent`](mysqladmin.md#option_mysqladmin_silent),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--silent` |

  Exit silently if a connection to the server cannot be
  established.
- [`--sleep=delay`](mysqladmin.md#option_mysqladmin_sleep),
  `-i delay`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sleep=delay` |

  Execute commands repeatedly, sleeping for
  *`delay`* seconds in between. The
  [`--count`](mysqladmin.md#option_mysqladmin_count) option determines
  the number of iterations. If
  [`--count`](mysqladmin.md#option_mysqladmin_count) is not given,
  [**mysqladmin**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") executes commands indefinitely
  until interrupted.
- [`--socket=path`](mysqladmin.md#option_mysqladmin_socket),
  `-S path`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--socket={file_name|pipe_name}` |
  | Type | String |

  For connections to `localhost`, the Unix
  socket file to use, or, on Windows, the name of the named
  pipe to use.

  On Windows, this option applies only if the server was
  started with the [`named_pipe`](server-system-variables.md#sysvar_named_pipe)
  system variable enabled to support named-pipe connections.
  In addition, the user making the connection must be a member
  of the Windows group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- `--ssl*`

  Options that begin with `--ssl` specify
  whether to connect to the server using encryption and
  indicate where to find SSL keys and certificates. See
  [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections").
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysqladmin.md#option_mysqladmin_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysqladmin.md#option_mysqladmin_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysqladmin.md#option_mysqladmin_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysqladmin.md#option_mysqladmin_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysqladmin.md#option_mysqladmin_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--tls-ciphersuites=ciphersuite_list`](mysqladmin.md#option_mysqladmin_tls-ciphersuites)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-ciphersuites=ciphersuite_list` |
  | Introduced | 8.0.16 |
  | Type | String |

  The permissible ciphersuites for encrypted connections that
  use TLSv1.3. The value is a list of one or more
  colon-separated ciphersuite names. The ciphersuites that can
  be named for this option depend on the SSL library used to
  compile MySQL. For details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").

  This option was added in MySQL 8.0.16.
- [`--tls-version=protocol_list`](mysqladmin.md#option_mysqladmin_tls-version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-version=protocol_list` |
  | Type | String |
  | Default Value (≥ 8.0.16) | `TLSv1,TLSv1.1,TLSv1.2,TLSv1.3` (OpenSSL 1.1.1 or higher)  `TLSv1,TLSv1.1,TLSv1.2` (otherwise) |
  | Default Value (≤ 8.0.15) | `TLSv1,TLSv1.1,TLSv1.2` |

  The permissible TLS protocols for encrypted connections. The
  value is a list of one or more comma-separated protocol
  names. The protocols that can be named for this option
  depend on the SSL library used to compile MySQL. For
  details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").
- [`--user=user_name`](mysqladmin.md#option_mysqladmin_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name,` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.

  If you are using the `Rewriter` plugin with
  MySQL 8.0.31 or later, you should grant this user the
  [`SKIP_QUERY_REWRITE`](privileges-provided.md#priv_skip-query-rewrite) privilege.
- [`--verbose`](mysqladmin.md#option_mysqladmin_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more information about what the program
  does.
- [`--version`](mysqladmin.md#option_mysqladmin_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
- [`--vertical`](mysqladmin.md#option_mysqladmin_vertical),
  `-E`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--vertical` |

  Print output vertically. This is similar to
  [`--relative`](mysqladmin.md#option_mysqladmin_relative), but prints
  output vertically.
- [`--wait[=count]`](mysqladmin.md#option_mysqladmin_wait),
  `-w[count]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--wait` |

  If the connection cannot be established, wait and retry
  instead of aborting. If a *`count`*
  value is given, it indicates the number of times to retry.
  The default is one time.
- [`--zstd-compression-level=level`](mysqladmin.md#option_mysqladmin_zstd-compression-level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--zstd-compression-level=#` |
  | Introduced | 8.0.18 |
  | Type | Integer |

  The compression level to use for connections to the server
  that use the `zstd` compression algorithm.
  The permitted levels are from 1 to 22, with larger values
  indicating increasing levels of compression. The default
  `zstd` compression level is 3. The
  compression level setting has no effect on connections that
  do not use `zstd` compression.

  For more information, see
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

  This option was added in MySQL 8.0.18.
