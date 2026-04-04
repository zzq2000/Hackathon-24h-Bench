## 15.3 Transactional and Locking Statements

[15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements](commit.md)

[15.3.2 Statements That Cannot Be Rolled Back](cannot-roll-back.md)

[15.3.3 Statements That Cause an Implicit Commit](implicit-commit.md)

[15.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT Statements](savepoint.md)

[15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements](lock-instance-for-backup.md)

[15.3.6 LOCK TABLES and UNLOCK TABLES Statements](lock-tables.md)

[15.3.7 SET TRANSACTION Statement](set-transaction.md)

[15.3.8 XA Transactions](xa.md)

MySQL supports local transactions (within a given client session)
through statements such as
[`SET autocommit`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"),
[`START TRANSACTION`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"),
[`COMMIT`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"), and
[`ROLLBACK`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"). See
[Section 15.3.1, “START TRANSACTION, COMMIT, and ROLLBACK Statements”](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"). XA transaction support enables MySQL to
participate in distributed transactions as well. See
[Section 15.3.8, “XA Transactions”](xa.md "15.3.8 XA Transactions").
