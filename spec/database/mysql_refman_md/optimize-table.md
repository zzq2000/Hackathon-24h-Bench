#### 15.7.3.4 OPTIMIZE TABLE Statement

```sql
OPTIMIZE [NO_WRITE_TO_BINLOG | LOCAL]
    TABLE tbl_name [, tbl_name] ...
```

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") reorganizes the
physical storage of table data and associated index data, to
reduce storage space and improve I/O efficiency when accessing
the table. The exact changes made to each table depend on the
[storage engine](glossary.md#glos_storage_engine "storage engine") used
by that table.

Use [`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") in these
cases, depending on the type of table:

- After doing substantial insert, update, or delete operations
  on an `InnoDB` table that has its own
  [.ibd file](glossary.md#glos_ibd_file ".ibd file") because it
  was created with the
  [`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table)
  option enabled. The table and indexes are reorganized, and
  disk space can be reclaimed for use by the operating system.
- After doing substantial insert, update, or delete operations
  on columns that are part of a `FULLTEXT`
  index in an `InnoDB` table. Set the
  configuration option
  [`innodb_optimize_fulltext_only=1`](innodb-parameters.md#sysvar_innodb_optimize_fulltext_only)
  first. To keep the index maintenance period to a reasonable
  time, set the
  [`innodb_ft_num_word_optimize`](innodb-parameters.md#sysvar_innodb_ft_num_word_optimize)
  option to specify how many words to update in the search
  index, and run a sequence of `OPTIMIZE
  TABLE` statements until the search index is fully
  updated.
- After deleting a large part of a `MyISAM`
  or `ARCHIVE` table, or making many changes
  to a `MyISAM` or `ARCHIVE`table with variable-length rows (tables that have
  [`VARCHAR`](char.md "13.3.2 The CHAR and VARCHAR Types"),
  [`VARBINARY`](binary-varbinary.md "13.3.3 The BINARY and VARBINARY Types"),
  [`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types"), or
  [`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns). Deleted rows
  are maintained in a linked list and subsequent
  [`INSERT`](insert.md "15.2.7 INSERT Statement") operations reuse old
  row positions. You can use [`OPTIMIZE
  TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") to reclaim the unused space and to
  defragment the data file. After extensive changes to a
  table, this statement may also improve performance of
  statements that use the table, sometimes significantly.

This statement requires [`SELECT`](privileges-provided.md#priv_select)
and [`INSERT`](privileges-provided.md#priv_insert) privileges for the
table.

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") works for
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"),
[`MyISAM`](myisam-storage-engine.md "18.2 The MyISAM Storage Engine"), and
[`ARCHIVE`](archive-storage-engine.md "18.5 The ARCHIVE Storage Engine") tables.
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is also supported
for dynamic columns of in-memory
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") tables. It does not work for
fixed-width columns of in-memory tables, nor does it work for
Disk Data tables. The performance of `OPTIMIZE`
on NDB Cluster tables can be tuned using
[`--ndb-optimization-delay`](mysql-cluster-options-variables.md#option_mysqld_ndb-optimization-delay), which
controls the length of time to wait between processing batches
of rows by [`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement"). For
more information, see
[Section 25.2.7.11, “Previous NDB Cluster Issues Resolved in NDB Cluster 8.0”](mysql-cluster-limitations-resolved.md "25.2.7.11 Previous NDB Cluster Issues Resolved in NDB Cluster 8.0").

For NDB Cluster tables, [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") can be interrupted by (for example) killing the
SQL thread performing the `OPTIMIZE` operation.

By default, [`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") does
*not* work for tables created using any other
storage engine and returns a result indicating this lack of
support. You can make [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") work for other storage engines by starting
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with the
[`--skip-new`](server-options.md#option_mysqld_skip-new) option. In this case,
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is just mapped to
[`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement").

This statement does not work with views.

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is supported for
partitioned tables. For information about using this statement
with partitioned tables and table partitions, see
[Section 26.3.4, “Maintenance of Partitions”](partitioning-maintenance.md "26.3.4 Maintenance of Partitions").

By default, the server writes [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") statements to the binary log so that they
replicate to replicas. To suppress logging, specify the optional
`NO_WRITE_TO_BINLOG` keyword or its alias
`LOCAL`.

- [OPTIMIZE TABLE Output](optimize-table.md#optimize-table-output "OPTIMIZE TABLE Output")
- [InnoDB Details](optimize-table.md#optimize-table-innodb-details "InnoDB Details")
- [MyISAM Details](optimize-table.md#optimize-table-myisam-details "MyISAM Details")
- [Other Considerations](optimize-table.md#optimize-table-other-considerations "Other Considerations")

##### OPTIMIZE TABLE Output

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") returns a result
set with the columns shown in the following table.

| Column | Value |
| --- | --- |
| `Table` | The table name |
| `Op` | Always `optimize` |
| `Msg_type` | `status`, `error`, `info`, `note`, or `warning` |
| `Msg_text` | An informational message |

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") table catches
and throws any errors that occur while copying table
statistics from the old file to the newly created file. For
example. if the user ID of the owner of the
`.MYD` or `.MYI` file is
different from the user ID of the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")
process, [`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement")
generates a "cannot change ownership of the file" error unless
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") is started by the
`root` user.

##### InnoDB Details

For `InnoDB` tables,
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is mapped to
[`ALTER TABLE ...
FORCE`](alter-table.md "15.1.9 ALTER TABLE Statement"), which rebuilds the table to update index
statistics and free unused space in the clustered index. This
is displayed in the output of [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") when you run it on an
`InnoDB` table, as shown here:

```sql
mysql> OPTIMIZE TABLE foo;
+----------+----------+----------+-------------------------------------------------------------------+
| Table    | Op       | Msg_type | Msg_text                                                          |
+----------+----------+----------+-------------------------------------------------------------------+
| test.foo | optimize | note     | Table does not support optimize, doing recreate + analyze instead |
| test.foo | optimize | status   | OK                                                                |
+----------+----------+----------+-------------------------------------------------------------------+
```

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") uses
[online DDL](innodb-online-ddl.md "17.12 InnoDB and Online DDL") for
regular and partitioned `InnoDB` tables,
which reduces downtime for concurrent DML operations. The
table rebuild triggered by [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is completed in place. An exclusive table lock
is only taken briefly during the prepare phase and the commit
phase of the operation. During the prepare phase, metadata is
updated and an intermediate table is created. During the
commit phase, table metadata changes are committed.

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") rebuilds the
table using the table copy method under the following
conditions:

- When the [`old_alter_table`](server-system-variables.md#sysvar_old_alter_table)
  system variable is enabled.
- When the server is started with the
  [`--skip-new`](server-options.md#option_mysqld_skip-new) option.

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") using
[online DDL](innodb-online-ddl.md "17.12 InnoDB and Online DDL") is not
supported for `InnoDB` tables that contain
`FULLTEXT` indexes. The table copy method is
used instead.

`InnoDB` stores data using a page-allocation
method and does not suffer from fragmentation in the same way
that legacy storage engines (such as
`MyISAM`) do. When considering whether or not
to run optimize, consider the workload of transactions that
your server is expected to process:

- Some level of fragmentation is expected.
  `InnoDB` only fills
  [pages](glossary.md#glos_page "page") 93% full, to
  leave room for updates without having to split pages.
- Delete operations might leave gaps that leave pages less
  filled than desired, which could make it worthwhile to
  optimize the table.
- Updates to rows usually rewrite the data within the same
  page, depending on the data type and row format, when
  sufficient space is available. See
  [Section 17.9.1.5, “How Compression Works for InnoDB Tables”](innodb-compression-internals.md "17.9.1.5 How Compression Works for InnoDB Tables") and
  [Section 17.10, “InnoDB Row Formats”](innodb-row-format.md "17.10 InnoDB Row Formats").
- High-concurrency workloads might leave gaps in indexes
  over time, as `InnoDB` retains multiple
  versions of the same data due through its
  [MVCC](glossary.md#glos_mvcc "MVCC") mechanism. See
  [Section 17.3, “InnoDB Multi-Versioning”](innodb-multi-versioning.md "17.3 InnoDB Multi-Versioning").

##### MyISAM Details

For `MyISAM` tables,
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") works as
follows:

1. If the table has deleted or split rows, repair the table.
2. If the index pages are not sorted, sort them.
3. If the table's statistics are not up to date (and the
   repair could not be accomplished by sorting the index),
   update them.

##### Other Considerations

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is performed
online for regular and partitioned `InnoDB`
tables. Otherwise, MySQL [locks
the table](glossary.md#glos_table_lock "table lock") during the time [`OPTIMIZE
TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") is running.

[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement") does not sort
R-tree indexes, such as spatial indexes on
`POINT` columns. (Bug #23578)
