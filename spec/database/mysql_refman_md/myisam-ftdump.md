### 6.6.3 myisam\_ftdump — Display Full-Text Index information

[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") displays information about
`FULLTEXT` indexes in `MyISAM`
tables. It reads the `MyISAM` index file
directly, so it must be run on the server host where the table
is located. Before using [**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information"), be
sure to issue a `FLUSH TABLES` statement first
if the server is running.

[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") scans and dumps the entire
index, which is not particularly fast. On the other hand, the
distribution of words changes infrequently, so it need not be
run often.

Invoke [**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") like this:

```terminal
myisam_ftdump [options] tbl_name index_num
```

The *`tbl_name`* argument should be the
name of a `MyISAM` table. You can also specify
a table by naming its index file (the file with the
`.MYI` suffix). If you do not invoke
[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") in the directory where the
table files are located, the table or index file name must be
preceded by the path name to the table's database directory.
Index numbers begin with 0.

Example: Suppose that the `test` database
contains a table named `mytexttable` that has
the following definition:

```sql
CREATE TABLE mytexttable
(
  id   INT NOT NULL,
  txt  TEXT NOT NULL,
  PRIMARY KEY (id),
  FULLTEXT (txt)
) ENGINE=MyISAM;
```

The index on `id` is index 0 and the
`FULLTEXT` index on `txt` is
index 1. If your working directory is the
`test` database directory, invoke
[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") as follows:

```terminal
myisam_ftdump mytexttable 1
```

If the path name to the `test` database
directory is `/usr/local/mysql/data/test`,
you can also specify the table name argument using that path
name. This is useful if you do not invoke
[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") in the database directory:

```terminal
myisam_ftdump /usr/local/mysql/data/test/mytexttable 1
```

You can use [**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") to generate a list
of index entries in order of frequency of occurrence like this
on Unix-like systems:

```terminal
myisam_ftdump -c mytexttable 1 | sort -r
```

On Windows, use:

```terminal
myisam_ftdump -c mytexttable 1 | sort /R
```

[**myisam\_ftdump**](myisam-ftdump.md "6.6.3 myisam_ftdump — Display Full-Text Index information") supports the following options:

- [`--help`](myisam-ftdump.md#option_myisam_ftdump_help),
  `-h` `-?`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--help` |

  Display a help message and exit.
- [`--count`](myisam-ftdump.md#option_myisam_ftdump_count),
  `-c`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--count` |

  Calculate per-word statistics (counts and global weights).
- [`--dump`](myisam-ftdump.md#option_myisam_ftdump_dump),
  `-d`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--dump` |

  Dump the index, including data offsets and word weights.
- [`--length`](myisam-ftdump.md#option_myisam_ftdump_length),
  `-l`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--length` |

  Report the length distribution.
- [`--stats`](myisam-ftdump.md#option_myisam_ftdump_stats),
  `-s`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--stats` |

  Report global index statistics. This is the default
  operation if no other operation is specified.
- [`--verbose`](myisam-ftdump.md#option_myisam_ftdump_verbose),
  `-v`

  |  |  |
  | --- | --- |
  | Command-Line Format | `--verbose` |

  Verbose mode. Print more output about what the program does.
