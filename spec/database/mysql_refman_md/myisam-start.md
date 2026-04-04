### 18.2.1 MyISAM Startup Options

The following options to [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") can be used to
change the behavior of `MyISAM` tables. For
additional information, see [Section 7.1.7, “Server Command Options”](server-options.md "7.1.7 Server Command Options").

**Table 18.3 MyISAM Option and Variable Reference**

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| --- | --- | --- | --- | --- | --- | --- |
| [bulk\_insert\_buffer\_size](server-system-variables.md#sysvar_bulk_insert_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [concurrent\_insert](server-system-variables.md#sysvar_concurrent_insert) | Yes | Yes | Yes |  | Global | Yes |
| [delay\_key\_write](server-system-variables.md#sysvar_delay_key_write) | Yes | Yes | Yes |  | Global | Yes |
| [have\_rtree\_keys](server-system-variables.md#sysvar_have_rtree_keys) |  |  | Yes |  | Global | No |
| [key\_buffer\_size](server-system-variables.md#sysvar_key_buffer_size) | Yes | Yes | Yes |  | Global | Yes |
| [log-isam](server-options.md#option_mysqld_log-isam) | Yes | Yes |  |  |  |  |
| [myisam-block-size](server-options.md#option_mysqld_myisam-block-size) | Yes | Yes |  |  |  |  |
| [myisam\_data\_pointer\_size](server-system-variables.md#sysvar_myisam_data_pointer_size) | Yes | Yes | Yes |  | Global | Yes |
| [myisam\_max\_sort\_file\_size](server-system-variables.md#sysvar_myisam_max_sort_file_size) | Yes | Yes | Yes |  | Global | Yes |
| [myisam\_mmap\_size](server-system-variables.md#sysvar_myisam_mmap_size) | Yes | Yes | Yes |  | Global | No |
| [myisam\_recover\_options](server-system-variables.md#sysvar_myisam_recover_options) | Yes | Yes | Yes |  | Global | No |
| [myisam\_repair\_threads](server-system-variables.md#sysvar_myisam_repair_threads) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_sort\_buffer\_size](server-system-variables.md#sysvar_myisam_sort_buffer_size) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_stats\_method](server-system-variables.md#sysvar_myisam_stats_method) | Yes | Yes | Yes |  | Both | Yes |
| [myisam\_use\_mmap](server-system-variables.md#sysvar_myisam_use_mmap) | Yes | Yes | Yes |  | Global | Yes |
| [tmp\_table\_size](server-system-variables.md#sysvar_tmp_table_size) | Yes | Yes | Yes |  | Both | Yes |

The following system variables affect the behavior of
`MyISAM` tables. For additional information, see
[Section 7.1.8, “Server System Variables”](server-system-variables.md "7.1.8 Server System Variables").

- [`bulk_insert_buffer_size`](server-system-variables.md#sysvar_bulk_insert_buffer_size)

  The size of the tree cache used in bulk insert optimization.

  Note

  This is a limit *per thread*!
- [`delay_key_write=ALL`](server-system-variables.md#sysvar_delay_key_write)

  Don't flush key buffers between writes for any
  `MyISAM` table.

  Note

  If you do this, you should not access
  `MyISAM` tables from another program (such
  as from another MySQL server or with
  [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")) when the tables are in use.
  Doing so risks index corruption. Using
  [`--external-locking`](server-options.md#option_mysqld_external-locking) does not
  eliminate this risk.
- [`myisam_max_sort_file_size`](server-system-variables.md#sysvar_myisam_max_sort_file_size)

  The maximum size of the temporary file that MySQL is permitted
  to use while re-creating a `MyISAM` index
  (during [`REPAIR TABLE`](repair-table.md "15.7.3.5 REPAIR TABLE Statement"),
  [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement"), or
  [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement")). If the file size
  would be larger than this value, the index is created using
  the key cache instead, which is slower. The value is given in
  bytes.
- [`myisam_recover_options=mode`](server-system-variables.md#sysvar_myisam_recover_options)

  Set the mode for automatic recovery of crashed
  `MyISAM` tables.
- [`myisam_sort_buffer_size`](server-system-variables.md#sysvar_myisam_sort_buffer_size)

  Set the size of the buffer used when recovering tables.

Automatic recovery is activated if you start
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with the
[`myisam_recover_options`](server-system-variables.md#sysvar_myisam_recover_options) system
variable set. In this case, when the server opens a
`MyISAM` table, it checks whether the table is
marked as crashed or whether the open count variable for the table
is not 0 and you are running the server with external locking
disabled. If either of these conditions is true, the following
happens:

- The server checks the table for errors.
- If the server finds an error, it tries to do a fast table
  repair (with sorting and without re-creating the data file).
- If the repair fails because of an error in the data file (for
  example, a duplicate-key error), the server tries again, this
  time re-creating the data file.
- If the repair still fails, the server tries once more with the
  old repair option method (write row by row without sorting).
  This method should be able to repair any type of error and has
  low disk space requirements.

If the recovery wouldn't be able to recover all rows from
previously completed statements and you didn't specify
`FORCE` in the value of the
[`myisam_recover_options`](server-system-variables.md#sysvar_myisam_recover_options) system
variable, automatic repair aborts with an error message in the
error log:

```none
Error: Couldn't repair table: test.g00pages
```

If you specify `FORCE`, a warning like this is
written instead:

```none
Warning: Found 344 of 354 rows when repairing ./test/g00pages
```

If the automatic recovery value includes
`BACKUP`, the recovery process creates files with
names of the form
`tbl_name-datetime.BAK`.
You should have a **cron** script that
automatically moves these files from the database directories to
backup media.
