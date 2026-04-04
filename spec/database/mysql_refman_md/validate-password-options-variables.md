#### 8.4.3.2 Password Validation Options and Variables

This section describes the system and status variables that
`validate_password` provides to enable its
operation to be configured and monitored.

- [Password Validation Component System Variables](validate-password-options-variables.md#validate-password-system-variables "Password Validation Component System Variables")
- [Password Validation Component Status Variables](validate-password-options-variables.md#validate-password-status-variables "Password Validation Component Status Variables")
- [Password Validation Plugin Options](validate-password-options-variables.md#validate-password-plugin-options "Password Validation Plugin Options")
- [Password Validation Plugin System Variables](validate-password-options-variables.md#validate-password-plugin-system-variables "Password Validation Plugin System Variables")
- [Password Validation Plugin Status Variables](validate-password-options-variables.md#validate-password-plugin-status-variables "Password Validation Plugin Status Variables")

##### Password Validation Component System Variables

If the `validate_password` component is
enabled, it exposes several system variables that enable
configuration of password checking:

```sql
mysql> SHOW VARIABLES LIKE 'validate_password.%';
+-------------------------------------------------+--------+
| Variable_name                                   | Value  |
+-------------------------------------------------+--------+
| validate_password.changed_characters_percentage | 0      |
| validate_password.check_user_name               | ON     |
| validate_password.dictionary_file               |        |
| validate_password.length                        | 8      |
| validate_password.mixed_case_count              | 1      |
| validate_password.number_count                  | 1      |
| validate_password.policy                        | MEDIUM |
| validate_password.special_char_count            | 1      |
+-------------------------------------------------+--------+
```

To change how passwords are checked, you can set these system
variables at server startup or at runtime. The following list
describes the meaning of each variable.

- [`validate_password.changed_characters_percentage`](validate-password-options-variables.md#sysvar_validate_password.changed_characters_percentage)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.changed-characters-percentage[=value]` |
  | Introduced | 8.0.34 |
  | System Variable | `validate_password.changed_characters_percentage` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `0` |
  | Minimum Value | `0` |
  | Maximum Value | `100` |

  Indicates the minimum number of characters, as a
  percentage of all characters, in a password that a user
  must change before `validate_password`
  accepts a new password for the user's own account.
  This applies only when changing an existing password, and
  has no effect when setting a user account's initial
  password.

  This variable is not available unless
  `validate_password` is installed.

  By default,
  `validate_password.changed_characters_percentage`
  permits all of the characters from the current password to
  be reused in the new password. The range of valid
  percentages is 0 to 100. If set to 100 percent, all of the
  characters from the current password are rejected,
  regardless of the casing. Characters
  '`abc`' and '`ABC`' are
  considered to be the same characters. If
  `validate_password` rejects the new
  password, it reports an error indicating the minimum
  number of characters that must differ.

  If the [`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement") statement
  does not provide the existing password in a
  [`REPLACE`](replace.md "15.2.12 REPLACE Statement") clause, this
  variable is not enforced. Whether the
  [`REPLACE`](replace.md "15.2.12 REPLACE Statement") clause is required
  is subject to the password verification policy as it
  applies to a given account. For an overview of the policy,
  see [Password Verification-Required Policy](password-management.md#password-reverification-policy "Password Verification-Required Policy").
- [`validate_password.check_user_name`](validate-password-options-variables.md#sysvar_validate_password.check_user_name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.check-user-name[={OFF|ON}]` |
  | System Variable | `validate_password.check_user_name` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `ON` |

  Whether `validate_password` compares
  passwords to the user name part of the effective user
  account for the current session and rejects them if they
  match. This variable is unavailable unless
  `validate_password` is installed.

  By default,
  [`validate_password.check_user_name`](validate-password-options-variables.md#sysvar_validate_password.check_user_name)
  is enabled. This variable controls user name matching
  independent of the value of
  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy).

  When
  [`validate_password.check_user_name`](validate-password-options-variables.md#sysvar_validate_password.check_user_name)
  is enabled, it has these effects:

  - Checking occurs in all contexts for which
    `validate_password` is invoked, which
    includes use of statements such as
    [`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement") or
    [`SET PASSWORD`](set-password.md "15.7.1.10 SET PASSWORD Statement") to change
    the current user's password, and invocation of
    functions such as
    [`VALIDATE_PASSWORD_STRENGTH()`](encryption-functions.md#function_validate-password-strength).
  - The user names used for comparison are taken from the
    values of the [`USER()`](information-functions.md#function_user)
    and [`CURRENT_USER()`](information-functions.md#function_current-user)
    functions for the current session. An implication is
    that a user who has sufficient privileges to set
    another user's password can set the password to
    that user's name, and cannot set that user'
    password to the name of the user executing the
    statement. For example,
    `'root'@'localhost'` can set the
    password for `'jeffrey'@'localhost'`
    to `'jeffrey'`, but cannot set the
    password to `'root`.
  - Only the user name part of the
    [`USER()`](information-functions.md#function_user) and
    [`CURRENT_USER()`](information-functions.md#function_current-user) function
    values is used, not the host name part. If a user name
    is empty, no comparison occurs.
  - If a password is the same as the user name or its
    reverse, a match occurs and the password is rejected.
  - User-name matching is case-sensitive. The password and
    user name values are compared as binary strings on a
    byte-by-byte basis.
  - If a password matches the user name,
    [`VALIDATE_PASSWORD_STRENGTH()`](encryption-functions.md#function_validate-password-strength)
    returns 0 regardless of how other
    `validate_password` system variables
    are set.
- [`validate_password.dictionary_file`](validate-password-options-variables.md#sysvar_validate_password.dictionary_file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.dictionary-file=file_name` |
  | System Variable | `validate_password.dictionary_file` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |

  The path name of the dictionary file that
  `validate_password` uses for checking
  passwords. This variable is unavailable unless
  `validate_password` is installed.

  By default, this variable has an empty value and
  dictionary checks are not performed. For dictionary checks
  to occur, the variable value must be nonempty. If the file
  is named as a relative path, it is interpreted relative to
  the server data directory. File contents should be
  lowercase, one word per line. Contents are treated as
  having a character set of `utf8mb3`. The
  maximum permitted file size is 1MB.

  For the dictionary file to be used during password
  checking, the password policy must be set to 2
  (`STRONG`); see the description of the
  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)
  system variable. Assuming that is true, each substring of
  the password of length 4 up to 100 is compared to the
  words in the dictionary file. Any match causes the
  password to be rejected. Comparisons are not
  case-sensitive.

  For
  [`VALIDATE_PASSWORD_STRENGTH()`](encryption-functions.md#function_validate-password-strength),
  the password is checked against all policies, including
  `STRONG`, so the strength assessment
  includes the dictionary check regardless of the
  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)
  value.

  [`validate_password.dictionary_file`](validate-password-options-variables.md#sysvar_validate_password.dictionary_file)
  can be set at runtime and assigning a value causes the
  named file to be read without a server restart.
- [`validate_password.length`](validate-password-options-variables.md#sysvar_validate_password.length)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.length=#` |
  | System Variable | `validate_password.length` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `8` |
  | Minimum Value | `0` |

  The minimum number of characters that
  `validate_password` requires passwords to
  have. This variable is unavailable unless
  `validate_password` is installed.

  The
  [`validate_password.length`](validate-password-options-variables.md#sysvar_validate_password.length)
  minimum value is a function of several other related
  system variables. The value cannot be set less than the
  value of this expression:

  ```none
  validate_password.number_count
  + validate_password.special_char_count
  + (2 * validate_password.mixed_case_count)
  ```

  If `validate_password` adjusts the value
  of
  [`validate_password.length`](validate-password-options-variables.md#sysvar_validate_password.length)
  due to the preceding constraint, it writes a message to
  the error log.
- [`validate_password.mixed_case_count`](validate-password-options-variables.md#sysvar_validate_password.mixed_case_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.mixed-case-count=#` |
  | System Variable | `validate_password.mixed_case_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  The minimum number of lowercase and uppercase characters
  that `validate_password` requires
  passwords to have if the password policy is
  `MEDIUM` or stronger. This variable is
  unavailable unless `validate_password` is
  installed.

  For a given
  [`validate_password.mixed_case_count`](validate-password-options-variables.md#sysvar_validate_password.mixed_case_count)
  value, the password must have that many lowercase
  characters, and that many uppercase characters.
- [`validate_password.number_count`](validate-password-options-variables.md#sysvar_validate_password.number_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.number-count=#` |
  | System Variable | `validate_password.number_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  The minimum number of numeric (digit) characters that
  `validate_password` requires passwords to
  have if the password policy is `MEDIUM`
  or stronger. This variable is unavailable unless
  `validate_password` is installed.
- [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.policy=value` |
  | System Variable | `validate_password.policy` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Enumeration |
  | Default Value | `1` |
  | Valid Values | `0`  `1`  `2` |

  The password policy enforced by
  `validate_password`. This variable is
  unavailable unless `validate_password` is
  installed.

  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)
  affects how `validate_password` uses its
  other policy-setting system variables, except for checking
  passwords against user names, which is controlled
  independently by
  [`validate_password.check_user_name`](validate-password-options-variables.md#sysvar_validate_password.check_user_name).

  The
  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)
  value can be specified using numeric values 0, 1, 2, or
  the corresponding symbolic values `LOW`,
  `MEDIUM`, `STRONG`. The
  following table describes the tests performed for each
  policy. For the length test, the required length is the
  value of the
  [`validate_password.length`](validate-password-options-variables.md#sysvar_validate_password.length)
  system variable. Similarly, the required values for the
  other tests are given by other
  `validate_password.xxx`
  variables.

  | Policy | Tests Performed |
  | --- | --- |
  | `0` or `LOW` | Length |
  | `1` or `MEDIUM` | Length; numeric, lowercase/uppercase, and special characters |
  | `2` or `STRONG` | Length; numeric, lowercase/uppercase, and special characters; dictionary file |
- [`validate_password.special_char_count`](validate-password-options-variables.md#sysvar_validate_password.special_char_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password.special-char-count=#` |
  | System Variable | `validate_password.special_char_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  The minimum number of nonalphanumeric characters that
  `validate_password` requires passwords to
  have if the password policy is `MEDIUM`
  or stronger. This variable is unavailable unless
  `validate_password` is installed.

##### Password Validation Component Status Variables

If the `validate_password` component is
enabled, it exposes status variables that provide operational
information:

```sql
mysql> SHOW STATUS LIKE 'validate_password.%';
+-----------------------------------------------+---------------------+
| Variable_name                                 | Value               |
+-----------------------------------------------+---------------------+
| validate_password.dictionary_file_last_parsed | 2019-10-03 08:33:49 |
| validate_password.dictionary_file_words_count | 1902                |
+-----------------------------------------------+---------------------+
```

The following list describes the meaning of each status
variable.

- [`validate_password.dictionary_file_last_parsed`](validate-password-options-variables.md#statvar_validate_password.dictionary_file_last_parsed)

  When the dictionary file was last parsed. This variable is
  unavailable unless `validate_password` is
  installed.
- [`validate_password.dictionary_file_words_count`](validate-password-options-variables.md#statvar_validate_password.dictionary_file_words_count)

  The number of words read from the dictionary file. This
  variable is unavailable unless
  `validate_password` is installed.

##### Password Validation Plugin Options

Note

In MySQL 8.0, the
`validate_password` plugin was
reimplemented as the `validate_password`
component. The `validate_password` plugin
is deprecated; expect it to be removed in a future version
of MySQL. Consequently, its options are also deprecated, and
you should expect them to be removed as well. MySQL
installations that use the plugin should make the transition
to using the component instead. See
[Section 8.4.3.3, “Transitioning to the Password Validation Component”](validate-password-transitioning.md "8.4.3.3 Transitioning to the Password Validation Component").

To control activation of the
`validate_password` plugin, use this option:

- [`--validate-password[=value]`](validate-password-options-variables.md#option_mysqld_validate-password)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password[=value]` |
  | Type | Enumeration |
  | Default Value | `ON` |
  | Valid Values | `ON`  `OFF`  `FORCE`  `FORCE_PLUS_PERMANENT` |

  This option controls how the server loads the deprecated
  `validate_password` plugin at startup.
  The value should be one of those available for
  plugin-loading options, as described in
  [Section 7.6.1, “Installing and Uninstalling Plugins”](plugin-loading.md "7.6.1 Installing and Uninstalling Plugins"). For example,
  [`--validate-password=FORCE_PLUS_PERMANENT`](validate-password-options-variables.md#option_mysqld_validate-password)
  tells the server to load the plugin at startup and
  prevents it from being removed while the server is
  running.

  This option is available only if the
  `validate_password` plugin has been
  previously registered with [`INSTALL
  PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement") or is loaded with
  [`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add). See
  [Section 8.4.3.1, “Password Validation Component Installation and Uninstallation”](validate-password-installation.md "8.4.3.1 Password Validation Component Installation and Uninstallation").

##### Password Validation Plugin System Variables

Note

In MySQL 8.0, the
`validate_password` plugin was
reimplemented as the `validate_password`
component. The `validate_password` plugin
is deprecated; expect it to be removed in a future version
of MySQL. Consequently, its system variables are also
deprecated and you should expect them to be removed as well.
Use the corresponding system variables of the
`validate_password` component instead; see
[Password Validation Component System Variables](validate-password-options-variables.md#validate-password-system-variables "Password Validation Component System Variables"). MySQL
installations that use the plugin should make the transition
to using the component instead. See
[Section 8.4.3.3, “Transitioning to the Password Validation Component”](validate-password-transitioning.md "8.4.3.3 Transitioning to the Password Validation Component").

- [`validate_password_check_user_name`](validate-password-options-variables.md#sysvar_validate_password_check_user_name)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-check-user-name[={OFF|ON}]` |
  | System Variable | `validate_password_check_user_name` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Boolean |
  | Default Value | `ON` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.check_user_name`](validate-password-options-variables.md#sysvar_validate_password.check_user_name)
  system variable of the
  `validate_password` component instead.
- [`validate_password_dictionary_file`](validate-password-options-variables.md#sysvar_validate_password_dictionary_file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-dictionary-file=file_name` |
  | System Variable | `validate_password_dictionary_file` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | File name |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.dictionary_file`](validate-password-options-variables.md#sysvar_validate_password.dictionary_file)
  system variable of the
  `validate_password` component instead.
- [`validate_password_length`](validate-password-options-variables.md#sysvar_validate_password_length)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-length=#` |
  | System Variable | `validate_password_length` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `8` |
  | Minimum Value | `0` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.length`](validate-password-options-variables.md#sysvar_validate_password.length)
  system variable of the
  `validate_password` component instead.
- [`validate_password_mixed_case_count`](validate-password-options-variables.md#sysvar_validate_password_mixed_case_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-mixed-case-count=#` |
  | System Variable | `validate_password_mixed_case_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.mixed_case_count`](validate-password-options-variables.md#sysvar_validate_password.mixed_case_count)
  system variable of the
  `validate_password` component instead.
- [`validate_password_number_count`](validate-password-options-variables.md#sysvar_validate_password_number_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-number-count=#` |
  | System Variable | `validate_password_number_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.number_count`](validate-password-options-variables.md#sysvar_validate_password.number_count)
  system variable of the
  `validate_password` component instead.
- [`validate_password_policy`](validate-password-options-variables.md#sysvar_validate_password_policy)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-policy=value` |
  | System Variable | `validate_password_policy` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Enumeration |
  | Default Value | `1` |
  | Valid Values | `0`  `1`  `2` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.policy`](validate-password-options-variables.md#sysvar_validate_password.policy)
  system variable of the
  `validate_password` component instead.
- [`validate_password_special_char_count`](validate-password-options-variables.md#sysvar_validate_password_special_char_count)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--validate-password-special-char-count=#` |
  | System Variable | `validate_password_special_char_count` |
  | Scope | Global |
  | Dynamic | Yes |
  | [`SET_VAR`](optimizer-hints.md#optimizer-hints-set-var "Variable-Setting Hint Syntax") Hint Applies | No |
  | Type | Integer |
  | Default Value | `1` |
  | Minimum Value | `0` |

  This `validate_password` plugin system
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.special_char_count`](validate-password-options-variables.md#sysvar_validate_password.special_char_count)
  system variable of the
  `validate_password` component instead.

##### Password Validation Plugin Status Variables

Note

In MySQL 8.0, the
`validate_password` plugin was
reimplemented as the `validate_password`
component. The `validate_password` plugin
is deprecated; expect it to be removed in a future version
of MySQL. Consequently, its status variables are also
deprecated; expect it to be removed. Use the corresponding
status variables of the `validate_password`
component; see
[Password Validation Component Status Variables](validate-password-options-variables.md#validate-password-status-variables "Password Validation Component Status Variables"). MySQL
installations that use the plugin should make the transition
to using the component instead. See
[Section 8.4.3.3, “Transitioning to the Password Validation Component”](validate-password-transitioning.md "8.4.3.3 Transitioning to the Password Validation Component").

- [`validate_password_dictionary_file_last_parsed`](validate-password-options-variables.md#statvar_validate_password_dictionary_file_last_parsed)

  This `validate_password` plugin status
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.dictionary_file_last_parsed`](validate-password-options-variables.md#statvar_validate_password.dictionary_file_last_parsed)
  status variable of the
  `validate_password` component instead.
- [`validate_password_dictionary_file_words_count`](validate-password-options-variables.md#statvar_validate_password_dictionary_file_words_count)

  This `validate_password` plugin status
  variable is deprecated; expect it to be removed in a
  future version of MySQL. Use the corresponding
  [`validate_password.dictionary_file_words_count`](validate-password-options-variables.md#statvar_validate_password.dictionary_file_words_count)
  status variable of the
  `validate_password` component instead.
