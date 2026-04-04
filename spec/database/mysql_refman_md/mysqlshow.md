### 6.5.7 mysqlshow — Display Database, Table, and Column Information

The [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") client can be used to quickly
see which databases exist, their tables, or a table's columns or
indexes.

[**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") provides a command-line interface
to several SQL [`SHOW`](show.md "15.7.7 SHOW Statements") statements.
See [Section 15.7.7, “SHOW Statements”](show.md "15.7.7 SHOW Statements"). The same information can be obtained
by using those statements directly. For example, you can issue
them from the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client program.

Invoke [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") like this:

```terminal
mysqlshow [options] [db_name [tbl_name [col_name]]]
```

- If no database is given, a list of database names is shown.
- If no table is given, all matching tables in the database
  are shown.
- If no column is given, all matching columns and column types
  in the table are shown.

The output displays only the names of those databases, tables,
or columns for which you have some privileges.

If the last argument contains shell or SQL wildcard characters
(`*`, `?`,
`%`, or `_`), only those names
that are matched by the wildcard are shown. If a database name
contains any underscores, those should be escaped with a
backslash (some Unix shells require two) to get a list of the
proper tables or columns. `*` and
`?` characters are converted into SQL
`%` and `_` wildcard
characters. This might cause some confusion when you try to
display the columns for a table with a `_` in
the name, because in this case, [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information")
shows you only the table names that match the pattern. This is
easily fixed by adding an extra `%` last on the
command line as a separate argument.

[**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") supports the following options,
which can be specified on the command line or in the
`[mysqlshow]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.18 mysqlshow Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--bind-address](mysqlshow.md#option_mysqlshow_bind-address) | Use specified network interface to connect to MySQL Server |  |  |
| [--character-sets-dir](mysqlshow.md#option_mysqlshow_character-sets-dir) | Directory where character sets can be found |  |  |
| [--compress](mysqlshow.md#option_mysqlshow_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](mysqlshow.md#option_mysqlshow_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--count](mysqlshow.md#option_mysqlshow_count) | Show the number of rows per table |  |  |
| [--debug](mysqlshow.md#option_mysqlshow_debug) | Write debugging log |  |  |
| [--debug-check](mysqlshow.md#option_mysqlshow_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysqlshow.md#option_mysqlshow_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysqlshow.md#option_mysqlshow_default-auth) | Authentication plugin to use |  |  |
| [--default-character-set](mysqlshow.md#option_mysqlshow_default-character-set) | Specify default character set |  |  |
| [--defaults-extra-file](mysqlshow.md#option_mysqlshow_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysqlshow.md#option_mysqlshow_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysqlshow.md#option_mysqlshow_defaults-group-suffix) | Option group suffix value |  |  |
| [--enable-cleartext-plugin](mysqlshow.md#option_mysqlshow_enable-cleartext-plugin) | Enable cleartext authentication plugin |  |  |
| [--get-server-public-key](mysqlshow.md#option_mysqlshow_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysqlshow.md#option_mysqlshow_help) | Display help message and exit |  |  |
| [--host](mysqlshow.md#option_mysqlshow_host) | Host on which MySQL server is located |  |  |
| [--keys](mysqlshow.md#option_mysqlshow_keys) | Show table indexes |  |  |
| [--login-path](mysqlshow.md#option_mysqlshow_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--no-defaults](mysqlshow.md#option_mysqlshow_no-defaults) | Read no option files |  |  |
| [--password](mysqlshow.md#option_mysqlshow_password) | Password to use when connecting to server |  |  |
| [--password1](mysqlshow.md#option_mysqlshow_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password2](mysqlshow.md#option_mysqlshow_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password3](mysqlshow.md#option_mysqlshow_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--pipe](mysqlshow.md#option_mysqlshow_pipe) | Connect to server using named pipe (Windows only) |  |  |
| [--plugin-dir](mysqlshow.md#option_mysqlshow_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysqlshow.md#option_mysqlshow_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysqlshow.md#option_mysqlshow_print-defaults) | Print default options |  |  |
| [--protocol](mysqlshow.md#option_mysqlshow_protocol) | Transport protocol to use |  |  |
| [--server-public-key-path](mysqlshow.md#option_mysqlshow_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--shared-memory-base-name](mysqlshow.md#option_mysqlshow_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--show-table-type](mysqlshow.md#option_mysqlshow_show-table-type) | Show a column indicating the table type |  |  |
| [--socket](mysqlshow.md#option_mysqlshow_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysqlshow.md#option_mysqlshow_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysqlshow.md#option_mysqlshow_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysqlshow.md#option_mysqlshow_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysqlshow.md#option_mysqlshow_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysqlshow.md#option_mysqlshow_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysqlshow.md#option_mysqlshow_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysqlshow.md#option_mysqlshow_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysqlshow.md#option_mysqlshow_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysqlshow.md#option_mysqlshow_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysqlshow.md#option_mysqlshow_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysqlshow.md#option_mysqlshow_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--status](mysqlshow.md#option_mysqlshow_status) | Display extra information about each table |  |  |
| [--tls-ciphersuites](mysqlshow.md#option_mysqlshow_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysqlshow.md#option_mysqlshow_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--user](mysqlshow.md#option_mysqlshow_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysqlshow.md#option_mysqlshow_verbose) | Verbose mode |  |  |
| [--version](mysqlshow.md#option_mysqlshow_version) | Display version information and exit |  |  |
| [--zstd-compression-level](mysqlshow.md#option_mysqlshow_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysqlshow.md#option_mysqlshow_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--bind-address=ip_address`](mysqlshow.md#option_mysqlshow_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=ip_address` |

  On a computer having multiple network interfaces, use this
  option to select which interface to use for connecting to
  the MySQL server.
- [`--character-sets-dir=dir_name`](mysqlshow.md#option_mysqlshow_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Type | String |
  | Default Value | `[none]` |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--compress`](mysqlshow.md#option_mysqlshow_compress),
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
- [`--compression-algorithms=value`](mysqlshow.md#option_mysqlshow_compression-algorithms)

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
- [`--count`](mysqlshow.md#option_mysqlshow_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--count` |

  Show the number of rows per table. This can be slow for
  non-`MyISAM` tables.
- [`--debug[=debug_options]`](mysqlshow.md#option_mysqlshow_debug),
  `-#
  [debug_options]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug[=debug_options]` |
  | Type | String |
  | Default Value | `d:t:o` |

  Write a debugging log. A typical
  *`debug_options`* string is
  `d:t:o,file_name`.
  The default is `d:t:o`.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-check`](mysqlshow.md#option_mysqlshow_debug-check)

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
- [`--debug-info`](mysqlshow.md#option_mysqlshow_debug-info)

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
- [`--default-character-set=charset_name`](mysqlshow.md#option_mysqlshow_default-character-set)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-character-set=charset_name` |
  | Type | String |

  Use *`charset_name`* as the default
  character set. See [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--default-auth=plugin`](mysqlshow.md#option_mysqlshow_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--defaults-extra-file=file_name`](mysqlshow.md#option_mysqlshow_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysqlshow.md#option_mysqlshow_defaults-file)

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
- [`--defaults-group-suffix=str`](mysqlshow.md#option_mysqlshow_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") normally reads the
  `[client]` and
  `[mysqlshow]` groups. If this option is
  given as
  [`--defaults-group-suffix=_other`](mysqlshow.md#option_mysqlshow_defaults-group-suffix),
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") also reads the
  `[client_other]` and
  `[mysqlshow_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--enable-cleartext-plugin`](mysqlshow.md#option_mysqlshow_enable-cleartext-plugin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--enable-cleartext-plugin` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Enable the `mysql_clear_password` cleartext
  authentication plugin. (See
  [Section 8.4.1.4, “Client-Side Cleartext Pluggable Authentication”](cleartext-pluggable-authentication.md "8.4.1.4 Client-Side Cleartext Pluggable Authentication").)
- [`--get-server-public-key`](mysqlshow.md#option_mysqlshow_get-server-public-key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--get-server-public-key` |
  | Type | Boolean |

  Request from the server the RSA public key that it uses for
  key pair-based password exchange. This option applies to
  clients that connect to the server using an account that
  authenticates with the
  `caching_sha2_password` authentication
  plugin. For connections by such accounts, the server does
  not send the public key to the client unless requested. The
  option is ignored for accounts that do not authenticate with
  that plugin. It is also ignored if RSA-based password
  exchange is not needed, as is the case when the client
  connects to the server using a secure connection.

  If
  [`--server-public-key-path=file_name`](mysqlshow.md#option_mysqlshow_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlshow.md#option_mysqlshow_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--host=host_name`](mysqlshow.md#option_mysqlshow_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Connect to the MySQL server on the given host.
- [`--keys`](mysqlshow.md#option_mysqlshow_keys),
  `-k`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keys` |

  Show table indexes.
- [`--login-path=name`](mysqlshow.md#option_mysqlshow_login-path)

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
- [`--no-defaults`](mysqlshow.md#option_mysqlshow_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysqlshow.md#option_mysqlshow_no-defaults) can be used
  to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysqlshow.md#option_mysqlshow_no-defaults) is used. To
  create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--password[=password]`](mysqlshow.md#option_mysqlshow_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") prompts for one. If given,
  there must be *no space* between
  [`--password=`](mysqlshow.md#option_mysqlshow_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") should not prompt for one, use
  the
  [`--skip-password`](mysqlshow.md#option_mysqlshow_password)
  option.
- [`--password1[=pass_val]`](mysqlshow.md#option_mysqlshow_password1)

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given,
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") prompts for one. If given,
  there must be *no space* between
  [`--password1=`](mysqlshow.md#option_mysqlshow_password1) and the
  password following it. If no password option is specified,
  the default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") should not prompt for one, use
  the
  [`--skip-password1`](mysqlshow.md#option_mysqlshow_password1)
  option.

  [`--password1`](mysqlshow.md#option_mysqlshow_password1) and
  [`--password`](mysqlshow.md#option_mysqlshow_password) are synonymous,
  as are
  [`--skip-password1`](mysqlshow.md#option_mysqlshow_password1)
  and
  [`--skip-password`](mysqlshow.md#option_mysqlshow_password).
- [`--password2[=pass_val]`](mysqlshow.md#option_mysqlshow_password2)

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlshow.md#option_mysqlshow_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](mysqlshow.md#option_mysqlshow_password3)

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlshow.md#option_mysqlshow_password1); see the
  description of that option for details.
- [`--pipe`](mysqlshow.md#option_mysqlshow_pipe),
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
- [`--plugin-dir=dir_name`](mysqlshow.md#option_mysqlshow_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the
  [`--default-auth`](mysqlshow.md#option_mysqlshow_default-auth) option is
  used to specify an authentication plugin but
  [**mysqlshow**](mysqlshow.md "6.5.7 mysqlshow — Display Database, Table, and Column Information") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysqlshow.md#option_mysqlshow_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--print-defaults`](mysqlshow.md#option_mysqlshow_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysqlshow.md#option_mysqlshow_protocol)

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
- [`--server-public-key-path=file_name`](mysqlshow.md#option_mysqlshow_server-public-key-path)

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
  [`--server-public-key-path=file_name`](mysqlshow.md#option_mysqlshow_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlshow.md#option_mysqlshow_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--shared-memory-base-name=name`](mysqlshow.md#option_mysqlshow_shared-memory-base-name)

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
- [`--show-table-type`](mysqlshow.md#option_mysqlshow_show-table-type),
  `-t`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--show-table-type` |

  Show a column indicating the table type, as in
  [`SHOW FULL
  TABLES`](show-tables.md "15.7.7.39 SHOW TABLES Statement"). The type is `BASE TABLE`
  or `VIEW`.
- [`--socket=path`](mysqlshow.md#option_mysqlshow_socket),
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
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysqlshow.md#option_mysqlshow_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysqlshow.md#option_mysqlshow_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysqlshow.md#option_mysqlshow_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysqlshow.md#option_mysqlshow_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysqlshow.md#option_mysqlshow_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--status`](mysqlshow.md#option_mysqlshow_status),
  `-i`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--status` |

  Display extra information about each table.
- [`--tls-ciphersuites=ciphersuite_list`](mysqlshow.md#option_mysqlshow_tls-ciphersuites)

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
- [`--tls-version=protocol_list`](mysqlshow.md#option_mysqlshow_tls-version)

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
- [`--user=user_name`](mysqlshow.md#option_mysqlshow_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name,` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.
- [`--verbose`](mysqlshow.md#option_mysqlshow_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more information about what the program
  does. This option can be used multiple times to increase the
  amount of information.
- [`--version`](mysqlshow.md#option_mysqlshow_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
- [`--zstd-compression-level=level`](mysqlshow.md#option_mysqlshow_zstd-compression-level)

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
