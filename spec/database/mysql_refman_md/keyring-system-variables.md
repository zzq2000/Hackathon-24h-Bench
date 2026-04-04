#### 8.4.4.19 Keyring System Variables

MySQL Keyring plugins support the following system variables.
Use them to configure keyring plugin operation. These variables
are unavailable unless the appropriate keyring plugin is
installed (see [Section 8.4.4.3, “Keyring Plugin Installation”](keyring-plugin-installation.md "8.4.4.3 Keyring Plugin Installation")).

- [`keyring_aws_cmk_id`](keyring-system-variables.md#sysvar_keyring_aws_cmk_id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-aws-cmk-id=value` |
  | System Variable | `keyring_aws_cmk_id` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The KMS key ID obtained from the AWS KMS server and used by
  the `keyring_aws` plugin. This variable is
  unavailable unless that plugin is installed.

  This variable is mandatory. If not specified,
  `keyring_aws` initialization fails.
- [`keyring_aws_conf_file`](keyring-system-variables.md#sysvar_keyring_aws_conf_file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-aws-conf-file=file_name` |
  | System Variable | `keyring_aws_conf_file` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `platform specific` |

  The location of the configuration file for the
  `keyring_aws` plugin. This variable is
  unavailable unless that plugin is installed.

  At plugin startup, `keyring_aws` reads the
  AWS secret access key ID and key from the configuration
  file. For the `keyring_aws` plugin to start
  successfully, the configuration file must exist and contain
  valid secret access key information, initialized as
  described in [Section 8.4.4.9, “Using the keyring\_aws Amazon Web Services Keyring Plugin”](keyring-aws-plugin.md "8.4.4.9 Using the keyring_aws Amazon Web Services Keyring Plugin").

  The default file name is
  `keyring_aws_conf`, located in the default
  keyring file directory. The location of this default
  directory is the same as for the
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) system
  variable. See the description of that variable for details,
  as well as for considerations to take into account if you
  create the directory manually.
- [`keyring_aws_data_file`](keyring-system-variables.md#sysvar_keyring_aws_data_file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-aws-data-file` |
  | System Variable | `keyring_aws_data_file` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `platform specific` |

  The location of the storage file for the
  `keyring_aws` plugin. This variable is
  unavailable unless that plugin is installed.

  At plugin startup, if the value assigned to
  [`keyring_aws_data_file`](keyring-system-variables.md#sysvar_keyring_aws_data_file)
  specifies a file that does not exist, the
  `keyring_aws` plugin attempts to create it
  (as well as its parent directory, if necessary). If the file
  does exist, `keyring_aws` reads any
  encrypted keys contained in the file into its in-memory
  cache. `keyring_aws` does not cache
  unencrypted keys in memory.

  The default file name is
  `keyring_aws_data`, located in the default
  keyring file directory. The location of this default
  directory is the same as for the
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) system
  variable. See the description of that variable for details,
  as well as for considerations to take into account if you
  create the directory manually.
- [`keyring_aws_region`](keyring-system-variables.md#sysvar_keyring_aws_region)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-aws-region=value` |
  | System Variable | `keyring_aws_region` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Enumeration |
  | Default Value | `us-east-1` |
  | Valid Values (≥ 8.0.30) | `af-south-1`  `ap-east-1`  `ap-northeast-1`  `ap-northeast-2`  `ap-northeast-3`  `ap-south-1`  `ap-southeast-1`  `ap-southeast-2`  `ca-central-1`  `cn-north-1`  `cn-northwest-1`  `eu-central-1`  `eu-north-1`  `eu-south-1`  `eu-west-1`  `eu-west-2`  `eu-west-3`  `me-south-1`  `sa-east-1`  `us-east-1`  `us-east-2`  `us-gov-east-1`  `us-iso-east-1`  `us-iso-west-1`  `us-isob-east-1`  `us-west-1`  `us-west-2` |
  | Valid Values (≥ 8.0.17, ≤ 8.0.29) | `ap-northeast-1`  `ap-northeast-2`  `ap-south-1`  `ap-southeast-1`  `ap-southeast-2`  `ca-central-1`  `cn-north-1`  `cn-northwest-1`  `eu-central-1`  `eu-west-1`  `eu-west-2`  `eu-west-3`  `sa-east-1`  `us-east-1`  `us-east-2`  `us-west-1`  `us-west-2` |
  | Valid Values (≤ 8.0.16) | `ap-northeast-1`  `ap-northeast-2`  `ap-south-1`  `ap-southeast-1`  `ap-southeast-2`  `eu-central-1`  `eu-west-1`  `sa-east-1`  `us-east-1`  `us-west-1`  `us-west-2` |

  The AWS region for the `keyring_aws`
  plugin. This variable is unavailable unless that plugin is
  installed.

  If not set, the AWS region defaults to
  `us-east-1`. Thus, for any other region,
  this variable must be set explicitly.
- [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-encrypted-file-data=file_name` |
  | Deprecated | 8.0.34 |
  | System Variable | `keyring_encrypted_file_data` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `platform specific` |

  Note

  As of MySQL 8.0.34, the
  `keyring_encrypted_file` plugin is
  deprecated and subject to removal in a future version of
  MySQL. Consider using
  `component_keyring_encrypted_file`
  instead; the
  `component_keyring_encrypted_file`
  component supersedes the
  `keyring_encrypted_file` plugin.

  The path name of the data file used for secure data storage
  by the `keyring_encrypted_file` plugin.
  This variable is unavailable unless that plugin is
  installed. The file location should be in a directory
  considered for use only by keyring plugins. For example, do
  not locate the file under the data directory.

  Keyring operations are transactional: The
  `keyring_encrypted_file` plugin uses a
  backup file during write operations to ensure that it can
  roll back to the original file if an operation fails. The
  backup file has the same name as the value of the
  [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data)
  system variable with a suffix of
  `.backup`.

  Do not use the same
  `keyring_encrypted_file` data file for
  multiple MySQL instances. Each instance should have its own
  unique data file.

  The default file name is
  `keyring_encrypted`, located in a
  directory that is platform specific and depends on the value
  of the [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout)
  **CMake** option, as shown in the following
  table. To specify the default directory for the file
  explicitly if you are building from source, use the
  [`INSTALL_MYSQLKEYRINGDIR`](source-configuration-options.md#option_cmake_install_mysqlkeyringdir)
  **CMake** option.

  | `INSTALL_LAYOUT` Value | Default `keyring_encrypted_file_data` Value |
  | --- | --- |
  | `DEB`, `RPM`, `SVR4` | `/var/lib/mysql-keyring/keyring_encrypted` |
  | Otherwise | `keyring/keyring_encrypted` under the [`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix) value |

  At plugin startup, if the value assigned to
  [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data)
  specifies a file that does not exist, the
  `keyring_encrypted_file` plugin attempts to
  create it (as well as its parent directory, if necessary).

  If you create the directory manually, it should have a
  restrictive mode and be accessible only to the account used
  to run the MySQL server. For example, on Unix and Unix-like
  systems, to use the
  `/usr/local/mysql/mysql-keyring`
  directory, the following commands (executed as
  `root`) create the directory and set its
  mode and ownership:

  ```terminal
  cd /usr/local/mysql
  mkdir mysql-keyring
  chmod 750 mysql-keyring
  chown mysql mysql-keyring
  chgrp mysql mysql-keyring
  ```

  If the `keyring_encrypted_file` plugin
  cannot create or access its data file, it writes an error
  message to the error log. If an attempted runtime assignment
  to
  [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data)
  results in an error, the variable value remains unchanged.

  Important

  Once the `keyring_encrypted_file` plugin
  has created its data file and started to use it, it is
  important not to remove the file. Loss of the file causes
  data encrypted using its keys to become inaccessible. (It
  is permissible to rename or move the file, as long as you
  change the value of
  [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data)
  to match.)
- [`keyring_encrypted_file_password`](keyring-system-variables.md#sysvar_keyring_encrypted_file_password)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-encrypted-file-password=password` |
  | Deprecated | 8.0.34 |
  | System Variable | `keyring_encrypted_file_password` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  Note

  As of MySQL 8.0.34, the
  `keyring_encrypted_file` plugin is
  deprecated and subject to removal in a future version of
  MySQL. Consider using
  `component_keyring_encrypted_file`
  instead; the
  `component_keyring_encrypted_file`
  component supersedes the
  `keyring_encrypted_file` plugin.

  The password used by the
  `keyring_encrypted_file` plugin. This
  variable is unavailable unless that plugin is installed.

  This variable is mandatory. If not specified,
  `keyring_encrypted_file` initialization
  fails.

  If this variable is specified in an option file, the file
  should have a restrictive mode and be accessible only to the
  account used to run the MySQL server.

  Important

  Once the
  [`keyring_encrypted_file_password`](keyring-system-variables.md#sysvar_keyring_encrypted_file_password)
  value has been set, changing it does not rotate the
  keyring password and could make the server inaccessible.
  If an incorrect password is provided, the
  `keyring_encrypted_file` plugin cannot
  load keys from the encrypted keyring file.

  The password value cannot be displayed at runtime with
  [`SHOW VARIABLES`](show-variables.md "15.7.7.41 SHOW VARIABLES Statement") or the
  Performance Schema
  [`global_variables`](performance-schema-system-variable-tables.md "29.12.14 Performance Schema System Variable Tables") table because
  the display value is obfuscated.
- [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-file-data=file_name` |
  | Deprecated | 8.0.34 |
  | System Variable | `keyring_file_data` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `platform specific` |

  Note

  As of MySQL 8.0.34, the `keyring_file`
  plugin is deprecated and subject to removal in a future
  version of MySQL. Consider using
  `component_keyring_file` instead; the
  `component_keyring_file` component
  supersedes the `keyring_file` plugin.

  The path name of the data file used for secure data storage
  by the `keyring_file` plugin. This variable
  is unavailable unless that plugin is installed. The file
  location should be in a directory considered for use only by
  keyring plugins. For example, do not locate the file under
  the data directory.

  Keyring operations are transactional: The
  `keyring_file` plugin uses a backup file
  during write operations to ensure that it can roll back to
  the original file if an operation fails. The backup file has
  the same name as the value of the
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) system
  variable with a suffix of `.backup`.

  Do not use the same `keyring_file` data
  file for multiple MySQL instances. Each instance should have
  its own unique data file.

  The default file name is `keyring`,
  located in a directory that is platform specific and depends
  on the value of the
  [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout)
  **CMake** option, as shown in the following
  table. To specify the default directory for the file
  explicitly if you are building from source, use the
  [`INSTALL_MYSQLKEYRINGDIR`](source-configuration-options.md#option_cmake_install_mysqlkeyringdir)
  **CMake** option.

  | `INSTALL_LAYOUT` Value | Default `keyring_file_data` Value |
  | --- | --- |
  | `DEB`, `RPM`, `SVR4` | `/var/lib/mysql-keyring/keyring` |
  | Otherwise | `keyring/keyring` under the [`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix) value |

  At plugin startup, if the value assigned to
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) specifies
  a file that does not exist, the
  `keyring_file` plugin attempts to create it
  (as well as its parent directory, if necessary).

  If you create the directory manually, it should have a
  restrictive mode and be accessible only to the account used
  to run the MySQL server. For example, on Unix and Unix-like
  systems, to use the
  `/usr/local/mysql/mysql-keyring`
  directory, the following commands (executed as
  `root`) create the directory and set its
  mode and ownership:

  ```terminal
  cd /usr/local/mysql
  mkdir mysql-keyring
  chmod 750 mysql-keyring
  chown mysql mysql-keyring
  chgrp mysql mysql-keyring
  ```

  If the `keyring_file` plugin cannot create
  or access its data file, it writes an error message to the
  error log. If an attempted runtime assignment to
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) results
  in an error, the variable value remains unchanged.

  Important

  Once the `keyring_file` plugin has
  created its data file and started to use it, it is
  important not to remove the file. For example,
  `InnoDB` uses the file to store the
  master key used to decrypt the data in tables that use
  `InnoDB` tablespace encryption; see
  [Section 17.13, “InnoDB Data-at-Rest Encryption”](innodb-data-encryption.md "17.13 InnoDB Data-at-Rest Encryption"). Loss of the file
  causes data in such tables to become inaccessible. (It is
  permissible to rename or move the file, as long as you
  change the value of
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) to
  match.) It is recommended that you create a separate
  backup of the keyring data file immediately after you
  create the first encrypted table and before and after
  master key rotation.
- [`keyring_hashicorp_auth_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_auth_path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-auth-path=value` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_auth_path` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `/v1/auth/approle/login` |

  The authentication path where AppRole authentication is
  enabled within the HashiCorp Vault server, for use by the
  `keyring_hashicorp` plugin. This variable
  is unavailable unless that plugin is installed.
- [`keyring_hashicorp_ca_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_ca_path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-ca-path=file_name` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_ca_path` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |
  | Default Value | `empty string` |

  The absolute path name of a local file accessible to the
  MySQL server that contains a properly formatted TLS
  certificate authority for use by the
  `keyring_hashicorp` plugin. This variable
  is unavailable unless that plugin is installed.

  If this variable is not set, the
  `keyring_hashicorp` plugin opens an HTTPS
  connection without using server certificate verification,
  and trusts any certificate delivered by the HashiCorp Vault
  server. For this to be safe, it must be assumed that the
  Vault server is not malicious and that no man-in-the-middle
  attack is possible. If those assumptions are invalid, set
  [`keyring_hashicorp_ca_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_ca_path)
  to the path of a trusted CA certificate. (For example, for
  the instructions in
  [Certificate and Key Preparation](keyring-hashicorp-plugin.md#keyring-hashicorp-certificate-configuration "Certificate and Key Preparation"),
  this is the `company.crt` file.)
- [`keyring_hashicorp_caching`](keyring-system-variables.md#sysvar_keyring_hashicorp_caching)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-caching[={OFF|ON}]` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_caching` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `OFF` |

  Whether to enable the optional in-memory key cache used by
  the `keyring_hashicorp` plugin to cache
  keys from the HashiCorp Vault server. This variable is
  unavailable unless that plugin is installed. If the cache is
  enabled, the plugin populates it during initialization.
  Otherwise, the plugin populates only the key list during
  initialization.

  Enabling the cache is a compromise: It improves performance,
  but maintains a copy of sensitive key information in memory,
  which may be undesirable for security purposes.
- [`keyring_hashicorp_commit_auth_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_auth_path)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_auth_path` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_auth_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_auth_path),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_commit_ca_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_ca_path)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_ca_path` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_ca_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_ca_path),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_commit_caching`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_caching)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_caching` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_caching`](keyring-system-variables.md#sysvar_keyring_hashicorp_caching),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_commit_role_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_role_id)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_role_id` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_role_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_role_id),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_commit_server_url`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_server_url)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_server_url` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_server_url`](keyring-system-variables.md#sysvar_keyring_hashicorp_server_url),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_commit_store_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_commit_store_path)

  |  |  |
  | --- | --- |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_commit_store_path` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  This variable is associated with
  [`keyring_hashicorp_store_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_store_path),
  from which it takes its value during
  `keyring_hashicorp` plugin initialization.
  This variable is unavailable unless that plugin is
  installed. It reflects the “committed” value
  actually used for plugin operation if initialization
  succeeds. For additional information, see
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration").
- [`keyring_hashicorp_role_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_role_id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-role-id=value` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_role_id` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `empty string` |

  The HashiCorp Vault AppRole authentication role ID, for use
  by the `keyring_hashicorp` plugin. This
  variable is unavailable unless that plugin is installed. The
  value must be in UUID format.

  This variable is mandatory. If not specified,
  `keyring_hashicorp` initialization fails.
- [`keyring_hashicorp_secret_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_secret_id)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-secret-id=value` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_secret_id` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `empty string` |

  The HashiCorp Vault AppRole authentication secret ID, for
  use by the `keyring_hashicorp` plugin. This
  variable is unavailable unless that plugin is installed. The
  value must be in UUID format.

  This variable is mandatory. If not specified,
  `keyring_hashicorp` initialization fails.

  The value of this variable is sensitive, so its value is
  masked by `*` characters when displayed.
- [`keyring_hashicorp_server_url`](keyring-system-variables.md#sysvar_keyring_hashicorp_server_url)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-server-url=value` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_server_url` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `https://127.0.0.1:8200` |

  The HashiCorp Vault server URL, for use by the
  `keyring_hashicorp` plugin. This variable
  is unavailable unless that plugin is installed. The value
  must begin with `https://`.
- [`keyring_hashicorp_store_path`](keyring-system-variables.md#sysvar_keyring_hashicorp_store_path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-hashicorp-store-path=value` |
  | Introduced | 8.0.18 |
  | System Variable | `keyring_hashicorp_store_path` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `empty string` |

  A store path within the HashiCorp Vault server that is
  writeable when appropriate AppRole credentials are provided
  by the `keyring_hashicorp` plugin. This
  variable is unavailable unless that plugin is installed. To
  specify the credentials, set the
  [`keyring_hashicorp_role_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_role_id)
  and
  [`keyring_hashicorp_secret_id`](keyring-system-variables.md#sysvar_keyring_hashicorp_secret_id)
  system variables (for example, as shown in
  [keyring\_hashicorp Configuration](keyring-hashicorp-plugin.md#keyring-hashicorp-plugin-configuration "keyring_hashicorp Configuration")).

  This variable is mandatory. If not specified,
  `keyring_hashicorp` initialization fails.
- [`keyring_oci_ca_certificate`](keyring-system-variables.md#sysvar_keyring_oci_ca_certificate)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-ca-certificate=file_name` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_ca_certificate` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |
  | Default Value | `empty string` |

  The path name of the CA certificate bundle file that the
  `keyring_oci` plugin uses for Oracle Cloud Infrastructure
  certificate verification. This variable is unavailable
  unless that plugin is installed.

  The file contains one or more certificates for peer
  verification. If no file is specified, the default CA bundle
  installed on the system is used. If the value is
  `disabled` (case-sensitive),
  `keyring_oci` performs no certificate
  verification.
- [`keyring_oci_compartment`](keyring-system-variables.md#sysvar_keyring_oci_compartment)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-compartment=ocid` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_compartment` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The OCID of the tenancy compartment that the
  `keyring_oci` plugin uses as the location
  of the MySQL keys. This variable is unavailable unless that
  plugin is installed.

  Prior to using `keyring_oci`, you must
  create a MySQL compartment or subcompartment if it does not
  exist. This compartment should contain no vault keys or
  vault secrets. It should not be used by systems other than
  MySQL Keyring.

  For information about managing compartments and obtaining
  the OCID, see
  [Managing
  Compartments](https://docs.cloud.oracle.com/en-us/iaas/Content/Identity/Tasks/managingcompartments.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_encryption_endpoint`](keyring-system-variables.md#sysvar_keyring_oci_encryption_endpoint)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-encryption-endpoint=value` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_encryption_endpoint` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The endpoint of the Oracle Cloud Infrastructure encryption server that the
  `keyring_oci` plugin uses for generating
  ciphertext for new keys. This variable is unavailable unless
  that plugin is installed.

  The encryption endpoint is vault specific and Oracle Cloud Infrastructure assigns
  it at vault-creation time. To obtain the endpoint OCID, view
  the configuration details for your
  `keyring_oci` vault, using the instructions
  at
  [Managing
  Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_key_file`](keyring-system-variables.md#sysvar_keyring_oci_key_file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-key-file=file_name` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_key_file` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The path name of the file containing the RSA private key
  that the `keyring_oci` plugin uses for
  Oracle Cloud Infrastructure authentication. This variable is unavailable unless
  that plugin is installed.

  You must also upload the corresponding RSA public key using
  the Console. The Console displays the key fingerprint value,
  which you can use to set the
  [`keyring_oci_key_fingerprint`](keyring-system-variables.md#sysvar_keyring_oci_key_fingerprint)
  system variable.

  For information about generating and uploading API keys, see
  [Required
  Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_key_fingerprint`](keyring-system-variables.md#sysvar_keyring_oci_key_fingerprint)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-key-fingerprint=value` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_key_fingerprint` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The fingerprint of the RSA private key that the
  `keyring_oci` plugin uses for Oracle Cloud Infrastructure
  authentication. This variable is unavailable unless that
  plugin is installed.

  To obtain the key fingerprint while creating the API keys,
  execute this command:

  ```terminal
  openssl rsa -pubout -outform DER -in ~/.oci/oci_api_key.pem | openssl md5 -c
  ```

  Alternatively, obtain the fingerprint from the Console,
  which automatically displays the fingerprint when you upload
  the RSA public key.

  For information about obtaining key fingerprints, see
  [Required
  Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_management_endpoint`](keyring-system-variables.md#sysvar_keyring_oci_management_endpoint)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-management-endpoint=value` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_management_endpoint` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The endpoint of the Oracle Cloud Infrastructure key management server that the
  `keyring_oci` plugin uses for listing
  existing keys. This variable is unavailable unless that
  plugin is installed.

  The key management endpoint is vault specific and Oracle Cloud Infrastructure
  assigns it at vault-creation time. To obtain the endpoint
  OCID, view the configuration details for your
  `keyring_oci` vault, using the instructions
  at
  [Managing
  Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_master_key`](keyring-system-variables.md#sysvar_keyring_oci_master_key)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-master-key=ocid` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_master_key` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The OCID of the Oracle Cloud Infrastructure master encryption key that the
  `keyring_oci` plugin uses for encryption of
  secrets. This variable is unavailable unless that plugin is
  installed.

  Prior to using `keyring_oci`, you must
  create a cryptographic key for the Oracle Cloud Infrastructure compartment if it
  does not exist. Provide a MySQL-specific name for the
  generated key, and do not use it for other purposes.

  For information about key creation, see
  [Managing
  Keys](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingkeys.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_secrets_endpoint`](keyring-system-variables.md#sysvar_keyring_oci_secrets_endpoint)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-secrets-endpoint=value` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_secrets_endpoint` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The endpoint of the Oracle Cloud Infrastructure secrets server that the
  `keyring_oci` plugin uses for listing,
  creating, and retiring secrets. This variable is unavailable
  unless that plugin is installed.

  The secrets endpoint is vault specific and Oracle Cloud Infrastructure assigns it
  at vault-creation time. To obtain the endpoint OCID, view
  the configuration details for your
  `keyring_oci` vault, using the instructions
  at
  [Managing
  Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_tenancy`](keyring-system-variables.md#sysvar_keyring_oci_tenancy)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-tenancy=ocid` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_tenancy` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The OCID of the Oracle Cloud Infrastructure tenancy that the
  `keyring_oci` plugin uses as the location
  of the MySQL compartment. This variable is unavailable
  unless that plugin is installed.

  Prior to using `keyring_oci`, you must
  create a tenancy if it does not exist. To obtain the tenancy
  OCID from the Console, use the instructions at
  [Required
  Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_user`](keyring-system-variables.md#sysvar_keyring_oci_user)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-user=ocid` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_user` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The OCID of the Oracle Cloud Infrastructure user that the
  `keyring_oci` plugin uses for cloud
  connections. This variable is unavailable unless that plugin
  is installed.

  Prior to using `keyring_oci`, this user
  must exist and be granted access to use the configured Oracle Cloud Infrastructure
  tenancy, compartment, and vault resources.

  To obtain the user OCID from the Console, use the
  instructions at
  [Required
  Keys and OCIDs](https://docs.cloud.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_vaults_endpoint`](keyring-system-variables.md#sysvar_keyring_oci_vaults_endpoint)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-vaults-endpoint=value` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_vaults_endpoint` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The endpoint of the Oracle Cloud Infrastructure vaults server that the
  `keyring_oci` plugin uses for obtaining the
  value of secrets. This variable is unavailable unless that
  plugin is installed.

  The vaults endpoint is vault specific and Oracle Cloud Infrastructure assigns it
  at vault-creation time. To obtain the endpoint OCID, view
  the configuration details for your
  `keyring_oci` vault, using the instructions
  at
  [Managing
  Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_oci_virtual_vault`](keyring-system-variables.md#sysvar_keyring_oci_virtual_vault)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-oci-virtual-vault=ocid` |
  | Introduced | 8.0.22 |
  | Deprecated | 8.0.31 |
  | System Variable | `keyring_oci_virtual_vault` |
  | Scope | Global |
  | Dynamic | No |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | String |

  The OCID of the Oracle Cloud Infrastructure Vault that the
  `keyring_oci` plugin uses for encryption
  operations. This variable is unavailable unless that plugin
  is installed.

  Prior to using `keyring_oci`, you must
  create a new vault in the MySQL compartment if it does not
  exist. (Alternatively, you can reuse an existing vault that
  is in a parent compartment of the MySQL compartment.)
  Compartment users can see and use only the keys in their
  respective compartments.

  For information about creating a vault and obtaining the
  vault OCID, see
  [Managing
  Vaults](https://docs.cloud.oracle.com/en-us/iaas/Content/KeyManagement/Tasks/managingvaults.htm).

  This variable is mandatory. If not specified,
  `keyring_oci` initialization fails.
- [`keyring_okv_conf_dir`](keyring-system-variables.md#sysvar_keyring_okv_conf_dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keyring-okv-conf-dir=dir_name` |
  | System Variable | `keyring_okv_conf_dir` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Directory name |
  | Default Value | `empty string` |

  The path name of the directory that stores configuration
  information used by the `keyring_okv`
  plugin. This variable is unavailable unless that plugin is
  installed. The location should be a directory considered for
  use only by the `keyring_okv` plugin. For
  example, do not locate the directory under the data
  directory.

  The default
  [`keyring_okv_conf_dir`](keyring-system-variables.md#sysvar_keyring_okv_conf_dir) value
  is empty. For the `keyring_okv` plugin to
  be able to access Oracle Key Vault, the value must be set to
  a directory that contains Oracle Key Vault configuration and
  SSL materials. For instructions on setting up this
  directory, see [Section 8.4.4.8, “Using the keyring\_okv KMIP Plugin”](keyring-okv-plugin.md "8.4.4.8 Using the keyring_okv KMIP Plugin").

  The directory should have a restrictive mode and be
  accessible only to the account used to run the MySQL server.
  For example, on Unix and Unix-like systems, to use the
  `/usr/local/mysql/mysql-keyring-okv`
  directory, the following commands (executed as
  `root`) create the directory and set its
  mode and ownership:

  ```terminal
  cd /usr/local/mysql
  mkdir mysql-keyring-okv
  chmod 750 mysql-keyring-okv
  chown mysql mysql-keyring-okv
  chgrp mysql mysql-keyring-okv
  ```

  If the value assigned to
  [`keyring_okv_conf_dir`](keyring-system-variables.md#sysvar_keyring_okv_conf_dir)
  specifies a directory that does not exist, or that does not
  contain configuration information that enables a connection
  to Oracle Key Vault to be established,
  `keyring_okv` writes an error message to
  the error log. If an attempted runtime assignment to
  [`keyring_okv_conf_dir`](keyring-system-variables.md#sysvar_keyring_okv_conf_dir)
  results in an error, the variable value and keyring
  operation remain unchanged.
- [`keyring_operations`](keyring-system-variables.md#sysvar_keyring_operations)

  |  |  |
  | --- | --- |
  | System Variable | `keyring_operations` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `ON` |

  Whether keyring operations are enabled. This variable is
  used during key migration operations. See
  [Section 8.4.4.14, “Migrating Keys Between Keyring Keystores”](keyring-key-migration.md "8.4.4.14 Migrating Keys Between Keyring Keystores"). The privileges
  required to modify this variable are
  [`ENCRYPTION_KEY_ADMIN`](privileges-provided.md#priv_encryption-key-admin) in
  addition to either
  [`SYSTEM_VARIABLES_ADMIN`](privileges-provided.md#priv_system-variables-admin) or the
  deprecated [`SUPER`](privileges-provided.md#priv_super) privilege.
