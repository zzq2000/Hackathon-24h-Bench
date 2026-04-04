# Chapter 25 MySQL NDB Cluster 8.0

**Table of Contents**

[25.1 General Information](mysql-cluster-general-info.md)

[25.2 NDB Cluster Overview](mysql-cluster-overview.md)
:   [25.2.1 NDB Cluster Core Concepts](mysql-cluster-basics.md)

    [25.2.2 NDB Cluster Nodes, Node Groups, Fragment Replicas, and Partitions](mysql-cluster-nodes-groups.md)

    [25.2.3 NDB Cluster Hardware, Software, and Networking Requirements](mysql-cluster-overview-requirements.md)

    [25.2.4 What is New in MySQL NDB Cluster 8.0](mysql-cluster-what-is-new.md)

    [25.2.5 Options, Variables, and Parameters Added, Deprecated or Removed in NDB 8.0](mysql-cluster-added-deprecated-removed.md)

    [25.2.6 MySQL Server Using InnoDB Compared with NDB Cluster](mysql-cluster-compared.md)

    [25.2.7 Known Limitations of NDB Cluster](mysql-cluster-limitations.md)

[25.3 NDB Cluster Installation](mysql-cluster-installation.md)
:   [25.3.1 Installation of NDB Cluster on Linux](mysql-cluster-install-linux.md)

    [25.3.2 Installing NDB Cluster on Windows](mysql-cluster-install-windows.md)

    [25.3.3 Initial Configuration of NDB Cluster](mysql-cluster-install-configuration.md)

    [25.3.4 Initial Startup of NDB Cluster](mysql-cluster-install-first-start.md)

    [25.3.5 NDB Cluster Example with Tables and Data](mysql-cluster-install-example-data.md)

    [25.3.6 Safe Shutdown and Restart of NDB Cluster](mysql-cluster-install-shutdown-restart.md)

    [25.3.7 Upgrading and Downgrading NDB Cluster](mysql-cluster-upgrade-downgrade.md)

    [25.3.8 The NDB Cluster Auto-Installer (NO LONGER SUPPORTED)](mysql-cluster-installer.md)

[25.4 Configuration of NDB Cluster](mysql-cluster-configuration.md)
:   [25.4.1 Quick Test Setup of NDB Cluster](mysql-cluster-quick.md)

    [25.4.2 Overview of NDB Cluster Configuration Parameters, Options, and Variables](mysql-cluster-configuration-overview.md)

    [25.4.3 NDB Cluster Configuration Files](mysql-cluster-config-file.md)

    [25.4.4 Using High-Speed Interconnects with NDB Cluster](mysql-cluster-interconnects.md)

[25.5 NDB Cluster Programs](mysql-cluster-programs.md)
:   [25.5.1 ndbd — The NDB Cluster Data Node Daemon](mysql-cluster-programs-ndbd.md)

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

[25.6 Management of NDB Cluster](mysql-cluster-management.md)
:   [25.6.1 Commands in the NDB Cluster Management Client](mysql-cluster-mgm-client-commands.md)

    [25.6.2 NDB Cluster Log Messages](mysql-cluster-logs-ndb-messages.md)

    [25.6.3 Event Reports Generated in NDB Cluster](mysql-cluster-event-reports.md)

    [25.6.4 Summary of NDB Cluster Start Phases](mysql-cluster-start-phases.md)

    [25.6.5 Performing a Rolling Restart of an NDB Cluster](mysql-cluster-rolling-restart.md)

    [25.6.6 NDB Cluster Single User Mode](mysql-cluster-single-user-mode.md)

    [25.6.7 Adding NDB Cluster Data Nodes Online](mysql-cluster-online-add-node.md)

    [25.6.8 Online Backup of NDB Cluster](mysql-cluster-backup.md)

    [25.6.9 Importing Data Into MySQL Cluster](mysql-cluster-importing-data.md)

    [25.6.10 MySQL Server Usage for NDB Cluster](mysql-cluster-mysqld.md)

    [25.6.11 NDB Cluster Disk Data Tables](mysql-cluster-disk-data.md)

    [25.6.12 Online Operations with ALTER TABLE in NDB Cluster](mysql-cluster-online-operations.md)

    [25.6.13 Privilege Synchronization and NDB\_STORED\_USER](mysql-cluster-privilege-synchronization.md)

    [25.6.14 File System Encryption for NDB Cluster](mysql-cluster-tde.md)

    [25.6.15 NDB API Statistics Counters and Variables](mysql-cluster-ndb-api-statistics.md)

    [25.6.16 ndbinfo: The NDB Cluster Information Database](mysql-cluster-ndbinfo.md)

    [25.6.17 INFORMATION\_SCHEMA Tables for NDB Cluster](mysql-cluster-information-schema-tables.md)

    [25.6.18 NDB Cluster and the Performance Schema](mysql-cluster-ps-tables.md)

    [25.6.19 Quick Reference: NDB Cluster SQL Statements](mysql-cluster-sql-statements.md)

    [25.6.20 NDB Cluster Security Issues](mysql-cluster-security.md)

[25.7 NDB Cluster Replication](mysql-cluster-replication.md)
:   [25.7.1 NDB Cluster Replication: Abbreviations and Symbols](mysql-cluster-replication-abbreviations.md)

    [25.7.2 General Requirements for NDB Cluster Replication](mysql-cluster-replication-general.md)

    [25.7.3 Known Issues in NDB Cluster Replication](mysql-cluster-replication-issues.md)

    [25.7.4 NDB Cluster Replication Schema and Tables](mysql-cluster-replication-schema.md)

    [25.7.5 Preparing the NDB Cluster for Replication](mysql-cluster-replication-preparation.md)

    [25.7.6 Starting NDB Cluster Replication (Single Replication Channel)](mysql-cluster-replication-starting.md)

    [25.7.7 Using Two Replication Channels for NDB Cluster Replication](mysql-cluster-replication-two-channels.md)

    [25.7.8 Implementing Failover with NDB Cluster Replication](mysql-cluster-replication-failover.md)

    [25.7.9 NDB Cluster Backups With NDB Cluster Replication](mysql-cluster-replication-backups.md)

    [25.7.10 NDB Cluster Replication: Bidirectional and Circular Replication](mysql-cluster-replication-multi-source.md)

    [25.7.11 NDB Cluster Replication Using the Multithreaded Applier](mysql-cluster-replication-mta.md)

    [25.7.12 NDB Cluster Replication Conflict Resolution](mysql-cluster-replication-conflict-resolution.md)

[25.8 NDB Cluster Release Notes](mysql-cluster-news.md)

This chapter provides information about MySQL
NDB Cluster, a
high-availability, high-redundancy version of MySQL adapted for the
distributed computing environment, using the
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine (also known as
[`NDBCLUSTER`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0")) to enable running several
computers with MySQL servers and other software in a cluster. NDB
Cluster 8.0, now available as a General Availability (GA) release
(beginning with version 8.0.19), incorporates version 8.0 of the
`NDB` storage engine. This chapter also provides
information specific to NDB Cluster 8.0, and covers releases through
8.0.43. NDB Cluster 8.4 (NDB
8.4.7), based on version 8.4 of the NDB storage
engine, is also available as an LTS release. See
[What is New in MySQL NDB Cluster 8.4](https://dev.mysql.com/doc/refman/8.4/en/mysql-cluster-what-is-new.html) for
information about differences in NDB 8.4 as compared to earlier
releases. NDB Cluster 7.6 and NDB Cluster 7.5, still available as GA
releases, use versions 7.6 and 7.5 of `NDB`,
respectively. NDB Cluster 7.6 and 7.5 are previous GA releases still
supported in production; for information about NDB Cluster 7.6, see
[What is New in NDB Cluster 7.6](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-what-is-new-7-6.html). For
similar information about NDB Cluster 7.5, see
[What is New in NDB Cluster 7.5](https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster-what-is-new-7-5.html). Previous
GA releases NDB Cluster 7.4 and NDB Cluster 7.3 incorporated
`NDB` versions 7.4 and 7.3, respectively.
*NDB 7.4 and older release series are no longer supported
or maintained*. Both NDB 8.0 and NDB 8.4 are supported in
production, and are recommended for new deployments.
