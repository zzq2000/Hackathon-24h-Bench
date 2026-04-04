### 10.8.4 Obtaining Execution Plan Information for a Named Connection

To obtain the execution plan for an explainable statement
executing in a named connection, use this statement:

```sql
EXPLAIN [options] FOR CONNECTION connection_id;
```

[`EXPLAIN FOR CONNECTION`](explain-for-connection.md "10.8.4 Obtaining Execution Plan Information for a Named Connection") returns
the [`EXPLAIN`](explain.md "15.8.2 EXPLAIN Statement") information that is
currently being used to execute a query in a given connection.
Because of changes to data (and supporting statistics) it may
produce a different result from running
[`EXPLAIN`](explain.md "15.8.2 EXPLAIN Statement") on the equivalent query
text. This difference in behavior can be useful in diagnosing
more transient performance problems. For example, if you are
running a statement in one session that is taking a long time to
complete, using [`EXPLAIN FOR
CONNECTION`](explain-for-connection.md "10.8.4 Obtaining Execution Plan Information for a Named Connection") in another session may yield useful
information about the cause of the delay.

*`connection_id`* is the connection
identifier, as obtained from the
`INFORMATION_SCHEMA`
[`PROCESSLIST`](information-schema-processlist-table.md "28.3.23 The INFORMATION_SCHEMA PROCESSLIST Table") table or the
[`SHOW PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement") statement. If
you have the [`PROCESS`](privileges-provided.md#priv_process) privilege,
you can specify the identifier for any connection. Otherwise,
you can specify the identifier only for your own connections. In
all cases, you must have sufficient privileges to explain the
query on the specified connection.

If the named connection is not executing a statement, the result
is empty. Otherwise, `EXPLAIN FOR CONNECTION`
applies only if the statement being executed in the named
connection is explainable. This includes
[`SELECT`](select.md "15.2.13 SELECT Statement"),
[`DELETE`](delete.md "15.2.2 DELETE Statement"),
[`INSERT`](insert.md "15.2.7 INSERT Statement"),
[`REPLACE`](replace.md "15.2.12 REPLACE Statement"), and
[`UPDATE`](update.md "15.2.17 UPDATE Statement"). (However,
`EXPLAIN FOR CONNECTION` does not work for
prepared statements, even prepared statements of those types.)

If the named connection is executing an explainable statement,
the output is what you would obtain by using
`EXPLAIN` on the statement itself.

If the named connection is executing a statement that is not
explainable, an error occurs. For example, you cannot name the
connection identifier for your current session because
`EXPLAIN` is not explainable:

```sql
mysql> SELECT CONNECTION_ID();
+-----------------+
| CONNECTION_ID() |
+-----------------+
|             373 |
+-----------------+
1 row in set (0.00 sec)

mysql> EXPLAIN FOR CONNECTION 373;
ERROR 1889 (HY000): EXPLAIN FOR CONNECTION command is supported
only for SELECT/UPDATE/INSERT/DELETE/REPLACE
```

The `Com_explain_other` status variable
indicates the number of
[`EXPLAIN FOR
CONNECTION`](explain.md "15.8.2 EXPLAIN Statement") statements executed.
