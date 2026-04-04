#### 19.5.1.13 Replication and FLUSH

Some forms of the [`FLUSH`](flush.md "15.7.8.3 FLUSH Statement") statement
are not logged because they could cause problems if replicated
to a replica: [`FLUSH LOGS`](flush.md#flush-logs) and
[`FLUSH TABLES WITH READ LOCK`](flush.md#flush-tables-with-read-lock). For
a syntax example, see [Section 15.7.8.3, “FLUSH Statement”](flush.md "15.7.8.3 FLUSH Statement"). The
[`FLUSH TABLES`](flush.md#flush-tables),
[`ANALYZE TABLE`](analyze-table.md "15.7.3.1 ANALYZE TABLE Statement"),
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement"), and
[`REPAIR TABLE`](repair-table.md "15.7.3.5 REPAIR TABLE Statement") statements are
written to the binary log and thus replicated to replicas. This
is not normally a problem because these statements do not modify
table data.

However, this behavior can cause difficulties under certain
circumstances. If you replicate the privilege tables in the
`mysql` database and update those tables
directly without using [`GRANT`](grant.md "15.7.1.6 GRANT Statement"), you
must issue a [`FLUSH PRIVILEGES`](flush.md#flush-privileges) on
the replicas to put the new privileges into effect. In addition,
if you use [`FLUSH TABLES`](flush.md#flush-tables) when
renaming a `MyISAM` table that is part of a
`MERGE` table, you must issue
[`FLUSH TABLES`](flush.md#flush-tables) manually on the
replicas. These statements are written to the binary log unless
you specify `NO_WRITE_TO_BINLOG` or its alias
`LOCAL`.
