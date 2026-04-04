#### 6.5.1.1 mysql Client Options

[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") supports the following options, which
can be specified on the command line or in the
`[mysql]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.12 mysql Client Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--authentication-oci-client-config-profile](mysql-command-options.md#option_mysql_authentication-oci-client-config-profile) | Name of the OCI profile defined in the OCI config file to use | 8.0.33 |  |
| [--auto-rehash](mysql-command-options.md#option_mysql_auto-rehash) | Enable automatic rehashing |  |  |
| [--auto-vertical-output](mysql-command-options.md#option_mysql_auto-vertical-output) | Enable automatic vertical result set display |  |  |
| [--batch](mysql-command-options.md#option_mysql_batch) | Do not use history file |  |  |
| [--binary-as-hex](mysql-command-options.md#option_mysql_binary-as-hex) | Display binary values in hexadecimal notation |  |  |
| [--binary-mode](mysql-command-options.md#option_mysql_binary-mode) | Disable \r\n - to - \n translation and treatment of \0 as end-of-query |  |  |
| [--bind-address](mysql-command-options.md#option_mysql_bind-address) | Use specified network interface to connect to MySQL Server |  |  |
| [--character-sets-dir](mysql-command-options.md#option_mysql_character-sets-dir) | Directory where character sets are installed |  |  |
| [--column-names](mysql-command-options.md#option_mysql_column-names) | Write column names in results |  |  |
| [--column-type-info](mysql-command-options.md#option_mysql_column-type-info) | Display result set metadata |  |  |
| [--commands](mysql-command-options.md#option_mysql_commands) | Enable or disable processing of local mysql client commands | 8.0.43 |  |
| [--comments](mysql-command-options.md#option_mysql_comments) | Whether to retain or strip comments in statements sent to the server |  |  |
| [--compress](mysql-command-options.md#option_mysql_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](mysql-command-options.md#option_mysql_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--connect-expired-password](mysql-command-options.md#option_mysql_connect-expired-password) | Indicate to server that client can handle expired-password sandbox mode |  |  |
| [--connect-timeout](mysql-command-options.md#option_mysql_connect-timeout) | Number of seconds before connection timeout |  |  |
| [--database](mysql-command-options.md#option_mysql_database) | The database to use |  |  |
| [--debug](mysql-command-options.md#option_mysql_debug) | Write debugging log; supported only if MySQL was built with debugging support |  |  |
| [--debug-check](mysql-command-options.md#option_mysql_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysql-command-options.md#option_mysql_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysql-command-options.md#option_mysql_default-auth) | Authentication plugin to use |  |  |
| [--default-character-set](mysql-command-options.md#option_mysql_default-character-set) | Specify default character set |  |  |
| [--defaults-extra-file](mysql-command-options.md#option_mysql_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysql-command-options.md#option_mysql_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysql-command-options.md#option_mysql_defaults-group-suffix) | Option group suffix value |  |  |
| [--delimiter](mysql-command-options.md#option_mysql_delimiter) | Set the statement delimiter |  |  |
| [--dns-srv-name](mysql-command-options.md#option_mysql_dns-srv-name) | Use DNS SRV lookup for host information | 8.0.22 |  |
| [--enable-cleartext-plugin](mysql-command-options.md#option_mysql_enable-cleartext-plugin) | Enable cleartext authentication plugin |  |  |
| [--execute](mysql-command-options.md#option_mysql_execute) | Execute the statement and quit |  |  |
| [--fido-register-factor](mysql-command-options.md#option_mysql_fido-register-factor) | Multifactor authentication factors for which registration must be done | 8.0.27 | 8.0.35 |
| [--force](mysql-command-options.md#option_mysql_force) | Continue even if an SQL error occurs |  |  |
| [--get-server-public-key](mysql-command-options.md#option_mysql_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysql-command-options.md#option_mysql_help) | Display help message and exit |  |  |
| [--histignore](mysql-command-options.md#option_mysql_histignore) | Patterns specifying which statements to ignore for logging |  |  |
| [--host](mysql-command-options.md#option_mysql_host) | Host on which MySQL server is located |  |  |
| [--html](mysql-command-options.md#option_mysql_html) | Produce HTML output |  |  |
| [--ignore-spaces](mysql-command-options.md#option_mysql_ignore-spaces) | Ignore spaces after function names |  |  |
| [--init-command](mysql-command-options.md#option_mysql_init-command) | SQL statement to execute after connecting |  |  |
| [--line-numbers](mysql-command-options.md#option_mysql_line-numbers) | Write line numbers for errors |  |  |
| [--load-data-local-dir](mysql-command-options.md#option_mysql_load-data-local-dir) | Directory for files named in LOAD DATA LOCAL statements | 8.0.21 |  |
| [--local-infile](mysql-command-options.md#option_mysql_local-infile) | Enable or disable for LOCAL capability for LOAD DATA |  |  |
| [--login-path](mysql-command-options.md#option_mysql_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--max-allowed-packet](mysql-command-options.md#option_mysql_max-allowed-packet) | Maximum packet length to send to or receive from server |  |  |
| [--max-join-size](mysql-command-options.md#option_mysql_max-join-size) | The automatic limit for rows in a join when using --safe-updates |  |  |
| [--named-commands](mysql-command-options.md#option_mysql_named-commands) | Enable named mysql commands |  |  |
| [--net-buffer-length](mysql-command-options.md#option_mysql_net-buffer-length) | Buffer size for TCP/IP and socket communication |  |  |
| [--network-namespace](mysql-command-options.md#option_mysql_network-namespace) | Specify network namespace | 8.0.22 |  |
| [--no-auto-rehash](mysql-command-options.md#option_mysql_no-auto-rehash) | Disable automatic rehashing |  |  |
| [--no-beep](mysql-command-options.md#option_mysql_no-beep) | Do not beep when errors occur |  |  |
| [--no-defaults](mysql-command-options.md#option_mysql_no-defaults) | Read no option files |  |  |
| --oci-config-file | Defines an alternate location for the Oracle Cloud Infrastructure CLI configuration file. | 8.0.27 |  |
| [--one-database](mysql-command-options.md#option_mysql_one-database) | Ignore statements except those for the default database named on the command line |  |  |
| [--pager](mysql-command-options.md#option_mysql_pager) | Use the given command for paging query output |  |  |
| [--password](mysql-command-options.md#option_mysql_password) | Password to use when connecting to server |  |  |
| [--password1](mysql-command-options.md#option_mysql_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password2](mysql-command-options.md#option_mysql_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password3](mysql-command-options.md#option_mysql_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--pipe](mysql-command-options.md#option_mysql_pipe) | Connect to server using named pipe (Windows only) |  |  |
| [--plugin-authentication-kerberos-client-mode](mysql-command-options.md#option_mysql_plugin-authentication-kerberos-client-mode) | Permit GSSAPI pluggable authentication through the MIT Kerberos library on Windows | 8.0.32 |  |
| [--plugin-dir](mysql-command-options.md#option_mysql_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysql-command-options.md#option_mysql_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysql-command-options.md#option_mysql_print-defaults) | Print default options |  |  |
| [--prompt](mysql-command-options.md#option_mysql_prompt) | Set the prompt to the specified format |  |  |
| [--protocol](mysql-command-options.md#option_mysql_protocol) | Transport protocol to use |  |  |
| [--quick](mysql-command-options.md#option_mysql_quick) | Do not cache each query result |  |  |
| [--raw](mysql-command-options.md#option_mysql_raw) | Write column values without escape conversion |  |  |
| [--reconnect](mysql-command-options.md#option_mysql_reconnect) | If the connection to the server is lost, automatically try to reconnect |  |  |
| [--safe-updates](mysql-command-options.md#option_mysql_safe-updates), [--i-am-a-dummy](mysql-command-options.md#option_mysql_safe-updates) | Allow only UPDATE and DELETE statements that specify key values |  |  |
| [--select-limit](mysql-command-options.md#option_mysql_select-limit) | The automatic limit for SELECT statements when using --safe-updates |  |  |
| [--server-public-key-path](mysql-command-options.md#option_mysql_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--shared-memory-base-name](mysql-command-options.md#option_mysql_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--show-warnings](mysql-command-options.md#option_mysql_show-warnings) | Show warnings after each statement if there are any |  |  |
| [--sigint-ignore](mysql-command-options.md#option_mysql_sigint-ignore) | Ignore SIGINT signals (typically the result of typing Control+C) |  |  |
| [--silent](mysql-command-options.md#option_mysql_silent) | Silent mode |  |  |
| [--skip-auto-rehash](mysql-command-options.md#option_mysql_auto-rehash) | Disable automatic rehashing |  |  |
| [--skip-column-names](mysql-command-options.md#option_mysql_skip-column-names) | Do not write column names in results |  |  |
| [--skip-line-numbers](mysql-command-options.md#option_mysql_skip-line-numbers) | Skip line numbers for errors |  |  |
| [--skip-named-commands](mysql-command-options.md#option_mysql_named-commands) | Disable named mysql commands |  |  |
| [--skip-pager](mysql-command-options.md#option_mysql_pager) | Disable paging |  |  |
| [--skip-reconnect](mysql-command-options.md#option_mysql_reconnect) | Disable reconnecting |  |  |
| [--skip-system-command](mysql-command-options.md#option_mysql_skip-system-command) | Disable system (\!) command | 8.0.40 |  |
| [--socket](mysql-command-options.md#option_mysql_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysql-command-options.md#option_mysql_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysql-command-options.md#option_mysql_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysql-command-options.md#option_mysql_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysql-command-options.md#option_mysql_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysql-command-options.md#option_mysql_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysql-command-options.md#option_mysql_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysql-command-options.md#option_mysql_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysql-command-options.md#option_mysql_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysql-command-options.md#option_mysql_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysql-command-options.md#option_mysql_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysql-command-options.md#option_mysql_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--syslog](mysql-command-options.md#option_mysql_syslog) | Log interactive statements to syslog |  |  |
| [--system-command](mysql-command-options.md#option_mysql_system-command) | Enable or disable system (\!) command | 8.0.40 |  |
| [--table](mysql-command-options.md#option_mysql_table) | Display output in tabular format |  |  |
| [--tee](mysql-command-options.md#option_mysql_tee) | Append a copy of output to named file |  |  |
| [--tls-ciphersuites](mysql-command-options.md#option_mysql_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysql-command-options.md#option_mysql_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--unbuffered](mysql-command-options.md#option_mysql_unbuffered) | Flush the buffer after each query |  |  |
| [--user](mysql-command-options.md#option_mysql_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysql-command-options.md#option_mysql_verbose) | Verbose mode |  |  |
| [--version](mysql-command-options.md#option_mysql_version) | Display version information and exit |  |  |
| [--vertical](mysql-command-options.md#option_mysql_vertical) | Print query output rows vertically (one line per column value) |  |  |
| [--wait](mysql-command-options.md#option_mysql_wait) | If the connection cannot be established, wait and retry instead of aborting |  |  |
| [--xml](mysql-command-options.md#option_mysql_xml) | Produce XML output |  |  |
| [--zstd-compression-level](mysql-command-options.md#option_mysql_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysql-command-options.md#option_mysql_help), `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--authentication-oci-client-config-profile`](mysql-command-options.md#option_mysql_authentication-oci-client-config-profile)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-oci-client-config-profile=profileName` |
  | Introduced | 8.0.33 |
  | Type | String |

  Specify the name of the OCI configuration profile to use. If
  not set, the default profile is used.
- [`--auto-rehash`](mysql-command-options.md#option_mysql_auto-rehash)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-rehash` |
  | Disabled by | `skip-auto-rehash` |

  Enable automatic rehashing. This option is on by default,
  which enables database, table, and column name completion.
  Use
  [`--disable-auto-rehash`](mysql-command-options.md#option_mysql_auto-rehash)
  to disable rehashing. That causes [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  to start faster, but you must issue the
  `rehash` command or its
  `\#` shortcut if you want to use name
  completion.

  To complete a name, enter the first part and press Tab. If
  the name is unambiguous, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") completes
  it. Otherwise, you can press Tab again to see the possible
  names that begin with what you have typed so far. Completion
  does not occur if there is no default database.

  Note

  This feature requires a MySQL client that is compiled with
  the **readline** library.
  Typically, the **readline**
  library is not available on Windows.
- [`--auto-vertical-output`](mysql-command-options.md#option_mysql_auto-vertical-output)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-vertical-output` |

  Cause result sets to be displayed vertically if they are too
  wide for the current window, and using normal tabular format
  otherwise. (This applies to statements terminated by
  `;` or `\G`.)
- [`--batch`](mysql-command-options.md#option_mysql_batch), `-B`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--batch` |

  Print results using tab as the column separator, with each
  row on a new line. With this option,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") does not use the history file.

  Batch mode results in nontabular output format and escaping
  of special characters. Escaping may be disabled by using raw
  mode; see the description for the
  [`--raw`](mysql-command-options.md#option_mysql_raw) option.
- [`--binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--binary-as-hex` |
  | Type | Boolean |
  | Default Value (≥ 8.0.19) | `FALSE in noninteractive mode` |
  | Default Value (≤ 8.0.18) | `FALSE` |

  When this option is given, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") displays
  binary data using hexadecimal notation
  (`0xvalue`).
  This occurs whether the overall output display format is
  tabular, vertical, HTML, or XML.

  [`--binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex) when enabled
  affects display of all binary strings, including those
  returned by functions such as
  [`CHAR()`](string-functions.md#function_char) and
  [`UNHEX()`](string-functions.md#function_unhex). The following
  example demonstrates this using the ASCII code for
  `A` (65 decimal, 41 hexadecimal):

  - [`--binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex) disabled:

    ```sql
    mysql> SELECT CHAR(0x41), UNHEX('41');
    +------------+-------------+
    | CHAR(0x41) | UNHEX('41') |
    +------------+-------------+
    | A          | A           |
    +------------+-------------+
    ```
  - [`--binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex) enabled:

    ```sql
    mysql> SELECT CHAR(0x41), UNHEX('41');
    +------------------------+--------------------------+
    | CHAR(0x41)             | UNHEX('41')              |
    +------------------------+--------------------------+
    | 0x41                   | 0x41                     |
    +------------------------+--------------------------+
    ```

  To write a binary string expression so that it displays as a
  character string regardless of whether
  [`--binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex) is enabled,
  use these techniques:

  - The [`CHAR()`](string-functions.md#function_char) function has a
    `USING
    charset` clause:

    ```sql
    mysql> SELECT CHAR(0x41 USING utf8mb4);
    +--------------------------+
    | CHAR(0x41 USING utf8mb4) |
    +--------------------------+
    | A                        |
    +--------------------------+
    ```
  - More generally, use
    [`CONVERT()`](cast-functions.md#function_convert) to convert an
    expression to a given character set:

    ```sql
    mysql> SELECT CONVERT(UNHEX('41') USING utf8mb4);
    +------------------------------------+
    | CONVERT(UNHEX('41') USING utf8mb4) |
    +------------------------------------+
    | A                                  |
    +------------------------------------+
    ```

  As of MySQL 8.0.19, when [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") operates
  in interactive mode, this option is enabled by default. In
  addition, output from the `status` (or
  `\s`) command includes this line when the
  option is enabled implicitly or explicitly:

  ```none
  Binary data as: Hexadecimal
  ```

  To disable hexadecimal notation, use
  [`--skip-binary-as-hex`](mysql-command-options.md#option_mysql_binary-as-hex)
- [`--binary-mode`](mysql-command-options.md#option_mysql_binary-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--binary-mode` |

  This option helps when processing
  [**mysqlbinlog**](mysqlbinlog.md "6.6.9 mysqlbinlog — Utility for Processing Binary Log Files") output that may contain
  [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") values. By default,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") translates `\r\n`
  in statement strings to `\n` and interprets
  `\0` as the statement terminator.
  [`--binary-mode`](mysql-command-options.md#option_mysql_binary-mode) disables both
  features. It also disables all [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  commands except `charset` and
  `delimiter` in noninteractive mode (for
  input piped to [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") or loaded using the
  `source` command).

  (*MySQL 8.0.43 and later:*)
  `--binary-mode`, when enabled, causes the
  server to disregard any setting for
  [`--commands`](mysql-command-options.md#option_mysql_commands) .
- [`--bind-address=ip_address`](mysql-command-options.md#option_mysql_bind-address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--bind-address=ip_address` |

  On a computer having multiple network interfaces, use this
  option to select which interface to use for connecting to
  the MySQL server.
- [`--character-sets-dir=dir_name`](mysql-command-options.md#option_mysql_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=dir_name` |
  | Type | Directory name |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--column-names`](mysql-command-options.md#option_mysql_column-names)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--column-names` |

  Write column names in results.
- [`--column-type-info`](mysql-command-options.md#option_mysql_column-type-info)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--column-type-info` |

  Display result set metadata. This information corresponds to
  the contents of C API `MYSQL_FIELD` data
  structures. See [C API Basic Data Structures](https://dev.mysql.com/doc/c-api/8.0/en/c-api-data-structures.html).
- [`--commands`](mysql-command-options.md#option_mysql_commands)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--commands` |
  | Introduced | 8.0.43 |
  | Type | Boolean |
  | Default Value | `TRUE` |

  Whether to enable or disable processing of local
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client commands. Setting this
  option to `FALSE` disables such processing,
  and has the effects listed here:

  - The following [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client commands
    are disabled:

    - `charset` (`/C`
      remains enabled)
    - `clear`
    - `connect`
    - `edit`
    - `ego`
    - `exit`
    - `go`
    - `help`
    - `nopager`
    - `notee`
    - `nowarning`
    - `pager`
    - `print`
    - `prompt`
    - `query_attributes`
    - `quit`
    - `rehash`
    - `resetconnection`
    - `ssl_session_data_print`
    - `source`
    - `status`
    - `system`
    - `tee`
    - `\u` (`use` is
      passed to the server)
    - `warnings`
  - The `\C` and
    `delimiter` commands remain enabled.
  - The [`--system-command`](mysql-command-options.md#option_mysql_system-command)
    option is ignored, and has no effect.

  This option has no effect when
  [`--binary-mode`](mysql-command-options.md#option_mysql_binary-mode) is enabled.

  When `--commands` is enabled, it is possible
  to disable (only) the system command using the
  [`--system-command`](mysql-command-options.md#option_mysql_system-command) option.

  This option was added in MySQL 8.0.43.
- [`--comments`](mysql-command-options.md#option_mysql_comments),
  `-c`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--comments` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Whether to strip or preserve comments in statements sent to
  the server. The default is
  [`--skip-comments`](mysql-command-options.md#option_mysql_comments)
  (strip comments), enable with
  [`--comments`](mysql-command-options.md#option_mysql_comments) (preserve
  comments).

  Note

  The [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client always passes
  optimizer hints to the server, regardless of whether this
  option is given.

  Comment stripping is deprecated. Expect this feature and
  the options to control it to be removed in a future MySQL
  release.
- [`--compress`](mysql-command-options.md#option_mysql_compress),
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
- [`--compression-algorithms=value`](mysql-command-options.md#option_mysql_compression-algorithms)

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
- [`--connect-expired-password`](mysql-command-options.md#option_mysql_connect-expired-password)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-expired-password` |

  Indicate to the server that the client can handle sandbox
  mode if the account used to connect has an expired password.
  This can be useful for noninteractive invocations of
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") because normally the server
  disconnects noninteractive clients that attempt to connect
  using an account with an expired password. (See
  [Section 8.2.16, “Server Handling of Expired Passwords”](expired-password-handling.md "8.2.16 Server Handling of Expired Passwords").)
- [`--connect-timeout=value`](mysql-command-options.md#option_mysql_connect-timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--connect-timeout=value` |
  | Type | Numeric |
  | Default Value | `0` |

  The number of seconds before connection timeout. (Default
  value is `0`.)
- [`--database=db_name`](mysql-command-options.md#option_mysql_database),
  `-D db_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--database=dbname` |
  | Type | String |

  The database to use. This is useful primarily in an option
  file.
- [`--debug[=debug_options]`](mysql-command-options.md#option_mysql_debug),
  `-#
  [debug_options]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug[=debug_options]` |
  | Type | String |
  | Default Value | `d:t:o,/tmp/mysql.trace` |

  Write a debugging log. A typical
  *`debug_options`* string is
  `d:t:o,file_name`.
  The default is `d:t:o,/tmp/mysql.trace`.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-check`](mysql-command-options.md#option_mysql_debug-check)

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
- [`--debug-info`](mysql-command-options.md#option_mysql_debug-info),
  `-T`

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
- [`--default-auth=plugin`](mysql-command-options.md#option_mysql_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--default-character-set=charset_name`](mysql-command-options.md#option_mysql_default-character-set)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-character-set=charset_name` |
  | Type | String |

  Use *`charset_name`* as the default
  character set for the client and connection.

  This option can be useful if the operating system uses one
  character set and the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client by
  default uses another. In this case, output may be formatted
  incorrectly. You can usually fix such issues by using this
  option to force the client to use the system character set
  instead.

  For more information, see
  [Section 12.4, “Connection Character Sets and Collations”](charset-connection.md "12.4 Connection Character Sets and Collations"), and
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--defaults-extra-file=file_name`](mysql-command-options.md#option_mysql_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysql-command-options.md#option_mysql_defaults-file)

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
- [`--defaults-group-suffix=str`](mysql-command-options.md#option_mysql_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") normally reads the
  `[client]` and `[mysql]`
  groups. If this option is given as
  [`--defaults-group-suffix=_other`](mysql-command-options.md#option_mysql_defaults-group-suffix),
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") also reads the
  `[client_other]` and
  `[mysql_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--delimiter=str`](mysql-command-options.md#option_mysql_delimiter)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--delimiter=str` |
  | Type | String |
  | Default Value | `;` |

  Set the statement delimiter. The default is the semicolon
  character (`;`).
- [`--disable-named-commands`](mysql-command-options.md#option_mysql_disable-named-commands)

  Disable named commands. Use the `\*` form
  only, or use named commands only at the beginning of a line
  ending with a semicolon (`;`).
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") starts with this option
  *enabled* by default. However, even with
  this option, long-format commands still work from the first
  line. See [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands").
- [`--dns-srv-name=name`](mysql-command-options.md#option_mysql_dns-srv-name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--dns-srv-name=name` |
  | Introduced | 8.0.22 |
  | Type | String |

  Specifies the name of a DNS SRV record that determines the
  candidate hosts to use for establishing a connection to a
  MySQL server. For information about DNS SRV support in
  MySQL, see [Section 6.2.6, “Connecting to the Server Using DNS SRV Records”](connecting-using-dns-srv.md "6.2.6 Connecting to the Server Using DNS SRV Records").

  Suppose that DNS is configured with this SRV information for
  the `example.com` domain:

  ```simple
  Name                     TTL   Class   Priority Weight Port Target
  _mysql._tcp.example.com. 86400 IN SRV  0        5      3306 host1.example.com
  _mysql._tcp.example.com. 86400 IN SRV  0        10     3306 host2.example.com
  _mysql._tcp.example.com. 86400 IN SRV  10       5      3306 host3.example.com
  _mysql._tcp.example.com. 86400 IN SRV  20       5      3306 host4.example.com
  ```

  To use that DNS SRV record, invoke [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  like this:

  ```terminal
  mysql --dns-srv-name=_mysql._tcp.example.com
  ```

  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") then attempts a connection to each
  server in the group until a successful connection is
  established. A failure to connect occurs only if a
  connection cannot be established to any of the servers. The
  priority and weight values in the DNS SRV record determine
  the order in which servers should be tried.

  When invoked with
  [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name),
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") attempts to establish TCP
  connections only.

  The [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) option
  takes precedence over the
  [`--host`](mysql-command-options.md#option_mysql_host) option if both are
  given. [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) causes
  connection establishment to use the
  [`mysql_real_connect_dns_srv()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.html)
  C API function rather than
  [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.html).
  However, if the `connect` command is
  subsequently used at runtime and specifies a host name
  argument, that host name takes precedence over any
  [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) option given at
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") startup to specify a DNS SRV
  record.

  This option was added in MySQL 8.0.22.
- [`--enable-cleartext-plugin`](mysql-command-options.md#option_mysql_enable-cleartext-plugin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--enable-cleartext-plugin` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Enable the `mysql_clear_password` cleartext
  authentication plugin. (See
  [Section 8.4.1.4, “Client-Side Cleartext Pluggable Authentication”](cleartext-pluggable-authentication.md "8.4.1.4 Client-Side Cleartext Pluggable Authentication").)
- [`--execute=statement`](mysql-command-options.md#option_mysql_execute),
  `-e statement`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--execute=statement` |
  | Type | String |

  Execute the statement and quit. The default output format is
  like that produced with
  [`--batch`](mysql-command-options.md#option_mysql_batch). See
  [Section 6.2.2.1, “Using Options on the Command Line”](command-line-options.md "6.2.2.1 Using Options on the Command Line"), for some examples.
  With this option, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") does not use the
  history file.
- [`--fido-register-factor=value`](mysql-command-options.md#option_mysql_fido-register-factor)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fido-register-factor=value` |
  | Introduced | 8.0.27 |
  | Deprecated | 8.0.35 |
  | Type | String |

  Note

  As of MySQL 8.0.35, this option is deprecated and subject
  to removal in a future MySQL release.

  The factor or factors for which FIDO device registration
  must be performed. This option value must be a single value,
  or two values separated by commas. Each value must be 2 or
  3, so the permitted option values are
  `'2'`, `'3'`,
  `'2,3'` and `'3,2'`.

  For example, an account that requires registration for a 3rd
  authentication factor invokes the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  client as follows:

  ```terminal
  mysql --user=user_name --fido-register-factor=3
  ```

  An account that requires registration for a 2nd and 3rd
  authentication factor invokes the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  client as follows:

  ```terminal
  mysql --user=user_name --fido-register-factor=2,3
  ```

  If registration is successful, a connection is established.
  If there is an authentication factor with a pending
  registration, a connection is placed into pending
  registration mode when attempting to connect to the server.
  In this case, disconnect and reconnect with the correct
  [`--fido-register-factor`](mysql-command-options.md#option_mysql_fido-register-factor) value
  to complete the registration.

  Registration is a two step process comprising
  *initiate registration* and
  *finish registration* steps. The initiate
  registration step executes this statement:

  ```sql
  ALTER USER user factor INITIATE REGISTRATION
  ```

  The statement returns a result set containing a 32 byte
  challenge, the user name, and the relying party ID (see
  [`authentication_fido_rp_id`](pluggable-authentication-system-variables.md#sysvar_authentication_fido_rp_id)).

  The finish registration step executes this statement:

  ```sql
  ALTER USER user factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS 'auth_string'
  ```

  The statement completes the registration and sends the
  following information to the server as part of the
  *`auth_string`*: authenticator data,
  an optional attestation certificate in X.509 format, and a
  signature.

  The initiate and registration steps must be performed in a
  single connection, as the challenge received by the client
  during the initiate step is saved to the client connection
  handler. Registration would fail if the registration step
  was performed by a different connection. The
  [`--fido-register-factor`](mysql-command-options.md#option_mysql_fido-register-factor) option
  executes both the initiate and registration steps, which
  avoids the failure scenario described above and prevents
  having to execute the [`ALTER
  USER`](alter-user.md "15.7.1.1 ALTER USER Statement") initiate and registration statements
  manually.

  The [`--fido-register-factor`](mysql-command-options.md#option_mysql_fido-register-factor)
  option is only available for the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client")
  client and MySQL Shell. Other MySQL client programs do not
  support it.

  For related information, see
  [Using FIDO Authentication](fido-pluggable-authentication.md#fido-pluggable-authentication-usage "Using FIDO Authentication").
- [`--force`](mysql-command-options.md#option_mysql_force), `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force` |

  Continue even if an SQL error occurs.
- [`--get-server-public-key`](mysql-command-options.md#option_mysql_get-server-public-key)

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
  [`--server-public-key-path=file_name`](mysql-command-options.md#option_mysql_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysql-command-options.md#option_mysql_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--histignore`](mysql-command-options.md#option_mysql_histignore)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--histignore=pattern_list` |
  | Type | String |

  A list of one or more colon-separated patterns specifying
  statements to ignore for logging purposes. These patterns
  are added to the default pattern list
  (`"*IDENTIFIED*:*PASSWORD*"`). The value
  specified for this option affects logging of statements
  written to the history file, and to
  `syslog` if the
  [`--syslog`](mysql-command-options.md#option_mysql_syslog) option is given. For
  more information, see [Section 6.5.1.3, “mysql Client Logging”](mysql-logging.md "6.5.1.3 mysql Client Logging").
- [`--host=host_name`](mysql-command-options.md#option_mysql_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Connect to the MySQL server on the given host.

  The [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) option
  takes precedence over the
  [`--host`](mysql-command-options.md#option_mysql_host) option if both are
  given. [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) causes
  connection establishment to use the
  [`mysql_real_connect_dns_srv()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect-dns-srv.html)
  C API function rather than
  [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.html).
  However, if the `connect` command is
  subsequently used at runtime and specifies a host name
  argument, that host name takes precedence over any
  [`--dns-srv-name`](mysql-command-options.md#option_mysql_dns-srv-name) option given at
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") startup to specify a DNS SRV
  record.
- [`--html`](mysql-command-options.md#option_mysql_html), `-H`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--html` |

  Produce HTML output.
- [`--ignore-spaces`](mysql-command-options.md#option_mysql_ignore-spaces),
  `-i`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ignore-spaces` |

  Ignore spaces after function names. The effect of this is
  described in the discussion for the
  [`IGNORE_SPACE`](sql-mode.md#sqlmode_ignore_space) SQL mode (see
  [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes")).
- [`--init-command=str`](mysql-command-options.md#option_mysql_init-command)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--init-command=str` |

  Single SQL statement to execute after connecting to the
  server. If auto-reconnect is enabled, the statement is
  executed again after reconnection occurs.
- [`--line-numbers`](mysql-command-options.md#option_mysql_line-numbers)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--line-numbers` |
  | Disabled by | `skip-line-numbers` |

  Write line numbers for errors. Disable this with
  [`--skip-line-numbers`](mysql-command-options.md#option_mysql_skip-line-numbers).
- [`--load-data-local-dir=dir_name`](mysql-command-options.md#option_mysql_load-data-local-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--load-data-local-dir=dir_name` |
  | Introduced | 8.0.21 |
  | Type | Directory name |
  | Default Value | `empty string` |

  This option affects the client-side `LOCAL`
  capability for [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement")
  operations. It specifies the directory in which files named
  in [`LOAD DATA
  LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statements must be located. The effect of
  [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir) depends
  on whether `LOCAL` data loading is enabled
  or disabled:

  - If `LOCAL` data loading is enabled,
    either by default in the MySQL client library or by
    specifying
    [`--local-infile[=1]`](mysql-command-options.md#option_mysql_local-infile), the
    [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir)
    option is ignored.
  - If `LOCAL` data loading is disabled,
    either by default in the MySQL client library or by
    specifying
    [`--local-infile=0`](mysql-command-options.md#option_mysql_local-infile), the
    [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir)
    option applies.

  When [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir)
  applies, the option value designates the directory in which
  local data files must be located. Comparison of the
  directory path name and the path name of files to be loaded
  is case-sensitive regardless of the case sensitivity of the
  underlying file system. If the option value is the empty
  string, it names no directory, with the result that no files
  are permitted for local data loading.

  For example, to explicitly disable local data loading except
  for files located in the `/my/local/data`
  directory, invoke [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") like this:

  ```terminal
  mysql --local-infile=0 --load-data-local-dir=/my/local/data
  ```

  When both [`--local-infile`](mysql-command-options.md#option_mysql_local-infile) and
  [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir) are
  given, the order in which they are given does not matter.

  Successful use of `LOCAL` load operations
  within [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") also requires that the
  server permits local loading; see
  [Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”](load-data-local-security.md "8.1.6 Security Considerations for LOAD DATA LOCAL")

  The [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir)
  option was added in MySQL 8.0.21.
- [`--local-infile[={0|1}]`](mysql-command-options.md#option_mysql_local-infile)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--local-infile[={0|1}]` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  By default, `LOCAL` capability for
  [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement") is determined by
  the default compiled into the MySQL client library. To
  enable or disable `LOCAL` data loading
  explicitly, use the
  [`--local-infile`](mysql-command-options.md#option_mysql_local-infile) option. When
  given with no value, the option enables
  `LOCAL` data loading. When given as
  [`--local-infile=0`](mysql-command-options.md#option_mysql_local-infile) or
  [`--local-infile=1`](mysql-command-options.md#option_mysql_local-infile), the option
  disables or enables `LOCAL` data loading.

  If `LOCAL` capability is disabled, the
  [`--load-data-local-dir`](mysql-command-options.md#option_mysql_load-data-local-dir) option
  can be used to permit restricted local loading of files
  located in a designated directory.

  Successful use of `LOCAL` load operations
  within [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") also requires that the
  server permits local loading; see
  [Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”](load-data-local-security.md "8.1.6 Security Considerations for LOAD DATA LOCAL")
- [`--login-path=name`](mysql-command-options.md#option_mysql_login-path)

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
- [`--max-allowed-packet=value`](mysql-command-options.md#option_mysql_max-allowed-packet)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--max-allowed-packet=value` |
  | Type | Numeric |
  | Default Value | `16777216` |

  The maximum size of the buffer for client/server
  communication. The default is 16MB, the maximum is 1GB.
- [`--max-join-size=value`](mysql-command-options.md#option_mysql_max-join-size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--max-join-size=value` |
  | Type | Numeric |
  | Default Value | `1000000` |

  The automatic limit for rows in a join when using
  [`--safe-updates`](mysql-command-options.md#option_mysql_safe-updates). (Default value
  is 1,000,000.)
- [`--named-commands`](mysql-command-options.md#option_mysql_named-commands),
  `-G`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--named-commands` |
  | Disabled by | `skip-named-commands` |

  Enable named [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") commands. Long-format
  commands are permitted, not just short-format commands. For
  example, `quit` and `\q`
  both are recognized. Use
  [`--skip-named-commands`](mysql-command-options.md#option_mysql_named-commands)
  to disable named commands. See
  [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands").
- [`--net-buffer-length=value`](mysql-command-options.md#option_mysql_net-buffer-length)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--net-buffer-length=value` |
  | Type | Numeric |
  | Default Value | `16384` |

  The buffer size for TCP/IP and socket communication.
  (Default value is 16KB.)
- [`--network-namespace=name`](mysql-command-options.md#option_mysql_network-namespace)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--network-namespace=name` |
  | Introduced | 8.0.22 |
  | Type | String |

  The network namespace to use for TCP/IP connections. If
  omitted, the connection uses the default (global) namespace.
  For information about network namespaces, see
  [Section 7.1.14, “Network Namespace Support”](network-namespace-support.md "7.1.14 Network Namespace Support").

  This option was added in MySQL 8.0.22. It is available only
  on platforms that implement network namespace support.
- [`--no-auto-rehash`](mysql-command-options.md#option_mysql_auto-rehash),
  `-A`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-auto-rehash` |
  | Deprecated | Yes |

  This has the same effect as
  `--skip-auto-rehash`.
  See the description for
  [`--auto-rehash`](mysql-command-options.md#option_mysql_auto-rehash).
- [`--no-beep`](mysql-command-options.md#option_mysql_no-beep), `-b`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-beep` |

  Do not beep when errors occur.
- [`--no-defaults`](mysql-command-options.md#option_mysql_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysql-command-options.md#option_mysql_no-defaults) can be used to
  prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when [`--no-defaults`](mysql-command-options.md#option_mysql_no-defaults)
  is used. To create `.mylogin.cnf`, use
  the [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--one-database`](mysql-command-options.md#option_mysql_one-database),
  `-o`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--one-database` |

  Ignore statements except those that occur while the default
  database is the one named on the command line. This option
  is rudimentary and should be used with care. Statement
  filtering is based only on
  [`USE`](use.md "15.8.4 USE Statement") statements.

  Initially, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") executes statements in
  the input because specifying a database
  *`db_name`* on the command line is
  equivalent to inserting
  [`USE
  db_name`](use.md "15.8.4 USE Statement") at the
  beginning of the input. Then, for each
  [`USE`](use.md "15.8.4 USE Statement") statement encountered,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") accepts or rejects following
  statements depending on whether the database named is the
  one on the command line. The content of the statements is
  immaterial.

  Suppose that [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") is invoked to process
  this set of statements:

  ```sql
  DELETE FROM db2.t2;
  USE db2;
  DROP TABLE db1.t1;
  CREATE TABLE db1.t1 (i INT);
  USE db1;
  INSERT INTO t1 (i) VALUES(1);
  CREATE TABLE db2.t1 (j INT);
  ```

  If the command line is [**mysql --force --one-database
  db1**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client"), [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") handles the input as
  follows:

  - The [`DELETE`](delete.md "15.2.2 DELETE Statement") statement is
    executed because the default database is
    `db1`, even though the statement names
    a table in a different database.
  - The [`DROP TABLE`](drop-table.md "15.1.32 DROP TABLE Statement") and
    [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statements
    are not executed because the default database is not
    `db1`, even though the statements name
    a table in `db1`.
  - The [`INSERT`](insert.md "15.2.7 INSERT Statement") and
    [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statements
    are executed because the default database is
    `db1`, even though the
    [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statement
    names a table in a different database.
- [`--pager[=command]`](mysql-command-options.md#option_mysql_pager)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--pager[=command]` |
  | Disabled by | `skip-pager` |
  | Type | String |

  Use the given command for paging query output. If the
  command is omitted, the default pager is the value of your
  `PAGER` environment variable. Valid pagers
  are **less**, **more**,
  **cat [> filename]**, and so forth. This
  option works only on Unix and only in interactive mode. To
  disable paging, use
  [`--skip-pager`](mysql-command-options.md#option_mysql_pager).
  [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands"), discusses output paging
  further.
- [`--password[=password]`](mysql-command-options.md#option_mysql_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") prompts for one. If given, there
  must be *no space* between
  [`--password=`](mysql-command-options.md#option_mysql_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") should not prompt for one, use the
  [`--skip-password`](mysql-command-options.md#option_mysql_password)
  option.
- [`--password1[=pass_val]`](mysql-command-options.md#option_mysql_password1)

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") prompts for one. If given, there
  must be *no space* between
  [`--password1=`](mysql-command-options.md#option_mysql_password1) and the password
  following it. If no password option is specified, the
  default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") should not prompt for one, use the
  [`--skip-password1`](mysql-command-options.md#option_mysql_password1)
  option.

  [`--password1`](mysql-command-options.md#option_mysql_password1) and
  [`--password`](mysql-command-options.md#option_mysql_password) are synonymous, as
  are
  [`--skip-password1`](mysql-command-options.md#option_mysql_password1)
  and
  [`--skip-password`](mysql-command-options.md#option_mysql_password).
- [`--password2[=pass_val]`](mysql-command-options.md#option_mysql_password2)

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysql-command-options.md#option_mysql_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](mysql-command-options.md#option_mysql_password3)

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysql-command-options.md#option_mysql_password1); see the
  description of that option for details.
- [`--pipe`](mysql-command-options.md#option_mysql_pipe), `-W`

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
- [`--plugin-authentication-kerberos-client-mode=value`](mysql-command-options.md#option_mysql_plugin-authentication-kerberos-client-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-authentication-kerberos-client-mode` |
  | Introduced | 8.0.32 |
  | Type | String |
  | Default Value | `SSPI` |
  | Valid Values | `GSSAPI`  `SSPI` |

  On Windows, the
  `authentication_kerberos_client`
  authentication plugin supports this plugin option. It
  provides two possible values that the client user can set at
  runtime: `SSPI` and
  `GSSAPI`.

  The default value for the client-side plugin option uses
  Security Support Provider Interface (SSPI), which is capable
  of acquiring credentials from the Windows in-memory cache.
  Alternatively, the client user can select a mode that
  supports Generic Security Service Application Program
  Interface (GSSAPI) through the MIT Kerberos library on
  Windows. GSSAPI is capable of acquiring cached credentials
  previously generated by using the **kinit**
  command.

  For more information, see
  [Commands
  for Windows Clients in GSSAPI Mode](kerberos-pluggable-authentication.md#kerberos-usage-win-gssapi-client-commands).
- [`--plugin-dir=dir_name`](mysql-command-options.md#option_mysql_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the [`--default-auth`](mysql-command-options.md#option_mysql_default-auth)
  option is used to specify an authentication plugin but
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysql-command-options.md#option_mysql_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--print-defaults`](mysql-command-options.md#option_mysql_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--prompt=format_str`](mysql-command-options.md#option_mysql_prompt)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--prompt=format_str` |
  | Type | String |
  | Default Value | `mysql>` |

  Set the prompt to the specified format. The default is
  `mysql>`. The special sequences that the
  prompt can contain are described in
  [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysql-command-options.md#option_mysql_protocol)

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
- [`--quick`](mysql-command-options.md#option_mysql_quick), `-q`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--quick` |

  Do not cache each query result, print each row as it is
  received. This may slow down the server if the output is
  suspended. With this option, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") does
  not use the history file.

  By default, [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") fetches all result rows
  before producing any output; while storing these, it
  calculates a running maximum column length from the actual
  value of each column in succession. When printing the
  output, it uses this maximum to format it. When
  `--quick` is specified,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") does not have the rows for which to
  calculate the length before starting, and so uses the
  maximum length. In the following example, table
  `t1` has a single column of type
  [`BIGINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") and containing 4 rows.
  The default output is 9 characters wide; this width is equal
  the maximum number of characters in any of the column values
  in the rows returned (5), plus 2 characters each for the
  spaces used as padding and the `|`
  characters used as column delimiters). The output when using
  the `--quick` option is 25 characters wide;
  this is equal to the number of characters needed to
  represent `-9223372036854775808`, which is
  the longest possible value that can be stored in a (signed)
  `BIGINT` column, or 19 characters, plus the
  4 characters used for padding and column delimiters. The
  difference can be seen here:

  ```terminal
  $> mysql -t test -e "SELECT * FROM t1"
  +-------+
  | c1    |
  +-------+
  |   100 |
  |  1000 |
  | 10000 |
  |    10 |
  +-------+

  $> mysql --quick -t test -e "SELECT * FROM t1"
  +----------------------+
  | c1                   |
  +----------------------+
  |                  100 |
  |                 1000 |
  |                10000 |
  |                   10 |
  +----------------------+
  ```
- [`--raw`](mysql-command-options.md#option_mysql_raw), `-r`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--raw` |

  For tabular output, the “boxing” around columns
  enables one column value to be distinguished from another.
  For nontabular output (such as is produced in batch mode or
  when the [`--batch`](mysql-command-options.md#option_mysql_batch) or
  [`--silent`](mysql-command-options.md#option_mysql_silent) option is given),
  special characters are escaped in the output so they can be
  identified easily. Newline, tab, `NUL`, and
  backslash are written as `\n`,
  `\t`, `\0`, and
  `\\`. The
  [`--raw`](mysql-command-options.md#option_mysql_raw) option disables this
  character escaping.

  The following example demonstrates tabular versus nontabular
  output and the use of raw mode to disable escaping:

  ```sql
  % mysql
  mysql> SELECT CHAR(92);
  +----------+
  | CHAR(92) |
  +----------+
  | \        |
  +----------+

  % mysql -s
  mysql> SELECT CHAR(92);
  CHAR(92)
  \\

  % mysql -s -r
  mysql> SELECT CHAR(92);
  CHAR(92)
  \
  ```
- [`--reconnect`](mysql-command-options.md#option_mysql_reconnect)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--reconnect` |
  | Disabled by | `skip-reconnect` |

  If the connection to the server is lost, automatically try
  to reconnect. A single reconnect attempt is made each time
  the connection is lost. To suppress reconnection behavior,
  use
  [`--skip-reconnect`](mysql-command-options.md#option_mysql_reconnect).
- [`--safe-updates`](mysql-command-options.md#option_mysql_safe-updates),
  [`--i-am-a-dummy`](mysql-command-options.md#option_mysql_safe-updates),
  `-U`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--safe-updates`  `--i-am-a-dummy` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  If this option is enabled,
  [`UPDATE`](update.md "15.2.17 UPDATE Statement") and
  [`DELETE`](delete.md "15.2.2 DELETE Statement") statements that do not
  use a key in the `WHERE` clause or a
  `LIMIT` clause produce an error. In
  addition, restrictions are placed on
  [`SELECT`](select.md "15.2.13 SELECT Statement") statements that
  produce (or are estimated to produce) very large result
  sets. If you have set this option in an option file, you can
  use
  [`--skip-safe-updates`](mysql-command-options.md#option_mysql_safe-updates)
  on the command line to override it. For more information
  about this option, see [Using Safe-Updates Mode (--safe-updates)](mysql-tips.md#safe-updates "Using Safe-Updates Mode (--safe-updates)").
- [`--select-limit=value`](mysql-command-options.md#option_mysql_select-limit)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--select-limit=value` |
  | Type | Numeric |
  | Default Value | `1000` |

  The automatic limit for
  [`SELECT`](select.md "15.2.13 SELECT Statement") statements when using
  [`--safe-updates`](mysql-command-options.md#option_mysql_safe-updates). (Default value
  is 1,000.)
- [`--server-public-key-path=file_name`](mysql-command-options.md#option_mysql_server-public-key-path)

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
  [`--server-public-key-path=file_name`](mysql-command-options.md#option_mysql_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysql-command-options.md#option_mysql_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--shared-memory-base-name=name`](mysql-command-options.md#option_mysql_shared-memory-base-name)

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
- [`--show-warnings`](mysql-command-options.md#option_mysql_show-warnings)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--show-warnings` |

  Cause warnings to be shown after each statement if there are
  any. This option applies to interactive and batch mode.
- [`--sigint-ignore`](mysql-command-options.md#option_mysql_sigint-ignore)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sigint-ignore` |

  Ignore `SIGINT` signals (typically the
  result of typing **Control+C**).

  Without this option, typing **Control+C**
  interrupts the current statement if there is one, or cancels
  any partial input line otherwise.
- [`--silent`](mysql-command-options.md#option_mysql_silent), `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--silent` |

  Silent mode. Produce less output. This option can be given
  multiple times to produce less and less output.

  This option results in nontabular output format and escaping
  of special characters. Escaping may be disabled by using raw
  mode; see the description for the
  [`--raw`](mysql-command-options.md#option_mysql_raw) option.
- [`--skip-column-names`](mysql-command-options.md#option_mysql_skip-column-names),
  `-N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--skip-column-names` |

  Do not write column names in results. Use of this option
  causes the output to be right-aligned, as shown here:

  ```terminal
  $> echo "SELECT * FROM t1" | mysql -t test
  +-------+
  | c1    |
  +-------+
  | a,c,d |
  | c     |
  +-------+
  $> echo "SELECT * FROM t1" | ./mysql -uroot -Nt test
  +-------+
  | a,c,d |
  |     c |
  +-------+
  ```
- [`--skip-line-numbers`](mysql-command-options.md#option_mysql_skip-line-numbers),
  `-L`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--skip-line-numbers` |

  Do not write line numbers for errors. Useful when you want
  to compare result files that include error messages.
- [`--skip-system-command`](mysql-command-options.md#option_mysql_skip-system-command)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--skip-system-command` |
  | Introduced | 8.0.40 |

  Disables the `system`
  (`\!`) command. Equivalent to
  [`--system-command=OFF`](mysql-command-options.md#option_mysql_system-command).
- [`--socket=path`](mysql-command-options.md#option_mysql_socket),
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
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysql-command-options.md#option_mysql_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysql-command-options.md#option_mysql_ssl-fips-mode) option differs
  from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysql-command-options.md#option_mysql_ssl-fips-mode) values
  are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysql-command-options.md#option_mysql_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysql-command-options.md#option_mysql_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--syslog`](mysql-command-options.md#option_mysql_syslog), `-j`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--syslog` |

  This option causes [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") to send
  interactive statements to the system logging facility. On
  Unix, this is `syslog`; on Windows, it is
  the Windows Event Log. The destination where logged messages
  appear is system dependent. On Linux, the destination is
  often the `/var/log/messages` file.

  Here is a sample of output generated on Linux by using
  `--syslog`. This output is formatted for
  readability; each logged message actually takes a single
  line.

  ```none
  Mar  7 12:39:25 myhost MysqlClient[20824]:
    SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
    DB_SERVER:'127.0.0.1', DB:'--', QUERY:'USE test;'
  Mar  7 12:39:28 myhost MysqlClient[20824]:
    SYSTEM_USER:'oscar', MYSQL_USER:'my_oscar', CONNECTION_ID:23,
    DB_SERVER:'127.0.0.1', DB:'test', QUERY:'SHOW TABLES;'
  ```

  For more information, see [Section 6.5.1.3, “mysql Client Logging”](mysql-logging.md "6.5.1.3 mysql Client Logging").
- [`--system-command[={ON|OFF}]`](mysql-command-options.md#option_mysql_system-command)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--system-command[={ON|OFF}]` |
  | Introduced | 8.0.40 |
  | Disabled by | `skip-system-command` |
  | Type | Boolean |
  | Default Value | `ON` |

  Enable or disable the `system`
  (`\!`) command. When this option is
  disabled, either by `--system-command=OFF` or
  by [`--skip-system-command`](mysql-command-options.md#option_mysql_skip-system-command), the
  `system` command is rejected with an error.

  (*MySQL 8.0.43 and later:*)
  [`--commands`](mysql-command-options.md#option_mysql_commands), when disabled (set
  to `FALSE`), causes the server to disregard
  any setting for this option.
- [`--table`](mysql-command-options.md#option_mysql_table), `-t`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--table` |

  Display output in table format. This is the default for
  interactive use, but can be used to produce table output in
  batch mode.
- [`--tee=file_name`](mysql-command-options.md#option_mysql_tee)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tee=file_name` |
  | Type | File name |

  Append a copy of output to the given file. This option works
  only in interactive mode. [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands"),
  discusses tee files further.
- [`--tls-ciphersuites=ciphersuite_list`](mysql-command-options.md#option_mysql_tls-ciphersuites)

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
- [`--tls-version=protocol_list`](mysql-command-options.md#option_mysql_tls-version)

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
- [`--unbuffered`](mysql-command-options.md#option_mysql_unbuffered),
  `-n`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--unbuffered` |

  Flush the buffer after each query.
- [`--user=user_name`](mysql-command-options.md#option_mysql_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.
- [`--verbose`](mysql-command-options.md#option_mysql_verbose), `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Produce more output about what the program
  does. This option can be given multiple times to produce
  more and more output. (For example, `-v -v
  -v` produces table output format even in batch
  mode.)
- [`--version`](mysql-command-options.md#option_mysql_version), `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
- [`--vertical`](mysql-command-options.md#option_mysql_vertical),
  `-E`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--vertical` |

  Print query output rows vertically (one line per column
  value). Without this option, you can specify vertical output
  for individual statements by terminating them with
  `\G`.
- [`--wait`](mysql-command-options.md#option_mysql_wait), `-w`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--wait` |

  If the connection cannot be established, wait and retry
  instead of aborting.
- [`--xml`](mysql-command-options.md#option_mysql_xml), `-X`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--xml` |

  Produce XML output.

  ```xml
  <field name="column_name">NULL</field>
  ```

  The output when [`--xml`](mysql-command-options.md#option_mysql_xml) is used
  with [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") matches that of
  [**mysqldump**](mysqldump.md "6.5.4 mysqldump — A Database Backup Program")
  [`--xml`](mysqldump.md#option_mysqldump_xml). See
  [Section 6.5.4, “mysqldump — A Database Backup Program”](mysqldump.md "6.5.4 mysqldump — A Database Backup Program"), for details.

  The XML output also uses an XML namespace, as shown here:

  ```terminal
  $> mysql --xml -uroot -e "SHOW VARIABLES LIKE 'version%'"
  <?xml version="1.0"?>

  <resultset statement="SHOW VARIABLES LIKE 'version%'" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <row>
  <field name="Variable_name">version</field>
  <field name="Value">5.0.40-debug</field>
  </row>

  <row>
  <field name="Variable_name">version_comment</field>
  <field name="Value">Source distribution</field>
  </row>

  <row>
  <field name="Variable_name">version_compile_machine</field>
  <field name="Value">i686</field>
  </row>

  <row>
  <field name="Variable_name">version_compile_os</field>
  <field name="Value">suse-linux-gnu</field>
  </row>
  </resultset>
  ```
- [`--zstd-compression-level=level`](mysql-command-options.md#option_mysql_zstd-compression-level)

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
