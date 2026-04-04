## 25.5 NDB Cluster Programs

[25.5.1 ndbd — The NDB Cluster Data Node Daemon](mysql-cluster-programs-ndbd.md)

[25.5.2 ndbinfo\_select\_all — Select From ndbinfo Tables](mysql-cluster-programs-ndbinfo-select-all.md)

[25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)](mysql-cluster-programs-ndbmtd.md)

[25.5.4 ndb\_mgmd — The NDB Cluster Management Server Daemon](mysql-cluster-programs-ndb-mgmd.md)

[25.5.5 ndb\_mgm — The NDB Cluster Management Client](mysql-cluster-programs-ndb-mgm.md)

[25.5.6 ndb\_blob\_tool — Check and Repair BLOB and TEXT columns of NDB Cluster Tables](mysql-cluster-programs-ndb-blob-tool.md)

[25.5.7 ndb\_config — Extract NDB Cluster Configuration Information](mysql-cluster-programs-ndb-config.md)

[25.5.8 ndb\_delete\_all — Delete All Rows from an NDB Table](mysql-cluster-programs-ndb-delete-all.md)

[25.5.9 ndb\_desc — Describe NDB Tables](mysql-cluster-programs-ndb-desc.md)

[25.5.10 ndb\_drop\_index — Drop Index from an NDB Table](mysql-cluster-programs-ndb-drop-index.md)

[25.5.11 ndb\_drop\_table — Drop an NDB Table](mysql-cluster-programs-ndb-drop-table.md)

[25.5.12 ndb\_error\_reporter — NDB Error-Reporting Utility](mysql-cluster-programs-ndb-error-reporter.md)

[25.5.13 ndb\_import — Import CSV Data Into NDB](mysql-cluster-programs-ndb-import.md)

[25.5.14 ndb\_index\_stat — NDB Index Statistics Utility](mysql-cluster-programs-ndb-index-stat.md)

[25.5.15 ndb\_move\_data — NDB Data Copy Utility](mysql-cluster-programs-ndb-move-data.md)

[25.5.16 ndb\_perror — Obtain NDB Error Message Information](mysql-cluster-programs-ndb-perror.md)

[25.5.17 ndb\_print\_backup\_file — Print NDB Backup File Contents](mysql-cluster-programs-ndb-print-backup-file.md)

[25.5.18 ndb\_print\_file — Print NDB Disk Data File Contents](mysql-cluster-programs-ndb-print-file.md)

[25.5.19 ndb\_print\_frag\_file — Print NDB Fragment List File Contents](mysql-cluster-programs-ndb-print-frag-file.md)

[25.5.20 ndb\_print\_schema\_file — Print NDB Schema File Contents](mysql-cluster-programs-ndb-print-schema-file.md)

[25.5.21 ndb\_print\_sys\_file — Print NDB System File Contents](mysql-cluster-programs-ndb-print-sys-file.md)

[25.5.22 ndb\_redo\_log\_reader — Check and Print Content of Cluster Redo Log](mysql-cluster-programs-ndb-redo-log-reader.md)

[25.5.23 ndb\_restore — Restore an NDB Cluster Backup](mysql-cluster-programs-ndb-restore.md)

[25.5.24 ndb\_secretsfile\_reader — Obtain Key Information from an Encrypted NDB Data File](mysql-cluster-programs-ndb-secretsfile-reader.md)

[25.5.25 ndb\_select\_all — Print Rows from an NDB Table](mysql-cluster-programs-ndb-select-all.md)

[25.5.26 ndb\_select\_count — Print Row Counts for NDB Tables](mysql-cluster-programs-ndb-select-count.md)

[25.5.27 ndb\_show\_tables — Display List of NDB Tables](mysql-cluster-programs-ndb-show-tables.md)

[25.5.28 ndb\_size.pl — NDBCLUSTER Size Requirement Estimator](mysql-cluster-programs-ndb-size-pl.md)

[25.5.29 ndb\_top — View CPU usage information for NDB threads](mysql-cluster-programs-ndb-top.md)

[25.5.30 ndb\_waiter — Wait for NDB Cluster to Reach a Given Status](mysql-cluster-programs-ndb-waiter.md)

[25.5.31 ndbxfrm — Compress, Decompress, Encrypt, and Decrypt Files Created by NDB Cluster](mysql-cluster-programs-ndbxfrm.md)

Using and managing an NDB Cluster requires several specialized
programs, which we describe in this chapter. We discuss the purposes
of these programs in an NDB Cluster, how to use the programs, and
what startup options are available for each of them.

These programs include the NDB Cluster data, management, and SQL
node processes ([**ndbd**](mysql-cluster-programs-ndbd.md "25.5.1 ndbd — The NDB Cluster Data Node Daemon"), [**ndbmtd**](mysql-cluster-programs-ndbmtd.md "25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)"),
[**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon"), and [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")) and the
management client ([**ndb\_mgm**](mysql-cluster-programs-ndb-mgm.md "25.5.5 ndb_mgm — The NDB Cluster Management Client")).

For information about using [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") as an NDB
Cluster process, see [Section 25.6.10, “MySQL Server Usage for NDB Cluster”](mysql-cluster-mysqld.md "25.6.10 MySQL Server Usage for NDB Cluster").

Other [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") utility, diagnostic, and
example programs are included with the NDB Cluster distribution.
These include [**ndb\_restore**](mysql-cluster-programs-ndb-restore.md "25.5.23 ndb_restore — Restore an NDB Cluster Backup"),
[**ndb\_show\_tables**](mysql-cluster-programs-ndb-show-tables.md "25.5.27 ndb_show_tables — Display List of NDB Tables"), and
[**ndb\_config**](mysql-cluster-programs-ndb-config.md "25.5.7 ndb_config — Extract NDB Cluster Configuration Information"). These programs are also covered in
this section.
