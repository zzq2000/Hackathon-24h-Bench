# Chapter 17 The InnoDB Storage Engine

**Table of Contents**

[17.1 Introduction to InnoDB](innodb-introduction.md)
:   [17.1.1 Benefits of Using InnoDB Tables](innodb-benefits.md)

    [17.1.2 Best Practices for InnoDB Tables](innodb-best-practices.md)

    [17.1.3 Verifying that InnoDB is the Default Storage Engine](innodb-check-availability.md)

    [17.1.4 Testing and Benchmarking with InnoDB](innodb-benchmarking.md)

[17.2 InnoDB and the ACID Model](mysql-acid.md)

[17.3 InnoDB Multi-Versioning](innodb-multi-versioning.md)

[17.4 InnoDB Architecture](innodb-architecture.md)

[17.5 InnoDB In-Memory Structures](innodb-in-memory-structures.md)
:   [17.5.1 Buffer Pool](innodb-buffer-pool.md)

    [17.5.2 Change Buffer](innodb-change-buffer.md)

    [17.5.3 Adaptive Hash Index](innodb-adaptive-hash.md)

    [17.5.4 Log Buffer](innodb-redo-log-buffer.md)

[17.6 InnoDB On-Disk Structures](innodb-on-disk-structures.md)
:   [17.6.1 Tables](innodb-tables.md)

    [17.6.2 Indexes](innodb-indexes.md)

    [17.6.3 Tablespaces](innodb-tablespace.md)

    [17.6.4 Doublewrite Buffer](innodb-doublewrite-buffer.md)

    [17.6.5 Redo Log](innodb-redo-log.md)

    [17.6.6 Undo Logs](innodb-undo-logs.md)

[17.7 InnoDB Locking and Transaction Model](innodb-locking-transaction-model.md)
:   [17.7.1 InnoDB Locking](innodb-locking.md)

    [17.7.2 InnoDB Transaction Model](innodb-transaction-model.md)

    [17.7.3 Locks Set by Different SQL Statements in InnoDB](innodb-locks-set.md)

    [17.7.4 Phantom Rows](innodb-next-key-locking.md)

    [17.7.5 Deadlocks in InnoDB](innodb-deadlocks.md)

    [17.7.6 Transaction Scheduling](innodb-transaction-scheduling.md)

[17.8 InnoDB Configuration](innodb-configuration.md)
:   [17.8.1 InnoDB Startup Configuration](innodb-init-startup-configuration.md)

    [17.8.2 Configuring InnoDB for Read-Only Operation](innodb-read-only-instance.md)

    [17.8.3 InnoDB Buffer Pool Configuration](innodb-performance-buffer-pool.md)

    [17.8.4 Configuring Thread Concurrency for InnoDB](innodb-performance-thread_concurrency.md)

    [17.8.5 Configuring the Number of Background InnoDB I/O Threads](innodb-performance-multiple_io_threads.md)

    [17.8.6 Using Asynchronous I/O on Linux](innodb-linux-native-aio.md)

    [17.8.7 Configuring InnoDB I/O Capacity](innodb-configuring-io-capacity.md)

    [17.8.8 Configuring Spin Lock Polling](innodb-performance-spin_lock_polling.md)

    [17.8.9 Purge Configuration](innodb-purge-configuration.md)

    [17.8.10 Configuring Optimizer Statistics for InnoDB](innodb-performance-optimizer-statistics.md)

    [17.8.11 Configuring the Merge Threshold for Index Pages](index-page-merge-threshold.md)

    [17.8.12 Enabling Automatic InnoDB Configuration for a Dedicated MySQL Server](innodb-dedicated-server.md)

[17.9 InnoDB Table and Page Compression](innodb-compression.md)
:   [17.9.1 InnoDB Table Compression](innodb-table-compression.md)

    [17.9.2 InnoDB Page Compression](innodb-page-compression.md)

[17.10 InnoDB Row Formats](innodb-row-format.md)

[17.11 InnoDB Disk I/O and File Space Management](innodb-disk-management.md)
:   [17.11.1 InnoDB Disk I/O](innodb-disk-io.md)

    [17.11.2 File Space Management](innodb-file-space.md)

    [17.11.3 InnoDB Checkpoints](innodb-checkpoints.md)

    [17.11.4 Defragmenting a Table](innodb-file-defragmenting.md)

    [17.11.5 Reclaiming Disk Space with TRUNCATE TABLE](innodb-truncate-table-reclaim-space.md)

[17.12 InnoDB and Online DDL](innodb-online-ddl.md)
:   [17.12.1 Online DDL Operations](innodb-online-ddl-operations.md)

    [17.12.2 Online DDL Performance and Concurrency](innodb-online-ddl-performance.md)

    [17.12.3 Online DDL Space Requirements](innodb-online-ddl-space-requirements.md)

    [17.12.4 Online DDL Memory Management](online-ddl-memory-management.md)

    [17.12.5 Configuring Parallel Threads for Online DDL Operations](online-ddl-parallel-thread-configuration.md)

    [17.12.6 Simplifying DDL Statements with Online DDL](innodb-online-ddl-single-multi.md)

    [17.12.7 Online DDL Failure Conditions](innodb-online-ddl-failure-conditions.md)

    [17.12.8 Online DDL Limitations](innodb-online-ddl-limitations.md)

[17.13 InnoDB Data-at-Rest Encryption](innodb-data-encryption.md)

[17.14 InnoDB Startup Options and System Variables](innodb-parameters.md)

[17.15 InnoDB INFORMATION\_SCHEMA Tables](innodb-information-schema.md)
:   [17.15.1 InnoDB INFORMATION\_SCHEMA Tables about Compression](innodb-information-schema-compression-tables.md)

    [17.15.2 InnoDB INFORMATION\_SCHEMA Transaction and Locking Information](innodb-information-schema-transactions.md)

    [17.15.3 InnoDB INFORMATION\_SCHEMA Schema Object Tables](innodb-information-schema-system-tables.md)

    [17.15.4 InnoDB INFORMATION\_SCHEMA FULLTEXT Index Tables](innodb-information-schema-fulltext_index-tables.md)

    [17.15.5 InnoDB INFORMATION\_SCHEMA Buffer Pool Tables](innodb-information-schema-buffer-pool-tables.md)

    [17.15.6 InnoDB INFORMATION\_SCHEMA Metrics Table](innodb-information-schema-metrics-table.md)

    [17.15.7 InnoDB INFORMATION\_SCHEMA Temporary Table Info Table](innodb-information-schema-temp-table-info.md)

    [17.15.8 Retrieving InnoDB Tablespace Metadata from INFORMATION\_SCHEMA.FILES](innodb-information-schema-files-table.md)

[17.16 InnoDB Integration with MySQL Performance Schema](innodb-performance-schema.md)
:   [17.16.1 Monitoring ALTER TABLE Progress for InnoDB Tables Using Performance Schema](monitor-alter-table-performance-schema.md)

    [17.16.2 Monitoring InnoDB Mutex Waits Using Performance Schema](monitor-innodb-mutex-waits-performance-schema.md)

[17.17 InnoDB Monitors](innodb-monitors.md)
:   [17.17.1 InnoDB Monitor Types](innodb-monitor-types.md)

    [17.17.2 Enabling InnoDB Monitors](innodb-enabling-monitors.md)

    [17.17.3 InnoDB Standard Monitor and Lock Monitor Output](innodb-standard-monitor.md)

[17.18 InnoDB Backup and Recovery](innodb-backup-recovery.md)
:   [17.18.1 InnoDB Backup](innodb-backup.md)

    [17.18.2 InnoDB Recovery](innodb-recovery.md)

[17.19 InnoDB and MySQL Replication](innodb-and-mysql-replication.md)

[17.20 InnoDB memcached Plugin](innodb-memcached.md)
:   [17.20.1 Benefits of the InnoDB memcached Plugin](innodb-memcached-benefits.md)

    [17.20.2 InnoDB memcached Architecture](innodb-memcached-intro.md)

    [17.20.3 Setting Up the InnoDB memcached Plugin](innodb-memcached-setup.md)

    [17.20.4 InnoDB memcached Multiple get and Range Query Support](innodb-memcached-multiple-get-range-query.md)

    [17.20.5 Security Considerations for the InnoDB memcached Plugin](innodb-memcached-security.md)

    [17.20.6 Writing Applications for the InnoDB memcached Plugin](innodb-memcached-developing.md)

    [17.20.7 The InnoDB memcached Plugin and Replication](innodb-memcached-replication.md)

    [17.20.8 InnoDB memcached Plugin Internals](innodb-memcached-internals.md)

    [17.20.9 Troubleshooting the InnoDB memcached Plugin](innodb-memcached-troubleshoot.md)

[17.21 InnoDB Troubleshooting](innodb-troubleshooting.md)
:   [17.21.1 Troubleshooting InnoDB I/O Problems](error-creating-innodb.md)

    [17.21.2 Troubleshooting Recovery Failures](innodb-troubleshooting-recovery.md)

    [17.21.3 Forcing InnoDB Recovery](forcing-innodb-recovery.md)

    [17.21.4 Troubleshooting InnoDB Data Dictionary Operations](innodb-troubleshooting-datadict.md)

    [17.21.5 InnoDB Error Handling](innodb-error-handling.md)

[17.22 InnoDB Limits](innodb-limits.md)

[17.23 InnoDB Restrictions and Limitations](innodb-restrictions-limitations.md)
