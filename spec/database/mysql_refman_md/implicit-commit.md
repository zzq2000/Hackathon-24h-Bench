### 15.3.3 Statements That Cause an Implicit Commit

The statements listed in this section (and any synonyms for them)
implicitly end any transaction active in the current session, as
if you had done a [`COMMIT`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements") before
executing the statement.

Most of these statements also cause an implicit commit after
executing. The intent is to handle each such statement in its own
special transaction. Transaction-control and locking statements
are exceptions: If an implicit commit occurs before execution,
another does not occur after.

- **Data definition language (DDL)
  statements that define or modify database objects.**
  [`ALTER EVENT`](alter-event.md "15.1.3 ALTER EVENT Statement"),
  [`ALTER FUNCTION`](alter-function.md "15.1.4 ALTER FUNCTION Statement"),
  [`ALTER PROCEDURE`](alter-procedure.md "15.1.7 ALTER PROCEDURE Statement"),
  [`ALTER SERVER`](alter-server.md "15.1.8 ALTER SERVER Statement"),
  [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement"),
  [`ALTER TABLESPACE`](alter-tablespace.md "15.1.10 ALTER TABLESPACE Statement"),
  [`ALTER VIEW`](alter-view.md "15.1.11 ALTER VIEW Statement"),
  [`CREATE DATABASE`](create-database.md "15.1.12 CREATE DATABASE Statement"),
  [`CREATE EVENT`](create-event.md "15.1.13 CREATE EVENT Statement"),
  [`CREATE FUNCTION`](create-function.md "15.1.14 CREATE FUNCTION Statement"),
  [`CREATE INDEX`](create-index.md "15.1.15 CREATE INDEX Statement"),
  [`CREATE PROCEDURE`](create-procedure.md "15.1.17 CREATE PROCEDURE and CREATE FUNCTION Statements"),
  [`CREATE ROLE`](create-role.md "15.7.1.2 CREATE ROLE Statement"),
  [`CREATE SERVER`](create-server.md "15.1.18 CREATE SERVER Statement"),
  [`CREATE SPATIAL REFERENCE
  SYSTEM`](create-spatial-reference-system.md "15.1.19 CREATE SPATIAL REFERENCE SYSTEM Statement"), [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement"),
  [`CREATE TABLESPACE`](create-tablespace.md "15.1.21 CREATE TABLESPACE Statement"),
  [`CREATE TRIGGER`](create-trigger.md "15.1.22 CREATE TRIGGER Statement"),
  [`CREATE VIEW`](create-view.md "15.1.23 CREATE VIEW Statement"),
  [`DROP DATABASE`](drop-database.md "15.1.24 DROP DATABASE Statement"),
  [`DROP EVENT`](drop-event.md "15.1.25 DROP EVENT Statement"),
  [`DROP FUNCTION`](drop-function.md "15.1.26 DROP FUNCTION Statement"),
  [`DROP INDEX`](drop-index.md "15.1.27 DROP INDEX Statement"),
  [`DROP PROCEDURE`](drop-procedure.md "15.1.29 DROP PROCEDURE and DROP FUNCTION Statements"),
  [`DROP ROLE`](drop-role.md "15.7.1.4 DROP ROLE Statement"),
  [`DROP SERVER`](drop-server.md "15.1.30 DROP SERVER Statement"),
  [`DROP SPATIAL REFERENCE SYSTEM`](drop-spatial-reference-system.md "15.1.31 DROP SPATIAL REFERENCE SYSTEM Statement"),
  [`DROP TABLE`](drop-table.md "15.1.32 DROP TABLE Statement"),
  [`DROP TABLESPACE`](drop-tablespace.md "15.1.33 DROP TABLESPACE Statement"),
  [`DROP TRIGGER`](drop-trigger.md "15.1.34 DROP TRIGGER Statement"),
  [`DROP VIEW`](drop-view.md "15.1.35 DROP VIEW Statement"),
  [`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement"),
  [`RENAME TABLE`](rename-table.md "15.1.36 RENAME TABLE Statement"),
  [`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement"),
  [`UNINSTALL PLUGIN`](uninstall-plugin.md "15.7.4.6 UNINSTALL PLUGIN Statement").

  [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") and
  [`DROP TABLE`](drop-table.md "15.1.32 DROP TABLE Statement") statements do not
  commit a transaction if the `TEMPORARY`
  keyword is used. (This does not apply to other operations on
  temporary tables such as [`ALTER
  TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement") and [`CREATE
  INDEX`](create-index.md "15.1.15 CREATE INDEX Statement"), which do cause a commit.) However, although
  no implicit commit occurs, neither can the statement be rolled
  back, which means that the use of such statements causes
  transactional atomicity to be violated. For example, if you
  use [`CREATE
  TEMPORARY TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") and then roll back the transaction,
  the table remains in existence.

  The [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statement in
  `InnoDB` is processed as a single
  transaction. This means that a
  [`ROLLBACK`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements")
  from the user does not undo [`CREATE
  TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") statements the user made during that
  transaction.

  [`CREATE TABLE ...
  SELECT`](create-table.md "15.1.20 CREATE TABLE Statement") causes an implicit commit before and after
  the statement is executed when you are creating nontemporary
  tables. (No commit occurs for `CREATE TEMPORARY TABLE
  ... SELECT`.)
- **Statements that implicitly use or modify
  tables in the `mysql` database.**
  [`ALTER USER`](alter-user.md "15.7.1.1 ALTER USER Statement"),
  [`CREATE USER`](create-user.md "15.7.1.3 CREATE USER Statement"),
  [`DROP USER`](drop-user.md "15.7.1.5 DROP USER Statement"),
  [`GRANT`](grant.md "15.7.1.6 GRANT Statement"),
  [`RENAME USER`](rename-user.md "15.7.1.7 RENAME USER Statement"),
  [`REVOKE`](revoke.md "15.7.1.8 REVOKE Statement"),
  [`SET PASSWORD`](set-password.md "15.7.1.10 SET PASSWORD Statement").
- **Transaction-control and locking
  statements.**
  [`BEGIN`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"),
  [`LOCK TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements"), `SET
  autocommit = 1` (if the value is not already 1),
  [`START
  TRANSACTION`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements"),
  [`UNLOCK
  TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements").

  [`UNLOCK
  TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements") commits a transaction only if any tables
  currently have been locked with [`LOCK
  TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements") to acquire nontransactional table locks. A
  commit does not occur for
  [`UNLOCK
  TABLES`](lock-tables.md "15.3.6 LOCK TABLES and UNLOCK TABLES Statements") following [`FLUSH TABLES
  WITH READ LOCK`](flush.md#flush-tables-with-read-lock) because the latter statement does not
  acquire table-level locks.

  Transactions cannot be nested. This is a consequence of the
  implicit commit performed for any current transaction when you
  issue a [`START
  TRANSACTION`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements") statement or one of its synonyms.

  Statements that cause an implicit commit cannot be used in an
  XA transaction while the transaction is in an
  `ACTIVE` state.

  The [`BEGIN`](commit.md "15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements")
  statement differs from the use of the `BEGIN`
  keyword that starts a
  [`BEGIN ...
  END`](begin-end.md "15.6.1 BEGIN ... END Compound Statement") compound statement. The latter does not cause an
  implicit commit. See [Section 15.6.1, “BEGIN ... END Compound Statement”](begin-end.md "15.6.1 BEGIN ... END Compound Statement").
- **Data loading statements.**
  [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement").
  [`LOAD DATA`](load-data.md "15.2.9 LOAD DATA Statement") causes an implicit
  commit only for tables using the
  [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine.
- **Administrative statements.**
  [`ANALYZE TABLE`](analyze-table.md "15.7.3.1 ANALYZE TABLE Statement"),
  [`CACHE INDEX`](cache-index.md "15.7.8.2 CACHE INDEX Statement"),
  [`CHECK TABLE`](check-table.md "15.7.3.2 CHECK TABLE Statement"),
  [`FLUSH`](flush.md "15.7.8.3 FLUSH Statement"),
  [`LOAD INDEX INTO
  CACHE`](load-index.md "15.7.8.5 LOAD INDEX INTO CACHE Statement"), [`OPTIMIZE
  TABLE`](optimize-table.md "15.7.3.4 OPTIMIZE TABLE Statement"), [`REPAIR TABLE`](repair-table.md "15.7.3.5 REPAIR TABLE Statement"),
  [`RESET`](reset.md "15.7.8.6 RESET Statement") (but not
  [`RESET PERSIST`](reset-persist.md "15.7.8.7 RESET PERSIST Statement")).
- **Replication control
  statements**.
  [`START
  REPLICA`](start-replica.md "15.4.2.6 START REPLICA Statement"),
  [`STOP
  REPLICA`](stop-replica.md "15.4.2.8 STOP REPLICA Statement"),
  [`RESET
  REPLICA`](reset-replica.md "15.4.2.4 RESET REPLICA Statement"), [`CHANGE REPLICATION
  SOURCE TO`](change-replication-source-to.md "15.4.2.3 CHANGE REPLICATION SOURCE TO Statement"), [`CHANGE MASTER
  TO`](change-master-to.md "15.4.2.1 CHANGE MASTER TO Statement"). The SLAVE keyword was replaced with REPLICA in
  MySQL 8.0.22.
