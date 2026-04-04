#### 15.7.1.6 GRANT Statement

```sql
GRANT
    priv_type [(column_list)]
      [, priv_type [(column_list)]] ...
    ON [object_type] priv_level
    TO user_or_role [, user_or_role] ...
    [WITH GRANT OPTION]
    [AS user
        [WITH ROLE
            DEFAULT
          | NONE
          | ALL
          | ALL EXCEPT role [, role ] ...
          | role [, role ] ...
        ]
    ]
}

GRANT PROXY ON user_or_role
    TO user_or_role [, user_or_role] ...
    [WITH GRANT OPTION]

GRANT role [, role] ...
    TO user_or_role [, user_or_role] ...
    [WITH ADMIN OPTION]

object_type: {
    TABLE
  | FUNCTION
  | PROCEDURE
}

priv_level: {
    *
  | *.*
  | db_name.*
  | db_name.tbl_name
  | tbl_name
  | db_name.routine_name
}

user_or_role: {
    user (see Section 8.2.4, “Specifying Account Names”)
  | role (see Section 8.2.5, “Specifying Role Names”)
}
```

The [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement assigns
privileges and roles to MySQL user accounts and roles. There are
several aspects to the [`GRANT`](grant.md "15.7.1.6 GRANT Statement")
statement, described under the following topics:

- [GRANT General Overview](grant.md#grant-overview "GRANT General Overview")
- [Object Quoting Guidelines](grant.md#grant-quoting "Object Quoting Guidelines")
- [Account Names](grant.md#grant-accounts "Account Names")
- [Privileges Supported by MySQL](grant.md#grant-privileges "Privileges Supported by MySQL")
- [Global Privileges](grant.md#grant-global-privileges "Global Privileges")
- [Database Privileges](grant.md#grant-database-privileges "Database Privileges")
- [Table Privileges](grant.md#grant-table-privileges "Table Privileges")
- [Column Privileges](grant.md#grant-column-privileges "Column Privileges")
- [Stored Routine Privileges](grant.md#grant-routine-privileges "Stored Routine Privileges")
- [Proxy User Privileges](grant.md#grant-proxy-privileges "Proxy User Privileges")
- [Granting Roles](grant.md#grant-roles "Granting Roles")
- [The `AS` Clause and Privilege Restrictions](grant.md#grant-as "The AS Clause and Privilege Restrictions")
- [Other Account Characteristics](grant.md#grant-other-characteristics "Other Account Characteristics")
- [MySQL and Standard SQL Versions of GRANT](grant.md#grant-mysql-vs-standard-sql "MySQL and Standard SQL Versions of GRANT")

##### GRANT General Overview

The [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement enables
system administrators to grant privileges and roles, which can
be granted to user accounts and roles. These syntax
restrictions apply:

- [`GRANT`](grant.md "15.7.1.6 GRANT Statement") cannot mix granting
  both privileges and roles in the same statement. A given
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement must grant
  either privileges or roles.
- The `ON` clause distinguishes whether the
  statement grants privileges or roles:

  - With `ON`, the statement grants
    privileges.
  - Without `ON`, the statement grants
    roles.
  - It is permitted to assign both privileges and roles to
    an account, but you must use separate
    [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statements, each
    with syntax appropriate to what is to be granted.

For more information about roles, see [Section 8.2.10, “Using Roles”](roles.md "8.2.10 Using Roles").

To grant a privilege with
[`GRANT`](grant.md "15.7.1.6 GRANT Statement"), you must have the
[`GRANT OPTION`](privileges-provided.md#priv_grant-option) privilege, and you
must have the privileges that you are granting.
(Alternatively, if you have the
[`UPDATE`](privileges-provided.md#priv_update) privilege for the grant
tables in the `mysql` system schema, you can
grant any account any privilege.) When the
[`read_only`](server-system-variables.md#sysvar_read_only) system variable is
enabled, [`GRANT`](grant.md "15.7.1.6 GRANT Statement") additionally
requires the [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin)
privilege (or the deprecated
[`SUPER`](privileges-provided.md#priv_super) privilege).

[`GRANT`](grant.md "15.7.1.6 GRANT Statement") either succeeds for all
named users and roles or rolls back and has no effect if any
error occurs. The statement is written to the binary log only
if it succeeds for all named users and roles.

The [`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement") statement is related
to [`GRANT`](grant.md "15.7.1.6 GRANT Statement") and enables
administrators to remove account privileges. See
[Section 15.7.1.8, “REVOKE Statement”](revoke.md "15.7.1.8 REVOKE Statement").

Each account name uses the format described in
[Section 8.2.4, “Specifying Account Names”](account-names.md "8.2.4 Specifying Account Names"). Each role name uses the
format described in [Section 8.2.5, “Specifying Role Names”](role-names.md "8.2.5 Specifying Role Names"). For example:

```sql
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
GRANT SELECT ON world.* TO 'role3';
```

The host name part of the account or role name, if omitted,
defaults to `'%'`.

Normally, a database administrator first uses
[`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement") to create an
account and define its nonprivilege characteristics such as
its password, whether it uses secure connections, and limits
on access to server resources, then uses
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") to define its privileges.
[`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement") may be used to
change the nonprivilege characteristics of existing accounts.
For example:

```sql
CREATE USER 'jeffrey'@'localhost' IDENTIFIED BY 'password';
GRANT ALL ON db1.* TO 'jeffrey'@'localhost';
GRANT SELECT ON db2.invoice TO 'jeffrey'@'localhost';
ALTER USER 'jeffrey'@'localhost' WITH MAX_QUERIES_PER_HOUR 90;
```

From the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") program,
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") responds with
`Query OK, 0 rows affected` when executed
successfully. To determine what privileges result from the
operation, use [`SHOW GRANTS`](show-grants.md "15.7.7.21 SHOW GRANTS Statement"). See
[Section 15.7.7.21, “SHOW GRANTS Statement”](show-grants.md "15.7.7.21 SHOW GRANTS Statement").

Important

Under some circumstances,
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") may be recorded in
server logs or on the client side in a history file such as
`~/.mysql_history`, which means that
cleartext passwords may be read by anyone having read access
to that information. For information about the conditions
under which this occurs for the server logs and how to
control it, see [Section 8.1.2.3, “Passwords and Logging”](password-logging.md "8.1.2.3 Passwords and Logging"). For
similar information about client-side logging, see
[Section 6.5.1.3, “mysql Client Logging”](mysql-logging.md "6.5.1.3 mysql Client Logging").

[`GRANT`](grant.md "15.7.1.6 GRANT Statement") supports host names up to
255 characters long (60 characters prior to MySQL 8.0.17).
User names can be up to 32 characters. Database, table,
column, and routine names can be up to 64 characters.

Warning

*Do not attempt to change the permissible length
for user names by altering the `mysql.user`
system table. Doing so results in unpredictable behavior
which may even make it impossible for users to log in to the
MySQL server*. Never alter the structure of tables
in the `mysql` system schema in any manner
except by means of the procedure described in
[Chapter 3, *Upgrading MySQL*](upgrading.md "Chapter 3 Upgrading MySQL").

##### Object Quoting Guidelines

Several objects within [`GRANT`](grant.md "15.7.1.6 GRANT Statement")
statements are subject to quoting, although quoting is
optional in many cases: Account, role, database, table,
column, and routine names. For example, if a
*`user_name`* or
*`host_name`* value in an account name
is legal as an unquoted identifier, you need not quote it.
However, quotation marks are necessary to specify a
*`user_name`* string containing special
characters (such as `-`), or a
*`host_name`* string containing special
characters or wildcard characters such as `%`
(for example, `'test-user'@'%.com'`). Quote
the user name and host name separately.

To specify quoted values:

- Quote database, table, column, and routine names as
  identifiers.
- Quote user names and host names as identifiers or as
  strings.
- Quote passwords as strings.

For string-quoting and identifier-quoting guidelines, see
[Section 11.1.1, “String Literals”](string-literals.md "11.1.1 String Literals"), and
[Section 11.2, “Schema Object Names”](identifiers.md "11.2 Schema Object Names").

Important

The use of the wildcard characters `%` and
`_` as described in the next few paragraphs
is deprecated as of MySQL 8.0.35 and thus subject to removal
in a future version of MySQL.

The `_` and `%` wildcards
are permitted when specifying database names in
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") statements that grant
privileges at the database level (`GRANT ... ON
db_name.*`). This means,
for example, that to use a `_` character as
part of a database name, specify it using the
`\` escape character as `\_`
in the [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement, to
prevent the user from being able to access additional
databases matching the wildcard pattern (for example,
`` GRANT ... ON `foo\_bar`.* TO ... ``).

Issuing multiple `GRANT` statements
containing wildcards may not have the expected effect on DML
statements; when resolving grants involving wildcards, MySQL
takes only the first matching grant into consideration. In
other words, if a user has two database-level grants using
wildcards that match the same database, the grant which was
created first is applied. Consider the database
`db` and table `t` created
using the statements shown here:

```sql
mysql> CREATE DATABASE db;
Query OK, 1 row affected (0.01 sec)

mysql> CREATE TABLE db.t (c INT);
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO db.t VALUES ROW(1);
Query OK, 1 row affected (0.00 sec)
```

Next (assuming that the current account is the MySQL
`root` account or another account having the
necessary privileges), we create a user `u`
then issue two `GRANT` statements containing
wildcards, like this:

```sql
mysql> CREATE USER u;
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT SELECT ON `d_`.* TO u;
Query OK, 0 rows affected (0.01 sec)

mysql> GRANT INSERT ON `d%`.* TO u;
Query OK, 0 rows affected (0.00 sec)

mysql> EXIT
```

```terminal
Bye
```

If we end the session and then log in again with the
[**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") client, this time as
**u**, we see that this account has only the
privilege provided by the first matching grant, but not the
second:

```terminal
$> mysql -uu -hlocalhost
```

```sql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.46-tr Source distribution

Copyright (c) 2000, 2023, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input
statement.

mysql> TABLE db.t;
+------+
| c    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

mysql> INSERT INTO db.t VALUES ROW(2);
ERROR 1142 (42000): INSERT command denied to user 'u'@'localhost' for table 't'
```

In privilege assignments, MySQL interprets occurrences of
unescaped `_` and `%` SQL
wildcard characters in database names as literal characters
under these circumstances:

- When a database name is not used to grant privileges at
  the database level, but as a qualifier for granting
  privileges to some other object such as a table or routine
  (for example, `GRANT ... ON
  db_name.tbl_name`).
- Enabling [`partial_revokes`](server-system-variables.md#sysvar_partial_revokes)
  causes MySQL to interpret unescaped `_`
  and `%` wildcard characters in database
  names as literal characters, just as if they had been
  escaped as `\_` and
  `\%`. Because this changes how MySQL
  interprets privileges, it may be advisable to avoid
  unescaped wildcard characters in privilege assignments for
  installations where
  [`partial_revokes`](server-system-variables.md#sysvar_partial_revokes) may be
  enabled. For more information, see
  [Section 8.2.12, “Privilege Restriction Using Partial Revokes”](partial-revokes.md "8.2.12 Privilege Restriction Using Partial Revokes").

##### Account Names

A *`user`* value in a
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement indicates a
MySQL account to which the statement applies. To accommodate
granting rights to users from arbitrary hosts, MySQL supports
specifying the *`user`* value in the
form
`'user_name'@'host_name'`.

You can specify wildcards in the host name. For example,
`'user_name'@'%.example.com'`
applies to *`user_name`* for any host
in the `example.com` domain, and
`'user_name'@'198.51.100.%'`
applies to *`user_name`* for any host
in the `198.51.100` class C subnet.

The simple form
`'user_name'` is a
synonym for
`'user_name'@'%'`.

Note

MySQL automatically assigns all privileges granted to
`'username'@'%'`
to the
`'username'@'localhost'`
account as well. This behavior is deprecated in MySQL 8.0.35
and later MySQL 8.0 releases, and is subject to removal in a
future version of MySQL.

*MySQL does not support wildcards in user
names*. To refer to an anonymous user, specify an
account with an empty user name with the
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement:

```sql
GRANT ALL ON test.* TO ''@'localhost' ...;
```

In this case, any user who connects from the local host with
the correct password for the anonymous user is permitted
access, with the privileges associated with the anonymous-user
account.

For additional information about user name and host name
values in account names, see [Section 8.2.4, “Specifying Account Names”](account-names.md "8.2.4 Specifying Account Names").

Warning

If you permit local anonymous users to connect to the MySQL
server, you should also grant privileges to all local users
as
`'user_name'@'localhost'`.
Otherwise, the anonymous user account for
`localhost` in the
`mysql.user` system table is used when
named users try to log in to the MySQL server from the local
machine. For details, see
[Section 8.2.6, “Access Control, Stage 1: Connection Verification”](connection-access.md "8.2.6 Access Control, Stage 1: Connection Verification").

To determine whether this issue applies to you, execute the
following query, which lists any anonymous users:

```sql
SELECT Host, User FROM mysql.user WHERE User='';
```

To avoid the problem just described, delete the local
anonymous user account using this statement:

```sql
DROP USER ''@'localhost';
```

##### Privileges Supported by MySQL

The following tables summarize the permissible static and
dynamic *`priv_type`* privilege types
that can be specified for the
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") and
[`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement") statements, and the
levels at which each privilege can be granted. For additional
information about each privilege, see
[Section 8.2.2, “Privileges Provided by MySQL”](privileges-provided.md "8.2.2 Privileges Provided by MySQL"). For information about
the differences between static and dynamic privileges, see
[Static Versus Dynamic Privileges](privileges-provided.md#static-dynamic-privileges "Static Versus Dynamic Privileges").

**Table 15.11 Permissible Static Privileges for GRANT and REVOKE**

| Privilege | Meaning and Grantable Levels |
| --- | --- |
| [`ALL [PRIVILEGES]`](privileges-provided.md#priv_all) | Grant all privileges at specified access level except [`GRANT OPTION`](privileges-provided.md#priv_grant-option) and [`PROXY`](privileges-provided.md#priv_proxy). |
| [`ALTER`](privileges-provided.md#priv_alter) | Enable use of [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement"). Levels: Global, database, table. |
| [`ALTER ROUTINE`](privileges-provided.md#priv_alter-routine) | Enable stored routines to be altered or dropped. Levels: Global, database, routine. |
| [`CREATE`](privileges-provided.md#priv_create) | Enable database and table creation. Levels: Global, database, table. |
| [`CREATE ROLE`](privileges-provided.md#priv_create-role) | Enable role creation. Level: Global. |
| [`CREATE ROUTINE`](privileges-provided.md#priv_create-routine) | Enable stored routine creation. Levels: Global, database. |
| [`CREATE TABLESPACE`](privileges-provided.md#priv_create-tablespace) | Enable tablespaces and log file groups to be created, altered, or dropped. Level: Global. |
| [`CREATE TEMPORARY TABLES`](privileges-provided.md#priv_create-temporary-tables) | Enable use of [`CREATE TEMPORARY TABLE`](create-table.md "15.1.20 CREATE TABLE Statement"). Levels: Global, database. |
| [`CREATE USER`](privileges-provided.md#priv_create-user) | Enable use of [`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement"), [`DROP USER`](drop-user.md "15.7.1.5 DROP USER Statement"), [`RENAME USER`](rename-user.md "15.7.1.7 RENAME USER Statement"), and [`REVOKE ALL PRIVILEGES`](revoke.md "15.7.1.8 REVOKE Statement"). Level: Global. |
| [`CREATE VIEW`](privileges-provided.md#priv_create-view) | Enable views to be created or altered. Levels: Global, database, table. |
| [`DELETE`](privileges-provided.md#priv_delete) | Enable use of [`DELETE`](delete.md "15.2.2 DELETE Statement"). Level: Global, database, table. |
| [`DROP`](privileges-provided.md#priv_drop) | Enable databases, tables, and views to be dropped. Levels: Global, database, table. |
| [`DROP ROLE`](privileges-provided.md#priv_drop-role) | Enable roles to be dropped. Level: Global. |
| [`EVENT`](privileges-provided.md#priv_event) | Enable use of events for the Event Scheduler. Levels: Global, database. |
| [`EXECUTE`](privileges-provided.md#priv_execute) | Enable the user to execute stored routines. Levels: Global, database, routine. |
| [`FILE`](privileges-provided.md#priv_file) | Enable the user to cause the server to read or write files. Level: Global. |
| [`GRANT OPTION`](privileges-provided.md#priv_grant-option) | Enable privileges to be granted to or removed from other accounts. Levels: Global, database, table, routine, proxy. |
| [`INDEX`](privileges-provided.md#priv_index) | Enable indexes to be created or dropped. Levels: Global, database, table. |
| [`INSERT`](privileges-provided.md#priv_insert) | Enable use of [`INSERT`](insert.md "15.2.7 INSERT Statement"). Levels: Global, database, table, column. |
| [`LOCK TABLES`](privileges-provided.md#priv_lock-tables) | Enable use of [`LOCK TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements") on tables for which you have the [`SELECT`](select.md "15.2.13 SELECT Statement") privilege. Levels: Global, database. |
| [`PROCESS`](privileges-provided.md#priv_process) | Enable the user to see all processes with [`SHOW PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement"). Level: Global. |
| [`PROXY`](privileges-provided.md#priv_proxy) | Enable user proxying. Level: From user to user. |
| [`REFERENCES`](privileges-provided.md#priv_references) | Enable foreign key creation. Levels: Global, database, table, column. |
| [`RELOAD`](privileges-provided.md#priv_reload) | Enable use of [`FLUSH`](flush.md "15.7.8.3 FLUSH Statement") operations. Level: Global. |
| [`REPLICATION CLIENT`](privileges-provided.md#priv_replication-client) | Enable the user to ask where source or replica servers are. Level: Global. |
| [`REPLICATION SLAVE`](privileges-provided.md#priv_replication-slave) | Enable replicas to read binary log events from the source. Level: Global. |
| [`SELECT`](privileges-provided.md#priv_select) | Enable use of [`SELECT`](select.md "15.2.13 SELECT Statement"). Levels: Global, database, table, column. |
| [`SHOW DATABASES`](privileges-provided.md#priv_show-databases) | Enable [`SHOW DATABASES`](show-databases.md "15.7.7.14 SHOW DATABASES Statement") to show all databases. Level: Global. |
| [`SHOW VIEW`](privileges-provided.md#priv_show-view) | Enable use of [`SHOW CREATE VIEW`](show-create-view.md "15.7.7.13 SHOW CREATE VIEW Statement"). Levels: Global, database, table. |
| [`SHUTDOWN`](privileges-provided.md#priv_shutdown) | Enable use of [**mysqladmin shutdown**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program"). Level: Global. |
| [`SUPER`](privileges-provided.md#priv_super) | Enable use of other administrative operations such as [`CHANGE REPLICATION SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement"), [`CHANGE MASTER TO`](change-master-to.md "15.4.2.1 CHANGE MASTER TO Statement"), [`KILL`](kill.md "15.7.8.4 KILL Statement"), [`PURGE BINARY LOGS`](purge-binary-logs.md "15.4.1.1 PURGE BINARY LOGS Statement"), [`SET GLOBAL`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment"), and [**mysqladmin debug**](mysqladmin.md "6.5.2 mysqladmin — A MySQL Server Administration Program") command. Level: Global. |
| [`TRIGGER`](privileges-provided.md#priv_trigger) | Enable trigger operations. Levels: Global, database, table. |
| [`UPDATE`](privileges-provided.md#priv_update) | Enable use of [`UPDATE`](update.md "15.2.17 UPDATE Statement"). Levels: Global, database, table, column. |
| [`USAGE`](privileges-provided.md#priv_usage) | Synonym for “no privileges” |

**Table 15.12 Permissible Dynamic Privileges for GRANT and REVOKE**

| Privilege | Meaning and Grantable Levels |
| --- | --- |
| [`APPLICATION_PASSWORD_ADMIN`](privileges-provided.md#priv_application-password-admin) | Enable dual password administration. Level: Global. |
| [`AUDIT_ABORT_EXEMPT`](privileges-provided.md#priv_audit-abort-exempt) | Allow queries blocked by audit log filter. Level: Global. |
| [`AUDIT_ADMIN`](privileges-provided.md#priv_audit-admin) | Enable audit log configuration. Level: Global. |
| [`AUTHENTICATION_POLICY_ADMIN`](privileges-provided.md#priv_authentication-policy-admin) | Enable authentication policy administration. Level: Global. |
| [`BACKUP_ADMIN`](privileges-provided.md#priv_backup-admin) | Enable backup administration. Level: Global. |
| [`BINLOG_ADMIN`](privileges-provided.md#priv_binlog-admin) | Enable binary log control. Level: Global. |
| [`BINLOG_ENCRYPTION_ADMIN`](privileges-provided.md#priv_binlog-encryption-admin) | Enable activation and deactivation of binary log encryption. Level: Global. |
| [`CLONE_ADMIN`](privileges-provided.md#priv_clone-admin) | Enable clone administration. Level: Global. |
| [`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) | Enable connection limit/restriction control. Level: Global. |
| [`ENCRYPTION_KEY_ADMIN`](privileges-provided.md#priv_encryption-key-admin) | Enable `InnoDB` key rotation. Level: Global. |
| [`FIREWALL_ADMIN`](privileges-provided.md#priv_firewall-admin) | Enable firewall rule administration, any user. Level: Global. |
| [`FIREWALL_EXEMPT`](privileges-provided.md#priv_firewall-exempt) | Exempt user from firewall restrictions. Level: Global. |
| [`FIREWALL_USER`](privileges-provided.md#priv_firewall-user) | Enable firewall rule administration, self. Level: Global. |
| [`FLUSH_OPTIMIZER_COSTS`](privileges-provided.md#priv_flush-optimizer-costs) | Enable optimizer cost reloading. Level: Global. |
| [`FLUSH_STATUS`](privileges-provided.md#priv_flush-status) | Enable status indicator flushing. Level: Global. |
| [`FLUSH_TABLES`](privileges-provided.md#priv_flush-tables) | Enable table flushing. Level: Global. |
| [`FLUSH_USER_RESOURCES`](privileges-provided.md#priv_flush-user-resources) | Enable user-resource flushing. Level: Global. |
| [`GROUP_REPLICATION_ADMIN`](privileges-provided.md#priv_group-replication-admin) | Enable Group Replication control. Level: Global. |
| [`INNODB_REDO_LOG_ARCHIVE`](privileges-provided.md#priv_innodb-redo-log-archive) | Enable redo log archiving administration. Level: Global. |
| [`INNODB_REDO_LOG_ENABLE`](privileges-provided.md#priv_innodb-redo-log-enable) | Enable or disable redo logging. Level: Global. |
| [`NDB_STORED_USER`](privileges-provided.md#priv_ndb-stored-user) | Enable sharing of user or role between SQL nodes (NDB Cluster). Level: Global. |
| [`PASSWORDLESS_USER_ADMIN`](privileges-provided.md#priv_passwordless-user-admin) | Enable passwordless user account administration. Level: Global. |
| [`PERSIST_RO_VARIABLES_ADMIN`](privileges-provided.md#priv_persist-ro-variables-admin) | Enable persisting read-only system variables. Level: Global. |
| [`REPLICATION_APPLIER`](privileges-provided.md#priv_replication-applier) | Act as the `PRIVILEGE_CHECKS_USER` for a replication channel. Level: Global. |
| [`REPLICATION_SLAVE_ADMIN`](privileges-provided.md#priv_replication-slave-admin) | Enable regular replication control. Level: Global. |
| [`RESOURCE_GROUP_ADMIN`](privileges-provided.md#priv_resource-group-admin) | Enable resource group administration. Level: Global. |
| [`RESOURCE_GROUP_USER`](privileges-provided.md#priv_resource-group-user) | Enable resource group administration. Level: Global. |
| [`ROLE_ADMIN`](privileges-provided.md#priv_role-admin) | Enable roles to be granted or revoked, use of `WITH ADMIN OPTION`. Level: Global. |
| [`SESSION_VARIABLES_ADMIN`](privileges-provided.md#priv_session-variables-admin) | Enable setting restricted session system variables. Level: Global. |
| [`SET_USER_ID`](privileges-provided.md#priv_set-user-id) | Enable setting non-self `DEFINER` values. Level: Global. |
| [`SHOW_ROUTINE`](privileges-provided.md#priv_show-routine) | Enable access to stored routine definitions. Level: Global. |
| [`SKIP_QUERY_REWRITE`](privileges-provided.md#priv_skip-query-rewrite) | Do not rewrite queries executed by this user. Level: Global. |
| [`SYSTEM_USER`](privileges-provided.md#priv_system-user) | Designate account as system account. Level: Global. |
| [`SYSTEM_VARIABLES_ADMIN`](privileges-provided.md#priv_system-variables-admin) | Enable modifying or persisting global system variables. Level: Global. |
| [`TABLE_ENCRYPTION_ADMIN`](privileges-provided.md#priv_table-encryption-admin) | Enable overriding default encryption settings. Level: Global. |
| [`TELEMETRY_LOG_ADMIN`](privileges-provided.md#priv_telemetry-log-admin) | Enable telemetry log configuration for MySQL HeatWave on AWS. Level: Global. |
| [`TP_CONNECTION_ADMIN`](privileges-provided.md#priv_tp-connection-admin) | Enable thread pool connection administration. Level: Global. |
| [`VERSION_TOKEN_ADMIN`](privileges-provided.md#priv_version-token-admin) | Enable use of Version Tokens functions. Level: Global. |
| [`XA_RECOVER_ADMIN`](privileges-provided.md#priv_xa-recover-admin) | Enable [`XA RECOVER`](xa-statements.md "15.3.8.1 XA Transaction SQL Statements") execution. Level: Global. |

A trigger is associated with a table. To create or drop a
trigger, you must have the
[`TRIGGER`](privileges-provided.md#priv_trigger) privilege for the
table, not the trigger.

In [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statements, the
[`ALL
[PRIVILEGES]`](privileges-provided.md#priv_all) or [`PROXY`](privileges-provided.md#priv_proxy)
privilege must be named by itself and cannot be specified
along with other privileges.
[`ALL
[PRIVILEGES]`](privileges-provided.md#priv_all) stands for all privileges available for
the level at which privileges are to be granted except for the
[`GRANT OPTION`](privileges-provided.md#priv_grant-option) and
[`PROXY`](privileges-provided.md#priv_proxy) privileges.

MySQL account information is stored in the tables of the
`mysql` system schema. For additional
details, consult [Section 8.2, “Access Control and Account Management”](access-control.md "8.2 Access Control and Account Management"), which
discusses the `mysql` system schema and the
access control system extensively.

If the grant tables hold privilege rows that contain
mixed-case database or table names and the
[`lower_case_table_names`](server-system-variables.md#sysvar_lower_case_table_names) system
variable is set to a nonzero value,
[`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement") cannot be used to revoke
these privileges. It is necessary in such cases to manipulate
the grant tables directly.
([`GRANT`](grant.md "15.7.1.6 GRANT Statement") does not create such
rows when
[`lower_case_table_names`](server-system-variables.md#sysvar_lower_case_table_names) is
set, but such rows might have been created prior to setting
that variable. The
[`lower_case_table_names`](server-system-variables.md#sysvar_lower_case_table_names)
setting can only be configured at server startup.)

Privileges can be granted at several levels, depending on the
syntax used for the `ON` clause. For
[`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement"), the same
`ON` syntax specifies which privileges to
remove.

For the global, database, table, and routine levels,
[`GRANT ALL`](grant.md "15.7.1.6 GRANT Statement")
assigns only the privileges that exist at the level you are
granting. For example, `GRANT ALL ON
db_name.*` is a
database-level statement, so it does not grant any global-only
privileges such as [`FILE`](privileges-provided.md#priv_file).
Granting [`ALL`](privileges-provided.md#priv_all) does not assign
the [`GRANT OPTION`](privileges-provided.md#priv_grant-option) or
[`PROXY`](privileges-provided.md#priv_proxy) privilege.

The *`object_type`* clause, if present,
should be specified as `TABLE`,
`FUNCTION`, or `PROCEDURE`
when the following object is a table, a stored function, or a
stored procedure.

The privileges that a user holds for a database, table,
column, or routine are formed additively as the logical
[`OR`](logical-operators.md#operator_or) of the account privileges at
each of the privilege levels, including the global level. It
is not possible to deny a privilege granted at a higher level
by absence of that privilege at a lower level. For example,
this statement grants the
[`SELECT`](privileges-provided.md#priv_select) and
[`INSERT`](privileges-provided.md#priv_insert) privileges globally:

```sql
GRANT SELECT, INSERT ON *.* TO u1;
```

The globally granted privileges apply to all databases,
tables, and columns, even though not granted at any of those
lower levels.

As of MySQL 8.0.16, it is possible to explicitly deny a
privilege granted at the global level by revoking it for
particular databases, if the
[`partial_revokes`](server-system-variables.md#sysvar_partial_revokes) system
variable is enabled:

```sql
GRANT SELECT, INSERT, UPDATE ON *.* TO u1;
REVOKE INSERT, UPDATE ON db1.* FROM u1;
```

The result of the preceding statements is that
[`SELECT`](privileges-provided.md#priv_select) applies globally to all
tables, whereas [`INSERT`](privileges-provided.md#priv_insert) and
[`UPDATE`](privileges-provided.md#priv_update) apply globally except to
tables in `db1`. Account access to
`db1` is read only.

Details of the privilege-checking procedure are presented in
[Section 8.2.7, “Access Control, Stage 2: Request Verification”](request-access.md "8.2.7 Access Control, Stage 2: Request Verification").

If you are using table, column, or routine privileges for even
one user, the server examines table, column, and routine
privileges for all users and this slows down MySQL a bit.
Similarly, if you limit the number of queries, updates, or
connections for any users, the server must monitor these
values.

MySQL enables you to grant privileges on databases or tables
that do not exist. For tables, the privileges to be granted
must include the [`CREATE`](privileges-provided.md#priv_create)
privilege. *This behavior is by design*,
and is intended to enable the database administrator to
prepare user accounts and privileges for databases or tables
that are to be created at a later time.

Important

*MySQL does not automatically revoke any privileges
when you drop a database or table*. However, if
you drop a routine, any routine-level privileges granted for
that routine are revoked.

##### Global Privileges

Global privileges are administrative or apply to all databases
on a given server. To assign global privileges, use
`ON *.*` syntax:

```sql
GRANT ALL ON *.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON *.* TO 'someuser'@'somehost';
```

The [`CREATE TABLESPACE`](privileges-provided.md#priv_create-tablespace),
[`CREATE USER`](privileges-provided.md#priv_create-user),
[`FILE`](privileges-provided.md#priv_file),
[`PROCESS`](privileges-provided.md#priv_process),
[`RELOAD`](privileges-provided.md#priv_reload),
[`REPLICATION CLIENT`](privileges-provided.md#priv_replication-client),
[`REPLICATION SLAVE`](privileges-provided.md#priv_replication-slave),
[`SHOW DATABASES`](privileges-provided.md#priv_show-databases),
[`SHUTDOWN`](privileges-provided.md#priv_shutdown), and
[`SUPER`](privileges-provided.md#priv_super),
[`CREATE ROLE`](privileges-provided.md#priv_create-role) and
[`DROP ROLE`](privileges-provided.md#priv_drop-role) static privileges are
administrative and can only be granted globally.

Dynamic privileges are all global and can only be granted
globally.

Other privileges can be granted globally or at more specific
levels.

The effect of [`GRANT OPTION`](privileges-provided.md#priv_grant-option)
granted at the global level differs for static and dynamic
privileges:

- [`GRANT OPTION`](privileges-provided.md#priv_grant-option) granted for
  any static global privilege applies to all static global
  privileges.
- [`GRANT OPTION`](privileges-provided.md#priv_grant-option) granted for
  any dynamic privilege applies only to that dynamic
  privilege.

`GRANT ALL` at the global level grants all
static global privileges and all currently registered dynamic
privileges. A dynamic privilege registered subsequent to
execution of the `GRANT` statement is not
granted retroactively to any account.

MySQL stores global privileges in the
`mysql.user` system table.

##### Database Privileges

Database privileges apply to all objects in a given database.
To assign database-level privileges, use `ON
db_name.*` syntax:

```sql
GRANT ALL ON mydb.* TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.* TO 'someuser'@'somehost';
```

If you use `ON *` syntax (rather than
`ON *.*`), privileges are assigned at the
database level for the default database. An error occurs if
there is no default database.

The [`CREATE`](privileges-provided.md#priv_create),
[`DROP`](privileges-provided.md#priv_drop),
[`EVENT`](privileges-provided.md#priv_event),
[`GRANT OPTION`](privileges-provided.md#priv_grant-option),
[`LOCK TABLES`](privileges-provided.md#priv_lock-tables), and
[`REFERENCES`](privileges-provided.md#priv_references) privileges can be
specified at the database level. Table or routine privileges
also can be specified at the database level, in which case
they apply to all tables or routines in the database.

MySQL stores database privileges in the
`mysql.db` system table.

##### Table Privileges

Table privileges apply to all columns in a given table. To
assign table-level privileges, use `ON
db_name.tbl_name` syntax:

```sql
GRANT ALL ON mydb.mytbl TO 'someuser'@'somehost';
GRANT SELECT, INSERT ON mydb.mytbl TO 'someuser'@'somehost';
```

If you specify *`tbl_name`* rather than
*`db_name.tbl_name`*, the statement
applies to *`tbl_name`* in the default
database. An error occurs if there is no default database.

The permissible *`priv_type`* values at
the table level are [`ALTER`](privileges-provided.md#priv_alter),
[`CREATE VIEW`](privileges-provided.md#priv_create-view),
[`CREATE`](privileges-provided.md#priv_create),
[`DELETE`](privileges-provided.md#priv_delete),
[`DROP`](privileges-provided.md#priv_drop),
[`GRANT OPTION`](privileges-provided.md#priv_grant-option),
[`INDEX`](privileges-provided.md#priv_index),
[`INSERT`](privileges-provided.md#priv_insert),
[`REFERENCES`](privileges-provided.md#priv_references),
[`SELECT`](privileges-provided.md#priv_select),
[`SHOW VIEW`](privileges-provided.md#priv_show-view),
[`TRIGGER`](privileges-provided.md#priv_trigger), and
[`UPDATE`](privileges-provided.md#priv_update).

Table-level privileges apply to base tables and views. They do
not apply to tables created with [`CREATE
TEMPORARY TABLE`](create-temporary-table.md "15.1.20.2 CREATE TEMPORARY TABLE Statement"), even if the table names match. For
information about `TEMPORARY` table
privileges, see [Section 15.1.20.2, “CREATE TEMPORARY TABLE Statement”](create-temporary-table.md "15.1.20.2 CREATE TEMPORARY TABLE Statement").

MySQL stores table privileges in the
`mysql.tables_priv` system table.

##### Column Privileges

Column privileges apply to single columns in a given table.
Each privilege to be granted at the column level must be
followed by the column or columns, enclosed within
parentheses.

```sql
GRANT SELECT (col1), INSERT (col1, col2) ON mydb.mytbl TO 'someuser'@'somehost';
```

The permissible *`priv_type`* values
for a column (that is, when you use a
*`column_list`* clause) are
[`INSERT`](privileges-provided.md#priv_insert),
[`REFERENCES`](privileges-provided.md#priv_references),
[`SELECT`](privileges-provided.md#priv_select), and
[`UPDATE`](privileges-provided.md#priv_update).

MySQL stores column privileges in the
`mysql.columns_priv` system table.

##### Stored Routine Privileges

The [`ALTER ROUTINE`](privileges-provided.md#priv_alter-routine),
[`CREATE ROUTINE`](privileges-provided.md#priv_create-routine),
[`EXECUTE`](privileges-provided.md#priv_execute), and
[`GRANT OPTION`](privileges-provided.md#priv_grant-option) privileges apply
to stored routines (procedures and functions). They can be
granted at the global and database levels. Except for
[`CREATE ROUTINE`](privileges-provided.md#priv_create-routine), these
privileges can be granted at the routine level for individual
routines.

```sql
GRANT CREATE ROUTINE ON mydb.* TO 'someuser'@'somehost';
GRANT EXECUTE ON PROCEDURE mydb.myproc TO 'someuser'@'somehost';
```

The permissible *`priv_type`* values at
the routine level are [`ALTER
ROUTINE`](privileges-provided.md#priv_alter-routine), [`EXECUTE`](privileges-provided.md#priv_execute), and
[`GRANT OPTION`](privileges-provided.md#priv_grant-option).
[`CREATE ROUTINE`](privileges-provided.md#priv_create-routine) is not a
routine-level privilege because you must have the privilege at
the global or database level to create a routine in the first
place.

MySQL stores routine-level privileges in the
`mysql.procs_priv` system table.

##### Proxy User Privileges

The [`PROXY`](privileges-provided.md#priv_proxy) privilege enables one
user to be a proxy for another. The proxy user impersonates or
takes the identity of the proxied user; that is, it assumes
the privileges of the proxied user.

```sql
GRANT PROXY ON 'localuser'@'localhost' TO 'externaluser'@'somehost';
```

When [`PROXY`](privileges-provided.md#priv_proxy) is granted, it must
be the only privilege named in the
[`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement, and the only
permitted `WITH` option is `WITH
GRANT OPTION`.

Proxying requires that the proxy user authenticate through a
plugin that returns the name of the proxied user to the server
when the proxy user connects, and that the proxy user have the
`PROXY` privilege for the proxied user. For
details and examples, see [Section 8.2.19, “Proxy Users”](proxy-users.md "8.2.19 Proxy Users").

MySQL stores proxy privileges in the
`mysql.proxies_priv` system table.

##### Granting Roles

`GRANT` syntax without an
`ON` clause grants roles rather than
individual privileges. A role is a named collection of
privileges; see [Section 8.2.10, “Using Roles”](roles.md "8.2.10 Using Roles"). For example:

```sql
GRANT 'role1', 'role2' TO 'user1'@'localhost', 'user2'@'localhost';
```

Each role to be granted must exist, as well as each user
account or role to which it is to be granted. As of MySQL
8.0.16, roles cannot be granted to anonymous users.

Granting a role does not automatically cause the role to be
active. For information about role activation and
inactivation, see [Activating Roles](roles.md#roles-activating "Activating Roles").

These privileges are required to grant roles:

- If you have the [`ROLE_ADMIN`](privileges-provided.md#priv_role-admin)
  privilege (or the deprecated
  [`SUPER`](privileges-provided.md#priv_super) privilege), you can
  grant or revoke any role to users or roles.
- If you were granted a role with a
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement that
  includes the `WITH ADMIN OPTION` clause,
  you become able to grant that role to other users or
  roles, or revoke it from other users or roles, as long as
  the role is active at such time as you subsequently grant
  or revoke it. This includes the ability to use
  `WITH ADMIN OPTION` itself.
- To grant a role that has the
  [`SYSTEM_USER`](privileges-provided.md#priv_system-user) privilege, you
  must have the [`SYSTEM_USER`](privileges-provided.md#priv_system-user)
  privilege.

It is possible to create circular references with
[`GRANT`](grant.md "15.7.1.6 GRANT Statement"). For example:

```sql
CREATE USER 'u1', 'u2';
CREATE ROLE 'r1', 'r2';

GRANT 'u1' TO 'u1';   -- simple loop: u1 => u1
GRANT 'r1' TO 'r1';   -- simple loop: r1 => r1

GRANT 'r2' TO 'u2';
GRANT 'u2' TO 'r2';   -- mixed user/role loop: u2 => r2 => u2
```

Circular grant references are permitted but add no new
privileges or roles to the grantee because a user or role
already has its privileges and roles.

##### The `AS` Clause and Privilege Restrictions

As of MySQL 8.0.16, [`GRANT`](grant.md "15.7.1.6 GRANT Statement") has
an `AS user [WITH
ROLE]` clause that specifies additional information
about the privilege context to use for statement execution.
This syntax is visible at the SQL level, although its primary
purpose is to enable uniform replication across all nodes of
grantor privilege restrictions imposed by partial revokes, by
causing those restrictions to appear in the binary log. For
information about partial revokes, see
[Section 8.2.12, “Privilege Restriction Using Partial Revokes”](partial-revokes.md "8.2.12 Privilege Restriction Using Partial Revokes").

When the `AS user`
clause is specified, statement execution takes into account
any privilege restrictions associated with the named user,
including all roles specified by `WITH ROLE`,
if present. The result is that the privileges actually granted
by the statement may be reduced relative to those specified.

These conditions apply to the `AS
user` clause:

- `AS` has an effect only when the named
  *`user`* has privilege restrictions
  (which implies that the
  [`partial_revokes`](server-system-variables.md#sysvar_partial_revokes) system
  variable is enabled).
- If `WITH ROLE` is given, all roles named
  must be granted to the named
  *`user`*.
- The named *`user`* should be a
  MySQL account specified as
  `'user_name'@'host_name'`,
  [`CURRENT_USER`](information-functions.md#function_current-user), or
  [`CURRENT_USER()`](information-functions.md#function_current-user). The current
  user may be named together with `WITH
  ROLE` for the case that the executing user wants
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") to execute with a set
  of roles applied that may differ from the roles active
  within the current session.
- `AS` cannot be used to gain privileges
  not possessed by the user who executes the
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement. The
  executing user must have at least the privileges to be
  granted, but the `AS` clause can only
  restrict the privileges granted, not escalate them.
- With respect to the privileges to be granted,
  `AS` cannot specify a user/role
  combination that has more privileges (fewer restrictions)
  than the user who executes the
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement. The
  `AS` user/role combination is permitted
  to have more privileges than the executing user, but only
  if the statement does not grant those additional
  privileges.
- `AS` is supported only for granting
  global privileges (`ON *.*`).
- `AS` is not supported for
  [`PROXY`](privileges-provided.md#priv_proxy) grants.

The following example illustrates the effect of the
`AS` clause. Create a user
`u1` that has some global privileges, as well
as restrictions on those privileges:

```sql
CREATE USER u1;
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO u1;
REVOKE INSERT, UPDATE ON schema1.* FROM u1;
REVOKE SELECT ON schema2.* FROM u1;
```

Also create a role `r1` that lifts some of
the privilege restrictions and grant the role to
`u1`:

```sql
CREATE ROLE r1;
GRANT INSERT ON schema1.* TO r1;
GRANT SELECT ON schema2.* TO r1;
GRANT r1 TO u1;
```

Now, using an account that has no privilege restrictions of
its own, grant to multiple users the same set of global
privileges, but each with different restrictions imposed by
the `AS` clause, and check which privileges
are actually granted.

- The [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement here
  has no `AS` clause, so the privileges
  granted are exactly those specified:

  ```sql
  mysql> CREATE USER u2;
  mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u2;
  mysql> SHOW GRANTS FOR u2;
  +-------------------------------------------------+
  | Grants for u2@%                                 |
  +-------------------------------------------------+
  | GRANT SELECT, INSERT, UPDATE ON *.* TO `u2`@`%` |
  +-------------------------------------------------+
  ```
- The [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement here
  has an `AS` clause, so the privileges
  granted are those specified but with the restrictions from
  `u1` applied:

  ```sql
  mysql> CREATE USER u3;
  mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u3 AS u1;
  mysql> SHOW GRANTS FOR u3;
  +----------------------------------------------------+
  | Grants for u3@%                                    |
  +----------------------------------------------------+
  | GRANT SELECT, INSERT, UPDATE ON *.* TO `u3`@`%`    |
  | REVOKE INSERT, UPDATE ON `schema1`.* FROM `u3`@`%` |
  | REVOKE SELECT ON `schema2`.* FROM `u3`@`%`         |
  +----------------------------------------------------+
  ```

  As mentioned previously, the `AS` clause
  can only add privilege restrictions; it cannot escalate
  privileges. Thus, although `u1` has the
  [`DELETE`](privileges-provided.md#priv_delete) privilege, that is
  not included in the privileges granted because the
  statement does not specify granting
  [`DELETE`](privileges-provided.md#priv_delete).
- The `AS` clause for the
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement here makes
  the role `r1` active for
  `u1`. That role lifts some of the
  restrictions on `u1`. Consequently, the
  privileges granted have some restrictions, but not so many
  as for the previous [`GRANT`](grant.md "15.7.1.6 GRANT Statement")
  statement:

  ```sql
  mysql> CREATE USER u4;
  mysql> GRANT SELECT, INSERT, UPDATE ON *.* TO u4 AS u1 WITH ROLE r1;
  mysql> SHOW GRANTS FOR u4;
  +-------------------------------------------------+
  | Grants for u4@%                                 |
  +-------------------------------------------------+
  | GRANT SELECT, INSERT, UPDATE ON *.* TO `u4`@`%` |
  | REVOKE UPDATE ON `schema1`.* FROM `u4`@`%`      |
  +-------------------------------------------------+
  ```

If a [`GRANT`](grant.md "15.7.1.6 GRANT Statement") statement includes
an `AS user`
clause, privilege restrictions on the user who executes the
statement are ignored (rather than applied as they would be in
the absence of an `AS` clause).

##### Other Account Characteristics

The optional `WITH` clause is used to enable
a user to grant privileges to other users. The `WITH
GRANT OPTION` clause gives the user the ability to
give to other users any privileges the user has at the
specified privilege level.

To grant the [`GRANT OPTION`](privileges-provided.md#priv_grant-option)
privilege to an account without otherwise changing its
privileges, do this:

```sql
GRANT USAGE ON *.* TO 'someuser'@'somehost' WITH GRANT OPTION;
```

Be careful to whom you give the [`GRANT
OPTION`](privileges-provided.md#priv_grant-option) privilege because two users with different
privileges may be able to combine privileges!

You cannot grant another user a privilege which you yourself
do not have; the [`GRANT OPTION`](privileges-provided.md#priv_grant-option)
privilege enables you to assign only those privileges which
you yourself possess.

Be aware that when you grant a user the
[`GRANT OPTION`](privileges-provided.md#priv_grant-option) privilege at a
particular privilege level, any privileges the user possesses
(or may be given in the future) at that level can also be
granted by that user to other users. Suppose that you grant a
user the [`INSERT`](privileges-provided.md#priv_insert) privilege on a
database. If you then grant the
[`SELECT`](privileges-provided.md#priv_select) privilege on the
database and specify `WITH GRANT OPTION`,
that user can give to other users not only the
[`SELECT`](privileges-provided.md#priv_select) privilege, but also
[`INSERT`](privileges-provided.md#priv_insert). If you then grant the
[`UPDATE`](privileges-provided.md#priv_update) privilege to the user on
the database, the user can grant
[`INSERT`](privileges-provided.md#priv_insert),
[`SELECT`](privileges-provided.md#priv_select), and
[`UPDATE`](privileges-provided.md#priv_update).

For a nonadministrative user, you should not grant the
[`ALTER`](privileges-provided.md#priv_alter) privilege globally or for
the `mysql` system schema. If you do that,
the user can try to subvert the privilege system by renaming
tables!

For additional information about security risks associated
with particular privileges, see
[Section 8.2.2, “Privileges Provided by MySQL”](privileges-provided.md "8.2.2 Privileges Provided by MySQL").

##### MySQL and Standard SQL Versions of GRANT

The biggest differences between the MySQL and standard SQL
versions of [`GRANT`](grant.md "15.7.1.6 GRANT Statement") are:

- MySQL associates privileges with the combination of a host
  name and user name and not with only a user name.
- Standard SQL does not have global or database-level
  privileges, nor does it support all the privilege types
  that MySQL supports.
- MySQL does not support the standard SQL
  `UNDER` privilege.
- Standard SQL privileges are structured in a hierarchical
  manner. If you remove a user, all privileges the user has
  been granted are revoked. This is also true in MySQL if
  you use [`DROP USER`](drop-user.md "15.7.1.5 DROP USER Statement"). See
  [Section 15.7.1.5, “DROP USER Statement”](drop-user.md "15.7.1.5 DROP USER Statement").
- In standard SQL, when you drop a table, all privileges for
  the table are revoked. In standard SQL, when you revoke a
  privilege, all privileges that were granted based on that
  privilege are also revoked. In MySQL, privileges can be
  dropped with [`DROP USER`](drop-user.md "15.7.1.5 DROP USER Statement") or
  [`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement") statements.
- In MySQL, it is possible to have the
  [`INSERT`](privileges-provided.md#priv_insert) privilege for only
  some of the columns in a table. In this case, you can
  still execute [`INSERT`](insert.md "15.2.7 INSERT Statement")
  statements on the table, provided that you insert values
  only for those columns for which you have the
  [`INSERT`](privileges-provided.md#priv_insert) privilege. The
  omitted columns are set to their implicit default values
  if strict SQL mode is not enabled. In strict mode, the
  statement is rejected if any of the omitted columns have
  no default value. (Standard SQL requires you to have the
  [`INSERT`](privileges-provided.md#priv_insert) privilege on all
  columns.) For information about strict SQL mode and
  implicit default values, see [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes"),
  and [Section 13.6, “Data Type Default Values”](data-type-defaults.md "13.6 Data Type Default Values").
