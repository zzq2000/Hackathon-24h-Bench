### 6.5.5 mysqlimport — A Data Import Program

The [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") client provides a
command-line interface to the [`LOAD
DATA`](load-data.md "15.2.9 LOAD DATA Statement") SQL statement. Most options to
[**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") correspond directly to clauses of
[`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement") syntax. See
[Section 15.2.9, “LOAD DATA Statement”](load-data.md "15.2.9 LOAD DATA Statement").

Invoke [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") like this:

```terminal
mysqlimport [options] db_name textfile1 [textfile2 ...]
```

For each text file named on the command line,
[**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") strips any extension from the
file name and uses the result to determine the name of the table
into which to import the file's contents. For example, files
named `patient.txt`,
`patient.text`, and
`patient` all would be imported into a table
named `patient`.

[**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") supports the following options,
which can be specified on the command line or in the
`[mysqlimport]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.16 mysqlimport Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--bind-address](mysqlimport.md#option_mysqlimport_bind-address) | Use specified network interface to connect to MySQL Server |  |  |
| [--character-sets-dir](mysqlimport.md#option_mysqlimport_character-sets-dir) | Directory where character sets can be found |  |  |
| [--columns](mysqlimport.md#option_mysqlimport_columns) | This option takes a comma-separated list of column names as its value |  |  |
| [--compress](mysqlimport.md#option_mysqlimport_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](mysqlimport.md#option_mysqlimport_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--debug](mysqlimport.md#option_mysqlimport_debug) | Write debugging log |  |  |
| [--debug-check](mysqlimport.md#option_mysqlimport_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysqlimport.md#option_mysqlimport_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysqlimport.md#option_mysqlimport_default-auth) | Authentication plugin to use |  |  |
| [--default-character-set](mysqlimport.md#option_mysqlimport_default-character-set) | Specify default character set |  |  |
| [--defaults-extra-file](mysqlimport.md#option_mysqlimport_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysqlimport.md#option_mysqlimport_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysqlimport.md#option_mysqlimport_defaults-group-suffix) | Option group suffix value |  |  |
| [--delete](mysqlimport.md#option_mysqlimport_delete) | Empty the table before importing the text file |  |  |
| [--enable-cleartext-plugin](mysqlimport.md#option_mysqlimport_enable-cleartext-plugin) | Enable cleartext authentication plugin |  |  |
| [--fields-enclosed-by](mysqlimport.md#option_mysqlimport_fields) | This option has the same meaning as the corresponding clause for LOAD DATA |  |  |
| [--fields-escaped-by](mysqlimport.md#option_mysqlimport_fields) | This option has the same meaning as the corresponding clause for LOAD DATA |  |  |
| [--fields-optionally-enclosed-by](mysqlimport.md#option_mysqlimport_fields) | This option has the same meaning as the corresponding clause for LOAD DATA |  |  |
| [--fields-terminated-by](mysqlimport.md#option_mysqlimport_fields) | This option has the same meaning as the corresponding clause for LOAD DATA |  |  |
| [--force](mysqlimport.md#option_mysqlimport_force) | Continue even if an SQL error occurs |  |  |
| [--get-server-public-key](mysqlimport.md#option_mysqlimport_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysqlimport.md#option_mysqlimport_help) | Display help message and exit |  |  |
| [--host](mysqlimport.md#option_mysqlimport_host) | Host on which MySQL server is located |  |  |
| [--ignore](mysqlimport.md#option_mysqlimport_ignore) | See the description for the --replace option |  |  |
| [--ignore-lines](mysqlimport.md#option_mysqlimport_ignore-lines) | Ignore the first N lines of the data file |  |  |
| [--lines-terminated-by](mysqlimport.md#option_mysqlimport_lines-terminated-by) | This option has the same meaning as the corresponding clause for LOAD DATA |  |  |
| [--local](mysqlimport.md#option_mysqlimport_local) | Read input files locally from the client host |  |  |
| [--lock-tables](mysqlimport.md#option_mysqlimport_lock-tables) | Lock all tables for writing before processing any text files |  |  |
| [--login-path](mysqlimport.md#option_mysqlimport_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--low-priority](mysqlimport.md#option_mysqlimport_low-priority) | Use LOW\_PRIORITY when loading the table |  |  |
| [--no-defaults](mysqlimport.md#option_mysqlimport_no-defaults) | Read no option files |  |  |
| [--password](mysqlimport.md#option_mysqlimport_password) | Password to use when connecting to server |  |  |
| [--password1](mysqlimport.md#option_mysqlimport_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password2](mysqlimport.md#option_mysqlimport_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password3](mysqlimport.md#option_mysqlimport_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--pipe](mysqlimport.md#option_mysqlimport_pipe) | Connect to server using named pipe (Windows only) |  |  |
| [--plugin-dir](mysqlimport.md#option_mysqlimport_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysqlimport.md#option_mysqlimport_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysqlimport.md#option_mysqlimport_print-defaults) | Print default options |  |  |
| [--protocol](mysqlimport.md#option_mysqlimport_protocol) | Transport protocol to use |  |  |
| [--replace](mysqlimport.md#option_mysqlimport_replace) | The --replace and --ignore options control handling of input rows that duplicate existing rows on unique key values |  |  |
| [--server-public-key-path](mysqlimport.md#option_mysqlimport_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--shared-memory-base-name](mysqlimport.md#option_mysqlimport_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--silent](mysqlimport.md#option_mysqlimport_silent) | Produce output only when errors occur |  |  |
| [--socket](mysqlimport.md#option_mysqlimport_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysqlimport.md#option_mysqlimport_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysqlimport.md#option_mysqlimport_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysqlimport.md#option_mysqlimport_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysqlimport.md#option_mysqlimport_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysqlimport.md#option_mysqlimport_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysqlimport.md#option_mysqlimport_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysqlimport.md#option_mysqlimport_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysqlimport.md#option_mysqlimport_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysqlimport.md#option_mysqlimport_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysqlimport.md#option_mysqlimport_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysqlimport.md#option_mysqlimport_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](mysqlimport.md#option_mysqlimport_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysqlimport.md#option_mysqlimport_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--use-threads](mysqlimport.md#option_mysqlimport_use-threads) | Number of threads for parallel file-loading |  |  |
| [--user](mysqlimport.md#option_mysqlimport_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysqlimport.md#option_mysqlimport_verbose) | Verbose mode |  |  |
| [--version](mysqlimport.md#option_mysqlimport_version) | Display version information and exit |  |  |
| [--zstd-compression-level](mysqlimport.md#option_mysqlimport_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysqlimport.md#option_mysqlimport_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--bind-address=ip_address`](mysqlimport.md#option_mysqlimport_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=ip_address` |

  On a computer having multiple network interfaces, use this
  option to select which interface to use for connecting to
  the MySQL server.
- [`--character-sets-dir=dir_name`](mysqlimport.md#option_mysqlimport_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Type | String |
  | Default Value | `[none]` |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--columns=column_list`](mysqlimport.md#option_mysqlimport_columns),
  `-c column_list`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--columns=column_list` |

  This option takes a list of comma-separated column names as
  its value. The order of the column names indicates how to
  match data file columns with table columns.
- [`--compress`](mysqlimport.md#option_mysqlimport_compress),
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
- [`--compression-algorithms=value`](mysqlimport.md#option_mysqlimport_compression-algorithms)

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
- [`--debug[=debug_options]`](mysqlimport.md#option_mysqlimport_debug),
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
- [`--debug-check`](mysqlimport.md#option_mysqlimport_debug-check)

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
- [`--debug-info`](mysqlimport.md#option_mysqlimport_debug-info)

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
- [`--default-character-set=charset_name`](mysqlimport.md#option_mysqlimport_default-character-set)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-character-set=charset_name` |
  | Type | String |

  Use *`charset_name`* as the default
  character set. See [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--default-auth=plugin`](mysqlimport.md#option_mysqlimport_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--defaults-extra-file=file_name`](mysqlimport.md#option_mysqlimport_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysqlimport.md#option_mysqlimport_defaults-file)

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
- [`--defaults-group-suffix=str`](mysqlimport.md#option_mysqlimport_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") normally reads the
  `[client]` and
  `[mysqlimport]` groups. If this option is
  given as
  [`--defaults-group-suffix=_other`](mysqlimport.md#option_mysqlimport_defaults-group-suffix),
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") also reads the
  `[client_other]` and
  `[mysqlimport_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--delete`](mysqlimport.md#option_mysqlimport_delete),
  `-D`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--delete` |

  Empty the table before importing the text file.
- [`--enable-cleartext-plugin`](mysqlimport.md#option_mysqlimport_enable-cleartext-plugin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--enable-cleartext-plugin` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Enable the `mysql_clear_password` cleartext
  authentication plugin. (See
  [Section 8.4.1.4, “Client-Side Cleartext Pluggable Authentication”](cleartext-pluggable-authentication.md "8.4.1.4 Client-Side Cleartext Pluggable Authentication").)
- [`--fields-terminated-by=...`](mysqlimport.md#option_mysqlimport_fields),
  [`--fields-enclosed-by=...`](mysqlimport.md#option_mysqlimport_fields),
  [`--fields-optionally-enclosed-by=...`](mysqlimport.md#option_mysqlimport_fields),
  [`--fields-escaped-by=...`](mysqlimport.md#option_mysqlimport_fields)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fields-terminated-by=string` |
  | Type | String |

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fields-enclosed-by=string` |
  | Type | String |

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fields-optionally-enclosed-by=string` |
  | Type | String |

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fields-escaped-by` |
  | Type | String |

  These options have the same meaning as the corresponding
  clauses for [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement"). See
  [Section 15.2.9, “LOAD DATA Statement”](load-data.md "15.2.9 LOAD DATA Statement").
- [`--force`](mysqlimport.md#option_mysqlimport_force),
  `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force` |

  Ignore errors. For example, if a table for a text file does
  not exist, continue processing any remaining files. Without
  [`--force`](mysqlimport.md#option_mysqlimport_force),
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") exits if a table does not
  exist.
- [`--get-server-public-key`](mysqlimport.md#option_mysqlimport_get-server-public-key)

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
  [`--server-public-key-path=file_name`](mysqlimport.md#option_mysqlimport_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlimport.md#option_mysqlimport_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--host=host_name`](mysqlimport.md#option_mysqlimport_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Import data to the MySQL server on the given host. The
  default host is `localhost`.
- [`--ignore`](mysqlimport.md#option_mysqlimport_ignore),
  `-i`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ignore` |

  See the description for the
  [`--replace`](mysqlimport.md#option_mysqlimport_replace) option.
- [`--ignore-lines=N`](mysqlimport.md#option_mysqlimport_ignore-lines)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ignore-lines=#` |
  | Type | Numeric |

  Ignore the first *`N`* lines of the
  data file.
- [`--lines-terminated-by=...`](mysqlimport.md#option_mysqlimport_lines-terminated-by)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--lines-terminated-by=string` |
  | Type | String |

  This option has the same meaning as the corresponding clause
  for [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement"). For example,
  to import Windows files that have lines terminated with
  carriage return/linefeed pairs, use
  [`--lines-terminated-by="\r\n"`](mysqlimport.md#option_mysqlimport_lines-terminated-by).
  (You might have to double the backslashes, depending on the
  escaping conventions of your command interpreter.) See
  [Section 15.2.9, “LOAD DATA Statement”](load-data.md "15.2.9 LOAD DATA Statement").
- [`--local`](mysqlimport.md#option_mysqlimport_local),
  `-L`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--local` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  By default, files are read by the server on the server host.
  With this option, [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") reads input
  files locally on the client host.

  Successful use of `LOCAL` load operations
  within [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") also requires that the
  server permits local loading; see
  [Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”](load-data-local-security.md "8.1.6 Security Considerations for LOAD DATA LOCAL")
- [`--lock-tables`](mysqldump.md#option_mysqldump_lock-tables),
  `-l`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--lock-tables` |

  Lock *all* tables for writing before
  processing any text files. This ensures that all tables are
  synchronized on the server.
- [`--login-path=name`](mysqlimport.md#option_mysqlimport_login-path)

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
- [`--low-priority`](mysqlimport.md#option_mysqlimport_low-priority)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--low-priority` |

  Use `LOW_PRIORITY` when loading the table.
  This affects only storage engines that use only table-level
  locking (such as `MyISAM`,
  `MEMORY`, and `MERGE`).
- [`--no-defaults`](mysqlimport.md#option_mysqlimport_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysqlimport.md#option_mysqlimport_no-defaults) can be
  used to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysqlimport.md#option_mysqlimport_no-defaults) is used.
  To create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--password[=password]`](mysqlimport.md#option_mysqlimport_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") prompts for one. If given,
  there must be *no space* between
  [`--password=`](mysqlimport.md#option_mysqlimport_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") should not prompt for one,
  use the
  [`--skip-password`](mysqlimport.md#option_mysqlimport_password)
  option.
- [`--password1[=pass_val]`](mysqlimport.md#option_mysqlimport_password1)

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given,
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") prompts for one. If given,
  there must be *no space* between
  [`--password1=`](mysqlimport.md#option_mysqlimport_password1) and the
  password following it. If no password option is specified,
  the default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") should not prompt for one,
  use the
  [`--skip-password1`](mysqlimport.md#option_mysqlimport_password1)
  option.

  [`--password1`](mysqlimport.md#option_mysqlimport_password1) and
  [`--password`](mysqlimport.md#option_mysqlimport_password) are
  synonymous, as are
  [`--skip-password1`](mysqlimport.md#option_mysqlimport_password1)
  and
  [`--skip-password`](mysqlimport.md#option_mysqlimport_password).
- [`--password2[=pass_val]`](mysqlimport.md#option_mysqlimport_password2)

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlimport.md#option_mysqlimport_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](mysqlimport.md#option_mysqlimport_password3)

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlimport.md#option_mysqlimport_password1); see the
  description of that option for details.
- [`--pipe`](mysqlimport.md#option_mysqlimport_pipe),
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
- [`--plugin-dir=dir_name`](mysqlimport.md#option_mysqlimport_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the
  [`--default-auth`](mysqlimport.md#option_mysqlimport_default-auth) option is
  used to specify an authentication plugin but
  [**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysqlimport.md#option_mysqlimport_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--print-defaults`](mysqlimport.md#option_mysqlimport_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysqlimport.md#option_mysqlimport_protocol)

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
- [`--replace`](mysqlimport.md#option_mysqlimport_replace),
  `-r`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--replace` |

  The [`--replace`](mysqlimport.md#option_mysqlimport_replace) and
  [`--ignore`](mysqlimport.md#option_mysqlimport_ignore) options control
  handling of input rows that duplicate existing rows on
  unique key values. If you specify
  [`--replace`](mysqlimport.md#option_mysqlimport_replace), new rows
  replace existing rows that have the same unique key value.
  If you specify [`--ignore`](mysqlimport.md#option_mysqlimport_ignore),
  input rows that duplicate an existing row on a unique key
  value are skipped. If you do not specify either option, an
  error occurs when a duplicate key value is found, and the
  rest of the text file is ignored.
- [`--server-public-key-path=file_name`](mysqlimport.md#option_mysqlimport_server-public-key-path)

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
  [`--server-public-key-path=file_name`](mysqlimport.md#option_mysqlimport_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlimport.md#option_mysqlimport_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--shared-memory-base-name=name`](mysqlimport.md#option_mysqlimport_shared-memory-base-name)

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
- [`--silent`](mysqlimport.md#option_mysqlimport_silent),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--silent` |

  Silent mode. Produce output only when errors occur.
- [`--socket=path`](mysqlimport.md#option_mysqlimport_socket),
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
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysqlimport.md#option_mysqlimport_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysqlimport.md#option_mysqlimport_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysqlimport.md#option_mysqlimport_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysqlimport.md#option_mysqlimport_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysqlimport.md#option_mysqlimport_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--tls-ciphersuites=ciphersuite_list`](mysqlimport.md#option_mysqlimport_tls-ciphersuites)

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
- [`--tls-version=protocol_list`](mysqlimport.md#option_mysqlimport_tls-version)

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
- [`--user=user_name`](mysqlimport.md#option_mysqlimport_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name,` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.
- [`--use-threads=N`](mysqlimport.md#option_mysqlimport_use-threads)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--use-threads=#` |
  | Type | Numeric |

  Load files in parallel using *`N`*
  threads.
- [`--verbose`](mysqlimport.md#option_mysqlimport_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more information about what the program
  does.
- [`--version`](mysqlimport.md#option_mysqlimport_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
- [`--zstd-compression-level=level`](mysqlimport.md#option_mysqlimport_zstd-compression-level)

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

Here is a sample session that demonstrates use of
[**mysqlimport**](mysqlimport.md "6.5.5 mysqlimport — A Data Import Program"):

```terminal
$> mysql -e 'CREATE TABLE imptest(id INT, n VARCHAR(30))' test
$> ed
a
100     Max Sydow
101     Count Dracula
.
w imptest.txt
32
q
$> od -c imptest.txt
0000000   1   0   0  \t   M   a   x       S   y   d   o   w  \n   1   0
0000020   1  \t   C   o   u   n   t       D   r   a   c   u   l   a  \n
0000040
$> mysqlimport --local test imptest.txt
test.imptest: Records: 2  Deleted: 0  Skipped: 0  Warnings: 0
$> mysql -e 'SELECT * FROM imptest' test
+------+---------------+
| id   | n             |
+------+---------------+
|  100 | Max Sydow     |
|  101 | Count Dracula |
+------+---------------+
```
