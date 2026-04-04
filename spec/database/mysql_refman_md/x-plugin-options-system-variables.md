#### 22.5.6.2 X Plugin Options and System Variables

To control activation of X Plugin, use this option:

- [`--mysqlx[=value]`](x-plugin-options-system-variables.md#option_mysqld_mysqlx)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx[=value]` |
  | Type | Enumeration |
  | Default Value | `ON` |
  | Valid Values | `ON`  `OFF`  `FORCE`  `FORCE_PLUS_PERMANENT` |

  This option controls how the server loads X Plugin at
  startup. In MySQL 8.0, X Plugin is enabled by
  default, but this option may be used to control its
  activation state.

  The option value should be one of those available for
  plugin-loading options, as described in
  [Section 7.6.1, “Installing and Uninstalling Plugins”](plugin-loading.md "7.6.1 Installing and Uninstalling Plugins").

If X Plugin is enabled, it exposes several system variables
that permit control over its operation:

- [`mysqlx_bind_address`](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-bind-address=addr` |
  | System Variable | `mysqlx_bind_address` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `*` |

  The network address on which X Plugin listens for TCP/IP
  connections. This variable is not dynamic and can be
  configured only at startup. This is the X Plugin equivalent
  of the [`bind_address`](server-system-variables.md#sysvar_bind_address) system
  variable; see that variable description for more
  information.

  By default, X Plugin accepts TCP/IP connections on all
  server host IPv4 interfaces, and, if the server host
  supports IPv6, on all IPv6 interfaces. If
  [`mysqlx_bind_address`](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address) is
  specified, its value must satisfy these requirements:

  - Prior to MySQL 8.0.21,
    [`mysqlx_bind_address`](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address)
    accepts a single address value, which may specify a
    single non-wildcard IP address (either IPv4 or IPv6), or
    a host name, or one of the wildcard address formats that
    permit listening on multiple network interfaces
    (`*`, `0.0.0.0`, or
    `::`).
  - As of MySQL 8.0.21,
    [`mysqlx_bind_address`](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address)
    accepts either a single value as just described, or a
    list of comma-separated values. When the variable names
    a list of multiple values, each value must specify a
    single non-wildcard IP address (either IPv4 or IPv6) or
    a host name. Wildcard address formats
    (`*`, `0.0.0.0`, or
    `::`) are not allowed in a list of
    values.
  - As of MySQL 8.0.22, the value may include a network
    namespace specifier.

  IP addresses can be specified as IPv4 or IPv6 addresses. For
  any value that is a host name, X Plugin resolves the name
  to an IP address and binds to that address. If a host name
  resolves to multiple IP addresses, X Plugin uses the first
  IPv4 address if there are any, or the first IPv6 address
  otherwise.

  X Plugin treats different types of addresses as follows:

  - If the address is `*`, X Plugin
    accepts TCP/IP connections on all server host IPv4
    interfaces, and, if the server host supports IPv6, on
    all IPv6 interfaces. Use this address to permit both
    IPv4 and IPv6 connections for X Plugin. This value is
    the default. If the variable specifies a list of
    multiple values, this value is not permitted.
  - If the address is `0.0.0.0`, X Plugin
    accepts TCP/IP connections on all server host IPv4
    interfaces. If the variable specifies a list of multiple
    values, this value is not permitted.
  - If the address is `::`, X Plugin
    accepts TCP/IP connections on all server host IPv4 and
    IPv6 interfaces. If the variable specifies a list of
    multiple values, this value is not permitted.
  - If the address is an IPv4-mapped address, X Plugin
    accepts TCP/IP connections for that address, in either
    IPv4 or IPv6 format. For example, if X Plugin is bound
    to `::ffff:127.0.0.1`, a client such as
    MySQL Shell can connect using
    `--host=127.0.0.1` or
    `--host=::ffff:127.0.0.1`.
  - If the address is a “regular” IPv4 or IPv6
    address (such as `127.0.0.1` or
    `::1`), X Plugin accepts TCP/IP
    connections only for that IPv4 or IPv6 address.

  These rules apply to specifying a network namespace for an
  address:

  - A network namespace can be specified for an IP address
    or a host name.
  - A network namespace cannot be specified for a wildcard
    IP address.
  - For a given address, the network namespace is optional.
    If given, it must be specified as a
    `/ns` suffix
    immediately following the address.
  - An address with no
    `/ns` suffix
    uses the host system global namespace. The global
    namespace is therefore the default.
  - An address with a
    `/ns` suffix
    uses the namespace named *`ns`*.
  - The host system must support network namespaces and each
    named namespace must previously have been set up. Naming
    a nonexistent namespace produces an error.
  - If the variable value specifies multiple addresses, it
    can include addresses in the global namespace, in named
    namespaces, or a mix.

  For additional information about network namespaces, see
  [Section 7.1.14, “Network Namespace Support”](network-namespace-support.md "7.1.14 Network Namespace Support").

  Important

  Because X Plugin is not a mandatory plugin, it does not
  prevent server startup if there is an error in the
  specified address or list of addresses (as MySQL Server
  does for [`bind_address`](server-system-variables.md#sysvar_bind_address)
  errors). With X Plugin, if one of the listed addresses
  cannot be parsed or if X Plugin cannot bind to it, the
  address is skipped, an error message is logged, and
  X Plugin attempts to bind to each of the remaining
  addresses. X Plugin's
  [`Mysqlx_address`](x-plugin-status-variables.md#statvar_Mysqlx_address) status
  variable displays only those addresses from the list for
  which the bind succeeded. If none of the listed addresses
  results in a successful bind, or if a single specified
  address fails, X Plugin logs the error message
  [`ER_XPLUGIN_FAILED_TO_PREPARE_IO_INTERFACES`](https://dev.mysql.com/doc/mysql-errors/8.0/en/server-error-reference.html#error_er_xplugin_failed_to_prepare_io_interfaces)
  stating that X Protocol cannot be used.
  [`mysqlx_bind_address`](x-plugin-options-system-variables.md#sysvar_mysqlx_bind_address) is
  not dynamic, so to fix any issues you must stop the
  server, correct the system variable value, and restart the
  server.
- [`mysqlx_compression_algorithms`](x-plugin-options-system-variables.md#sysvar_mysqlx_compression_algorithms)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-compression-algorithms=value` |
  | Introduced | 8.0.19 |
  | System Variable | `mysqlx_compression_algorithms` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Set |
  | Default Value | `deflate_stream,lz4_message,zstd_stream` |
  | Valid Values | `deflate_stream`  `lz4_message`  `zstd_stream` |

  The compression algorithms that are permitted for use on
  X Protocol connections. By default, the Deflate, LZ4, and
  zstd algorithms are all permitted. To disallow any of the
  algorithms, set
  [`mysqlx_compression_algorithms`](x-plugin-options-system-variables.md#sysvar_mysqlx_compression_algorithms)
  to include only the ones you permit. The algorithm names
  `deflate_stream`,
  `lz4_message`, and
  `zstd_stream` can be specified in any
  combination, and the order and case are not important. If
  you set the system variable to the empty string, no
  compression algorithms are permitted and only uncompressed
  connections are used. Use the algorithm-specific system
  variables to adjust the default and maximum compression
  level for each permitted algorithm. For more details, and
  information on how connection compression for X Protocol
  relates to the equivalent settings for MySQL Server, see
  [Section 22.5.5, “Connection Compression with X Plugin”](x-plugin-connection-compression.md "22.5.5 Connection Compression with X Plugin").
- [`mysqlx_connect_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_connect_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-connect-timeout=#` |
  | System Variable | `mysqlx_connect_timeout` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `30` |
  | Minimum Value | `1` |
  | Maximum Value | `1000000000` |
  | Unit | seconds |

  The number of seconds X Plugin waits for the first packet
  to be received from newly connected clients. This is the
  X Plugin equivalent of
  [`connect_timeout`](server-system-variables.md#sysvar_connect_timeout); see that
  variable description for more information.
- [`mysqlx_deflate_default_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_deflate_default_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_deflate_default_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_deflate_default_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `3` |
  | Minimum Value | `1` |
  | Maximum Value | `9` |

  The default compression level that the server uses for the
  Deflate algorithm on X Protocol connections. Specify the
  level as an integer from 1 (the lowest compression effort)
  to 9 (the highest effort). This level is used if the client
  does not request a compression level during capability
  negotiation. If you do not specify this system variable, the
  server uses level 3 as the default. For more information,
  see [Section 22.5.5, “Connection Compression with X Plugin”](x-plugin-connection-compression.md "22.5.5 Connection Compression with X Plugin").
- [`mysqlx_deflate_max_client_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_deflate_max_client_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_deflate_max_client_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_deflate_max_client_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `5` |
  | Minimum Value | `1` |
  | Maximum Value | `9` |

  The maximum compression level that the server permits for
  the Deflate algorithm on X Protocol connections. The range
  is the same as for the default compression level for this
  algorithm. If the client requests a higher compression level
  than this, the server uses the level you set here. If you do
  not specify this system variable, the server sets a maximum
  compression level of 5.
- [`mysqlx_document_id_unique_prefix`](x-plugin-options-system-variables.md#sysvar_mysqlx_document_id_unique_prefix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-document-id-unique-prefix=#` |
  | System Variable | `mysqlx_document_id_unique_prefix` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `0` |
  | Minimum Value | `0` |
  | Maximum Value | `65535` |

  Sets the first 4 bytes of document IDs generated by the
  server when documents are added to a collection. By setting
  this variable to a unique value per instance, you can ensure
  document IDs are unique across instances. See
  [Understanding Document IDs](https://dev.mysql.com/doc/x-devapi-userguide/en/understanding-automatic-document-ids.html).
- [`mysqlx_enable_hello_notice`](x-plugin-options-system-variables.md#sysvar_mysqlx_enable_hello_notice)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-enable-hello-notice[={OFF|ON}]` |
  | System Variable | `mysqlx_enable_hello_notice` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `ON` |

  Controls messages sent to classic MySQL protocol clients that try
  to connect over X Protocol. When enabled, clients which do
  not support X Protocol that attempt to connect to the
  server X Protocol port receive an error explaining they are
  using the wrong protocol.
- [`mysqlx_idle_worker_thread_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_idle_worker_thread_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-idle-worker-thread-timeout=#` |
  | System Variable | `mysqlx_idle_worker_thread_timeout` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `60` |
  | Minimum Value | `0` |
  | Maximum Value | `3600` |
  | Unit | seconds |

  The number of seconds after which idle worker threads are
  terminated.
- [`mysqlx_interactive_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_interactive_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-interactive-timeout=#` |
  | System Variable | `mysqlx_interactive_timeout` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `28800` |
  | Minimum Value | `1` |
  | Maximum Value | `2147483` |
  | Unit | seconds |

  The default value of the
  [`mysqlx_wait_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_wait_timeout) session
  variable for interactive clients. (The number of seconds to
  wait for interactive clients to timeout.)
- [`mysqlx_lz4_default_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_lz4_default_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_lz4_default_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_lz4_default_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `2` |
  | Minimum Value | `0` |
  | Maximum Value | `16` |

  The default compression level that the server uses for the
  LZ4 algorithm on X Protocol connections. Specify the level
  as an integer from 0 (the lowest compression effort) to 16
  (the highest effort). This level is used if the client does
  not request a compression level during capability
  negotiation. If you do not specify this system variable, the
  server uses level 2 as the default. For more information,
  see [Section 22.5.5, “Connection Compression with X Plugin”](x-plugin-connection-compression.md "22.5.5 Connection Compression with X Plugin").
- [`mysqlx_lz4_max_client_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_lz4_max_client_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_lz4_max_client_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_lz4_max_client_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `8` |
  | Minimum Value | `0` |
  | Maximum Value | `16` |

  The maximum compression level that the server permits for
  the LZ4 algorithm on X Protocol connections. The range is
  the same as for the default compression level for this
  algorithm. If the client requests a higher compression level
  than this, the server uses the level you set here. If you do
  not specify this system variable, the server sets a maximum
  compression level of 8.
- [`mysqlx_max_allowed_packet`](x-plugin-options-system-variables.md#sysvar_mysqlx_max_allowed_packet)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-max-allowed-packet=#` |
  | System Variable | `mysqlx_max_allowed_packet` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `67108864` |
  | Minimum Value | `512` |
  | Maximum Value | `1073741824` |
  | Unit | bytes |

  The maximum size of network packets that can be received by
  X Plugin. This limit also applies when compression is used
  for the connection, so the network packet must be smaller
  than this size after the message has been decompressed. This
  is the X Plugin equivalent of
  [`max_allowed_packet`](server-system-variables.md#sysvar_max_allowed_packet); see
  that variable description for more information.
- [`mysqlx_max_connections`](x-plugin-options-system-variables.md#sysvar_mysqlx_max_connections)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-max-connections=#` |
  | System Variable | `mysqlx_max_connections` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `100` |
  | Minimum Value | `1` |
  | Maximum Value | `65535` |

  The maximum number of concurrent client connections
  X Plugin can accept. This is the X Plugin equivalent of
  [`max_connections`](server-system-variables.md#sysvar_max_connections); see that
  variable description for more information.

  For modifications to this variable, if the new value is
  smaller than the current number of connections, the new
  limit is taken into account only for new connections.
- [`mysqlx_min_worker_threads`](x-plugin-options-system-variables.md#sysvar_mysqlx_min_worker_threads)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-min-worker-threads=#` |
  | System Variable | `mysqlx_min_worker_threads` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `2` |
  | Minimum Value | `1` |
  | Maximum Value | `100` |

  The minimum number of worker threads used by X Plugin for
  handling client requests.
- [`mysqlx_port`](x-plugin-options-system-variables.md#sysvar_mysqlx_port)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-port=port_num` |
  | System Variable | `mysqlx_port` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `33060` |
  | Minimum Value | `1` |
  | Maximum Value | `65535` |

  The network port on which X Plugin listens for TCP/IP
  connections. This is the X Plugin equivalent of
  [`port`](server-system-variables.md#sysvar_port); see that variable
  description for more information.
- [`mysqlx_port_open_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_port_open_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-port-open-timeout=#` |
  | System Variable | `mysqlx_port_open_timeout` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `0` |
  | Minimum Value | `0` |
  | Maximum Value | `120` |
  | Unit | seconds |

  The number of seconds X Plugin waits for a TCP/IP port to
  become free.
- [`mysqlx_read_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_read_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-read-timeout=#` |
  | System Variable | `mysqlx_read_timeout` |
  | Scope | Session |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `30` |
  | Minimum Value | `1` |
  | Maximum Value | `2147483` |
  | Unit | seconds |

  The number of seconds that X Plugin waits for blocking read
  operations to complete. After this time, if the read
  operation is not successful, X Plugin closes the connection
  and returns a warning notice with the error code
  ER\_IO\_READ\_ERROR to the client
  application.
- [`mysqlx_socket`](x-plugin-options-system-variables.md#sysvar_mysqlx_socket)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-socket=file_name` |
  | System Variable | `mysqlx_socket` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `/tmp/mysqlx.sock` |

  The path to a Unix socket file which X Plugin uses for
  connections. This setting is only used by MySQL Server when
  running on Unix operating systems. Clients can use this
  socket to connect to MySQL Server using X Plugin.

  The default [`mysqlx_socket`](x-plugin-options-system-variables.md#sysvar_mysqlx_socket)
  path and file name is based on the default path and file
  name for the main socket file for MySQL Server, with the
  addition of an `x` appended to the file
  name. The default path and file name for the main socket
  file is `/tmp/mysql.sock`, therefore the
  default path and file name for the X Plugin socket file is
  `/tmp/mysqlx.sock`.

  If you specify an alternative path and file name for the
  main socket file at server startup using the
  [`socket`](server-system-variables.md#sysvar_socket) system variable,
  this does not affect the default for the X Plugin socket
  file. In this situation, if you want to store both sockets
  at a single path, you must set the
  [`mysqlx_socket`](x-plugin-options-system-variables.md#sysvar_mysqlx_socket) system
  variable as well. For example in a configuration file:

  ```ini
  socket=/home/sockets/mysqld/mysql.sock
  mysqlx_socket=/home/sockets/xplugin/xplugin.sock
  ```

  If you change the default path and file name for the main
  socket file at compile time using the
  [`MYSQL_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysql_unix_addr) compile
  option, this does affect the default for the X Plugin
  socket file, which is formed by appending an
  `x` to the
  [`MYSQL_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysql_unix_addr) file name. If
  you want to set a different default for the X Plugin socket
  file at compile time, use the
  [`MYSQLX_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysqlx_unix_addr) compile
  option.

  The `MYSQLX_UNIX_PORT` environment variable
  can also be used to set a default for the X Plugin socket
  file at server startup (see
  [Section 6.9, “Environment Variables”](environment-variables.md "6.9 Environment Variables")). If you set this
  environment variable, it overrides the compiled
  [`MYSQLX_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysqlx_unix_addr) value, but is
  overridden by the
  [`mysqlx_socket`](x-plugin-options-system-variables.md#sysvar_mysqlx_socket) value.
- [`mysqlx_ssl_ca`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_ca)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-ca=file_name` |
  | System Variable | `mysqlx_ssl_ca` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_ca`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_ca) system
  variable is like [`ssl_ca`](server-system-variables.md#sysvar_ssl_ca),
  except that it applies to X Plugin rather than the MySQL
  Server main connection interface. For information about
  configuring encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_capath`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_capath)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-capath=dir_name` |
  | System Variable | `mysqlx_ssl_capath` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Directory name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_capath`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_capath)
  system variable is like
  [`ssl_capath`](server-system-variables.md#sysvar_ssl_capath), except that it
  applies to X Plugin rather than the MySQL Server main
  connection interface. For information about configuring
  encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_cert`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cert)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-cert=file_name` |
  | System Variable | `mysqlx_ssl_cert` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_cert`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cert) system
  variable is like [`ssl_cert`](server-system-variables.md#sysvar_ssl_cert),
  except that it applies to X Plugin rather than the MySQL
  Server main connection interface. For information about
  configuring encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_cipher`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cipher)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-cipher=name` |
  | System Variable | `mysqlx_ssl_cipher` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_cipher`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_cipher)
  system variable is like
  [`ssl_cipher`](server-system-variables.md#sysvar_ssl_cipher), except that it
  applies to X Plugin rather than the MySQL Server main
  connection interface. For information about configuring
  encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_crl`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crl)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-crl=file_name` |
  | System Variable | `mysqlx_ssl_crl` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_crl`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crl) system
  variable is like [`ssl_crl`](server-system-variables.md#sysvar_ssl_crl),
  except that it applies to X Plugin rather than the MySQL
  Server main connection interface. For information about
  configuring encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_crlpath`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crlpath)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-crlpath=dir_name` |
  | System Variable | `mysqlx_ssl_crlpath` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Directory name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_crlpath`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_crlpath)
  system variable is like
  [`ssl_crlpath`](server-system-variables.md#sysvar_ssl_crlpath), except that it
  applies to X Plugin rather than the MySQL Server main
  connection interface. For information about configuring
  encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_ssl_key`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-ssl-key=file_name` |
  | System Variable | `mysqlx_ssl_key` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `NULL` |

  The [`mysqlx_ssl_key`](x-plugin-options-system-variables.md#sysvar_mysqlx_ssl_key) system
  variable is like [`ssl_key`](server-system-variables.md#sysvar_ssl_key),
  except that it applies to X Plugin rather than the MySQL
  Server main connection interface. For information about
  configuring encryption support for X Plugin, see
  [Section 22.5.3, “Using Encrypted Connections with X Plugin”](x-plugin-encrypted-connections.md "22.5.3 Using Encrypted Connections with X Plugin").
- [`mysqlx_wait_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_wait_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-wait-timeout=#` |
  | System Variable | `mysqlx_wait_timeout` |
  | Scope | Session |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `28800` |
  | Minimum Value | `1` |
  | Maximum Value | `2147483` |
  | Unit | seconds |

  The number of seconds that X Plugin waits for activity on a
  connection. After this time, if the read operation is not
  successful, X Plugin closes the connection. If the client
  is noninteractive, the initial value of the session variable
  is copied from the global
  [`mysqlx_wait_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_wait_timeout)
  variable. For interactive clients, the initial value is
  copied from the session
  [`mysqlx_interactive_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_interactive_timeout).
- [`mysqlx_write_timeout`](x-plugin-options-system-variables.md#sysvar_mysqlx_write_timeout)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx-write-timeout=#` |
  | System Variable | `mysqlx_write_timeout` |
  | Scope | Session |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `60` |
  | Minimum Value | `1` |
  | Maximum Value | `2147483` |
  | Unit | seconds |

  The number of seconds that X Plugin waits for blocking
  write operations to complete. After this time, if the write
  operation is not successful, X Plugin closes the
  connection.
- [`mysqlx_zstd_default_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_zstd_default_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_zstd_default_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_zstd_default_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `3` |
  | Minimum Value | `-131072` |
  | Maximum Value | `22` |

  The default compression level that the server uses for the
  zstd algorithm on X Protocol connections. For versions of
  the zstd library from 1.4.0, you can set positive values
  from 1 to 22 (the highest compression effort), or negative
  values which represent progressively lower effort. A value
  of 0 is converted to a value of 1. For earlier versions of
  the zstd library, you can only specify the value 3. This
  level is used if the client does not request a compression
  level during capability negotiation. If you do not specify
  this system variable, the server uses level 3 as the
  default. For more information, see
  [Section 22.5.5, “Connection Compression with X Plugin”](x-plugin-connection-compression.md "22.5.5 Connection Compression with X Plugin").
- [`mysqlx_zstd_max_client_compression_level`](x-plugin-options-system-variables.md#sysvar_mysqlx_zstd_max_client_compression_level)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--mysqlx_zstd_max_client_compression_level=#` |
  | Introduced | 8.0.20 |
  | System Variable | `mysqlx_zstd_max_client_compression_level` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `11` |
  | Minimum Value | `-131072` |
  | Maximum Value | `22` |

  The maximum compression level that the server permits for
  the zstd algorithm on X Protocol connections. The range is
  the same as for the default compression level for this
  algorithm. If the client requests a higher compression level
  than this, the server uses the level you set here. If you do
  not specify this system variable, the server sets a maximum
  compression level of 11.
