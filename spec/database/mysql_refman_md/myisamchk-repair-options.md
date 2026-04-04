#### 6.6.4.3 myisamchk Repair Options

[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") supports the following options for
table repair operations (operations performed when an option
such as [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover) or
[`--safe-recover`](myisamchk-repair-options.md#option_myisamchk_safe-recover) is given):

- [`--backup`](myisamchk-repair-options.md#option_myisamchk_backup),
  `-B`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--backup` |

  Make a backup of the `.MYD` file as
  `file_name-time.BAK`
- [`--character-sets-dir=dir_name`](myisamchk-repair-options.md#option_myisamchk_character-sets-dir)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--character-sets-dir=path` |
  | Type | String |
  | Default Value | `[none]` |

  The directory where character sets are installed. See
  [Section 12.15, “Character Set Configuration”](charset-configuration.md "12.15 Character Set Configuration").
- [`--correct-checksum`](myisamchk-repair-options.md#option_myisamchk_correct-checksum)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--correct-checksum` |

  Correct the checksum information for the table.
- [`--data-file-length=len`](myisamchk-repair-options.md#option_myisamchk_data-file-length),
  `-D len`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--data-file-length=len` |
  | Type | Numeric |

  The maximum length of the data file (when re-creating data
  file when it is “full”).
- [`--extend-check`](myisamchk-check-options.md#option_myisamchk_extend-check),
  `-e`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--extend-check` |

  Do a repair that tries to recover every possible row from
  the data file. Normally, this also finds a lot of garbage
  rows. Do not use this option unless you are desperate.

  See also the description of this option under table checking
  options.

  For a description of the output format, see
  [Section 6.6.4.5, “Obtaining Table Information with myisamchk”](myisamchk-table-info.md "6.6.4.5 Obtaining Table Information with myisamchk").
- [`--force`](myisamchk-check-options.md#option_myisamchk_force),
  `-f`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--force` |

  Overwrite old intermediate files (files with names like
  `tbl_name.TMD`)
  instead of aborting.
- [`--keys-used=val`](myisamchk-repair-options.md#option_myisamchk_keys-used),
  `-k val`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--keys-used=val` |
  | Type | Numeric |

  For [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), the option value is a bit
  value that indicates which indexes to update. Each binary
  bit of the option value corresponds to a table index, where
  the first index is bit 0. An option value of 0 disables
  updates to all indexes, which can be used to get faster
  inserts. Deactivated indexes can be reactivated by using
  [**myisamchk -r**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility").
- [`--max-record-length=len`](myisamchk-repair-options.md#option_myisamchk_max-record-length)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--max-record-length=len` |
  | Type | Numeric |

  Skip rows larger than the given length if
  [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") cannot allocate memory to hold
  them.
- [`--parallel-recover`](myisamchk-repair-options.md#option_myisamchk_parallel-recover),
  `-p`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--parallel-recover` |

  Note

  This option is deprecated in MySQL 8.0.28 and removed in
  MySQL 8.0.30.

  Use the same technique as `-r` and
  `-n`, but create all the keys in parallel,
  using different threads. *This is beta-quality
  code. Use at your own risk!*
- [`--quick`](myisamchk-repair-options.md#option_myisamchk_quick),
  `-q`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--quick` |

  Achieve a faster repair by modifying only the index file,
  not the data file. You can specify this option twice to
  force [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to modify the original
  data file in case of duplicate keys.
- [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover),
  `-r`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--recover` |

  Do a repair that can fix almost any problem except unique
  keys that are not unique (which is an extremely unlikely
  error with `MyISAM` tables). If you want to
  recover a table, this is the option to try first. You should
  try [`--safe-recover`](myisamchk-repair-options.md#option_myisamchk_safe-recover) only if
  [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") reports that the table cannot
  be recovered using
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover). (In the
  unlikely case that
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover) fails, the data
  file remains intact.)

  If you have lots of memory, you should increase the value of
  `myisam_sort_buffer_size`.
- [`--safe-recover`](myisamchk-repair-options.md#option_myisamchk_safe-recover),
  `-o`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--safe-recover` |

  Do a repair using an old recovery method that reads through
  all rows in order and updates all index trees based on the
  rows found. This is an order of magnitude slower than
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover), but can handle
  a couple of very unlikely cases that
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover) cannot. This
  recovery method also uses much less disk space than
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover). Normally, you
  should repair first using
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover), and then with
  [`--safe-recover`](myisamchk-repair-options.md#option_myisamchk_safe-recover) only if
  [`--recover`](myisamchk-repair-options.md#option_myisamchk_recover) fails.

  If you have lots of memory, you should increase the value of
  `key_buffer_size`.
- [`--set-collation=name`](myisamchk-repair-options.md#option_myisamchk_set-collation)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--set-collation=name` |
  | Type | String |

  Specify the collation to use for sorting table indexes. The
  character set name is implied by the first part of the
  collation name.
- [`--sort-recover`](myisamchk-repair-options.md#option_myisamchk_sort-recover),
  `-n`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--sort-recover` |

  Force [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to use sorting to resolve
  the keys even if the temporary files would be very large.
- [`--tmpdir=dir_name`](myisamchk-repair-options.md#option_myisamchk_tmpdir),
  `-t dir_name`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--tmpdir=dir_name` |
  | Type | Directory name |

  The path of the directory to be used for storing temporary
  files. If this is not set, [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") uses
  the value of the `TMPDIR` environment
  variable. [`--tmpdir`](myisamchk-repair-options.md#option_myisamchk_tmpdir) can be
  set to a list of directory paths that are used successively
  in round-robin fashion for creating temporary files. The
  separator character between directory names is the colon
  (`:`) on Unix and the semicolon
  (`;`) on Windows.
- [`--unpack`](myisamchk-repair-options.md#option_myisamchk_unpack),
  `-u`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--unpack` |

  Unpack a table that was packed with
  [**myisampack**](myisampack.md "6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables").
