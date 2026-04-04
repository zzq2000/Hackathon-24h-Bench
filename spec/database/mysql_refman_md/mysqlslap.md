### 6.5.8 mysqlslap — A Load Emulation Client

[**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") is a diagnostic program designed to
emulate client load for a MySQL server and to report the timing
of each stage. It works as if multiple clients are accessing the
server.

Invoke [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") like this:

```terminal
mysqlslap [options]
```

Some options such as [`--create`](mysqlslap.md#option_mysqlslap_create)
or [`--query`](mysqlslap.md#option_mysqlslap_query) enable you to
specify a string containing an SQL statement or a file
containing statements. If you specify a file, by default it must
contain one statement per line. (That is, the implicit statement
delimiter is the newline character.) Use the
[`--delimiter`](mysqlslap.md#option_mysqlslap_delimiter) option to specify
a different delimiter, which enables you to specify statements
that span multiple lines or place multiple statements on a
single line. You cannot include comments in a file;
[**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") does not understand them.

[**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") runs in three stages:

1. Create schema, table, and optionally any stored programs or
   data to use for the test. This stage uses a single client
   connection.
2. Run the load test. This stage can use many client
   connections.
3. Clean up (disconnect, drop table if specified). This stage
   uses a single client connection.

Examples:

Supply your own create and query SQL statements, with 50 clients
querying and 200 selects for each (enter the command on a single
line):

```terminal
mysqlslap --delimiter=";"
  --create="CREATE TABLE a (b int);INSERT INTO a VALUES (23)"
  --query="SELECT * FROM a" --concurrency=50 --iterations=200
```

Let [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") build the query SQL statement
with a table of two [`INT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") columns
and three [`VARCHAR`](char.md "13.3.2 The CHAR and VARCHAR Types") columns. Use
five clients querying 20 times each. Do not create the table or
insert the data (that is, use the previous test's schema and
data):

```terminal
mysqlslap --concurrency=5 --iterations=20
  --number-int-cols=2 --number-char-cols=3
  --auto-generate-sql
```

Tell the program to load the create, insert, and query SQL
statements from the specified files, where the
`create.sql` file has multiple table creation
statements delimited by `';'` and multiple
insert statements delimited by `';'`. The
`--query` file should contain multiple queries
delimited by `';'`. Run all the load
statements, then run all the queries in the query file with five
clients (five times each):

```terminal
mysqlslap --concurrency=5
  --iterations=5 --query=query.sql --create=create.sql
  --delimiter=";"
```

[**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") supports the following options,
which can be specified on the command line or in the
`[mysqlslap]` and `[client]`
groups of an option file. For information about option files
used by MySQL programs, see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.19 mysqlslap Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--auto-generate-sql](mysqlslap.md#option_mysqlslap_auto-generate-sql) | Generate SQL statements automatically when they are not supplied in files or using command options |  |  |
| [--auto-generate-sql-add-autoincrement](mysqlslap.md#option_mysqlslap_auto-generate-sql-add-autoincrement) | Add AUTO\_INCREMENT column to automatically generated tables |  |  |
| [--auto-generate-sql-execute-number](mysqlslap.md#option_mysqlslap_auto-generate-sql-execute-number) | Specify how many queries to generate automatically |  |  |
| [--auto-generate-sql-guid-primary](mysqlslap.md#option_mysqlslap_auto-generate-sql-guid-primary) | Add a GUID-based primary key to automatically generated tables |  |  |
| [--auto-generate-sql-load-type](mysqlslap.md#option_mysqlslap_auto-generate-sql-load-type) | Specify the test load type |  |  |
| [--auto-generate-sql-secondary-indexes](mysqlslap.md#option_mysqlslap_auto-generate-sql-secondary-indexes) | Specify how many secondary indexes to add to automatically generated tables |  |  |
| [--auto-generate-sql-unique-query-number](mysqlslap.md#option_mysqlslap_auto-generate-sql-unique-query-number) | How many different queries to generate for automatic tests |  |  |
| [--auto-generate-sql-unique-write-number](mysqlslap.md#option_mysqlslap_auto-generate-sql-unique-write-number) | How many different queries to generate for --auto-generate-sql-write-number |  |  |
| [--auto-generate-sql-write-number](mysqlslap.md#option_mysqlslap_auto-generate-sql-write-number) | How many row inserts to perform on each thread |  |  |
| [--commit](mysqlslap.md#option_mysqlslap_commit) | How many statements to execute before committing |  |  |
| [--compress](mysqlslap.md#option_mysqlslap_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](mysqlslap.md#option_mysqlslap_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--concurrency](mysqlslap.md#option_mysqlslap_concurrency) | Number of clients to simulate when issuing the SELECT statement |  |  |
| [--create](mysqlslap.md#option_mysqlslap_create) | File or string containing the statement to use for creating the table |  |  |
| [--create-schema](mysqlslap.md#option_mysqlslap_create-schema) | Schema in which to run the tests |  |  |
| [--csv](mysqlslap.md#option_mysqlslap_csv) | Generate output in comma-separated values format |  |  |
| [--debug](mysqlslap.md#option_mysqlslap_debug) | Write debugging log |  |  |
| [--debug-check](mysqlslap.md#option_mysqlslap_debug-check) | Print debugging information when program exits |  |  |
| [--debug-info](mysqlslap.md#option_mysqlslap_debug-info) | Print debugging information, memory, and CPU statistics when program exits |  |  |
| [--default-auth](mysqlslap.md#option_mysqlslap_default-auth) | Authentication plugin to use |  |  |
| [--defaults-extra-file](mysqlslap.md#option_mysqlslap_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysqlslap.md#option_mysqlslap_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysqlslap.md#option_mysqlslap_defaults-group-suffix) | Option group suffix value |  |  |
| [--delimiter](mysqlslap.md#option_mysqlslap_delimiter) | Delimiter to use in SQL statements |  |  |
| [--detach](mysqlslap.md#option_mysqlslap_detach) | Detach (close and reopen) each connection after each N statements |  |  |
| [--enable-cleartext-plugin](mysqlslap.md#option_mysqlslap_enable-cleartext-plugin) | Enable cleartext authentication plugin |  |  |
| [--engine](mysqlslap.md#option_mysqlslap_engine) | Storage engine to use for creating the table |  |  |
| [--get-server-public-key](mysqlslap.md#option_mysqlslap_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysqlslap.md#option_mysqlslap_help) | Display help message and exit |  |  |
| [--host](mysqlslap.md#option_mysqlslap_host) | Host on which MySQL server is located |  |  |
| [--iterations](mysqlslap.md#option_mysqlslap_iterations) | Number of times to run the tests |  |  |
| [--login-path](mysqlslap.md#option_mysqlslap_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--no-defaults](mysqlslap.md#option_mysqlslap_no-defaults) | Read no option files |  |  |
| [--no-drop](mysqlslap.md#option_mysqlslap_no-drop) | Do not drop any schema created during the test run |  |  |
| [--number-char-cols](mysqlslap.md#option_mysqlslap_number-char-cols) | Number of VARCHAR columns to use if --auto-generate-sql is specified |  |  |
| [--number-int-cols](mysqlslap.md#option_mysqlslap_number-int-cols) | Number of INT columns to use if --auto-generate-sql is specified |  |  |
| [--number-of-queries](mysqlslap.md#option_mysqlslap_number-of-queries) | Limit each client to approximately this number of queries |  |  |
| [--only-print](mysqlslap.md#option_mysqlslap_only-print) | Do not connect to databases. mysqlslap only prints what it would have done |  |  |
| [--password](mysqlslap.md#option_mysqlslap_password) | Password to use when connecting to server |  |  |
| [--password1](mysqlslap.md#option_mysqlslap_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password2](mysqlslap.md#option_mysqlslap_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--password3](mysqlslap.md#option_mysqlslap_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |  |
| [--pipe](mysqlslap.md#option_mysqlslap_pipe) | Connect to server using named pipe (Windows only) |  |  |
| [--plugin-dir](mysqlslap.md#option_mysqlslap_plugin-dir) | Directory where plugins are installed |  |  |
| [--port](mysqlslap.md#option_mysqlslap_port) | TCP/IP port number for connection |  |  |
| [--post-query](mysqlslap.md#option_mysqlslap_post-query) | File or string containing the statement to execute after the tests have completed |  |  |
| [--post-system](mysqlslap.md#option_mysqlslap_post-system) | String to execute using system() after the tests have completed |  |  |
| [--pre-query](mysqlslap.md#option_mysqlslap_pre-query) | File or string containing the statement to execute before running the tests |  |  |
| [--pre-system](mysqlslap.md#option_mysqlslap_pre-system) | String to execute using system() before running the tests |  |  |
| [--print-defaults](mysqlslap.md#option_mysqlslap_print-defaults) | Print default options |  |  |
| [--protocol](mysqlslap.md#option_mysqlslap_protocol) | Transport protocol to use |  |  |
| [--query](mysqlslap.md#option_mysqlslap_query) | File or string containing the SELECT statement to use for retrieving data |  |  |
| [--server-public-key-path](mysqlslap.md#option_mysqlslap_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--shared-memory-base-name](mysqlslap.md#option_mysqlslap_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |  |
| [--silent](mysqlslap.md#option_mysqlslap_silent) | Silent mode |  |  |
| [--socket](mysqlslap.md#option_mysqlslap_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--sql-mode](mysqlslap.md#option_mysqlslap_sql-mode) | Set SQL mode for client session |  |  |
| [--ssl-ca](mysqlslap.md#option_mysqlslap_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysqlslap.md#option_mysqlslap_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysqlslap.md#option_mysqlslap_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysqlslap.md#option_mysqlslap_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysqlslap.md#option_mysqlslap_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysqlslap.md#option_mysqlslap_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysqlslap.md#option_mysqlslap_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysqlslap.md#option_mysqlslap_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysqlslap.md#option_mysqlslap_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysqlslap.md#option_mysqlslap_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysqlslap.md#option_mysqlslap_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](mysqlslap.md#option_mysqlslap_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysqlslap.md#option_mysqlslap_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--user](mysqlslap.md#option_mysqlslap_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysqlslap.md#option_mysqlslap_verbose) | Verbose mode |  |  |
| [--version](mysqlslap.md#option_mysqlslap_version) | Display version information and exit |  |  |
| [--zstd-compression-level](mysqlslap.md#option_mysqlslap_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--help`](mysqlslap.md#option_mysqlslap_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--auto-generate-sql`](mysqlslap.md#option_mysqlslap_auto-generate-sql),
  `-a`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Generate SQL statements automatically when they are not
  supplied in files or using command options.
- [`--auto-generate-sql-add-autoincrement`](mysqlslap.md#option_mysqlslap_auto-generate-sql-add-autoincrement)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-add-autoincrement` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Add an `AUTO_INCREMENT` column to
  automatically generated tables.
- [`--auto-generate-sql-execute-number=N`](mysqlslap.md#option_mysqlslap_auto-generate-sql-execute-number)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-execute-number=#` |
  | Type | Numeric |

  Specify how many queries to generate automatically.
- [`--auto-generate-sql-guid-primary`](mysqlslap.md#option_mysqlslap_auto-generate-sql-guid-primary)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-guid-primary` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Add a GUID-based primary key to automatically generated
  tables.
- [`--auto-generate-sql-load-type=type`](mysqlslap.md#option_mysqlslap_auto-generate-sql-load-type)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-load-type=type` |
  | Type | Enumeration |
  | Default Value | `mixed` |
  | Valid Values | `read`  `write`  `key`  `update`  `mixed` |

  Specify the test load type. The permissible values are
  `read` (scan tables),
  `write` (insert into tables),
  `key` (read primary keys),
  `update` (update primary keys), or
  `mixed` (half inserts, half scanning
  selects). The default is `mixed`.
- [`--auto-generate-sql-secondary-indexes=N`](mysqlslap.md#option_mysqlslap_auto-generate-sql-secondary-indexes)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-secondary-indexes=#` |
  | Type | Numeric |
  | Default Value | `0` |

  Specify how many secondary indexes to add to automatically
  generated tables. By default, none are added.
- [`--auto-generate-sql-unique-query-number=N`](mysqlslap.md#option_mysqlslap_auto-generate-sql-unique-query-number)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-unique-query-number=#` |
  | Type | Numeric |
  | Default Value | `10` |

  How many different queries to generate for automatic tests.
  For example, if you run a `key` test that
  performs 1000 selects, you can use this option with a value
  of 1000 to run 1000 unique queries, or with a value of 50 to
  perform 50 different selects. The default is 10.
- [`--auto-generate-sql-unique-write-number=N`](mysqlslap.md#option_mysqlslap_auto-generate-sql-unique-write-number)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-unique-write-number=#` |
  | Type | Numeric |
  | Default Value | `10` |

  How many different queries to generate for
  [`--auto-generate-sql-write-number`](mysqlslap.md#option_mysqlslap_auto-generate-sql-write-number).
  The default is 10.
- [`--auto-generate-sql-write-number=N`](mysqlslap.md#option_mysqlslap_auto-generate-sql-write-number)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--auto-generate-sql-write-number=#` |
  | Type | Numeric |
  | Default Value | `100` |

  How many row inserts to perform. The default is 100.
- [`--commit=N`](mysqlslap.md#option_mysqlslap_commit)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--commit=#` |
  | Type | Numeric |
  | Default Value | `0` |

  How many statements to execute before committing. The
  default is 0 (no commits are done).
- [`--compress`](mysqlslap.md#option_mysqlslap_compress),
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
- [`--compression-algorithms=value`](mysqlslap.md#option_mysqlslap_compression-algorithms)

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
- [`--concurrency=N`](mysqlslap.md#option_mysqlslap_concurrency),
  `-c N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--concurrency=#` |
  | Type | Numeric |

  The number of parallel clients to simulate.
- [`--create=value`](mysqlslap.md#option_mysqlslap_create)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--create=value` |
  | Type | String |

  The file or string containing the statement to use for
  creating the table.
- [`--create-schema=value`](mysqlslap.md#option_mysqlslap_create-schema)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--create-schema=value` |
  | Type | String |

  The schema in which to run the tests.

  Note

  If the
  [`--auto-generate-sql`](mysqlslap.md#option_mysqlslap_auto-generate-sql)
  option is also given, [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") drops
  the schema at the end of the test run. To avoid this, use
  the [`--no-drop`](mysqlslap.md#option_mysqlslap_no-drop) option as
  well.
- [`--csv[=file_name]`](mysqlslap.md#option_mysqlslap_csv)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--csv=[file]` |
  | Type | File name |

  Generate output in comma-separated values format. The output
  goes to the named file, or to the standard output if no file
  is given.
- [`--debug[=debug_options]`](mysqlslap.md#option_mysqlslap_debug),
  `-#
  [debug_options]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug[=debug_options]` |
  | Type | String |
  | Default Value | `d:t:o,/tmp/mysqlslap.trace` |

  Write a debugging log. A typical
  *`debug_options`* string is
  `d:t:o,file_name`.
  The default is
  `d:t:o,/tmp/mysqlslap.trace`.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- [`--debug-check`](mysqlslap.md#option_mysqlslap_debug-check)

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
- [`--debug-info`](mysqlslap.md#option_mysqlslap_debug-info),
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
- [`--default-auth=plugin`](mysqlslap.md#option_mysqlslap_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--defaults-extra-file=file_name`](mysqlslap.md#option_mysqlslap_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysqlslap.md#option_mysqlslap_defaults-file)

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
- [`--defaults-group-suffix=str`](mysqlslap.md#option_mysqlslap_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") normally reads the
  `[client]` and
  `[mysqlslap]` groups. If this option is
  given as
  [`--defaults-group-suffix=_other`](mysqlslap.md#option_mysqlslap_defaults-group-suffix),
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") also reads the
  `[client_other]` and
  `[mysqlslap_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--delimiter=str`](mysqlslap.md#option_mysqlslap_delimiter),
  `-F str`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--delimiter=str` |
  | Type | String |

  The delimiter to use in SQL statements supplied in files or
  using command options.
- [`--detach=N`](mysqlslap.md#option_mysqlslap_detach)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--detach=#` |
  | Type | Numeric |
  | Default Value | `0` |

  Detach (close and reopen) each connection after each
  *`N`* statements. The default is 0
  (connections are not detached).
- [`--enable-cleartext-plugin`](mysqlslap.md#option_mysqlslap_enable-cleartext-plugin)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--enable-cleartext-plugin` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Enable the `mysql_clear_password` cleartext
  authentication plugin. (See
  [Section 8.4.1.4, “Client-Side Cleartext Pluggable Authentication”](cleartext-pluggable-authentication.md "8.4.1.4 Client-Side Cleartext Pluggable Authentication").)
- [`--engine=engine_name`](mysqlslap.md#option_mysqlslap_engine),
  `-e engine_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--engine=engine_name` |
  | Type | String |

  The storage engine to use for creating tables.
- [`--get-server-public-key`](mysqlslap.md#option_mysqlslap_get-server-public-key)

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
  [`--server-public-key-path=file_name`](mysqlslap.md#option_mysqlslap_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlslap.md#option_mysqlslap_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--host=host_name`](mysqlslap.md#option_mysqlslap_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  Connect to the MySQL server on the given host.
- [`--iterations=N`](mysqlslap.md#option_mysqlslap_iterations),
  `-i N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--iterations=#` |
  | Type | Numeric |

  The number of times to run the tests.
- [`--login-path=name`](mysqlslap.md#option_mysqlslap_login-path)

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
- [`--no-drop`](mysqlslap.md#option_mysqlslap_no-drop)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-drop` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Prevent [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") from dropping any
  schema it creates during the test run.
- [`--no-defaults`](mysqlslap.md#option_mysqlslap_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysqlslap.md#option_mysqlslap_no-defaults) can be used
  to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysqlslap.md#option_mysqlslap_no-defaults) is used. To
  create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--number-char-cols=N`](mysqlslap.md#option_mysqlslap_number-char-cols),
  `-x N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--number-char-cols=#` |
  | Type | Numeric |

  The number of [`VARCHAR`](char.md "13.3.2 The CHAR and VARCHAR Types") columns
  to use if
  [`--auto-generate-sql`](mysqlslap.md#option_mysqlslap_auto-generate-sql) is
  specified.
- [`--number-int-cols=N`](mysqlslap.md#option_mysqlslap_number-int-cols),
  `-y N`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--number-int-cols=#` |
  | Type | Numeric |

  The number of [`INT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") columns to
  use if [`--auto-generate-sql`](mysqlslap.md#option_mysqlslap_auto-generate-sql)
  is specified.
- [`--number-of-queries=N`](mysqlslap.md#option_mysqlslap_number-of-queries)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--number-of-queries=#` |
  | Type | Numeric |

  Limit each client to approximately this many queries. Query
  counting takes into account the statement delimiter. For
  example, if you invoke [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") as
  follows, the `;` delimiter is recognized so
  that each instance of the query string counts as two
  queries. As a result, 5 rows (not 10) are inserted.

  ```terminal
  mysqlslap --delimiter=";" --number-of-queries=10
            --query="use test;insert into t values(null)"
  ```
- [`--only-print`](mysqlslap.md#option_mysqlslap_only-print)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--only-print` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  Do not connect to databases. [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client")
  only prints what it would have done.
- [`--password[=password]`](mysqlslap.md#option_mysqlslap_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given,
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") prompts for one. If given,
  there must be *no space* between
  [`--password=`](mysqlslap.md#option_mysqlslap_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") should not prompt for one, use
  the
  [`--skip-password`](mysqlslap.md#option_mysqlslap_password)
  option.
- [`--password1[=pass_val]`](mysqlslap.md#option_mysqlslap_password1)

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given,
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") prompts for one. If given,
  there must be *no space* between
  [`--password1=`](mysqlslap.md#option_mysqlslap_password1) and the
  password following it. If no password option is specified,
  the default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") should not prompt for one, use
  the
  [`--skip-password1`](mysqlslap.md#option_mysqlslap_password1)
  option.

  [`--password1`](mysqlslap.md#option_mysqlslap_password1) and
  [`--password`](mysqlslap.md#option_mysqlslap_password) are synonymous,
  as are
  [`--skip-password1`](mysqlslap.md#option_mysqlslap_password1)
  and
  [`--skip-password`](mysqlslap.md#option_mysqlslap_password).
- [`--password2[=pass_val]`](mysqlslap.md#option_mysqlslap_password2)

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlslap.md#option_mysqlslap_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](mysqlslap.md#option_mysqlslap_password3)

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](mysqlslap.md#option_mysqlslap_password1); see the
  description of that option for details.
- [`--pipe`](mysqlslap.md#option_mysqlslap_pipe),
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
- [`--plugin-dir=dir_name`](mysqlslap.md#option_mysqlslap_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the
  [`--default-auth`](mysqlslap.md#option_mysqlslap_default-auth) option is
  used to specify an authentication plugin but
  [**mysqlslap**](mysqlslap.md "6.5.8 mysqlslap — A Load Emulation Client") does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](mysqlslap.md#option_mysqlslap_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--post-query=value`](mysqlslap.md#option_mysqlslap_post-query)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--post-query=value` |
  | Type | String |

  The file or string containing the statement to execute after
  the tests have completed. This execution is not counted for
  timing purposes.
- [`--post-system=str`](mysqlslap.md#option_mysqlslap_post-system)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--post-system=str` |
  | Type | String |

  The string to execute using `system()`
  after the tests have completed. This execution is not
  counted for timing purposes.
- [`--pre-query=value`](mysqlslap.md#option_mysqlslap_pre-query)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--pre-query=value` |
  | Type | String |

  The file or string containing the statement to execute
  before running the tests. This execution is not counted for
  timing purposes.
- [`--pre-system=str`](mysqlslap.md#option_mysqlslap_pre-system)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--pre-system=str` |
  | Type | String |

  The string to execute using `system()`
  before running the tests. This execution is not counted for
  timing purposes.
- [`--print-defaults`](mysqlslap.md#option_mysqlslap_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysqlslap.md#option_mysqlslap_protocol)

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
- [`--query=value`](mysqlslap.md#option_mysqlslap_query),
  `-q value`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--query=value` |
  | Type | String |

  The file or string containing the
  [`SELECT`](select.md "15.2.13 SELECT Statement") statement to use for
  retrieving data.
- [`--server-public-key-path=file_name`](mysqlslap.md#option_mysqlslap_server-public-key-path)

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
  [`--server-public-key-path=file_name`](mysqlslap.md#option_mysqlslap_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysqlslap.md#option_mysqlslap_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--shared-memory-base-name=name`](mysqlslap.md#option_mysqlslap_shared-memory-base-name)

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
- [`--silent`](mysqlslap.md#option_mysqlslap_silent),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--silent` |

  Silent mode. No output.
- [`--socket=path`](mysqlslap.md#option_mysqlslap_socket),
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
- [`--sql-mode=mode`](mysqlslap.md#option_mysqlslap_sql-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sql-mode=mode` |
  | Type | String |

  Set the SQL mode for the client session.
- `--ssl*`

  Options that begin with `--ssl` specify
  whether to connect to the server using encryption and
  indicate where to find SSL keys and certificates. See
  [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections").
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysqlslap.md#option_mysqlslap_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysqlslap.md#option_mysqlslap_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](mysqlslap.md#option_mysqlslap_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysqlslap.md#option_mysqlslap_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysqlslap.md#option_mysqlslap_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--tls-ciphersuites=ciphersuite_list`](mysqlslap.md#option_mysqlslap_tls-ciphersuites)

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
- [`--tls-version=protocol_list`](mysqlslap.md#option_mysqlslap_tls-version)

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
- [`--user=user_name`](mysqlslap.md#option_mysqlslap_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name,` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.
- [`--verbose`](mysqlslap.md#option_mysqlslap_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more information about what the program
  does. This option can be used multiple times to increase the
  amount of information.
- [`--version`](mysqlslap.md#option_mysqlslap_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
- [`--zstd-compression-level=level`](mysqlslap.md#option_mysqlslap_zstd-compression-level)

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
