#### 6.6.4.2 myisamchk Check Options

[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") supports the following options for
table checking operations:

- [`--check`](myisamchk-check-options.md#option_myisamchk_check),
  `-c`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--check` |

  Check the table for errors. This is the default operation if
  you specify no option that selects an operation type
  explicitly.
- [`--check-only-changed`](myisamchk-check-options.md#option_myisamchk_check-only-changed),
  `-C`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--check-only-changed` |

  Check only tables that have changed since the last check.
- [`--extend-check`](myisamchk-check-options.md#option_myisamchk_extend-check),
  `-e`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--extend-check` |

  Check the table very thoroughly. This is quite slow if the
  table has many indexes. This option should only be used in
  extreme cases. Normally, [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") or
  [**myisamchk --medium-check**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") should be able
  to determine whether there are any errors in the table.

  If you are using
  [`--extend-check`](myisamchk-check-options.md#option_myisamchk_extend-check) and have
  plenty of memory, setting the
  `key_buffer_size` variable to a large value
  helps the repair operation run faster.

  See also the description of this option under table repair
  options.

  For a description of the output format, see
  [Section 6.6.4.5, “Obtaining Table Information with myisamchk”](myisamchk-table-info.md "6.6.4.5 Obtaining Table Information with myisamchk").
- [`--fast`](myisamchk-check-options.md#option_myisamchk_fast),
  `-F`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--fast` |

  Check only tables that haven't been closed properly.
- [`--force`](myisamchk-check-options.md#option_myisamchk_force),
  `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force` |

  Do a repair operation automatically if
  [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") finds any errors in the table.
  The repair type is the same as that specified with the
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover) or
  `-r` option.
- [`--information`](myisamchk-check-options.md#option_myisamchk_information),
  `-i`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--information` |

  Print informational statistics about the table that is
  checked.
- [`--medium-check`](myisamchk-check-options.md#option_myisamchk_medium-check),
  `-m`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--medium-check` |

  Do a check that is faster than an
  [`--extend-check`](myisamchk-check-options.md#option_myisamchk_extend-check) operation.
  This finds only 99.99% of all errors, which should be good
  enough in most cases.
- [`--read-only`](myisamchk-check-options.md#option_myisamchk_read-only),
  `-T`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--read-only` |

  Do not mark the table as checked. This is useful if you use
  [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to check a table that is in use
  by some other application that does not use locking, such as
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") when run with external locking
  disabled.
- [`--update-state`](myisamchk-check-options.md#option_myisamchk_update-state),
  `-U`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--update-state` |

  Store information in the `.MYI` file to
  indicate when the table was checked and whether the table
  crashed. This should be used to get full benefit of the
  [`--check-only-changed`](myisamchk-check-options.md#option_myisamchk_check-only-changed)
  option, but you shouldn't use this option if the
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") server is using the table and you
  are running it with external locking disabled.
