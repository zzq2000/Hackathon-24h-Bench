### 6.6.8 mysql\_migrate\_keyring — Keyring Key Migration Utility

The [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") utility migrates
keys between one keyring component and another. It supports
offline and online migrations.

Invoke [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") like this (enter
the command on a single line):

```terminal
mysql_migrate_keyring
  --component-dir=dir_name
  --source-keyring=name
  --destination-keyring=name
  [other options]
```

For information about key migrations and instructions describing
how to perform them using
[**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") and other methods, see
[Section 8.4.4.14, “Migrating Keys Between Keyring Keystores”](keyring-key-migration.md "8.4.4.14 Migrating Keys Between Keyring Keystores").

[**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") supports the following
options, which can be specified on the command line or in the
`[mysql_migrate_keyring]` group of an option
file. For information about option files used by MySQL programs,
see [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.22 mysql\_migrate\_keyring Options**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--component-dir](mysql-migrate-keyring.md#option_mysql_migrate_keyring_component-dir) | Directory for keyring components |  |  |
| [--defaults-extra-file](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-extra-file) | Read named option file in addition to usual option files |  |  |
| [--defaults-file](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-file) | Read only named option file |  |  |
| [--defaults-group-suffix](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-group-suffix) | Option group suffix value |  |  |
| [--destination-keyring](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring) | Destination keyring component name |  |  |
| [--destination-keyring-configuration-dir](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring-configuration-dir) | Destination keyring component configuration directory |  |  |
| [--get-server-public-key](mysql-migrate-keyring.md#option_mysql_migrate_keyring_get-server-public-key) | Request RSA public key from server |  |  |
| [--help](mysql-migrate-keyring.md#option_mysql_migrate_keyring_help) | Display help message and exit |  |  |
| [--host](mysql-migrate-keyring.md#option_mysql_migrate_keyring_host) | Host on which MySQL server is located |  |  |
| [--login-path](mysql-migrate-keyring.md#option_mysql_migrate_keyring_login-path) | Read login path options from .mylogin.cnf |  |  |
| [--no-defaults](mysql-migrate-keyring.md#option_mysql_migrate_keyring_no-defaults) | Read no option files |  |  |
| [--online-migration](mysql-migrate-keyring.md#option_mysql_migrate_keyring_online-migration) | Migration source is an active server |  |  |
| [--password](mysql-migrate-keyring.md#option_mysql_migrate_keyring_password) | Password to use when connecting to server |  |  |
| [--port](mysql-migrate-keyring.md#option_mysql_migrate_keyring_port) | TCP/IP port number for connection |  |  |
| [--print-defaults](mysql-migrate-keyring.md#option_mysql_migrate_keyring_print-defaults) | Print default options |  |  |
| [--server-public-key-path](mysql-migrate-keyring.md#option_mysql_migrate_keyring_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--socket](mysql-migrate-keyring.md#option_mysql_migrate_keyring_socket) | Unix socket file or Windows named pipe to use |  |  |
| [--source-keyring](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring) | Source keyring component name |  |  |
| [--source-keyring-configuration-dir](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring-configuration-dir) | Source keyring component configuration directory |  |  |
| [--ssl-ca](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | File that contains X.509 key |  |  |
| [--ssl-mode](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | Desired security state of connection to server |  |  |
| [--ssl-session-data](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](mysql-migrate-keyring.md#option_mysql_migrate_keyring_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections |  |  |
| [--tls-version](mysql-migrate-keyring.md#option_mysql_migrate_keyring_tls-version) | Permissible TLS protocols for encrypted connections |  |  |
| [--user](mysql-migrate-keyring.md#option_mysql_migrate_keyring_user) | MySQL user name to use when connecting to server |  |  |
| [--verbose](mysql-migrate-keyring.md#option_mysql_migrate_keyring_verbose) | Verbose mode |  |  |
| [--version](mysql-migrate-keyring.md#option_mysql_migrate_keyring_version) | Display version information and exit |  |  |

- [`--help`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_help),
  `-h`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--component-dir=dir_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_component-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--component-dir=dir_name` |
  | Type | Directory name |

  The directory where keyring components are located. This is
  typically the value of the
  [`plugin_dir`](server-system-variables.md#sysvar_plugin_dir) system variable
  for the local MySQL server.

  Note

  [`--component-dir`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_component-dir),
  [`--source-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring),
  and
  [`--destination-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring)
  are mandatory for all keyring migration operations
  performed by [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility"). In
  addition, the source and destination components must
  differ, and both components must be properly configured so
  that [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") can load and
  use them.
- [`--defaults-extra-file=file_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-extra-file)

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
- [`--defaults-file=file_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-file)

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
- [`--defaults-group-suffix=str`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=str` |
  | Type | String |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example,
  [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") normally reads the
  `[mysql_migrate_keyring]` group. If this
  option is given as
  [`--defaults-group-suffix=_other`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_defaults-group-suffix),
  [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") also reads the
  `[mysql_migrate_keyring_other]` group.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--destination-keyring=name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--destination-keyring=name` |
  | Type | String |

  The destination keyring component for key migration. The
  format and interpretation of the option value is the same as
  described for the
  [`--source-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring)
  option.

  Note

  [`--component-dir`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_component-dir),
  [`--source-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring),
  and
  [`--destination-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring)
  are mandatory for all keyring migration operations
  performed by [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility"). In
  addition, the source and destination components must
  differ, and both components must be properly configured so
  that [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") can load and
  use them.
- [`--destination-keyring-configuration-dir=dir_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring-configuration-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--destination-keyring-configuration-dir=dir_name` |
  | Type | Directory name |

  This option applies only if the destination keyring
  component global configuration file contains
  `"read_local_config": true`, indicating
  that component configuration is contained in the local
  configuration file. The option value specifies the directory
  containing that local file.
- [`--get-server-public-key`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_get-server-public-key)

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
  [`--server-public-key-path=file_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--host=host_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  The host location of the running server that is currently
  using one of the key migration keystores. Migration always
  occurs on the local host, so the option always specifies a
  value for connecting to a local server, such as
  `localhost`, `127.0.0.1`,
  `::1`, or the local host IP address or host
  name.
- [`--login-path=name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_login-path)

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
- [`--no-defaults`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_no-defaults)
  can be used to prevent them from being read.

  The exception is that the `.mylogin.cnf`
  file is read in all cases, if it exists. This permits
  passwords to be specified in a safer way than on the command
  line even when
  [`--no-defaults`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_no-defaults)
  is used. To create `.mylogin.cnf`, use
  the [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--online-migration`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_online-migration)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--online-migration` |
  | Type | Boolean |
  | Default Value | `FALSE` |

  This option is mandatory when a running server is using the
  keyring. It tells [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility")
  to perform an online key migration. The option has these
  effects:

  - [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") connects to the
    server using any connection options specified; these
    options are otherwise ignored.
  - After [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") connects
    to the server, it tells the server to pause keyring
    operations. When key copying is complete,
    [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") tells the
    server it can resume keyring operations before
    disconnecting.
- [`--password[=password]`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_password),
  `-p[password]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |

  The password of the MySQL account used for connecting to the
  running server that is currently using one of the key
  migration keystores. The password value is optional. If not
  given, [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") prompts for
  one. If given, there must be *no space*
  between
  [`--password=`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that
  [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") should not prompt
  for one, use the
  [`--skip-password`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_password)
  option.
- [`--port=port_num`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `0` |

  For TCP/IP connections, the port number for connecting to
  the running server that is currently using one of the key
  migration keystores.
- [`--print-defaults`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |

  Print the program name and all options that it gets from
  option files.

  For additional information about this and other option-file
  options, see [Section 6.2.2.3, “Command-Line Options that Affect Option-File Handling”](option-file-options.md "6.2.2.3 Command-Line Options that Affect Option-File Handling").
- [`--server-public-key-path=file_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_server-public-key-path)

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
  [`--server-public-key-path=file_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_get-server-public-key).

  For `sha256_password`, this option applies
  only if MySQL was built using OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--socket=path`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_socket),
  `-S path`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--socket={file_name|pipe_name}` |
  | Type | String |

  For Unix socket file or Windows named pipe connections, the
  socket file or named pipe for connecting to the running
  server that is currently using one of the key migration
  keystores.

  On Windows, this option applies only if the server was
  started with the [`named_pipe`](server-system-variables.md#sysvar_named_pipe)
  system variable enabled to support named-pipe connections.
  In addition, the user making the connection must be a member
  of the Windows group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- [`--source-keyring=name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--source-keyring=name` |
  | Type | String |

  The source keyring component for key migration. This is the
  component library file name specified without any
  platform-specific extension such as `.so`
  or `.dll`. For example, to use the
  component for which the library file is
  `component_keyring_file.so`, specify the
  option as
  [`--source-keyring=component_keyring_file`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring).

  Note

  [`--component-dir`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_component-dir),
  [`--source-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring),
  and
  [`--destination-keyring`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_destination-keyring)
  are mandatory for all keyring migration operations
  performed by [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility"). In
  addition, the source and destination components must
  differ, and both components must be properly configured so
  that [**mysql\_migrate\_keyring**](mysql-migrate-keyring.md "6.6.8 mysql_migrate_keyring — Keyring Key Migration Utility") can load and
  use them.
- [`--source-keyring-configuration-dir=dir_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_source-keyring-configuration-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--source-keyring-configuration-dir=dir_name` |
  | Type | Directory name |

  This option applies only if the source keyring component
  global configuration file contains
  `"read_local_config": true`, indicating
  that component configuration is contained in the local
  configuration file. The option value specifies the directory
  containing that local file.
- `--ssl*`

  Options that begin with `--ssl` specify
  whether to connect to the server using encryption and
  indicate where to find SSL keys and certificates. See
  [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections").
- [`--ssl-fips-mode={OFF|ON|STRICT}`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode)
  option differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These
  [`--ssl-fips-mode`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode)
  values are permitted:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permitted value for
  [`--ssl-fips-mode`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode)
  is `OFF`. In this case, setting
  [`--ssl-fips-mode`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_ssl-fips-mode)
  to `ON` or `STRICT`
  causes the client to produce a warning at startup and to
  operate in non-FIPS mode.

  As of MySQL 8.0.34, this option is deprecated. Expect it to
  be removed in a future version of MySQL.
- [`--tls-ciphersuites=ciphersuite_list`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_tls-ciphersuites)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-ciphersuites=ciphersuite_list` |
  | Type | String |

  The permissible ciphersuites for encrypted connections that
  use TLSv1.3. The value is a list of one or more
  colon-separated ciphersuite names. The ciphersuites that can
  be named for this option depend on the SSL library used to
  compile MySQL. For details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").
- [`--tls-version=protocol_list`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_tls-version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-version=protocol_list` |
  | Type | String |
  | Default Value | `TLSv1,TLSv1.1,TLSv1.2,TLSv1.3` (OpenSSL 1.1.1 or higher)  `TLSv1,TLSv1.1,TLSv1.2` (otherwise) |

  The permissible TLS protocols for encrypted connections. The
  value is a list of one or more comma-separated protocol
  names. The protocols that can be named for this option
  depend on the SSL library used to compile MySQL. For
  details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").
- [`--user=user_name`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name` |
  | Type | String |

  The user name of the MySQL account used for connecting to
  the running server that is currently using one of the key
  migration keystores.
- [`--verbose`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Produce more output about what the program
  does.
- [`--version`](mysql-migrate-keyring.md#option_mysql_migrate_keyring_version),
  `-V`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--version` |

  Display version information and exit.
