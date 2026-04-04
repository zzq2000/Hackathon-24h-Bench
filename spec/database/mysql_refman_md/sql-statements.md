# Chapter 15 SQL Statements

**Table of Contents**

[15.1 Data Definition Statements](sql-data-definition-statements.md)
:   [15.1.1 Atomic Data Definition Statement Support](atomic-ddl.md)

    [15.1.2 ALTER DATABASE Statement](alter-database.md)

    [15.1.3 ALTER EVENT Statement](alter-event.md)

    [15.1.4 ALTER FUNCTION Statement](alter-function.md)

    [15.1.5 ALTER INSTANCE Statement](alter-instance.md)

    [15.1.6 ALTER LOGFILE GROUP Statement](alter-logfile-group.md)

    [15.1.7 ALTER PROCEDURE Statement](alter-procedure.md)

    [15.1.8 ALTER SERVER Statement](alter-server.md)

    [15.1.9 ALTER TABLE Statement](alter-table.md)

    [15.1.10 ALTER TABLESPACE Statement](alter-tablespace.md)

    [15.1.11 ALTER VIEW Statement](alter-view.md)

    [15.1.12 CREATE DATABASE Statement](create-database.md)

    [15.1.13 CREATE EVENT Statement](create-event.md)

    [15.1.14 CREATE FUNCTION Statement](create-function.md)

    [15.1.15 CREATE INDEX Statement](create-index.md)

    [15.1.16 CREATE LOGFILE GROUP Statement](create-logfile-group.md)

    [15.1.17 CREATE PROCEDURE and CREATE FUNCTION Statements](create-procedure.md)

    [15.1.18 CREATE SERVER Statement](create-server.md)

    [15.1.19 CREATE SPATIAL REFERENCE SYSTEM Statement](create-spatial-reference-system.md)

    [15.1.20 CREATE TABLE Statement](create-table.md)

    [15.1.21 CREATE TABLESPACE Statement](create-tablespace.md)

    [15.1.22 CREATE TRIGGER Statement](create-trigger.md)

    [15.1.23 CREATE VIEW Statement](create-view.md)

    [15.1.24 DROP DATABASE Statement](drop-database.md)

    [15.1.25 DROP EVENT Statement](drop-event.md)

    [15.1.26 DROP FUNCTION Statement](drop-function.md)

    [15.1.27 DROP INDEX Statement](drop-index.md)

    [15.1.28 DROP LOGFILE GROUP Statement](drop-logfile-group.md)

    [15.1.29 DROP PROCEDURE and DROP FUNCTION Statements](drop-procedure.md)

    [15.1.30 DROP SERVER Statement](drop-server.md)

    [15.1.31 DROP SPATIAL REFERENCE SYSTEM Statement](drop-spatial-reference-system.md)

    [15.1.32 DROP TABLE Statement](drop-table.md)

    [15.1.33 DROP TABLESPACE Statement](drop-tablespace.md)

    [15.1.34 DROP TRIGGER Statement](drop-trigger.md)

    [15.1.35 DROP VIEW Statement](drop-view.md)

    [15.1.36 RENAME TABLE Statement](rename-table.md)

    [15.1.37 TRUNCATE TABLE Statement](truncate-table.md)

[15.2 Data Manipulation Statements](sql-data-manipulation-statements.md)
:   [15.2.1 CALL Statement](call.md)

    [15.2.2 DELETE Statement](delete.md)

    [15.2.3 DO Statement](do.md)

    [15.2.4 EXCEPT Clause](except.md)

    [15.2.5 HANDLER Statement](handler.md)

    [15.2.6 IMPORT TABLE Statement](import-table.md)

    [15.2.7 INSERT Statement](insert.md)

    [15.2.8 INTERSECT Clause](intersect.md)

    [15.2.9 LOAD DATA Statement](load-data.md)

    [15.2.10 LOAD XML Statement](load-xml.md)

    [15.2.11 Parenthesized Query Expressions](parenthesized-query-expressions.md)

    [15.2.12 REPLACE Statement](replace.md)

    [15.2.13 SELECT Statement](select.md)

    [15.2.14 Set Operations with UNION, INTERSECT, and EXCEPT](set-operations.md)

    [15.2.15 Subqueries](subqueries.md)

    [15.2.16 TABLE Statement](table.md)

    [15.2.17 UPDATE Statement](update.md)

    [15.2.18 UNION Clause](union.md)

    [15.2.19 VALUES Statement](values.md)

    [15.2.20 WITH (Common Table Expressions)](with.md)

[15.3 Transactional and Locking Statements](sql-transactional-statements.md)
:   [15.3.1 START TRANSACTION, COMMIT, and ROLLBACK Statements](commit.md)

    [15.3.2 Statements That Cannot Be Rolled Back](cannot-roll-back.md)

    [15.3.3 Statements That Cause an Implicit Commit](implicit-commit.md)

    [15.3.4 SAVEPOINT, ROLLBACK TO SAVEPOINT, and RELEASE SAVEPOINT Statements](savepoint.md)

    [15.3.5 LOCK INSTANCE FOR BACKUP and UNLOCK INSTANCE Statements](lock-instance-for-backup.md)

    [15.3.6 LOCK TABLES and UNLOCK TABLES Statements](lock-tables.md)

    [15.3.7 SET TRANSACTION Statement](set-transaction.md)

    [15.3.8 XA Transactions](xa.md)

[15.4 Replication Statements](sql-replication-statements.md)
:   [15.4.1 SQL Statements for Controlling Source Servers](replication-statements-master.md)

    [15.4.2 SQL Statements for Controlling Replica Servers](replication-statements-replica.md)

    [15.4.3 SQL Statements for Controlling Group Replication](replication-statements-group.md)

[15.5 Prepared Statements](sql-prepared-statements.md)
:   [15.5.1 PREPARE Statement](prepare.md)

    [15.5.2 EXECUTE Statement](execute.md)

    [15.5.3 DEALLOCATE PREPARE Statement](deallocate-prepare.md)

[15.6 Compound Statement Syntax](sql-compound-statements.md)
:   [15.6.1 BEGIN ... END Compound Statement](begin-end.md)

    [15.6.2 Statement Labels](statement-labels.md)

    [15.6.3 DECLARE Statement](declare.md)

    [15.6.4 Variables in Stored Programs](stored-program-variables.md)

    [15.6.5 Flow Control Statements](flow-control-statements.md)

    [15.6.6 Cursors](cursors.md)

    [15.6.7 Condition Handling](condition-handling.md)

    [15.6.8 Restrictions on Condition Handling](condition-handling-restrictions.md)

[15.7 Database Administration Statements](sql-server-administration-statements.md)
:   [15.7.1 Account Management Statements](account-management-statements.md)

    [15.7.2 Resource Group Management Statements](resource-group-statements.md)

    [15.7.3 Table Maintenance Statements](table-maintenance-statements.md)

    [15.7.4 Component, Plugin, and Loadable Function Statements](component-statements.md)

    [15.7.5 CLONE Statement](clone.md)

    [15.7.6 SET Statements](set-statement.md)

    [15.7.7 SHOW Statements](show.md)

    [15.7.8 Other Administrative Statements](other-administrative-statements.md)

[15.8 Utility Statements](sql-utility-statements.md)
:   [15.8.1 DESCRIBE Statement](describe.md)

    [15.8.2 EXPLAIN Statement](explain.md)

    [15.8.3 HELP Statement](help.md)

    [15.8.4 USE Statement](use.md)

This chapter describes the syntax for the
[SQL](glossary.md#glos_sql "SQL") statements supported by MySQL.
