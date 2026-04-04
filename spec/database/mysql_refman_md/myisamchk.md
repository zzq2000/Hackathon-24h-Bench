### 6.6.4 myisamchk — MyISAM Table-Maintenance Utility

[6.6.4.1 myisamchk General Options](myisamchk-general-options.md)

[6.6.4.2 myisamchk Check Options](myisamchk-check-options.md)

[6.6.4.3 myisamchk Repair Options](myisamchk-repair-options.md)

[6.6.4.4 Other myisamchk Options](myisamchk-other-options.md)

[6.6.4.5 Obtaining Table Information with myisamchk](myisamchk-table-info.md)

[6.6.4.6 myisamchk Memory Usage](myisamchk-memory.md)

The [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") utility gets information about
your database tables or checks, repairs, or optimizes them.
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") works with
`MyISAM` tables (tables that have
`.MYD` and `.MYI` files
for storing data and indexes).

You can also use the [`CHECK TABLE`](check-table.md "15.7.3.2 CHECK TABLE Statement")
and [`REPAIR TABLE`](repair-table.md "15.7.3.5 REPAIR TABLE Statement") statements to
check and repair `MyISAM` tables. See
[Section 15.7.3.2, “CHECK TABLE Statement”](check-table.md "15.7.3.2 CHECK TABLE Statement"), and
[Section 15.7.3.5, “REPAIR TABLE Statement”](repair-table.md "15.7.3.5 REPAIR TABLE Statement").

The use of [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") with partitioned tables
is not supported.

Caution

It is best to make a backup of a table before performing a
table repair operation; under some circumstances the operation
might cause data loss. Possible causes include but are not
limited to file system errors.

Invoke [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") like this:

```terminal
myisamchk [options] tbl_name ...
```

The *`options`* specify what you want
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to do. They are described in the
following sections. You can also get a list of options by
invoking [**myisamchk --help**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility").

With no options, [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") simply checks your
table as the default operation. To get more information or to
tell [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to take corrective action,
specify options as described in the following discussion.

*`tbl_name`* is the database table you
want to check or repair. If you run [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")
somewhere other than in the database directory, you must specify
the path to the database directory, because
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") has no idea where the database is
located. In fact, [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") does not actually
care whether the files you are working on are located in a
database directory. You can copy the files that correspond to a
database table into some other location and perform recovery
operations on them there.

You can name several tables on the [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")
command line if you wish. You can also specify a table by naming
its index file (the file with the `.MYI`
suffix). This enables you to specify all tables in a directory
by using the pattern `*.MYI`. For example, if
you are in a database directory, you can check all the
`MyISAM` tables in that directory like this:

```terminal
myisamchk *.MYI
```

If you are not in the database directory, you can check all the
tables there by specifying the path to the directory:

```terminal
myisamchk /path/to/database_dir/*.MYI
```

You can even check all tables in all databases by specifying a
wildcard with the path to the MySQL data directory:

```terminal
myisamchk /path/to/datadir/*/*.MYI
```

The recommended way to quickly check all
`MyISAM` tables is:

```terminal
myisamchk --silent --fast /path/to/datadir/*/*.MYI
```

If you want to check all `MyISAM` tables and
repair any that are corrupted, you can use the following
command:

```terminal
myisamchk --silent --force --fast --update-state \
          --key_buffer_size=64M --myisam_sort_buffer_size=64M \
          --read_buffer_size=1M --write_buffer_size=1M \
          /path/to/datadir/*/*.MYI
```

This command assumes that you have more than 64MB free. For more
information about memory allocation with
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), see
[Section 6.6.4.6, “myisamchk Memory Usage”](myisamchk-memory.md "6.6.4.6 myisamchk Memory Usage").

For additional information about using
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), see
[Section 9.6, “MyISAM Table Maintenance and Crash Recovery”](myisam-table-maintenance.md "9.6 MyISAM Table Maintenance and Crash Recovery").

Important

*You must ensure that no other program is using the
tables while you are running
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")*. The most effective
means of doing so is to shut down the MySQL server while
running [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), or to lock all tables
that [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") is being used on.

Otherwise, when you run [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), it may
display the following error message:

```none
warning: clients are using or haven't closed the table properly
```

This means that you are trying to check a table that has been
updated by another program (such as the
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") server) that hasn't yet closed the
file or that has died without closing the file properly, which
can sometimes lead to the corruption of one or more
`MyISAM` tables.

If [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") is running, you must force it to
flush any table modifications that are still buffered in
memory by using [`FLUSH TABLES`](flush.md#flush-tables).
You should then ensure that no one is using the tables while
you are running [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")

However, the easiest way to avoid this problem is to use
[`CHECK TABLE`](check-table.md "15.7.3.2 CHECK TABLE Statement") instead of
[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") to check tables. See
[Section 15.7.3.2, “CHECK TABLE Statement”](check-table.md "15.7.3.2 CHECK TABLE Statement").

[**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility") supports the following options,
which can be specified on the command line or in the
`[myisamchk]` group of an option file. For
information about option files used by MySQL programs, see
[Section 6.2.2.2, “Using Option Files”](option-files.md "6.2.2.2 Using Option Files").

**Table 6.20 myisamchk Options**

| Option Name | Description |
| --- | --- |
| [--analyze](myisamchk-other-options.md#option_myisamchk_analyze) | Analyze the distribution of key values |
| [--backup](myisamchk-repair-options.md#option_myisamchk_backup) | Make a backup of the .MYD file as file\_name-time.BAK |
| [--block-search](myisamchk-other-options.md#option_myisamchk_block-search) | Find the record that a block at the given offset belongs to |
| [--character-sets-dir](myisamchk-repair-options.md#option_myisamchk_character-sets-dir) | Directory where character sets can be found |
| [--check](myisamchk-check-options.md#option_myisamchk_check) | Check the table for errors |
| [--check-only-changed](myisamchk-check-options.md#option_myisamchk_check-only-changed) | Check only tables that have changed since the last check |
| [--correct-checksum](myisamchk-repair-options.md#option_myisamchk_correct-checksum) | Correct the checksum information for the table |
| [--data-file-length](myisamchk-repair-options.md#option_myisamchk_data-file-length) | Maximum length of the data file (when re-creating data file when it is full) |
| [--debug](myisamchk-general-options.md#option_myisamchk_debug) | Write debugging log |
| --decode\_bits | Decode\_bits |
| [--defaults-extra-file](myisamchk-general-options.md#option_myisamchk_defaults-extra-file) | Read named option file in addition to usual option files |
| [--defaults-file](myisamchk-general-options.md#option_myisamchk_defaults-file) | Read only named option file |
| [--defaults-group-suffix](myisamchk-general-options.md#option_myisamchk_defaults-group-suffix) | Option group suffix value |
| [--description](myisamchk-other-options.md#option_myisamchk_description) | Print some descriptive information about the table |
| [--extend-check](myisamchk-check-options.md#option_myisamchk_extend-check) | Do very thorough table check or repair that tries to recover every possible row from the data file |
| [--fast](myisamchk-check-options.md#option_myisamchk_fast) | Check only tables that haven't been closed properly |
| [--force](myisamchk-check-options.md#option_myisamchk_force) | Do a repair operation automatically if myisamchk finds any errors in the table |
| --force | Overwrite old temporary files. For use with the -r or -o option |
| --ft\_max\_word\_len | Maximum word length for FULLTEXT indexes |
| --ft\_min\_word\_len | Minimum word length for FULLTEXT indexes |
| --ft\_stopword\_file | Use stopwords from this file instead of built-in list |
| [--HELP](myisamchk-general-options.md#option_myisamchk_HELP) | Display help message and exit |
| [--help](myisamchk-general-options.md#option_myisamchk_help) | Display help message and exit |
| [--information](myisamchk-check-options.md#option_myisamchk_information) | Print informational statistics about the table that is checked |
| --key\_buffer\_size | Size of buffer used for index blocks for MyISAM tables |
| [--keys-used](myisamchk-repair-options.md#option_myisamchk_keys-used) | A bit-value that indicates which indexes to update |
| [--max-record-length](myisamchk-repair-options.md#option_myisamchk_max-record-length) | Skip rows larger than the given length if myisamchk cannot allocate memory to hold them |
| [--medium-check](myisamchk-check-options.md#option_myisamchk_medium-check) | Do a check that is faster than an --extend-check operation |
| --myisam\_block\_size | Block size to be used for MyISAM index pages |
| --myisam\_sort\_buffer\_size | The buffer that is allocated when sorting the index when doing a REPAIR or when creating indexes with CREATE INDEX or ALTER TABLE |
| [--no-defaults](myisamchk-general-options.md#option_myisamchk_no-defaults) | Read no option files |
| [--parallel-recover](myisamchk-repair-options.md#option_myisamchk_parallel-recover) | Uses the same technique as -r and -n, but creates all the keys in parallel, using different threads (beta) |
| [--print-defaults](myisamchk-general-options.md#option_myisamchk_print-defaults) | Print default options |
| [--quick](myisamchk-repair-options.md#option_myisamchk_quick) | Achieve a faster repair by not modifying the data file |
| --read\_buffer\_size | Each thread that does a sequential scan allocates a buffer of this size for each table it scans |
| [--read-only](myisamchk-check-options.md#option_myisamchk_read-only) | Do not mark the table as checked |
| [--recover](myisamchk-repair-options.md#option_myisamchk_recover) | Do a repair that can fix almost any problem except unique keys that aren't unique |
| [--safe-recover](myisamchk-repair-options.md#option_myisamchk_safe-recover) | Do a repair using an old recovery method that reads through all rows in order and updates all index trees based on the rows found |
| [--set-auto-increment](myisamchk-other-options.md#option_myisamchk_set-auto-increment) | Force AUTO\_INCREMENT numbering for new records to start at the given value |
| [--set-collation](myisamchk-repair-options.md#option_myisamchk_set-collation) | Specify the collation to use for sorting table indexes |
| [--silent](myisamchk-general-options.md#option_myisamchk_silent) | Silent mode |
| --sort\_buffer\_size | The buffer that is allocated when sorting the index when doing a REPAIR or when creating indexes with CREATE INDEX or ALTER TABLE |
| [--sort-index](myisamchk-other-options.md#option_myisamchk_sort-index) | Sort the index tree blocks in high-low order |
| --sort\_key\_blocks | sort\_key\_blocks |
| [--sort-records](myisamchk-other-options.md#option_myisamchk_sort-records) | Sort records according to a particular index |
| [--sort-recover](myisamchk-repair-options.md#option_myisamchk_sort-recover) | Force myisamchk to use sorting to resolve the keys even if the temporary files would be very large |
| --stats\_method | Specifies how MyISAM index statistics collection code should treat NULLs |
| [--tmpdir](myisamchk-repair-options.md#option_myisamchk_tmpdir) | Directory to be used for storing temporary files |
| [--unpack](myisamchk-repair-options.md#option_myisamchk_unpack) | Unpack a table that was packed with myisampack |
| [--update-state](myisamchk-check-options.md#option_myisamchk_update-state) | Store information in the .MYI file to indicate when the table was checked and whether the table crashed |
| [--verbose](myisamchk-general-options.md#option_myisamchk_verbose) | Verbose mode |
| [--version](myisamchk-general-options.md#option_myisamchk_version) | Display version information and exit |
| [--wait](myisamchk-general-options.md#option_myisamchk_wait) | Wait for locked table to be unlocked, instead of terminating |
| --write\_buffer\_size | Write buffer size |
