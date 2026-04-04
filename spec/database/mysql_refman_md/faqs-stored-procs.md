## A.4 MySQL 8.0 FAQ: Stored Procedures and Functions

A.4.1. [Does MySQL support stored procedures and functions?](faqs-stored-procs.md#faq-mysql-have-procedures-functions)

A.4.2. [Where can I find documentation for MySQL stored procedures and stored functions?](faqs-stored-procs.md#faq-mysql-where-procedures-functions-docs)

A.4.3. [Is there a discussion forum for MySQL stored procedures?](faqs-stored-procs.md#faq-mysql-where-procedures-forum)

A.4.4. [Where can I find the ANSI SQL 2003 specification for stored procedures?](faqs-stored-procs.md#faq-mysql-where-ansi-2003-spec)

A.4.5. [How do you manage stored routines?](faqs-stored-procs.md#faq-mysql-how-manage-routines)

A.4.6. [Is there a way to view all stored procedures and stored functions in a given database?](faqs-stored-procs.md#faq-mysql-how-view-procedures-functions)

A.4.7. [Where are stored procedures stored?](faqs-stored-procs.md#faq-mysql-where-procedures-stored)

A.4.8. [Is it possible to group stored procedures or stored functions into packages?](faqs-stored-procs.md#faq-mysql-how-group-procedures-functions)

A.4.9. [Can a stored procedure call another stored procedure?](faqs-stored-procs.md#faq-mysql-can-procedure-call-procedure)

A.4.10. [Can a stored procedure call a trigger?](faqs-stored-procs.md#faq-mysql-can-procedure-call-trigger)

A.4.11. [Can a stored procedure access tables?](faqs-stored-procs.md#faq-mysql-can-procedure-access-table)

A.4.12. [Do stored procedures have a statement for raising application errors?](faqs-stored-procs.md#faq-mysql-can-procedure-raise-error)

A.4.13. [Do stored procedures provide exception handling?](faqs-stored-procs.md#faq-mysql-have-exceptions)

A.4.14. [Can MySQL stored routines return result sets?](faqs-stored-procs.md#faq-mysql-can-routine-results)

A.4.15. [Is WITH RECOMPILE supported for stored procedures?](faqs-stored-procs.md#faq-mysql-have-with-recompile)

A.4.16. [Is there a MySQL equivalent to using mod\_plsql as a gateway on Apache to talk directly to a stored procedure in the database?](faqs-stored-procs.md#faq-mysql-have-mod-plsql)

A.4.17. [Can I pass an array as input to a stored procedure?](faqs-stored-procs.md#faq-mysql-can-procedure-array)

A.4.18. [Can I pass a cursor as an IN parameter to a stored procedure?](faqs-stored-procs.md#faq-mysql-can-pass-cursor-in)

A.4.19. [Can I return a cursor as an OUT parameter from a stored procedure?](faqs-stored-procs.md#faq-mysql-can-return-cursor-out)

A.4.20. [Can I print out a variable's value within a stored routine for debugging purposes?](faqs-stored-procs.md#faq-mysql-can-print-var-in-procedure)

A.4.21. [Can I commit or roll back transactions inside a stored procedure?](faqs-stored-procs.md#faq-mysql-can-rollback-transaction-procedure)

A.4.22. [Do MySQL stored procedures and functions work with replication?](faqs-stored-procs.md#faq-mysql-can-procedures-replicatation)

A.4.23. [Are stored procedures and functions created on a replication source server replicated to a replica?](faqs-stored-procs.md#faq-mysql-are-procedures-replicated)

A.4.24. [How are actions that take place inside stored procedures and functions replicated?](faqs-stored-procs.md#faq-mysql-how-procedures-replicated)

A.4.25. [Are there special security requirements for using stored procedures and functions together with replication?](faqs-stored-procs.md#faq-mysql-security-procedures-replication)

A.4.26. [What limitations exist for replicating stored procedure and function actions?](faqs-stored-procs.md#faq-mysql-limitations-procedures-replication)

A.4.27. [Do the preceding limitations affect the ability of MySQL to do point-in-time recovery?](faqs-stored-procs.md#faq-mysql-limitations-pit-recovery)

A.4.28. [What is being done to correct the aforementioned limitations?](faqs-stored-procs.md#faq-mysql-when-limitations-resolved)

|  |  |
| --- | --- |
| **A.4.1.** | Does MySQL support stored procedures and functions? |
|  | Yes. MySQL supports two types of stored routines, stored procedures, and stored functions. |
| **A.4.2.** | Where can I find documentation for MySQL stored procedures and stored functions? |
|  | See [Section 27.2, “Using Stored Routines”](stored-routines.md "27.2 Using Stored Routines"). |
| **A.4.3.** | Is there a discussion forum for MySQL stored procedures? |
|  | Yes. See <https://forums.mysql.com/list.php?98>. |
| **A.4.4.** | Where can I find the ANSI SQL 2003 specification for stored procedures? |
|  | Unfortunately, the official specifications are not freely available (ANSI makes them available for purchase). However, there are books, such as *SQL-99 Complete, Really* by Peter Gulutzan and Trudy Pelzer, that provide a comprehensive overview of the standard, including coverage of stored procedures. |
| **A.4.5.** | How do you manage stored routines? |
|  | It is always good practice to use a clear naming scheme for your stored routines. You can manage stored procedures with `CREATE [FUNCTION|PROCEDURE]`, `ALTER [FUNCTION|PROCEDURE]`, `DROP [FUNCTION|PROCEDURE]`, and `SHOW CREATE [FUNCTION|PROCEDURE]`. You can obtain information about existing stored procedures using the [`ROUTINES`](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table") table in the `INFORMATION_SCHEMA` database (see [Section 28.3.30, “The INFORMATION\_SCHEMA ROUTINES Table”](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table")). |
| **A.4.6.** | Is there a way to view all stored procedures and stored functions in a given database? |
|  | Yes. For a database named *`dbname`*, use this query on the [`INFORMATION_SCHEMA.ROUTINES`](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table") table:   ```sql SELECT ROUTINE_TYPE, ROUTINE_NAME     FROM INFORMATION_SCHEMA.ROUTINES     WHERE ROUTINE_SCHEMA='dbname'; ```   For more information, see [Section 28.3.30, “The INFORMATION\_SCHEMA ROUTINES Table”](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table").  The body of a stored routine can be viewed using [`SHOW CREATE FUNCTION`](show-create-function.md "15.7.7.8 SHOW CREATE FUNCTION Statement") (for a stored function) or [`SHOW CREATE PROCEDURE`](show-create-procedure.md "15.7.7.9 SHOW CREATE PROCEDURE Statement") (for a stored procedure). See [Section 15.7.7.9, “SHOW CREATE PROCEDURE Statement”](show-create-procedure.md "15.7.7.9 SHOW CREATE PROCEDURE Statement"), for more information. |
| **A.4.7.** | Where are stored procedures stored? |
|  | Stored procedures are stored in the `mysql.routines` and `mysql.parameters` tables, which are part of the data dictionary. You cannot access these tables directly. Instead, query the `INFORMATION_SCHEMA` [`ROUTINES`](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table") and [`PARAMETERS`](information-schema-parameters-table.md "28.3.20 The INFORMATION_SCHEMA PARAMETERS Table") tables. See [Section 28.3.30, “The INFORMATION\_SCHEMA ROUTINES Table”](information-schema-routines-table.md "28.3.30 The INFORMATION_SCHEMA ROUTINES Table"), and [Section 28.3.20, “The INFORMATION\_SCHEMA PARAMETERS Table”](information-schema-parameters-table.md "28.3.20 The INFORMATION_SCHEMA PARAMETERS Table").  You can also use [`SHOW CREATE FUNCTION`](show-create-function.md "15.7.7.8 SHOW CREATE FUNCTION Statement") to obtain information about stored functions, and [`SHOW CREATE PROCEDURE`](show-create-procedure.md "15.7.7.9 SHOW CREATE PROCEDURE Statement") to obtain information about stored procedures. See [Section 15.7.7.9, “SHOW CREATE PROCEDURE Statement”](show-create-procedure.md "15.7.7.9 SHOW CREATE PROCEDURE Statement"). |
| **A.4.8.** | Is it possible to group stored procedures or stored functions into packages? |
|  | No. This is not supported in MySQL. |
| **A.4.9.** | Can a stored procedure call another stored procedure? |
|  | Yes. |
| **A.4.10.** | Can a stored procedure call a trigger? |
|  | A stored procedure can execute an SQL statement, such as an [`UPDATE`](update.md "15.2.17 UPDATE Statement"), that causes a trigger to activate. |
| **A.4.11.** | Can a stored procedure access tables? |
|  | Yes. A stored procedure can access one or more tables as required. |
| **A.4.12.** | Do stored procedures have a statement for raising application errors? |
|  | Yes. MySQL implements the SQL standard `SIGNAL` and `RESIGNAL` statements. See [Section 15.6.7, “Condition Handling”](condition-handling.md "15.6.7 Condition Handling"). |
| **A.4.13.** | Do stored procedures provide exception handling? |
|  | MySQL implements [`HANDLER`](handler.md "15.2.5 HANDLER Statement") definitions according to the SQL standard. See [Section 15.6.7.2, “DECLARE ... HANDLER Statement”](declare-handler.md "15.6.7.2 DECLARE ... HANDLER Statement"), for details. |
| **A.4.14.** | Can MySQL stored routines return result sets? |
|  | *Stored procedures* can, but stored functions cannot. If you perform an ordinary [`SELECT`](select.md "15.2.13 SELECT Statement") inside a stored procedure, the result set is returned directly to the client. You need to use the MySQL 4.1 (or higher) client/server protocol for this to work. This means that, for example, in PHP, you need to use the `mysqli` extension rather than the old `mysql` extension. |
| **A.4.15.** | Is `WITH RECOMPILE` supported for stored procedures? |
|  | No. |
| **A.4.16.** | Is there a MySQL equivalent to using `mod_plsql` as a gateway on Apache to talk directly to a stored procedure in the database? |
|  | There is no equivalent in MySQL. |
| **A.4.17.** | Can I pass an array as input to a stored procedure? |
|  | No. |
| **A.4.18.** | Can I pass a cursor as an `IN` parameter to a stored procedure? |
|  | Cursors are only available inside stored procedures. |
| **A.4.19.** | Can I return a cursor as an `OUT` parameter from a stored procedure? |
|  | Cursors are only available inside stored procedures. However, if you do not open a cursor on a [`SELECT`](select.md "15.2.13 SELECT Statement"), the result is sent directly to the client. You can also `SELECT INTO` variables. See [Section 15.2.13, “SELECT Statement”](select.md "15.2.13 SELECT Statement"). |
| **A.4.20.** | Can I print out a variable's value within a stored routine for debugging purposes? |
|  | Yes, you can do this in a *stored procedure*, but not in a stored function. If you perform an ordinary [`SELECT`](select.md "15.2.13 SELECT Statement") inside a stored procedure, the result set is returned directly to the client. You must use the MySQL 4.1 (or above) client/server protocol for this to work. This means that, for example, in PHP, you need to use the `mysqli` extension rather than the old `mysql` extension. |
| **A.4.21.** | Can I commit or roll back transactions inside a stored procedure? |
|  | Yes. However, you cannot perform transactional operations within a stored function. |
| **A.4.22.** | Do MySQL stored procedures and functions work with replication? |
|  | Yes, standard actions carried out in stored procedures and functions are replicated from a replication source server to a replica. There are a few limitations that are described in detail in [Section 27.7, “Stored Program Binary Logging”](stored-programs-logging.md "27.7 Stored Program Binary Logging"). |
| **A.4.23.** | Are stored procedures and functions created on a replication source server replicated to a replica? |
|  | Yes, creation of stored procedures and functions carried out through normal DDL statements on a replication source server are replicated to a replica, so that the objects exist on both servers. `ALTER` and `DROP` statements for stored procedures and functions are also replicated. |
| **A.4.24.** | How are actions that take place inside stored procedures and functions replicated? |
|  | MySQL records each DML event that occurs in a stored procedure and replicates those individual actions to a replica. The actual calls made to execute stored procedures are not replicated.  Stored functions that change data are logged as function invocations, not as the DML events that occur inside each function. |
| **A.4.25.** | Are there special security requirements for using stored procedures and functions together with replication? |
|  | Yes. Because a replica has authority to execute any statement read from a source's binary log, special security constraints exist for using stored functions with replication. If replication or binary logging in general (for the purpose of point-in-time recovery) is active, then MySQL DBAs have two security options open to them:  1. Any user wishing to create stored functions must be    granted the [`SUPER`](privileges-provided.md#priv_super)    privilege. 2. Alternatively, a DBA can set the    [`log_bin_trust_function_creators`](replication-options-binary-log.md#sysvar_log_bin_trust_function_creators)    system variable to 1, which enables anyone with the    standard [`CREATE ROUTINE`](privileges-provided.md#priv_create-routine)    privilege to create stored functions. |
| **A.4.26.** | What limitations exist for replicating stored procedure and function actions? |
|  | Nondeterministic (random) or time-based actions embedded in stored procedures may not replicate properly. By their very nature, randomly produced results are not predictable and cannot be exactly reproduced; therefore, random actions replicated to a replica do not mirror those performed on a source. Declaring stored functions to be `DETERMINISTIC` or setting the [`log_bin_trust_function_creators`](replication-options-binary-log.md#sysvar_log_bin_trust_function_creators) system variable to 0 keeps random operations producing random values from being invoked.  In addition, time-based actions cannot be reproduced on a replica because the timing of such actions in a stored procedure is not reproducible through the binary log used for replication. It records only DML events and does not factor in timing constraints.  Finally, nontransactional tables for which errors occur during large DML actions (such as bulk inserts) may experience replication issues in that a source may be partially updated from DML activity, but no updates are done to the replica because of the errors that occurred. A workaround is for a function's DML actions to be carried out with the `IGNORE` keyword so that updates on the source that cause errors are ignored and updates that do not cause errors are replicated to the replica. |
| **A.4.27.** | Do the preceding limitations affect the ability of MySQL to do point-in-time recovery? |
|  | The same limitations that affect replication do affect point-in-time recovery. |
| **A.4.28.** | What is being done to correct the aforementioned limitations? |
|  | You can choose either statement-based replication or row-based replication. The original replication implementation is based on statement-based binary logging. Row-based binary logging resolves the limitations mentioned earlier.  Mixed replication is also available (by starting the server with [`--binlog-format=mixed`](replication-options-binary-log.md#sysvar_binlog_format)). This hybrid form of replication “knows” whether statement-level replication can safely be used, or row-level replication is required.  For additional information, see [Section 19.2.1, “Replication Formats”](replication-formats.md "19.2.1 Replication Formats"). |
