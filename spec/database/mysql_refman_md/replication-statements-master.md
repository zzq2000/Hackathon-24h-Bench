### 15.4.1 SQL Statements for Controlling Source Servers

[15.4.1.1 PURGE BINARY LOGS Statement](purge-binary-logs.md)

[15.4.1.2 RESET MASTER Statement](reset-master.md)

[15.4.1.3 SET sql\_log\_bin Statement](set-sql-log-bin.md)

This section discusses statements for managing replication source
servers. [Section 15.4.2, “SQL Statements for Controlling Replica Servers”](replication-statements-replica.md "15.4.2 SQL Statements for Controlling Replica Servers"),
discusses statements for managing replica servers.

In addition to the statements described here, the following
[`SHOW`](show.md "15.7.7 SHOW Statements") statements are used with
source servers in replication. For information about these
statements, see [Section 15.7.7, “SHOW Statements”](show.md "15.7.7 SHOW Statements").

- [`SHOW BINARY LOGS`](show-binary-logs.md "15.7.7.1 SHOW BINARY LOGS Statement")
- [`SHOW BINLOG EVENTS`](show-binlog-events.md "15.7.7.2 SHOW BINLOG EVENTS Statement")
- [`SHOW MASTER STATUS`](show-master-status.md "15.7.7.23 SHOW MASTER STATUS Statement")
- [`SHOW
  REPLICAS`](show-replicas.md "15.7.7.33 SHOW REPLICAS Statement") (or before MySQL 8.0.22,
  [`SHOW SLAVE
  HOSTS`](show-slave-hosts.md "15.7.7.34 SHOW SLAVE HOSTS | SHOW REPLICAS Statement"))
