#### 19.5.1.22 Replication of the mysql System Schema

Data modification statements made to tables in the
`mysql` schema are replicated according to the
value of [`binlog_format`](replication-options-binary-log.md#sysvar_binlog_format); if this
value is `MIXED`, these statements are
replicated using row-based format. However, statements that
would normally update this information indirectly—such
[`GRANT`](grant.md "15.7.1.6 GRANT Statement"),
[`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement"), and statements
manipulating triggers, stored routines, and views—are
replicated to replicas using statement-based replication.
