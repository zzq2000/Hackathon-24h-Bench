### 15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements

```sql
LOCK INSTANCE FOR BACKUP

UNLOCK INSTANCE
```

`LOCK INSTANCE FOR BACKUP` acquires an
instance-level *backup lock* that permits DML
during an online backup while preventing operations that could
result in an inconsistent snapshot.

Executing the `LOCK INSTANCE FOR BACKUP`
statement requires the [`BACKUP_ADMIN`](privileges-provided.md#priv_backup-admin)
privilege. The [`BACKUP_ADMIN`](privileges-provided.md#priv_backup-admin)
privilege is automatically granted to users with the
[`RELOAD`](privileges-provided.md#priv_reload) privilege when performing an
in-place upgrade to MySQL 8.0 from an earlier
version.

Multiple sessions can hold a backup lock simultaneously.

`UNLOCK INSTANCE` releases a backup lock held by
the current session. A backup lock held by a session is also
released if the session is terminated.

`LOCK INSTANCE FOR BACKUP` prevents files from
being created, renamed, or removed. [`REPAIR
TABLE`](repair-table.md "15.7.3.5 REPAIR TABLE Statement") [`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement"),
[`OPTIMIZE TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement"), and account
management statements are blocked. See
[Section 15.7.1, “Account Management Statements”](account-management-statements.md "15.7.1 Account Management Statements"). Operations that
modify `InnoDB` files that are not recorded in
the `InnoDB` redo log are also blocked.

`LOCK INSTANCE FOR BACKUP` permits DDL operations
that only affect user-created temporary tables. In effect, files
that belong to user-created temporary tables can be created,
renamed, or removed while a backup lock is held. Creation of
binary log files is also permitted.

[`PURGE BINARY LOGS`](purge-binary-logs.md "15.4.1.1 PURGE BINARY LOGS Statement") should not be
issued while a [`LOCK INSTANCE FOR
BACKUP`](lock-instance-for-backup.md "15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements") statement is in effect for the instance, because
it contravenes the rules of the backup lock by removing files from
the server. From MySQL 8.0.28, this is disallowed.

A backup lock acquired by `LOCK INSTANCE FOR
BACKUP` is independent of transactional locks and locks
taken by
[`FLUSH
TABLES tbl_name [,
tbl_name] ... WITH READ LOCK`](flush.md#flush-tables-with-read-lock-with-list),
and the following sequences of statements are permitted:

```sql
LOCK INSTANCE FOR BACKUP;
FLUSH TABLES tbl_name [, tbl_name] ... WITH READ LOCK;
UNLOCK TABLES;
UNLOCK INSTANCE;
```

```sql
FLUSH TABLES tbl_name [, tbl_name] ... WITH READ LOCK;
LOCK INSTANCE FOR BACKUP;
UNLOCK INSTANCE;
UNLOCK TABLES;
```

The [`lock_wait_timeout`](server-system-variables.md#sysvar_lock_wait_timeout) setting
defines the amount of time that a `LOCK INSTANCE FOR
BACKUP` statement waits to acquire a lock before giving
up.
