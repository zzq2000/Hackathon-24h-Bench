#### 8.4.1.13 Pluggable Authentication System Variables

These variables are unavailable unless the appropriate
server-side plugin is installed:

- `authentication_ldap_sasl` for system
  variables with names of the form
  `authentication_ldap_sasl_xxx`
- `authentication_ldap_simple` for system
  variables with names of the form
  `authentication_ldap_simple_xxx`

**Table 8.29 Authentication Plugin System Variable
Summary**

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| --- | --- | --- | --- | --- | --- | --- |
| [authentication\_fido\_rp\_id](pluggable-authentication-system-variables.md#sysvar_authentication_fido_rp_id) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_kerberos\_service\_key\_tab](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_key_tab) | Yes | Yes | Yes |  | Global | No |
| [authentication\_kerberos\_service\_principal](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_principal) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_auth\_method\_name](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_auth_method_name) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_base\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_base_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_root\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_bind\_root\_pwd](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_pwd) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_ca\_path](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_ca_path) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_group\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_group\_search\_filter](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_filter) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_init\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_log\_status](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_log_status) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_max\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_referral](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_referral) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_server\_host](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_host) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_server\_port](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_port) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_tls](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_tls) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_sasl\_user\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_user_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_auth\_method\_name](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_auth_method_name) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_base\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_base_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_root\_dn](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_bind\_root\_pwd](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_pwd) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_ca\_path](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_ca_path) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_group\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_group\_search\_filter](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_filter) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_init\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_log\_status](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_log_status) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_max\_pool\_size](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_referral](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_referral) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_server\_host](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_host) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_server\_port](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_port) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_tls](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_tls) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_ldap\_simple\_user\_search\_attr](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_user_search_attr) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_policy](server-system-variables.md#sysvar_authentication_policy) | Yes | Yes | Yes |  | Global | Yes |
| [authentication\_windows\_log\_level](server-system-variables.md#sysvar_authentication_windows_log_level) | Yes | Yes | Yes |  | Global | No |
| [authentication\_windows\_use\_principal\_name](server-system-variables.md#sysvar_authentication_windows_use_principal_name) | Yes | Yes | Yes |  | Global | No |

- [`authentication_fido_rp_id`](pluggable-authentication-system-variables.md#sysvar_authentication_fido_rp_id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-fido-rp-id=value` |
  | Introduced | 8.0.27 |
  | Deprecated | 8.0.35 |
  | System Variable | `authentication_fido_rp_id` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `MySQL` |

  This variable specifies the relying party ID used for FIDO
  device registration and FIDO authentication. If FIDO
  authentication is attempted and this value is not the one
  expected by the FIDO device, the device assumes that it is
  not talking to the correct server and an error occurs. The
  maximum value length is 255 characters.

  Note

  As of MySQL 8.0.35, this plugin variable is deprecated and
  subject to removal in a future MySQL release.
- [`authentication_kerberos_service_key_tab`](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_key_tab)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-kerberos-service-key-tab=file_name` |
  | Introduced | 8.0.26 |
  | System Variable | `authentication_kerberos_service_key_tab` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `datadir/mysql.keytab` |

  The name of the server-side key-table
  (“keytab”) file containing Kerberos service
  keys to authenticate MySQL service tickets received from
  clients. The file name should be given as an absolute path
  name. If this variable is not set, the default is
  `mysql.keytab` in the data directory.

  The file must exist and contain a valid key for the service
  principal name (SPN) or authentication of clients will fail.
  (The SPN and same key also must be created in the Kerberos
  server.) The file may contain multiple service principal
  names and their respective key combinations.

  The file must be generated by the Kerberos server
  administrator and be copied to a location accessible by the
  MySQL server. The file can be validated to make sure that it
  is correct and was copied properly using this command:

  ```terminal
  klist -k file_name
  ```

  For information about keytab files, see
  <https://web.mit.edu/kerberos/krb5-latest/doc/basic/keytab_def.html>.
- [`authentication_kerberos_service_principal`](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_principal)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-kerberos-service-principal=name` |
  | Introduced | 8.0.26 |
  | System Variable | `authentication_kerberos_service_principal` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `mysql/host_name@realm_name` |

  The Kerberos service principal name (SPN) that the MySQL
  server sends to clients.

  The value is composed from the service name
  (`mysql`), a host name, and a realm name.
  The default value is
  `mysql/host_name@realm_name`.
  The realm in the service principal name enables retrieving
  the exact service key.

  To use a nondefault value, set the value using the same
  format. For example, to use a host name of
  `krbauth.example.com` and a realm of
  `MYSQL.LOCAL`, set
  [`authentication_kerberos_service_principal`](pluggable-authentication-system-variables.md#sysvar_authentication_kerberos_service_principal)
  to `mysql/krbauth.example.com@MYSQL.LOCAL`.

  The service principal name and service key must already be
  present in the database managed by the KDC server.

  There can be service principal names that differ only by
  realm name.
- [`authentication_ldap_sasl_auth_method_name`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_auth_method_name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-auth-method-name=value` |
  | System Variable | `authentication_ldap_sasl_auth_method_name` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `SCRAM-SHA-1` |
  | Valid Values (≥ 8.0.23) | `SCRAM-SHA-1`  `SCRAM-SHA-256`  `GSSAPI` |
  | Valid Values (≥ 8.0.20, ≤ 8.0.22) | `SCRAM-SHA-1`  `GSSAPI` |
  | Valid Values (≤ 8.0.19) | `SCRAM-SHA-1` |

  For SASL LDAP authentication, the authentication method
  name. Communication between the authentication plugin and
  the LDAP server occurs according to this authentication
  method to ensure password security.

  These authentication method values are permitted:

  - `SCRAM-SHA-1`: Use a SASL
    challenge-response mechanism.

    The client-side
    `authentication_ldap_sasl_client`
    plugin communicates with the SASL server, using the
    password to create a challenge and obtain a SASL request
    buffer, then passes this buffer to the server-side
    `authentication_ldap_sasl` plugin. The
    client-side and server-side SASL LDAP plugins use SASL
    messages for secure transmission of credentials within
    the LDAP protocol, to avoid sending the cleartext
    password between the MySQL client and server.
  - `SCRAM-SHA-256`: Use a SASL
    challenge-response mechanism.

    This method is similar to
    `SCRAM-SHA-1`, but is more secure. It
    is available in MySQL 8.0.23 and higher. It requires an
    OpenLDAP server built using Cyrus SASL 2.1.27 or higher.
  - `GSSAPI`: Use Kerberos, a passwordless
    and ticket-based protocol.

    GSSAPI/Kerberos is supported as an authentication method
    for MySQL clients and servers only on Linux. It is
    useful in Linux environments where applications access
    LDAP using Microsoft Active Directory, which has
    Kerberos enabled by default.

    The client-side
    `authentication_ldap_sasl_client`
    plugin obtains a service ticket using the
    ticket-granting ticket (TGT) from Kerberos, but does not
    use LDAP services directly. The server-side
    `authentication_ldap_sasl` plugin
    routes Kerberos messages between the client-side plugin
    and the LDAP server. Using the credentials thus
    obtained, the server-side plugin then communicates with
    the LDAP server to interpret LDAP authentication
    messages and retrieve LDAP groups.
- [`authentication_ldap_sasl_bind_base_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_base_dn)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-bind-base-dn=value` |
  | System Variable | `authentication_ldap_sasl_bind_base_dn` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For SASL LDAP authentication, the base distinguished name
  (DN). This variable can be used to limit the scope of
  searches by anchoring them at a certain location (the
  “base”) within the search tree.

  Suppose that members of one set of LDAP user entries each
  have this form:

  ```ini
  uid=user_name,ou=People,dc=example,dc=com
  ```

  And that members of another set of LDAP user entries each
  have this form:

  ```ini
  uid=user_name,ou=Admin,dc=example,dc=com
  ```

  Then searches work like this for different base DN values:

  - If the base DN is
    `ou=People,dc=example,dc=com`: Searches
    find user entries only in the first set.
  - If the base DN is
    `ou=Admin,dc=example,dc=com`: Searches
    find user entries only in the second set.
  - If the base DN is
    `ou=dc=example,dc=com`: Searches find
    user entries in the first or second set.

  In general, more specific base DN values result in faster
  searches because they limit the search scope more.
- [`authentication_ldap_sasl_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_dn)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-bind-root-dn=value` |
  | System Variable | `authentication_ldap_sasl_bind_root_dn` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For SASL LDAP authentication, the root distinguished name
  (DN). This variable is used in conjunction with
  [`authentication_ldap_sasl_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_pwd)
  as the credentials for authenticating to the LDAP server for
  the purpose of performing searches. Authentication uses
  either one or two LDAP bind operations, depending on whether
  the MySQL account names an LDAP user DN:

  - If the account does not name a user DN:
    `authentication_ldap_sasl` performs an
    initial LDAP binding using
    [`authentication_ldap_sasl_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_dn)
    and
    [`authentication_ldap_sasl_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_pwd).
    (These are both empty by default, so if they are not
    set, the LDAP server must permit anonymous connections.)
    The resulting bind LDAP handle is used to search for the
    user DN, based on the client user name.
    `authentication_ldap_sasl` performs a
    second bind using the user DN and client-supplied
    password.
  - If the account does name a user DN: The first bind
    operation is unnecessary in this case.
    `authentication_ldap_sasl` performs a
    single bind using the user DN and client-supplied
    password. This is faster than if the MySQL account does
    not specify an LDAP user DN.
- [`authentication_ldap_sasl_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_pwd)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-bind-root-pwd=value` |
  | System Variable | `authentication_ldap_sasl_bind_root_pwd` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For SASL LDAP authentication, the password for the root
  distinguished name. This variable is used in conjunction
  with
  [`authentication_ldap_sasl_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_bind_root_dn).
  See the description of that variable.
- [`authentication_ldap_sasl_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_ca_path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-ca-path=value` |
  | System Variable | `authentication_ldap_sasl_ca_path` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For SASL LDAP authentication, the absolute path of the
  certificate authority file. Specify this file if it is
  desired that the authentication plugin perform verification
  of the LDAP server certificate.

  Note

  In addition to setting the
  [`authentication_ldap_sasl_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_ca_path)
  variable to the file name, you must add the appropriate
  certificate authority certificates to the file and enable
  the
  [`authentication_ldap_sasl_tls`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_tls)
  system variable. These variables can be set to override
  the default OpenLDAP TLS configuration; see
  [LDAP Pluggable Authentication and ldap.conf](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-conf "LDAP Pluggable Authentication and ldap.conf")
- [`authentication_ldap_sasl_group_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_attr)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-group-search-attr=value` |
  | System Variable | `authentication_ldap_sasl_group_search_attr` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `cn` |

  For SASL LDAP authentication, the name of the attribute that
  specifies group names in LDAP directory entries. If
  [`authentication_ldap_sasl_group_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_attr)
  has its default value of `cn`, searches
  return the `cn` value as the group name.
  For example, if an LDAP entry with a `uid`
  value of `user1` has a
  `cn` attribute of
  `mygroup`, searches for
  `user1` return `mygroup`
  as the group name.

  This variable should be the empty string if you want no
  group or proxy authentication.

  If the group search attribute is
  `isMemberOf`, LDAP authentication directly
  retrieves the user attribute `isMemberOf`
  value and assigns it as group information. If the group
  search attribute is not `isMemberOf`, LDAP
  authentication searches for all groups where the user is a
  member. (The latter is the default behavior.) This behavior
  is based on how LDAP group information can be stored two
  ways: 1) A group entry can have an attribute named
  `memberUid` or `member`
  with a value that is a user name; 2) A user entry can have
  an attribute named `isMemberOf` with values
  that are group names.
- [`authentication_ldap_sasl_group_search_filter`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_group_search_filter)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-group-search-filter=value` |
  | System Variable | `authentication_ldap_sasl_group_search_filter` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `(|(&(objectClass=posixGroup)(memberUid=%s))(&(objectClass=group)(member=%s)))` |

  For SASL LDAP authentication, the custom group search
  filter.

  The search filter value can contain `{UA}`
  and `{UD}` notation to represent the user
  name and the full user DN. For example,
  `{UA}` is replaced with a user name such as
  `"admin"`, whereas `{UD}`
  is replaced with a use full DN such as
  `"uid=admin,ou=People,dc=example,dc=com"`.
  The following value is the default, which supports both
  OpenLDAP and Active Directory:

  ```simple
  (|(&(objectClass=posixGroup)(memberUid={UA}))
    (&(objectClass=group)(member={UD})))
  ```

  In some cases for the user scenario,
  `memberOf` is a simple user attribute that
  holds no group information. For additional flexibility, an
  optional `{GA}` prefix can be used with the
  group search attribute. Any group attribute with a {GA}
  prefix is treated as a user attribute having group names.
  For example, with a value of
  `{GA}MemberOf`, if the group value is the
  DN, the first attribute value from the group DN is returned
  as the group name.
- [`authentication_ldap_sasl_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-init-pool-size=#` |
  | System Variable | `authentication_ldap_sasl_init_pool_size` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `10` |
  | Minimum Value | `0` |
  | Maximum Value | `32767` |
  | Unit | connections |

  For SASL LDAP authentication, the initial size of the pool
  of connections to the LDAP server. Choose the value for this
  variable based on the average number of concurrent
  authentication requests to the LDAP server.

  The plugin uses
  [`authentication_ldap_sasl_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size)
  and
  [`authentication_ldap_sasl_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size)
  together for connection-pool management:

  - When the authentication plugin initializes, it creates
    [`authentication_ldap_sasl_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size)
    connections, unless
    [`authentication_ldap_sasl_max_pool_size=0`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size)
    to disable pooling.
  - If the plugin receives an authentication request when
    there are no free connections in the current connection
    pool, the plugin can create a new connection, up to the
    maximum connection pool size given by
    [`authentication_ldap_sasl_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size).
  - If the plugin receives a request when the pool size is
    already at its maximum and there are no free
    connections, authentication fails.
  - When the plugin unloads, it closes all pooled
    connections.

  Changes to plugin system variable settings may have no
  effect on connections already in the pool. For example,
  modifying the LDAP server host, port, or TLS settings does
  not affect existing connections. However, if the original
  variable values were invalid and the connection pool could
  not be initialized, the plugin attempts to reinitialize the
  pool for the next LDAP request. In this case, the new system
  variable values are used for the reinitialization attempt.

  If
  [`authentication_ldap_sasl_max_pool_size=0`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size)
  to disable pooling, each LDAP connection opened by the
  plugin uses the values the system variables have at that
  time.
- [`authentication_ldap_sasl_log_status`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_log_status)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-log-status=#` |
  | System Variable | `authentication_ldap_sasl_log_status` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `1` |
  | Maximum Value (≥ 8.0.18) | `6` |
  | Maximum Value (≤ 8.0.17) | `5` |

  For SASL LDAP authentication, the logging level for messages
  written to the error log. The following table shows the
  permitted level values and their meanings.

  **Table 8.30 Log Levels for authentication\_ldap\_sasl\_log\_status**

  | Option Value | Types of Messages Logged |
  | --- | --- |
  | `1` | No messages |
  | `2` | Error messages |
  | `3` | Error and warning messages |
  | `4` | Error, warning, and information messages |
  | `5` | Same as previous level plus debugging messages from MySQL |
  | `6` | Same as previous level plus debugging messages from LDAP library |

  Log level 6 is available as of MySQL 8.0.18.

  On the client side, messages can be logged to the standard
  output by setting the
  `AUTHENTICATION_LDAP_CLIENT_LOG`
  environment variable. The permitted and default values are
  the same as for
  [`authentication_ldap_sasl_log_status`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_log_status).

  The `AUTHENTICATION_LDAP_CLIENT_LOG`
  environment variable applies only to SASL LDAP
  authentication. It has no effect for simple LDAP
  authentication because the client plugin in that case is
  `mysql_clear_password`, which knows nothing
  about LDAP operations.
- [`authentication_ldap_sasl_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_max_pool_size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-max-pool-size=#` |
  | System Variable | `authentication_ldap_sasl_max_pool_size` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1000` |
  | Minimum Value | `0` |
  | Maximum Value | `32767` |
  | Unit | connections |

  For SASL LDAP authentication, the maximum size of the pool
  of connections to the LDAP server. To disable connection
  pooling, set this variable to 0.

  This variable is used in conjunction with
  [`authentication_ldap_sasl_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_init_pool_size).
  See the description of that variable.
- [`authentication_ldap_sasl_referral`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_referral)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-referral[={OFF|ON}]` |
  | Introduced | 8.0.20 |
  | System Variable | `authentication_ldap_sasl_referral` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `OFF` |

  For SASL LDAP authentication, whether to enable LDAP search
  referral. See
  [LDAP Search Referral](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-referral "LDAP Search Referral").

  This variable can be set to override the default OpenLDAP
  referral configuration; see
  [LDAP Pluggable Authentication and ldap.conf](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-conf "LDAP Pluggable Authentication and ldap.conf")
- [`authentication_ldap_sasl_server_host`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-server-host=host_name` |
  | System Variable | `authentication_ldap_sasl_server_host` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The LDAP server host for SASL LDAP authentication; this can
  be a host name or IP address.
- [`authentication_ldap_sasl_server_port`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_port)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-server-port=port_num` |
  | System Variable | `authentication_ldap_sasl_server_port` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `389` |
  | Minimum Value | `1` |
  | Maximum Value | `32376` |

  For SASL LDAP authentication, the LDAP server TCP/IP port
  number.

  As of MySQL 8.0.14, if the LDAP port number is configured as
  636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead
  of LDAP. (LDAPS differs from `startTLS`.)
- [`authentication_ldap_sasl_tls`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_tls)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-tls[={OFF|ON}]` |
  | System Variable | `authentication_ldap_sasl_tls` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `OFF` |

  For SASL LDAP authentication, whether connections by the
  plugin to the LDAP server are secure. If this variable is
  enabled, the plugin uses TLS to connect securely to the LDAP
  server. This variable can be set to override the default
  OpenLDAP TLS configuration; see
  [LDAP Pluggable Authentication and ldap.conf](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-conf "LDAP Pluggable Authentication and ldap.conf") If
  you enable this variable, you may also wish to set the
  [`authentication_ldap_sasl_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_ca_path)
  variable.

  MySQL LDAP plugins support the StartTLS method, which
  initializes TLS on top of a plain LDAP connection.

  As of MySQL 8.0.14, LDAPS can be used by setting the
  [`authentication_ldap_sasl_server_port`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_server_port)
  system variable.
- [`authentication_ldap_sasl_user_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_user_search_attr)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-sasl-user-search-attr=value` |
  | System Variable | `authentication_ldap_sasl_user_search_attr` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `uid` |

  For SASL LDAP authentication, the name of the attribute that
  specifies user names in LDAP directory entries. If a user
  distinguished name is not provided, the authentication
  plugin searches for the name using this attribute. For
  example, if the
  [`authentication_ldap_sasl_user_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_sasl_user_search_attr)
  value is `uid`, a search for the user name
  `user1` finds entries with a
  `uid` value of `user1`.
- [`authentication_ldap_simple_auth_method_name`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_auth_method_name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-auth-method-name=value` |
  | System Variable | `authentication_ldap_simple_auth_method_name` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `SIMPLE` |
  | Valid Values | `SIMPLE`  `AD-FOREST` |

  For simple LDAP authentication, the authentication method
  name. Communication between the authentication plugin and
  the LDAP server occurs according to this authentication
  method.

  Note

  For all simple LDAP authentication methods, it is
  recommended to also set TLS parameters to require that
  communication with the LDAP server take place over secure
  connections.

  These authentication method values are permitted:

  - `SIMPLE`: Use simple LDAP
    authentication. This method uses either one or two LDAP
    bind operations, depending on whether the MySQL account
    names an LDAP user distinguished name. See the
    description of
    [`authentication_ldap_simple_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn).
  - `AD-FOREST`: A variation on
    `SIMPLE`, such that authentication
    searches all domains in the Active Directory forest,
    performing an LDAP bind to each Active Directory domain
    until the user is found in some domain.
- [`authentication_ldap_simple_bind_base_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_base_dn)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-bind-base-dn=value` |
  | System Variable | `authentication_ldap_simple_bind_base_dn` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For simple LDAP authentication, the base distinguished name
  (DN). This variable can be used to limit the scope of
  searches by anchoring them at a certain location (the
  “base”) within the search tree.

  Suppose that members of one set of LDAP user entries each
  have this form:

  ```ini
  uid=user_name,ou=People,dc=example,dc=com
  ```

  And that members of another set of LDAP user entries each
  have this form:

  ```ini
  uid=user_name,ou=Admin,dc=example,dc=com
  ```

  Then searches work like this for different base DN values:

  - If the base DN is
    `ou=People,dc=example,dc=com`: Searches
    find user entries only in the first set.
  - If the base DN is
    `ou=Admin,dc=example,dc=com`: Searches
    find user entries only in the second set.
  - If the base DN is
    `ou=dc=example,dc=com`: Searches find
    user entries in the first or second set.

  In general, more specific base DN values result in faster
  searches because they limit the search scope more.
- [`authentication_ldap_simple_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-bind-root-dn=value` |
  | System Variable | `authentication_ldap_simple_bind_root_dn` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For simple LDAP authentication, the root distinguished name
  (DN). This variable is used in conjunction with
  [`authentication_ldap_simple_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_pwd)
  as the credentials for authenticating to the LDAP server for
  the purpose of performing searches. Authentication uses
  either one or two LDAP bind operations, depending on whether
  the MySQL account names an LDAP user DN:

  - If the account does not name a user DN:
    `authentication_ldap_simple` performs
    an initial LDAP binding using
    [`authentication_ldap_simple_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn)
    and
    [`authentication_ldap_simple_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_pwd).
    (These are both empty by default, so if they are not
    set, the LDAP server must permit anonymous connections.)
    The resulting bind LDAP handle is used to search for the
    user DN, based on the client user name.
    `authentication_ldap_simple` performs a
    second bind using the user DN and client-supplied
    password.
  - If the account does name a user DN: The first bind
    operation is unnecessary in this case.
    `authentication_ldap_simple` performs a
    single bind using the user DN and client-supplied
    password. This is faster than if the MySQL account does
    not specify an LDAP user DN.
- [`authentication_ldap_simple_bind_root_pwd`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_pwd)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-bind-root-pwd=value` |
  | System Variable | `authentication_ldap_simple_bind_root_pwd` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For simple LDAP authentication, the password for the root
  distinguished name. This variable is used in conjunction
  with
  [`authentication_ldap_simple_bind_root_dn`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_bind_root_dn).
  See the description of that variable.
- [`authentication_ldap_simple_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_ca_path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-ca-path=value` |
  | System Variable | `authentication_ldap_simple_ca_path` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `NULL` |

  For simple LDAP authentication, the absolute path of the
  certificate authority file. Specify this file if it is
  desired that the authentication plugin perform verification
  of the LDAP server certificate.

  Note

  In addition to setting the
  [`authentication_ldap_simple_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_ca_path)
  variable to the file name, you must add the appropriate
  certificate authority certificates to the file and enable
  the
  [`authentication_ldap_simple_tls`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_tls)
  system variable. These variables can be set to override
  the default OpenLDAP TLS configuration; see
  [LDAP Pluggable Authentication and ldap.conf](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-conf "LDAP Pluggable Authentication and ldap.conf")
- [`authentication_ldap_simple_group_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_attr)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-group-search-attr=value` |
  | System Variable | `authentication_ldap_simple_group_search_attr` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `cn` |

  For simple LDAP authentication, the name of the attribute
  that specifies group names in LDAP directory entries. If
  [`authentication_ldap_simple_group_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_attr)
  has its default value of `cn`, searches
  return the `cn` value as the group name.
  For example, if an LDAP entry with a `uid`
  value of `user1` has a
  `cn` attribute of
  `mygroup`, searches for
  `user1` return `mygroup`
  as the group name.

  If the group search attribute is
  `isMemberOf`, LDAP authentication directly
  retrieves the user attribute `isMemberOf`
  value and assigns it as group information. If the group
  search attribute is not `isMemberOf`, LDAP
  authentication searches for all groups where the user is a
  member. (The latter is the default behavior.) This behavior
  is based on how LDAP group information can be stored two
  ways: 1) A group entry can have an attribute named
  `memberUid` or `member`
  with a value that is a user name; 2) A user entry can have
  an attribute named `isMemberOf` with values
  that are group names.
- [`authentication_ldap_simple_group_search_filter`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_group_search_filter)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-group-search-filter=value` |
  | System Variable | `authentication_ldap_simple_group_search_filter` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `(|(&(objectClass=posixGroup)(memberUid=%s))(&(objectClass=group)(member=%s)))` |

  For simple LDAP authentication, the custom group search
  filter.

  The search filter value can contain `{UA}`
  and `{UD}` notation to represent the user
  name and the full user DN. For example,
  `{UA}` is replaced with a user name such as
  `"admin"`, whereas `{UD}`
  is replaced with a use full DN such as
  `"uid=admin,ou=People,dc=example,dc=com"`.
  The following value is the default, which supports both
  OpenLDAP and Active Directory:

  ```simple
  (|(&(objectClass=posixGroup)(memberUid={UA}))
    (&(objectClass=group)(member={UD})))
  ```

  In some cases for the user scenario,
  `memberOf` is a simple user attribute that
  holds no group information. For additional flexibility, an
  optional `{GA}` prefix can be used with the
  group search attribute. Any group attribute with a {GA}
  prefix is treated as a user attribute having group names.
  For example, with a value of
  `{GA}MemberOf`, if the group value is the
  DN, the first attribute value from the group DN is returned
  as the group name.
- [`authentication_ldap_simple_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-init-pool-size=#` |
  | System Variable | `authentication_ldap_simple_init_pool_size` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `10` |
  | Minimum Value | `0` |
  | Maximum Value | `32767` |
  | Unit | connections |

  For simple LDAP authentication, the initial size of the pool
  of connections to the LDAP server. Choose the value for this
  variable based on the average number of concurrent
  authentication requests to the LDAP server.

  The plugin uses
  [`authentication_ldap_simple_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size)
  and
  [`authentication_ldap_simple_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size)
  together for connection-pool management:

  - When the authentication plugin initializes, it creates
    [`authentication_ldap_simple_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size)
    connections, unless
    [`authentication_ldap_simple_max_pool_size=0`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size)
    to disable pooling.
  - If the plugin receives an authentication request when
    there are no free connections in the current connection
    pool, the plugin can create a new connection, up to the
    maximum connection pool size given by
    [`authentication_ldap_simple_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size).
  - If the plugin receives a request when the pool size is
    already at its maximum and there are no free
    connections, authentication fails.
  - When the plugin unloads, it closes all pooled
    connections.

  Changes to plugin system variable settings may have no
  effect on connections already in the pool. For example,
  modifying the LDAP server host, port, or TLS settings does
  not affect existing connections. However, if the original
  variable values were invalid and the connection pool could
  not be initialized, the plugin attempts to reinitialize the
  pool for the next LDAP request. In this case, the new system
  variable values are used for the reinitialization attempt.

  If
  [`authentication_ldap_simple_max_pool_size=0`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size)
  to disable pooling, each LDAP connection opened by the
  plugin uses the values the system variables have at that
  time.
- [`authentication_ldap_simple_log_status`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_log_status)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-log-status=#` |
  | System Variable | `authentication_ldap_simple_log_status` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `1` |
  | Maximum Value (≥ 8.0.18) | `6` |
  | Maximum Value (≤ 8.0.17) | `5` |

  For simple LDAP authentication, the logging level for
  messages written to the error log. The following table shows
  the permitted level values and their meanings.

  **Table 8.31 Log Levels for authentication\_ldap\_simple\_log\_status**

  | Option Value | Types of Messages Logged |
  | --- | --- |
  | `1` | No messages |
  | `2` | Error messages |
  | `3` | Error and warning messages |
  | `4` | Error, warning, and information messages |
  | `5` | Same as previous level plus debugging messages from MySQL |
  | `6` | Same as previous level plus debugging messages from LDAP library |

  Log level 6 is available as of MySQL 8.0.18.
- [`authentication_ldap_simple_max_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_max_pool_size)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-max-pool-size=#` |
  | System Variable | `authentication_ldap_simple_max_pool_size` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1000` |
  | Minimum Value | `0` |
  | Maximum Value | `32767` |
  | Unit | connections |

  For simple LDAP authentication, the maximum size of the pool
  of connections to the LDAP server. To disable connection
  pooling, set this variable to 0.

  This variable is used in conjunction with
  [`authentication_ldap_simple_init_pool_size`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_init_pool_size).
  See the description of that variable.
- [`authentication_ldap_simple_referral`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_referral)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-referral[={OFF|ON}]` |
  | Introduced | 8.0.20 |
  | System Variable | `authentication_ldap_simple_referral` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `OFF` |

  For simple LDAP authentication, whether to enable LDAP
  search referral. See
  [LDAP Search Referral](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-referral "LDAP Search Referral").
- [`authentication_ldap_simple_server_host`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_host)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-server-host=host_name` |
  | System Variable | `authentication_ldap_simple_server_host` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  For simple LDAP authentication, the LDAP server host. The
  permitted values for this variable depend on the
  authentication method:

  - For
    [`authentication_ldap_simple_auth_method_name=SIMPLE`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_auth_method_name):
    The LDAP server host can be a host name or IP address.
  - For
    [`authentication_ldap_simple_auth_method_name=AD-FOREST`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_auth_method_name).
    The LDAP server host can be an Active Directory domain
    name. For example, for an LDAP server URL of
    `ldap://example.mem.local:389`, the
    domain name can be `mem.local`.

    An Active Directory forest setup can have multiple
    domains (LDAP server IPs), which can be discovered using
    DNS. On Unix and Unix-like systems, some additional
    setup may be required to configure your DNS server with
    SRV records that specify the LDAP servers for the Active
    Directory domain. For information about DNS SRV, see
    [RFC
    2782](https://tools.ietf.org/html/rfc2782).

    Suppose that your configuration has these properties:

    - The name server that provides information about
      Active Directory domains has IP address
      `10.172.166.100`.
    - The LDAP servers have names
      `ldap1.mem.local` through
      `ldap3.mem.local` and IP addresses
      `10.172.166.101` through
      `10.172.166.103`.

    You want the LDAP servers to be discoverable using SRV
    searches. For example, at the command line, a command
    like this should list the LDAP servers:

    ```terminal
    host -t SRV _ldap._tcp.mem.local
    ```

    Perform the DNS configuration as follows:

    1. Add a line to `/etc/resolv.conf`
       to specify the name server that provides information
       about Active Directory domains:

       ```none
       nameserver 10.172.166.100
       ```
    2. Configure the appropriate zone file for the name
       server with SRV records for the LDAP servers:

       ```none
       _ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap1.mem.local.
       _ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap2.mem.local.
       _ldap._tcp.mem.local. 86400 IN SRV 0 100 389 ldap3.mem.local.
       ```
    3. It may also be necessary to specify the IP address
       for the LDAP servers in
       `/etc/hosts` if the server host
       cannot be resolved. For example, add lines like this
       to the file:

       ```none
       10.172.166.101 ldap1.mem.local
       10.172.166.102 ldap2.mem.local
       10.172.166.103 ldap3.mem.local
       ```

    With the DNS configured as just described, the
    server-side LDAP plugin can discover the LDAP servers
    and tries to authenticate in all domains until
    authentication succeeds or there are no more servers.

    Windows needs no such settings as just described. Given
    the LDAP server host in the
    [`authentication_ldap_simple_server_host`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_host)
    value, the Windows LDAP library searches all domains and
    attempts to authenticate.
- [`authentication_ldap_simple_server_port`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_port)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-server-port=port_num` |
  | System Variable | `authentication_ldap_simple_server_port` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `389` |
  | Minimum Value | `1` |
  | Maximum Value | `32376` |

  For simple LDAP authentication, the LDAP server TCP/IP port
  number.

  As of MySQL 8.0.14, if the LDAP port number is configured as
  636 or 3269, the plugin uses LDAPS (LDAP over SSL) instead
  of LDAP. (LDAPS differs from `startTLS`.)
- [`authentication_ldap_simple_tls`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_tls)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-tls[={OFF|ON}]` |
  | System Variable | `authentication_ldap_simple_tls` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `OFF` |

  For simple LDAP authentication, whether connections by the
  plugin to the LDAP server are secure. If this variable is
  enabled, the plugin uses TLS to connect securely to the LDAP
  server. This variable can be set to override the default
  OpenLDAP TLS configuration; see
  [LDAP Pluggable Authentication and ldap.conf](ldap-pluggable-authentication.md#ldap-pluggable-authentication-ldap-conf "LDAP Pluggable Authentication and ldap.conf") If
  you enable this variable, you may also wish to set the
  [`authentication_ldap_simple_ca_path`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_ca_path)
  variable.

  MySQL LDAP plugins support the StartTLS method, which
  initializes TLS on top of a plain LDAP connection.

  As of MySQL 8.0.14, LDAPS can be used by setting the
  [`authentication_ldap_simple_server_port`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_server_port)
  system variable.
- [`authentication_ldap_simple_user_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_user_search_attr)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--authentication-ldap-simple-user-search-attr=value` |
  | System Variable | `authentication_ldap_simple_user_search_attr` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `uid` |

  For simple LDAP authentication, the name of the attribute
  that specifies user names in LDAP directory entries. If a
  user distinguished name is not provided, the authentication
  plugin searches for the name using this attribute. For
  example, if the
  [`authentication_ldap_simple_user_search_attr`](pluggable-authentication-system-variables.md#sysvar_authentication_ldap_simple_user_search_attr)
  value is `uid`, a search for the user name
  `user1` finds entries with a
  `uid` value of `user1`.
