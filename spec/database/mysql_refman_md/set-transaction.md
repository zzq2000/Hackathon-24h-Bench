### 15.3.7 SET TRANSACTION Statement

```sql
SET [GLOBAL | SESSION] TRANSACTION
    transaction_characteristic [, transaction_characteristic] ...

transaction_characteristic: {
    ISOLATION LEVEL level
  | access_mode
}

level: {
     REPEATABLE READ
   | READ COMMITTED
   | READ UNCOMMITTED
   | SERIALIZABLE
}

access_mode: {
     READ WRITE
   | READ ONLY
}
```

This statement specifies
[transaction](glossary.md#glos_transaction "transaction")
characteristics. It takes a list of one or more characteristic
values separated by commas. Each characteristic value sets the
transaction [isolation
level](glossary.md#glos_isolation_level "isolation level") or access mode. The isolation level is used for
operations on [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine") tables. The
access mode specifies whether transactions operate in read/write
or read-only mode.

In addition, [`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") can
include an optional `GLOBAL` or
`SESSION` keyword to indicate the scope of the
statement.

- [Transaction Isolation Levels](set-transaction.md#set-transaction-isolation-level "Transaction Isolation Levels")
- [Transaction Access Mode](set-transaction.md#set-transaction-access-mode "Transaction Access Mode")
- [Transaction Characteristic Scope](set-transaction.md#set-transaction-scope "Transaction Characteristic Scope")

#### Transaction Isolation Levels

To set the transaction isolation level, use an
`ISOLATION LEVEL
level` clause. It is not
permitted to specify multiple `ISOLATION LEVEL`
clauses in the same [`SET
TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") statement.

The default isolation level is
[`REPEATABLE READ`](innodb-transaction-isolation-levels.md#isolevel_repeatable-read). Other
permitted values are [`READ
COMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-committed), [`READ
UNCOMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-uncommitted), and
[`SERIALIZABLE`](innodb-transaction-isolation-levels.md#isolevel_serializable). For information
about these isolation levels, see
[Section 17.7.2.1, “Transaction Isolation Levels”](innodb-transaction-isolation-levels.md "17.7.2.1 Transaction Isolation Levels").

#### Transaction Access Mode

To set the transaction access mode, use a `READ
WRITE` or `READ ONLY` clause. It is
not permitted to specify multiple access-mode clauses in the
same [`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") statement.

By default, a transaction takes place in read/write mode, with
both reads and writes permitted to tables used in the
transaction. This mode may be specified explicitly using
[`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") with an access
mode of `READ WRITE`.

If the transaction access mode is set to `READ
ONLY`, changes to tables are prohibited. This may
enable storage engines to make performance improvements that are
possible when writes are not permitted.

In read-only mode, it remains possible to change tables created
with the `TEMPORARY` keyword using DML
statements. Changes made with DDL statements are not permitted,
just as with permanent tables.

The `READ WRITE` and `READ
ONLY` access modes also may be specified for an
individual transaction using the
[`START
TRANSACTION`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements") statement.

#### Transaction Characteristic Scope

You can set transaction characteristics globally, for the
current session, or for the next transaction only:

- With the `GLOBAL` keyword:

  - The statement applies globally for all subsequent
    sessions.
  - Existing sessions are unaffected.
- With the `SESSION` keyword:

  - The statement applies to all subsequent transactions
    performed within the current session.
  - The statement is permitted within transactions, but does
    not affect the current ongoing transaction.
  - If executed between transactions, the statement
    overrides any preceding statement that sets the
    next-transaction value of the named characteristics.
- Without any `SESSION` or
  `GLOBAL` keyword:

  - The statement applies only to the next single
    transaction performed within the session.
  - Subsequent transactions revert to using the session
    value of the named characteristics.
  - The statement is not permitted within transactions:

    ```sql
    mysql> START TRANSACTION;
    Query OK, 0 rows affected (0.02 sec)

    mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
    ERROR 1568 (25001): Transaction characteristics can't be changed
    while a transaction is in progress
    ```

A change to global transaction characteristics requires the
[`CONNECTION_ADMIN`](privileges-provided.md#priv_connection-admin) privilege (or
the deprecated [`SUPER`](privileges-provided.md#priv_super) privilege).
Any session is free to change its session characteristics (even
in the middle of a transaction), or the characteristics for its
next transaction (prior to the start of that transaction).

To set the global isolation level at server startup, use the
[`--transaction-isolation=level`](server-options.md#option_mysqld_transaction-isolation)
option on the command line or in an option file. Values of
*`level`* for this option use dashes
rather than spaces, so the permissible values are
[`READ-UNCOMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-uncommitted),
[`READ-COMMITTED`](innodb-transaction-isolation-levels.md#isolevel_read-committed),
[`REPEATABLE-READ`](innodb-transaction-isolation-levels.md#isolevel_repeatable-read), or
[`SERIALIZABLE`](innodb-transaction-isolation-levels.md#isolevel_serializable).

Similarly, to set the global transaction access mode at server
startup, use the
[`--transaction-read-only`](server-options.md#option_mysqld_transaction-read-only) option.
The default is `OFF` (read/write mode) but the
value can be set to `ON` for a mode of read
only.

For example, to set the isolation level to
[`REPEATABLE READ`](innodb-transaction-isolation-levels.md#isolevel_repeatable-read) and the
access mode to `READ WRITE`, use these lines in
the `[mysqld]` section of an option file:

```ini
[mysqld]
transaction-isolation = REPEATABLE-READ
transaction-read-only = OFF
```

At runtime, characteristics at the global, session, and
next-transaction scope levels can be set indirectly using the
[`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") statement, as
described previously. They can also be set directly using the
[`SET`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment")
statement to assign values to the
[`transaction_isolation`](server-system-variables.md#sysvar_transaction_isolation) and
[`transaction_read_only`](server-system-variables.md#sysvar_transaction_read_only) system
variables:

- [`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") permits
  optional `GLOBAL` and
  `SESSION` keywords for setting transaction
  characteristics at different scope levels.
- The
  [`SET`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment")
  statement for assigning values to the
  [`transaction_isolation`](server-system-variables.md#sysvar_transaction_isolation) and
  [`transaction_read_only`](server-system-variables.md#sysvar_transaction_read_only)
  system variables has syntaxes for setting these variables at
  different scope levels.

The following tables show the characteristic scope level set by
each [`SET TRANSACTION`](set-transaction.md "15.3.7 SET TRANSACTION Statement") and
variable-assignment syntax.

**Table 15.9 SET TRANSACTION Syntax for Transaction Characteristics**

| Syntax | Affected Characteristic Scope |
| --- | --- |
| `SET GLOBAL TRANSACTION transaction_characteristic` | Global |
| `SET SESSION TRANSACTION transaction_characteristic` | Session |
| `SET TRANSACTION transaction_characteristic` | Next transaction only |

**Table 15.10 SET Syntax for Transaction Characteristics**

| Syntax | Affected Characteristic Scope |
| --- | --- |
| `SET GLOBAL var_name = value` | Global |
| `SET @@GLOBAL.var_name = value` | Global |
| `SET PERSIST var_name = value` | Global |
| `SET @@PERSIST.var_name = value` | Global |
| `SET PERSIST_ONLY var_name = value` | No runtime effect |
| `SET @@PERSIST_ONLY.var_name = value` | No runtime effect |
| `SET SESSION var_name = value` | Session |
| `SET @@SESSION.var_name = value` | Session |
| `SET var_name = value` | Session |
| `SET @@var_name = value` | Next transaction only |

It is possible to check the global and session values of
transaction characteristics at runtime:

```sql
SELECT @@GLOBAL.transaction_isolation, @@GLOBAL.transaction_read_only;
SELECT @@SESSION.transaction_isolation, @@SESSION.transaction_read_only;
```
