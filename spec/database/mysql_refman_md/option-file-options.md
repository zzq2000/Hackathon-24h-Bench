#### 6.2.2.3 Command-Line Options that Affect Option-File Handling

Most MySQL programs that support option files handle the
following options. Because these options affect option-file
handling, they must be given on the command line and not in an
option file. To work properly, each of these options must be
given before other options, with these exceptions:

- [`--print-defaults`](option-file-options.md#option_general_print-defaults) may be used
  immediately after
  [`--defaults-file`](option-file-options.md#option_general_defaults-file),
  [`--defaults-extra-file`](option-file-options.md#option_general_defaults-extra-file), or
  [`--login-path`](option-file-options.md#option_general_login-path).
- On Windows, if the server is started with the
  [`--defaults-file`](option-file-options.md#option_general_defaults-file) and
  [`--install`](server-options.md#option_mysqld_install) options,
  [`--install`](server-options.md#option_mysqld_install) must be first. See
  [Section 2.3.4.8, “Starting MySQL as a Windows Service”](windows-start-service.md "2.3.4.8 Starting MySQL as a Windows Service").

When specifying file names as option values, avoid the use of
the `~` shell metacharacter because it might
not be interpreted as you expect.

**Table 6.3 Option File Option Summary**

| Option Name | Description |
| --- | --- |
| [--defaults-extra-file](option-file-options.md#option_general_defaults-extra-file) | Read named option file in addition to usual option files |
| [--defaults-file](option-file-options.md#option_general_defaults-file) | Read only named option file |
| [--defaults-group-suffix](option-file-options.md#option_general_defaults-group-suffix) | Option group suffix value |
| [--login-path](option-file-options.md#option_general_login-path) | Read login path options from .mylogin.cnf |
| [--no-defaults](option-file-options.md#option_general_no-defaults) | Read no option files |

- [`--defaults-extra-file=file_name`](option-file-options.md#option_general_defaults-extra-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-extra-file=filename` |
  | Type | File name |
  | Default Value | `[none]` |

  Read this option file after the global option file but (on
  Unix) before the user option file and (on all platforms)
  before the login path file. (For information about the order
  in which option files are used, see
  [Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").) If the file does not exist
  or is otherwise inaccessible, an error occurs. If
  *`file_name`* is not an absolute path
  name, it is interpreted relative to the current directory.

  See the introduction to this section regarding constraints
  on the position in which this option may be specified.
- [`--defaults-file=file_name`](option-file-options.md#option_general_defaults-file)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-file=filename` |
  | Type | File name |
  | Default Value | `[none]` |

  Read only the given option file. If the file does not exist
  or is otherwise inaccessible, an error occurs.
  *`file_name`* is interpreted relative
  to the current directory if given as a relative path name
  rather than a full path name.

  Exceptions: Even with
  [`--defaults-file`](option-file-options.md#option_general_defaults-file),
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") reads
  `mysqld-auto.cnf` and client programs
  read `.mylogin.cnf`.

  See the introduction to this section regarding constraints
  on the position in which this option may be specified.
- [`--defaults-group-suffix=str`](option-file-options.md#option_general_defaults-group-suffix)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--defaults-group-suffix=string` |
  | Type | String |
  | Default Value | `[none]` |

  Read not only the usual option groups, but also groups with
  the usual names and a suffix of
  *`str`*. For example, the
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client normally reads the
  `[client]` and `[mysql]`
  groups. If this option is given as
  [`--defaults-group-suffix=_other`](option-file-options.md#option_general_defaults-group-suffix),
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") also reads the
  `[client_other]` and
  `[mysql_other]` groups.
- [`--login-path=name`](option-file-options.md#option_general_login-path)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--login-path=name` |
  | Type | String |
  | Default Value | `[none]` |

  Read options from the named login path in the
  `.mylogin.cnf` login path file. A
  “login path” is an option group containing
  options that specify which MySQL server to connect to and
  which account to authenticate as. To create or modify a
  login path file, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").

  A client program reads the option group corresponding to the
  named login path, in addition to option groups that the
  program reads by default. Consider this command:

  ```terminal
  mysql --login-path=mypath
  ```

  By default, the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client reads the
  `[client]` and `[mysql]`
  option groups. So for the command shown,
  [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") reads `[client]`
  and `[mysql]` from other option files, and
  `[client]`, `[mysql]`, and
  `[mypath]` from the login path file.

  Client programs read the login path file even when the
  [`--no-defaults`](option-file-options.md#option_general_no-defaults) option is
  used.

  To specify an alternate login path file name, set the
  `MYSQL_TEST_LOGIN_FILE` environment
  variable.

  See the introduction to this section regarding constraints
  on the position in which this option may be specified.
- [`--no-defaults`](option-file-options.md#option_general_no-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--no-defaults` |
  | Type | Boolean |
  | Default Value | `false` |

  Do not read any option files. If program startup fails due
  to reading unknown options from an option file,
  [`--no-defaults`](option-file-options.md#option_general_no-defaults) can be used to
  prevent them from being read.

  The exception is that client programs read the
  `.mylogin.cnf` login path file, if it
  exists, even when
  [`--no-defaults`](option-file-options.md#option_general_no-defaults) is used. This
  permits passwords to be specified in a safer way than on the
  command line even if
  [`--no-defaults`](option-file-options.md#option_general_no-defaults) is present. To
  create `.mylogin.cnf`, use the
  [**mysql\_config\_editor**](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility") utility. See
  [Section 6.6.7, “mysql\_config\_editor — MySQL Configuration Utility”](mysql-config-editor.md "6.6.7 mysql_config_editor — MySQL Configuration Utility").
- [`--print-defaults`](option-file-options.md#option_general_print-defaults)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--print-defaults` |
  | Type | Boolean |
  | Default Value | `false` |

  Print the program name and all options that it gets from
  option files. Password values are masked.

  See the introduction to this section regarding constraints
  on the position in which this option may be specified.
