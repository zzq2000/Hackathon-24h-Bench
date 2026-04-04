### 6.2.3 Command Options for Connecting to the Server

This section describes options supported by most MySQL client
programs that control how client programs establish connections to
the server, whether connections are encrypted, and whether
connections are compressed. These options can be given on the
command line or in an option file.

- [Command Options for Connection Establishment](connection-options.md#connection-establishment-options "Command Options for Connection Establishment")
- [Command Options for Encrypted Connections](connection-options.md#encrypted-connection-options "Command Options for Encrypted Connections")
- [Command Options for Connection Compression](connection-options.md#connection-compression-options "Command Options for Connection Compression")

#### Command Options for Connection Establishment

This section describes options that control how client programs
establish connections to the server. For additional information
and examples showing how to use them, see
[Section 6.2.4, “Connecting to the MySQL Server Using Command Options”](connecting.md "6.2.4 Connecting to the MySQL Server Using Command Options").

**Table 6.4 Connection-Establishment Option Summary**

| Option Name | Description | Introduced |
| --- | --- | --- |
| [--default-auth](connection-options.md#option_general_default-auth) | Authentication plugin to use |  |
| [--host](connection-options.md#option_general_host) | Host on which MySQL server is located |  |
| [--password](connection-options.md#option_general_password) | Password to use when connecting to server |  |
| [--password1](connection-options.md#option_general_password1) | First multifactor authentication password to use when connecting to server | 8.0.27 |
| [--password2](connection-options.md#option_general_password2) | Second multifactor authentication password to use when connecting to server | 8.0.27 |
| [--password3](connection-options.md#option_general_password3) | Third multifactor authentication password to use when connecting to server | 8.0.27 |
| [--pipe](connection-options.md#option_general_pipe) | Connect to server using named pipe (Windows only) |  |
| [--plugin-dir](connection-options.md#option_general_plugin-dir) | Directory where plugins are installed |  |
| [--port](connection-options.md#option_general_port) | TCP/IP port number for connection |  |
| [--protocol](connection-options.md#option_general_protocol) | Transport protocol to use |  |
| [--shared-memory-base-name](connection-options.md#option_general_shared-memory-base-name) | Shared-memory name for shared-memory connections (Windows only) |  |
| [--socket](connection-options.md#option_general_socket) | Unix socket file or Windows named pipe to use |  |
| [--user](connection-options.md#option_general_user) | MySQL user name to use when connecting to server |  |

- [`--default-auth=plugin`](connection-options.md#option_general_default-auth)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--default-auth=plugin` |
  | Type | String |

  A hint about which client-side authentication plugin to use.
  See [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--host=host_name`](connection-options.md#option_general_host),
  `-h host_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--host=host_name` |
  | Type | String |
  | Default Value | `localhost` |

  The host on which the MySQL server is running. The value can
  be a host name, IPv4 address, or IPv6 address. The default
  value is `localhost`.
- [`--password[=pass_val]`](connection-options.md#option_general_password),
  `-p[pass_val]`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password[=password]` |
  | Type | String |
  | Default Value | `[none]` |

  The password of the MySQL account used for connecting to the
  server. The password value is optional. If not given, the
  client program prompts for one. If given, there must be
  *no space* between
  [`--password=`](connection-options.md#option_general_password) or
  `-p` and the password following it. If no
  password option is specified, the default is to send no
  password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that the
  client program should not prompt for one, use the
  [`--skip-password`](connection-options.md#option_general_password)
  option.
- [`--password1[=pass_val]`](connection-options.md#option_general_password1)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password1[=password]` |
  | Introduced | 8.0.27 |
  | Type | String |

  The password for multifactor authentication factor 1 of the
  MySQL account used for connecting to the server. The
  password value is optional. If not given, the client program
  prompts for one. If given, there must be *no
  space* between
  [`--password1=`](connection-options.md#option_general_password1) and the
  password following it. If no password option is specified,
  the default is to send no password.

  Specifying a password on the command line should be
  considered insecure. To avoid giving the password on the
  command line, use an option file. See
  [Section 8.1.2.1, “End-User Guidelines for Password Security”](password-security-user.md "8.1.2.1 End-User Guidelines for Password Security").

  To explicitly specify that there is no password and that the
  client program should not prompt for one, use the
  [`--skip-password1`](connection-options.md#option_general_password1)
  option.

  [`--password1`](connection-options.md#option_general_password1) and
  [`--password`](connection-options.md#option_general_password) are synonymous,
  as are
  [`--skip-password1`](connection-options.md#option_general_password1)
  and
  [`--skip-password`](connection-options.md#option_general_password).
- [`--password2[=pass_val]`](connection-options.md#option_general_password2)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password2[=password]` |
  | Introduced | 8.0.27 |
  | Type | String |

  The password for multifactor authentication factor 2 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](connection-options.md#option_general_password1); see the
  description of that option for details.
- [`--password3[=pass_val]`](connection-options.md#option_general_password3)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--password3[=password]` |
  | Introduced | 8.0.27 |
  | Type | String |

  The password for multifactor authentication factor 3 of the
  MySQL account used for connecting to the server. The
  semantics of this option are similar to the semantics for
  [`--password1`](connection-options.md#option_general_password1); see the
  description of that option for details.
- [`--pipe`](connection-options.md#option_general_pipe), `-W`

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
- [`--plugin-dir=dir_name`](connection-options.md#option_general_plugin-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--plugin-dir=dir_name` |
  | Type | Directory name |

  The directory in which to look for plugins. Specify this
  option if the [`--default-auth`](connection-options.md#option_general_default-auth)
  option is used to specify an authentication plugin but the
  client program does not find it. See
  [Section 8.2.17, “Pluggable Authentication”](pluggable-authentication.md "8.2.17 Pluggable Authentication").
- [`--port=port_num`](connection-options.md#option_general_port),
  `-P port_num`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--port=port_num` |
  | Type | Numeric |
  | Default Value | `3306` |

  For TCP/IP connections, the port number to use. The default
  port number is 3306.
- [`--protocol={TCP|SOCKET|PIPE|MEMORY}`](connection-options.md#option_general_protocol)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--protocol=type` |
  | Type | String |
  | Default Value | `[see text]` |
  | Valid Values | `TCP`  `SOCKET`  `PIPE`  `MEMORY` |

  This option explicitly specifies which transport protocol to
  use for connecting to the server. It is useful when other
  connection parameters normally result in use of a protocol
  other than the one you want. For example, connections on
  Unix to `localhost` are made using a Unix
  socket file by default:

  ```terminal
  mysql --host=localhost
  ```

  To force TCP/IP transport to be used instead, specify a
  [`--protocol`](connection-options.md#option_general_protocol) option:

  ```terminal
  mysql --host=localhost --protocol=TCP
  ```

  The following table shows the permissible
  [`--protocol`](connection-options.md#option_general_protocol) option values and
  indicates the applicable platforms for each value. The
  values are not case-sensitive.

  | [`--protocol`](connection-options.md#option_general_protocol) Value | Transport Protocol Used | Applicable Platforms |
  | --- | --- | --- |
  | `TCP` | TCP/IP transport to local or remote server | All |
  | `SOCKET` | Unix socket-file transport to local server | Unix and Unix-like systems |
  | `PIPE` | Named-pipe transport to local server | Windows |
  | `MEMORY` | Shared-memory transport to local server | Windows |

  See also [Section 6.2.7, “Connection Transport Protocols”](transport-protocols.md "6.2.7 Connection Transport Protocols")
- [`--shared-memory-base-name=name`](connection-options.md#option_general_shared-memory-base-name)

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
- [`--socket=path`](connection-options.md#option_general_socket),
  `-S path`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--socket={file_name|pipe_name}` |
  | Type | String |

  On Unix, the name of the Unix socket file to use for
  connections made using a named pipe to a local server. The
  default Unix socket file name is
  `/tmp/mysql.sock`.

  On Windows, the name of the named pipe to use for
  connections to a local server. The default Windows pipe name
  is `MySQL`. The pipe name is not
  case-sensitive.

  On Windows, this option applies only if the server was
  started with the [`named_pipe`](server-system-variables.md#sysvar_named_pipe)
  system variable enabled to support named-pipe connections.
  In addition, the user making the connection must be a member
  of the Windows group specified by the
  [`named_pipe_full_access_group`](server-system-variables.md#sysvar_named_pipe_full_access_group)
  system variable.
- [`--user=user_name`](connection-options.md#option_general_user),
  `-u user_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--user=user_name` |
  | Type | String |

  The user name of the MySQL account to use for connecting to
  the server. The default user name is `ODBC`
  on Windows or your Unix login name on Unix.

#### Command Options for Encrypted Connections

This section describes options for client programs that specify
whether to use encrypted connections to the server, the names of
certificate and key files, and other parameters related to
encrypted-connection support. For examples of suggested use and
how to check whether a connection is encrypted, see
[Section 8.3.1, “Configuring MySQL to Use Encrypted Connections”](using-encrypted-connections.md "8.3.1 Configuring MySQL to Use Encrypted Connections").

Note

These options have an effect only for connections that use a
transport protocol subject to encryption; that is, TCP/IP and
Unix socket-file connections. See
[Section 6.2.7, “Connection Transport Protocols”](transport-protocols.md "6.2.7 Connection Transport Protocols")

For information about using encrypted connections from the MySQL
C API, see [Support for Encrypted Connections](https://dev.mysql.com/doc/c-api/8.0/en/c-api-encrypted-connections.html).

**Table 6.5 Connection-Encryption Option Summary**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--get-server-public-key](connection-options.md#option_general_get-server-public-key) | Request RSA public key from server |  |  |
| [--server-public-key-path](connection-options.md#option_general_server-public-key-path) | Path name to file containing RSA public key |  |  |
| [--ssl-ca](connection-options.md#option_general_ssl-ca) | File that contains list of trusted SSL Certificate Authorities |  |  |
| [--ssl-capath](connection-options.md#option_general_ssl-capath) | Directory that contains trusted SSL Certificate Authority certificate files |  |  |
| [--ssl-cert](connection-options.md#option_general_ssl-cert) | File that contains X.509 certificate |  |  |
| [--ssl-cipher](connection-options.md#option_general_ssl-cipher) | Permissible ciphers for connection encryption |  |  |
| [--ssl-crl](connection-options.md#option_general_ssl-crl) | File that contains certificate revocation lists |  |  |
| [--ssl-crlpath](connection-options.md#option_general_ssl-crlpath) | Directory that contains certificate revocation-list files |  |  |
| [--ssl-fips-mode](connection-options.md#option_general_ssl-fips-mode) | Whether to enable FIPS mode on client side |  | 8.0.34 |
| [--ssl-key](connection-options.md#option_general_ssl-key) | File that contains X.509 key |  |  |
| [--ssl-mode](connection-options.md#option_general_ssl-mode) | Desired security state of connection to server |  |  |
| [--ssl-session-data](connection-options.md#option_general_ssl-session-data) | File that contains SSL session data | 8.0.29 |  |
| [--ssl-session-data-continue-on-failed-reuse](connection-options.md#option_general_ssl-session-data-continue-on-failed-reuse) | Whether to establish connections if session reuse fails | 8.0.29 |  |
| [--tls-ciphersuites](connection-options.md#option_general_tls-ciphersuites) | Permissible TLSv1.3 ciphersuites for encrypted connections | 8.0.16 |  |
| [--tls-version](connection-options.md#option_general_tls-version) | Permissible TLS protocols for encrypted connections |  |  |

- [`--get-server-public-key`](connection-options.md#option_general_get-server-public-key)

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
  [`--server-public-key-path=file_name`](connection-options.md#option_general_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](connection-options.md#option_general_get-server-public-key).

  For information about the
  `caching_sha2_password` plugin, see
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--server-public-key-path=file_name`](connection-options.md#option_general_server-public-key-path)

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
  [`--server-public-key-path=file_name`](connection-options.md#option_general_server-public-key-path)
  is given and specifies a valid public key file, it takes
  precedence over
  [`--get-server-public-key`](connection-options.md#option_general_get-server-public-key).

  This option is available only if MySQL was built using
  OpenSSL.

  For information about the `sha256_password`
  and `caching_sha2_password` plugins, see
  [Section 8.4.1.3, “SHA-256 Pluggable Authentication”](sha256-pluggable-authentication.md "8.4.1.3 SHA-256 Pluggable Authentication"), and
  [Section 8.4.1.2, “Caching SHA-2 Pluggable Authentication”](caching-sha2-pluggable-authentication.md "8.4.1.2 Caching SHA-2 Pluggable Authentication").
- [`--ssl-ca=file_name`](connection-options.md#option_general_ssl-ca)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-ca=file_name` |
  | Type | File name |

  The path name of the Certificate Authority (CA) certificate
  file in PEM format. The file contains a list of trusted SSL
  Certificate Authorities.

  To tell the client not to authenticate the server
  certificate when establishing an encrypted connection to the
  server, specify neither
  [`--ssl-ca`](connection-options.md#option_general_ssl-ca) nor
  [`--ssl-capath`](connection-options.md#option_general_ssl-capath). The server
  still verifies the client according to any applicable
  requirements established for the client account, and it
  still uses any [`ssl_ca`](server-system-variables.md#sysvar_ssl_ca) or
  [`ssl_capath`](server-system-variables.md#sysvar_ssl_capath) system variable
  values specified on the server side.

  To specify the CA file for the server, set the
  [`ssl_ca`](server-system-variables.md#sysvar_ssl_ca) system variable.
- [`--ssl-capath=dir_name`](connection-options.md#option_general_ssl-capath)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-capath=dir_name` |
  | Type | Directory name |

  The path name of the directory that contains trusted SSL
  certificate authority (CA) certificate files in PEM format.

  To tell the client not to authenticate the server
  certificate when establishing an encrypted connection to the
  server, specify neither
  [`--ssl-ca`](connection-options.md#option_general_ssl-ca) nor
  [`--ssl-capath`](connection-options.md#option_general_ssl-capath). The server
  still verifies the client according to any applicable
  requirements established for the client account, and it
  still uses any [`ssl_ca`](server-system-variables.md#sysvar_ssl_ca) or
  [`ssl_capath`](server-system-variables.md#sysvar_ssl_capath) system variable
  values specified on the server side.

  To specify the CA directory for the server, set the
  [`ssl_capath`](server-system-variables.md#sysvar_ssl_capath) system variable.
- [`--ssl-cert=file_name`](connection-options.md#option_general_ssl-cert)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-cert=file_name` |
  | Type | File name |

  The path name of the client SSL public key certificate file
  in PEM format.

  To specify the server SSL public key certificate file, set
  the [`ssl_cert`](server-system-variables.md#sysvar_ssl_cert) system
  variable.

  Note

  Chained SSL certificate support was added in v8.0.30;
  previously only the first certificate was read.
- [`--ssl-cipher=cipher_list`](connection-options.md#option_general_ssl-cipher)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-cipher=name` |
  | Type | String |

  The list of permissible encryption ciphers for connections
  that use TLS protocols up through TLSv1.2. If no cipher in
  the list is supported, encrypted connections that use these
  TLS protocols do not work.

  For greatest portability,
  *`cipher_list`* should be a list of
  one or more cipher names, separated by colons. Examples:

  ```terminal
  --ssl-cipher=AES128-SHA
  --ssl-cipher=DHE-RSA-AES128-GCM-SHA256:AES128-SHA
  ```

  OpenSSL supports the syntax for specifying ciphers described
  in the OpenSSL documentation at
  <https://www.openssl.org/docs/manmaster/man1/ciphers.html>.

  For information about which encryption ciphers MySQL
  supports, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").

  To specify the encryption ciphers for the server, set the
  [`ssl_cipher`](server-system-variables.md#sysvar_ssl_cipher) system variable.
- [`--ssl-crl=file_name`](connection-options.md#option_general_ssl-crl)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-crl=file_name` |
  | Type | File name |

  The path name of the file containing certificate revocation
  lists in PEM format.

  If neither [`--ssl-crl`](connection-options.md#option_general_ssl-crl) nor
  [`--ssl-crlpath`](connection-options.md#option_general_ssl-crlpath) is given, no
  CRL checks are performed, even if the CA path contains
  certificate revocation lists.

  To specify the revocation-list file for the server, set the
  [`ssl_crl`](server-system-variables.md#sysvar_ssl_crl) system variable.
- [`--ssl-crlpath=dir_name`](connection-options.md#option_general_ssl-crlpath)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-crlpath=dir_name` |
  | Type | Directory name |

  The path name of the directory that contains certificate
  revocation-list files in PEM format.

  If neither [`--ssl-crl`](connection-options.md#option_general_ssl-crl) nor
  [`--ssl-crlpath`](connection-options.md#option_general_ssl-crlpath) is given, no
  CRL checks are performed, even if the CA path contains
  certificate revocation lists.

  To specify the revocation-list directory for the server, set
  the [`ssl_crlpath`](server-system-variables.md#sysvar_ssl_crlpath) system
  variable.
- [`--ssl-fips-mode={OFF|ON|STRICT}`](connection-options.md#option_general_ssl-fips-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-fips-mode={OFF|ON|STRICT}` |
  | Deprecated | 8.0.34 |
  | Type | Enumeration |
  | Default Value | `OFF` |
  | Valid Values | `OFF`  `ON`  `STRICT` |

  Controls whether to enable FIPS mode on the client side. The
  [`--ssl-fips-mode`](connection-options.md#option_general_ssl-fips-mode) option
  differs from other
  `--ssl-xxx`
  options in that it is not used to establish encrypted
  connections, but rather to affect which cryptographic
  operations to permit. See [Section 8.8, “FIPS Support”](fips-mode.md "8.8 FIPS Support").

  These [`--ssl-fips-mode`](connection-options.md#option_general_ssl-fips-mode) values
  are permissible:

  - `OFF`: Disable FIPS mode.
  - `ON`: Enable FIPS mode.
  - `STRICT`: Enable “strict”
    FIPS mode.

  Note

  If the OpenSSL FIPS Object Module is not available, the
  only permissible value for
  [`--ssl-fips-mode`](connection-options.md#option_general_ssl-fips-mode) is
  `OFF`. In this case, setting
  [`--ssl-fips-mode`](connection-options.md#option_general_ssl-fips-mode) to
  `ON` or `STRICT` causes
  the client to produce a warning at startup and to operate
  in non-FIPS mode.

  To specify the FIPS mode for the server, set the
  [`ssl_fips_mode`](server-system-variables.md#sysvar_ssl_fips_mode) system
  variable.
- [`--ssl-key=file_name`](connection-options.md#option_general_ssl-key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-key=file_name` |
  | Type | File name |

  The path name of the client SSL private key file in PEM
  format. For better security, use a certificate with an RSA
  key size of at least 2048 bits.

  If the key file is protected by a passphrase, the client
  program prompts the user for the passphrase. The password
  must be given interactively; it cannot be stored in a file.
  If the passphrase is incorrect, the program continues as if
  it could not read the key.

  To specify the server SSL private key file, set the
  [`ssl_key`](server-system-variables.md#sysvar_ssl_key) system variable.
- [`--ssl-mode=mode`](connection-options.md#option_general_ssl-mode)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-mode=mode` |
  | Type | Enumeration |
  | Default Value | `PREFERRED` |
  | Valid Values | `DISABLED`  `PREFERRED`  `REQUIRED`  `VERIFY_CA`  `VERIFY_IDENTITY` |

  This option specifies the desired security state of the
  connection to the server. These mode values are permissible,
  in order of increasing strictness:

  - `DISABLED`: Establish an unencrypted
    connection.
  - `PREFERRED`: Establish an encrypted
    connection if the server supports encrypted connections,
    falling back to an unencrypted connection if an
    encrypted connection cannot be established. This is the
    default if [`--ssl-mode`](connection-options.md#option_general_ssl-mode) is
    not specified.

    Connections over Unix socket files are not encrypted
    with a mode of `PREFERRED`. To enforce
    encryption for Unix socket-file connections, use a mode
    of `REQUIRED` or stricter. (However,
    socket-file transport is secure by default, so
    encrypting a socket-file connection makes it no more
    secure and increases CPU load.)
  - `REQUIRED`: Establish an encrypted
    connection if the server supports encrypted connections.
    The connection attempt fails if an encrypted connection
    cannot be established.
  - `VERIFY_CA`: Like
    `REQUIRED`, but additionally verify the
    server Certificate Authority (CA) certificate against
    the configured CA certificates. The connection attempt
    fails if no valid matching CA certificates are found.
  - `VERIFY_IDENTITY`: Like
    `VERIFY_CA`, but additionally perform
    host name identity verification by checking the host
    name the client uses for connecting to the server
    against the identity in the certificate that the server
    sends to the client:

    - As of MySQL 8.0.12, if the client uses OpenSSL 1.0.2
      or higher, the client checks whether the host name
      that it uses for connecting matches either the
      Subject Alternative Name value or the Common Name
      value in the server certificate. Host name identity
      verification also works with certificates that
      specify the Common Name using wildcards.
    - Otherwise, the client checks whether the host name
      that it uses for connecting matches the Common Name
      value in the server certificate.

    The connection fails if there is a mismatch. For
    encrypted connections, this option helps prevent
    man-in-the-middle attacks.

    Note

    Host name identity verification with
    `VERIFY_IDENTITY` does not work with
    self-signed certificates that are created
    automatically by the server or manually using
    [**mysql\_ssl\_rsa\_setup**](mysql-ssl-rsa-setup.md "6.4.3 mysql_ssl_rsa_setup — Create SSL/RSA Files") (see
    [Section 8.3.3.1, “Creating SSL and RSA Certificates and Keys using MySQL”](creating-ssl-rsa-files-using-mysql.md "8.3.3.1 Creating SSL and RSA Certificates and Keys using MySQL")).
    Such self-signed certificates do not contain the
    server name as the Common Name value.

  Important

  The default setting,
  [`--ssl-mode=PREFERRED`](connection-options.md#option_general_ssl-mode),
  produces an encrypted connection if the other default
  settings are unchanged. However, to help prevent
  sophisticated man-in-the-middle attacks, it is important
  for the client to verify the server’s identity. The
  settings
  [`--ssl-mode=VERIFY_CA`](connection-options.md#option_general_ssl-mode) and
  [`--ssl-mode=VERIFY_IDENTITY`](connection-options.md#option_general_ssl-mode)
  are a better choice than the default setting to help
  prevent this type of attack. To implement one of these
  settings, you must first ensure that the CA certificate
  for the server is reliably available to all the clients
  that use it in your environment, otherwise availability
  issues will result. For this reason, they are not the
  default setting.

  The [`--ssl-mode`](connection-options.md#option_general_ssl-mode) option
  interacts with CA certificate options as follows:

  - If [`--ssl-mode`](connection-options.md#option_general_ssl-mode) is not
    explicitly set otherwise, use of
    [`--ssl-ca`](connection-options.md#option_general_ssl-ca) or
    [`--ssl-capath`](connection-options.md#option_general_ssl-capath) implies
    [`--ssl-mode=VERIFY_CA`](connection-options.md#option_general_ssl-mode).
  - For [`--ssl-mode`](connection-options.md#option_general_ssl-mode) values of
    `VERIFY_CA` or
    `VERIFY_IDENTITY`,
    [`--ssl-ca`](connection-options.md#option_general_ssl-ca) or
    [`--ssl-capath`](connection-options.md#option_general_ssl-capath) is also
    required, to supply a CA certificate that matches the
    one used by the server.
  - An explicit [`--ssl-mode`](connection-options.md#option_general_ssl-mode)
    option with a value other than
    `VERIFY_CA` or
    `VERIFY_IDENTITY`, together with an
    explicit [`--ssl-ca`](connection-options.md#option_general_ssl-ca) or
    [`--ssl-capath`](connection-options.md#option_general_ssl-capath) option,
    produces a warning that no verification of the server
    certificate is performed, despite a CA certificate
    option being specified.

  To require use of encrypted connections by a MySQL account,
  use [`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement") to create the
  account with a `REQUIRE SSL` clause, or use
  [`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement") for an existing
  account to add a `REQUIRE SSL` clause. This
  causes connection attempts by clients that use the account
  to be rejected unless MySQL supports encrypted connections
  and an encrypted connection can be established.

  The `REQUIRE` clause permits other
  encryption-related options, which can be used to enforce
  security requirements stricter than `REQUIRE
  SSL`. For additional details about which command
  options may or must be specified by clients that connect
  using accounts configured using the various
  `REQUIRE` options, see
  [CREATE USER SSL/TLS Options](create-user.md#create-user-tls "CREATE USER SSL/TLS Options").
- [`--ssl-session-data=file_name`](connection-options.md#option_general_ssl-session-data)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-session-data=file_name` |
  | Introduced | 8.0.29 |
  | Type | File name |

  The path name of the client SSL session data file in PEM
  format for session reuse.

  When you invoke a MySQL client program with the
  [`--ssl-session-data`](connection-options.md#option_general_ssl-session-data) option,
  the client attempts to deserialize session data from the
  file, if provided, and then use it to establish a new
  connection. If you supply a file, but the session is not
  reused, then the connection fails unless you also specified
  the
  [`--ssl-session-data-continue-on-failed-reuse`](connection-options.md#option_general_ssl-session-data-continue-on-failed-reuse)
  option on the command line when you invoked the client
  program.

  The [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") command,
  `ssl_session_data_print`, generates the
  session data file (see [Section 6.5.1.2, “mysql Client Commands”](mysql-commands.md "6.5.1.2 mysql Client Commands")).
- [`ssl-session-data-continue-on-failed-reuse`](connection-options.md#option_general_ssl-session-data-continue-on-failed-reuse)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ssl-session-data-continue-on-failed-reuse` |
  | Introduced | 8.0.29 |
  | Type | Boolean |
  | Default Value | `OFF` |

  Controls whether a new connection is started to replace an
  attempted connection that tried but failed to reuse session
  data specified with the
  [`--ssl-session-data`](connection-options.md#option_general_ssl-session-data)
  command-line option. By default, the
  [`--ssl-session-data-continue-on-failed-reuse`](connection-options.md#option_general_ssl-session-data-continue-on-failed-reuse)
  command-line option is off, which causes a client program to
  return a connect failure when session data are supplied and
  not reused.

  To ensure that a new, unrelated connection opens after
  session reuse fails silently, invoke MySQL client programs
  with both the
  [`--ssl-session-data`](connection-options.md#option_general_ssl-session-data) and
  [`--ssl-session-data-continue-on-failed-reuse`](connection-options.md#option_general_ssl-session-data-continue-on-failed-reuse)
  command-line options.
- [`--tls-ciphersuites=ciphersuite_list`](connection-options.md#option_general_tls-ciphersuites)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-ciphersuites=ciphersuite_list` |
  | Introduced | 8.0.16 |
  | Type | String |
  | Default Value | `empty string` |

  This option specifies which ciphersuites the client permits
  for encrypted connections that use TLSv1.3. The value is a
  list of zero or more colon-separated ciphersuite names. For
  example:

  ```terminal
  mysql --tls-ciphersuites="suite1:suite2:suite3"
  ```

  The ciphersuites that can be named for this option depend on
  the SSL library used to compile MySQL. If this option is not
  set, the client permits the default set of ciphersuites. If
  the option is set to the empty string, no ciphersuites are
  enabled and encrypted connections cannot be established. For
  more information, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").

  This option was added in MySQL 8.0.16.

  To specify which ciphersuites the server permits, set the
  [`tls_ciphersuites`](server-system-variables.md#sysvar_tls_ciphersuites) system
  variable.
- [`--tls-version=protocol_list`](connection-options.md#option_general_tls-version)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tls-version=protocol_list` |
  | Type | String |
  | Default Value (≥ 8.0.16) | `TLSv1,TLSv1.1,TLSv1.2,TLSv1.3` (OpenSSL 1.1.1 or higher)  `TLSv1,TLSv1.1,TLSv1.2` (otherwise) |
  | Default Value (≤ 8.0.15) | `TLSv1,TLSv1.1,TLSv1.2` |

  This option specifies the TLS protocols the client permits
  for encrypted connections. The value is a list of one or
  more comma-separated protocol versions. For example:

  ```terminal
  mysql --tls-version="TLSv1.2,TLSv1.3"
  ```

  The protocols that can be named for this option depend on
  the SSL library used to compile MySQL, and on the MySQL
  Server release.

  Important

  - Support for the TLSv1 and TLSv1.1 connection protocols
    is removed from MySQL Server as of MySQL 8.0.28. The
    protocols were deprecated from MySQL 8.0.26, though
    MySQL Server clients do not return warnings to the
    user if a deprecated TLS protocol version is used.
    From MySQL 8.0.28 onwards, clients, including MySQL
    Shell, that support the
    [`--tls-version`](connection-options.md#option_general_tls-version) option
    cannot make a TLS/SSL connection with the protocol set
    to TLSv1 or TLSv1.1. If a client attempts to connect
    using these protocols, for TCP connections, the
    connection fails, and an error is returned to the
    client. For socket connections, if
    [`--ssl-mode`](connection-options.md#option_general_ssl-mode) is set to
    `REQUIRED`, the connection fails,
    otherwise the connection is made but with TLS/SSL
    disabled. See
    [Removal of Support for the TLSv1 and TLSv1.1 Protocols](encrypted-connection-protocols-ciphers.md#encrypted-connection-deprecated-protocols "Removal of Support for the TLSv1 and TLSv1.1 Protocols")
    for more information.
  - Support for the TLSv1.3 protocol is available in MySQL
    Server as of MySQL 8.0.16, provided that MySQL Server
    was compiled using OpenSSL 1.1.1 or higher. The server
    checks the version of OpenSSL at startup, and if it is
    lower than 1.1.1, TLSv1.3 is removed from the default
    value for the server system variables relating to the
    TLS version (such as the
    [`tls_version`](server-system-variables.md#sysvar_tls_version) system
    variable).

  Permitted protocols should be chosen such as not to leave
  “holes” in the list. For example, these values
  do not have holes:

  ```terminal
  --tls-version="TLSv1,TLSv1.1,TLSv1.2,TLSv1.3"
  --tls-version="TLSv1.1,TLSv1.2,TLSv1.3"
  --tls-version="TLSv1.2,TLSv1.3"
  --tls-version="TLSv1.3"

  From MySQL 8.0.28, only the last two values are suitable.
  ```

  These values do have holes and should not be used:

  ```terminal
  --tls-version="TLSv1,TLSv1.2"
  --tls-version="TLSv1.1,TLSv1.3"
  ```

  For details, see
  [Section 8.3.2, “Encrypted Connection TLS Protocols and Ciphers”](encrypted-connection-protocols-ciphers.md "8.3.2 Encrypted Connection TLS Protocols and Ciphers").

  To specify which TLS protocols the server permits, set the
  [`tls_version`](server-system-variables.md#sysvar_tls_version) system
  variable.

#### Command Options for Connection Compression

This section describes options that enable client programs to
control use of compression for connections to the server. For
additional information and examples showing how to use them, see
[Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control").

**Table 6.6 Connection-Compression Option Summary**

| Option Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [--compress](connection-options.md#option_general_compress) | Compress all information sent between client and server |  | 8.0.18 |
| [--compression-algorithms](connection-options.md#option_general_compression-algorithms) | Permitted compression algorithms for connections to server | 8.0.18 |  |
| [--zstd-compression-level](connection-options.md#option_general_zstd-compression-level) | Compression level for connections to server that use zstd compression | 8.0.18 |  |

- [`--compress`](connection-options.md#option_general_compress),
  `-C`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--compress[={OFF|ON}]` |
  | Deprecated | 8.0.18 |
  | Type | Boolean |
  | Default Value | `OFF` |

  Compress all information sent between the client and the
  server if possible.

  As of MySQL 8.0.18, this option is deprecated. Expect it to
  be removed in a future version of MySQL. See
  [Configuring Legacy Connection Compression](connection-compression-control.md#connection-compression-legacy-configuration "Configuring Legacy Connection Compression").
- [`--compression-algorithms=value`](connection-options.md#option_general_compression-algorithms)

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

  This option was added in MySQL 8.0.18.
- [`--zstd-compression-level=level`](connection-options.md#option_general_zstd-compression-level)

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

  This option was added in MySQL 8.0.18.
