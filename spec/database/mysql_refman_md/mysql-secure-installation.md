### 6.4.2 mysql\_secure\_installation — Improve MySQL Installation Security

This program enables you to improve the security of your MySQL
installation in the following ways:

- You can set a password for `root` accounts.
- You can remove `root` accounts that are
  accessible from outside the local host.
- You can remove anonymous-user accounts.
- You can remove the `test` database (which
  by default can be accessed by all users, even anonymous
  users), and privileges that permit anyone to access
  databases with names that start with
  `test_`.

[**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") helps you implement
security recommendations similar to those described at
[Section 2.9.4, “Securing the Initial MySQL Account”](default-privileges.md "2.9.4 Securing the Initial MySQL Account").

Normal usage is to connect to the local MySQL server; invoke
[**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") without arguments:

```terminal
mysql_secure_installation
```

When executed, [**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security")
prompts you to determine which actions to perform.

The `validate_password` component can be used
for password strength checking. If the plugin is not installed,
[**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") prompts the user
whether to install it. Any passwords entered later are checked
using the plugin if it is enabled.

Most of the usual MySQL client options such as
[`--host`](mysql-secure-installation.md#option_mysql_secure_installation_host) and
[`--port`](mysql-secure-installation.md#option_mysql_secure_installation_port) can be
used on the command line and in option files. For example, to
connect to the local server over IPv6 using port 3307, use this
command:

```terminal
mysql_secure_installation --host=::1 --port=3307
```

[**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") supports the
following options, which can be specified on the command line or
in the `[mysql_secure_installation]` and
`[client]` groups of an option file. For
information about option files used by MySQL programs, see
[Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.9 mysql\_secure\_installation Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--defaults-extra-file](option-file-options.md#option_general_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](option-file-options.md#option_general_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](option-file-options.md#option_general_defaults-group-suffix) | Option group suffix value |  |  |
| [--help](mysql-secure-installation.md#option_mysql_secure_installation_help) | Display help message and exit |  |  |
| [--host](mysql-secure-installation.md#option_mysql_secure_installation_host) | Host on which MySQL server is located |  |  |
| [--no-defaults](option-file-options.md#option_general_no-defaults) | Read no option files |  |  |
| [--password](mysql-secure-installation.md#option_mysql_secure_installation_password) | Accepted but always ignored. Whenever mysql\_secure\_installation is invoked, the user is prompted for a password, regardless |  |  |
| [--port](mysql-secure-installation.md#option_mysql_secure_installation_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](option-file-options.md#option_general_print-defaults) | Print default options |  |  |
| [--protocol](mysql-secure-installation.md#option_mysql_secure_installation_protocol) | Transport protocol to use |  |  |
| [--socket](mysql-secure-installation.md#option_mysql_secure_installation_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--ssl-ca](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysql-command-options.md#option_mysql_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysql-secure-installation.md#option_mysql_secure_installation_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](mysql-secure-installation.md#option_mysql_secure_installation_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](mysql-secure-installation.md#option_mysql_secure_installation_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--use-default](mysql-secure-installation.md#option_mysql_secure_installation_use-default) | Execute with no user interactivity |  |  |
| [--user](mysql-secure-installation.md#option_mysql_secure_installation_user) | MySQL user name to use when connecting to server |  |  |

- [`--help`](mysql-secure-installation.md#option_mysql_secure_installation_help),
  `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--defaults-extra-file=file_name`](mysql-secure-installation.md#option_mysql_secure_installation_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysql-secure-installation.md#option_mysql_secure_installation_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=file_name` |
  | Type | File name |

  Use only the given option file. If the file does not exist
  or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--defaults-group-suffix=str`](mysql-secure-installation.md#option_mysql_secure_installation_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") normally reads
  the `[client]` and
  `[mysql_secure_installation]` groups. If
  this option is given as
  [`--defaults-group-suffix=_other`](mysql-secure-installation.md#option_mysql_secure_installation_defaults-group-suffix),
  [**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security") also reads the
  `[client_other]` and
  `[mysql_secure_installation_other]` groups.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--host=host_name`](mysql-secure-installation.md#option_mysql_secure_installation_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host` |

  Connect to the MySQL server on the given host.
- [`--no-defaults`](mysql-secure-installation.md#option_mysql_secure_installation_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysql-secure-installation.md#option_mysql_secure_installation_no-defaults)
  can be used to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysql-secure-installation.md#option_mysql_secure_installation_no-defaults)
  is used. To create `.mylogin.cnf`, use
  the [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--password=password`](mysql-secure-installation.md#option_mysql_secure_installation_password),
  `-p password`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password=password` |
  | Type | String |
  | Default Value | `[none]` |

  This option is accepted but ignored. Whether or not this
  option is used, [**mysql\_secure\_installation**](mysql-secure-installation.md "6.4.2 mysql_secure_installation — Improve MySQL Installation Security")
  always prompts the user for a password.
- [`--port=port_num`](mysql-secure-installation.md#option_mysql_secure_installation_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use.
- [`--print-defaults`](mysql-secure-installation.md#option_mysql_secure_installation_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](mysql-secure-installation.md#option_mysql_secure_installation_protocol)

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
- [`--socket=path`](mysql-secure-installation.md#option_mysql_secure_installation_socket),
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
  In addition, the connection must be a member of the Windows
  group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- `--ssl*`

  Options that begin with `--ssl` specify
  whether to connect to the server using encryption and
  indicate where to find SSL keys and certificates. See
  [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections").
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode)
  option differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These
  [`--ssl-fips-mode`](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode)
  is `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysql-secure-installation.md#option_mysql_secure_installation_ssl-fips-mode)
  to `ON` or `STRICT`
  causes the client to produce a warning at startup and to
  operate in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--tls-ciphersuites=ciphersuite_list`](mysql-secure-installation.md#option_mysql_secure_installation_tls-ciphersuites)

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
- [`--tls-version=protocol_list`](mysql-secure-installation.md#option_mysql_secure_installation_tls-version)

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
- [`--use-default`](mysql-secure-installation.md#option_mysql_secure_installation_use-default)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--use-default` |
  | Type | Boolean |

  Execute noninteractively. This option can be used for
  unattended installation operations.
- [`--user=user_name`](mysql-secure-installation.md#option_mysql_secure_installation_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server.
