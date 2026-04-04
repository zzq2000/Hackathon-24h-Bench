#### 15.1.20.1 Files Created by CREATE TABLE

For an `InnoDB` table created in a
file-per-table tablespace or general tablespace, table data and
associated indexes are stored in a
[.ibd file](glossary.md#glos_ibd_file ".ibd file") in the database
directory. When an `InnoDB` table is created in
the system tablespace, table data and indexes are stored in the
[ibdata\* files](glossary.md#glos_ibdata_file "ibdata file") that
represent the system tablespace. The
[`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table) option
controls whether tables are created in file-per-table
tablespaces or the system tablespace, by default. The
`TABLESPACE` option can be used to place a
table in a file-per-table tablespace, general tablespace, or the
system tablespace, regardless of the
[`innodb_file_per_table`](innodb-parameters.md#sysvar_innodb_file_per_table) setting.

For `MyISAM` tables, the storage engine creates
data and index files. Thus, for each `MyISAM`
table *`tbl_name`*, there are two disk
files.

| File | Purpose |
| --- | --- |
| `tbl_name.MYD` | Data file |
| `tbl_name.MYI` | Index file |

[Chapter 18, *Alternative Storage Engines*](storage-engines.md "Chapter 18 Alternative Storage Engines"), describes what files each
storage engine creates to represent tables. If a table name
contains special characters, the names for the table files
contain encoded versions of those characters as described in
[Section 11.2.4, “Mapping of Identifiers to File Names”](identifier-mapping.md "11.2.4 Mapping of Identifiers to File Names").
