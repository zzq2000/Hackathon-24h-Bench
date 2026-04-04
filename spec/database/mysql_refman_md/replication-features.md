### 19.5.1 Replication Features and Issues

[19.5.1.1 Replication and AUTO\_INCREMENT](replication-features-auto-increment.md)

[19.5.1.2 Replication and BLACKHOLE Tables](replication-features-blackhole.md)

[19.5.1.3 Replication and Character Sets](replication-features-charset.md)

[19.5.1.4 Replication and CHECKSUM TABLE](replication-features-checksum-table.md)

[19.5.1.5 Replication of CREATE SERVER, ALTER SERVER, and DROP SERVER](replication-features-create-alter-drop-server.md)

[19.5.1.6 Replication of CREATE ... IF NOT EXISTS Statements](replication-features-create-if-not-exists.md)

[19.5.1.7 Replication of CREATE TABLE ... SELECT Statements](replication-features-create-select.md)

[19.5.1.8 Replication of CURRENT\_USER()](replication-features-current-user.md)

[19.5.1.9 Replication with Differing Table Definitions on Source and Replica](replication-features-differing-tables.md)

[19.5.1.10 Replication and DIRECTORY Table Options](replication-features-directory.md)

[19.5.1.11 Replication of DROP ... IF EXISTS Statements](replication-features-drop-if-exists.md)

[19.5.1.12 Replication and Floating-Point Values](replication-features-floatvalues.md)

[19.5.1.13 Replication and FLUSH](replication-features-flush.md)

[19.5.1.14 Replication and System Functions](replication-features-functions.md)

[19.5.1.15 Replication and Fractional Seconds Support](replication-features-fractional-seconds.md)

[19.5.1.16 Replication of Invoked Features](replication-features-invoked.md)

[19.5.1.17 Replication of JSON Documents](replication-features-json.md)

[19.5.1.18 Replication and LIMIT](replication-features-limit.md)

[19.5.1.19 Replication and LOAD DATA](replication-features-load-data.md)

[19.5.1.20 Replication and max\_allowed\_packet](replication-features-max-allowed-packet.md)

[19.5.1.21 Replication and MEMORY Tables](replication-features-memory.md)

[19.5.1.22 Replication of the mysql System Schema](replication-features-mysqldb.md)

[19.5.1.23 Replication and the Query Optimizer](replication-features-optimizer.md)

[19.5.1.24 Replication and Partitioning](replication-features-partitioning.md)

[19.5.1.25 Replication and REPAIR TABLE](replication-features-repair-table.md)

[19.5.1.26 Replication and Reserved Words](replication-features-reserved-words.md)

[19.5.1.27 Replication and Row Searches](replication-features-row-searches.md)

[19.5.1.28 Replication and Source or Replica Shutdowns](replication-features-shutdowns.md)

[19.5.1.29 Replica Errors During Replication](replication-features-errors.md)

[19.5.1.30 Replication and Server SQL Mode](replication-features-sql-mode.md)

[19.5.1.31 Replication and Temporary Tables](replication-features-temptables.md)

[19.5.1.32 Replication Retries and Timeouts](replication-features-timeout.md)

[19.5.1.33 Replication and Time Zones](replication-features-timezone.md)

[19.5.1.34 Replication and Transaction Inconsistencies](replication-features-transaction-inconsistencies.md)

[19.5.1.35 Replication and Transactions](replication-features-transactions.md)

[19.5.1.36 Replication and Triggers](replication-features-triggers.md)

[19.5.1.37 Replication and TRUNCATE TABLE](replication-features-truncate.md)

[19.5.1.38 Replication and User Name Length](replication-features-user-names.md)

[19.5.1.39 Replication and Variables](replication-features-variables.md)

[19.5.1.40 Replication and Views](replication-features-views.md)

The following sections provide information about what is supported
and what is not in MySQL replication, and about specific issues
and situations that may occur when replicating certain statements.

Statement-based replication depends on compatibility at the SQL
level between the source and replica. In other words, successful
statement-based replication requires that any SQL features used be
supported by both the source and the replica servers. If you use a
feature on the source server that is available only in the current
version of MySQL, you cannot replicate to a replica that uses an
earlier version of MySQL. Such incompatibilities can also occur
within a release series as well as between versions.

If you are planning to use statement-based replication between
MySQL 8.0 and a previous MySQL release series, it is
a good idea to consult the edition of the *MySQL
Reference Manual* corresponding to the earlier release
series for information regarding the replication characteristics
of that series.

With MySQL's statement-based replication, there may be issues with
replicating stored routines or triggers. You can avoid these
issues by using MySQL's row-based replication instead. For a
detailed list of issues, see
[Section 27.7, “Stored Program Binary Logging”](stored-programs-logging.md "27.7 Stored Program Binary Logging"). For more information
about row-based logging and row-based replication, see
[Section 7.4.4.1, “Binary Logging Formats”](binary-log-formats.md "7.4.4.1 Binary Logging Formats"), and
[Section 19.2.1, “Replication Formats”](replication-formats.md "19.2.1 Replication Formats").

For additional information specific to replication and
`InnoDB`, see
[Section 17.19, “InnoDB and MySQL Replication”](innodb-and-mysql-replication.md "17.19 InnoDB and MySQL Replication"). For information
relating to replication with NDB Cluster, see
[Section 25.7, “NDB Cluster Replication”](mysql-cluster-replication.md "25.7 NDB Cluster Replication").
