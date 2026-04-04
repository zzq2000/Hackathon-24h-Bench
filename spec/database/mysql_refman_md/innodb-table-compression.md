### 17.9.1 InnoDB Table Compression

[17.9.1.1 Overview of Table Compression](innodb-compression-background.md)

[17.9.1.2 Creating Compressed Tables](innodb-compression-usage.md)

[17.9.1.3 Tuning Compression for InnoDB Tables](innodb-compression-tuning.md)

[17.9.1.4 Monitoring InnoDB Table Compression at Runtime](innodb-compression-tuning-monitoring.md)

[17.9.1.5 How Compression Works for InnoDB Tables](innodb-compression-internals.md)

[17.9.1.6 Compression for OLTP Workloads](innodb-performance-compression-oltp.md)

[17.9.1.7 SQL Compression Syntax Warnings and Errors](innodb-compression-syntax-warnings.md)

This section describes `InnoDB` table
compression, which is supported with `InnoDB`
tables that reside in
[file\_per\_table](glossary.md#glos_file_per_table "file-per-table")
tablespaces or [general
tablespaces](glossary.md#glos_general_tablespace "general tablespace"). Table compression is enabled using the
`ROW_FORMAT=COMPRESSED` attribute with
[`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or
[`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement").
