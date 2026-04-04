### 6.6.10 mysqldumpslow — Summarize Slow Query Log Files

The MySQL slow query log contains information about queries that
take a long time to execute (see
[Section 7.4.5, “The Slow Query Log”](slow-query-log.md "7.4.5 The Slow Query Log")).
[**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files") parses MySQL slow query log
files and summarizes their contents.

Normally, [**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files") groups queries that
are similar except for the particular values of number and
string data values. It “abstracts” these values to
`N` and `'S'` when displaying
summary output. To modify value abstracting behavior, use the
`-a` and `-n` options.

Invoke [**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files") like this:

```terminal
mysqldumpslow [options] [log_file ...]
```

Example output with no options given:

```terminal
Reading mysql slow query log from /usr/local/mysql/data/mysqld80-slow.log
Count: 1  Time=4.32s (4s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1

Count: 3  Time=2.53s (7s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t2 select * from t1 limit N

Count: 3  Time=2.13s (6s)  Lock=0.00s (0s)  Rows=0.0 (0), root[root]@localhost
 insert into t1 select * from t1
```

[**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files") supports the following options.

**Table 6.24 mysqldumpslow Options**

| Option Name | Description |
| --- | --- |
| [-a](mysqldumpslow.md#option_mysqldumpslow_abstract) | Do not abstract all numbers to N and strings to 'S' |
| [-n](mysqldumpslow.md#option_mysqldumpslow_abstract-numbers) | Abstract numbers with at least the specified digits |
| [--debug](mysqldumpslow.md#option_mysqldumpslow_debug) | Write debugging information |
| [-g](mysqldumpslow.md#option_mysqldumpslow_grep) | Only consider statements that match the pattern |
| [--help](mysqldumpslow.md#option_mysqldumpslow_help) | Display help message and exit |
| [-h](mysqldumpslow.md#option_mysqldumpslow_host) | Host name of the server in the log file name |
| [-i](mysqldumpslow.md#option_mysqldumpslow_instance) | Name of the server instance |
| [-l](mysqldumpslow.md#option_mysqldumpslow_lock) | Do not subtract lock time from total time |
| [-r](mysqldumpslow.md#option_mysqldumpslow_reverse) | Reverse the sort order |
| [-s](mysqldumpslow.md#option_mysqldumpslow_sort) | How to sort output |
| [-t](mysqldumpslow.md#option_mysqldumpslow_top) | Display only first num queries |
| [--verbose](mysqldumpslow.md#option_mysqldumpslow_verbose) | Verbose mode |

- [`--help`](mysqldumpslow.md#option_mysqldumpslow_help)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- `-a`

  Do not abstract all numbers to `N` and
  strings to `'S'`.
- [`--debug`](mysqldumpslow.md#option_mysqldumpslow_debug),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--debug` |

  Run in debug mode.

  This option is available only if MySQL was built using
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug). MySQL release
  binaries provided by Oracle are *not*
  built using this option.
- `-g pattern`

  |  |  |
  | --- | --- |
  | Type | String |

  Consider only queries that match the
  (**grep**-style) pattern.
- `-h host_name`

  |  |  |
  | --- | --- |
  | Type | String |
  | Default Value | `*` |

  Host name of MySQL server for
  `*-slow.log` file name. The value can
  contain a wildcard. The default is `*`
  (match all).
- `-i name`

  |  |  |
  | --- | --- |
  | Type | String |

  Name of server instance (if using
  [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script") startup script).
- `-l`

  Do not subtract lock time from total time.
- `-n N`

  |  |  |
  | --- | --- |
  | Type | Numeric |

  Abstract numbers with at least *`N`*
  digits within names.
- `-r`

  Reverse the sort order.
- `-s sort_type`

  |  |  |
  | --- | --- |
  | Type | String |
  | Default Value | `at` |

  How to sort the output. The value of
  *`sort_type`* should be chosen from
  the following list:

  - `t`, `at`: Sort by
    query time or average query time
  - `l`, `al`: Sort by
    lock time or average lock time
  - `r`, `ar`: Sort by
    rows sent or average rows sent
  - `c`: Sort by count

  By default, [**mysqldumpslow**](mysqldumpslow.md "6.6.10 mysqldumpslow — Summarize Slow Query Log Files") sorts by
  average query time (equivalent to `-s at`).
- `-t N`

  |  |  |
  | --- | --- |
  | Type | Numeric |

  Display only the first *`N`* queries
  in the output.
- [`--verbose`](mysqldumpslow.md#option_mysqldumpslow_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more information about what the program
  does.
