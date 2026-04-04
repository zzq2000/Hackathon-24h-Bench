## A.5 MySQL 8.0 FAQ: Triggers

A.5.1. [Where can I find the documentation for MySQL 8.0 triggers?](faqs-triggers.md#faq-mysql-where-triggers-docs)

A.5.2. [Is there a discussion forum for MySQL Triggers?](faqs-triggers.md#faq-mysql-where-triggers-forum)

A.5.3. [Does MySQL have statement-level or row-level triggers?](faqs-triggers.md#faq-mysql-have-trigger-levels)

A.5.4. [Are there any default triggers?](faqs-triggers.md#faq-mysql-have-trigger-defaults)

A.5.5. [How are triggers managed in MySQL?](faqs-triggers.md#faq-mysql-how-triggers-managed)

A.5.6. [Is there a way to view all triggers in a given database?](faqs-triggers.md#faq-mysql-can-view-all-triggers)

A.5.7. [Where are triggers stored?](faqs-triggers.md#faq-mysql-how-triggers-stored)

A.5.8. [Can a trigger call a stored procedure?](faqs-triggers.md#faq-mysql-can-trigger-procedure)

A.5.9. [Can triggers access tables?](faqs-triggers.md#faq-mysql-can-triggers-tables)

A.5.10. [Can a table have multiple triggers with the same trigger event and action time?](faqs-triggers.md#faq-mysql-can-triggers-same-events)

A.5.11. [Is it possible for a trigger to update tables on a remote server?](faqs-triggers.md#faq-mysql-can-triggers-remote)

A.5.12. [Do triggers work with replication?](faqs-triggers.md#faq-mysql-can-triggers-replication)

A.5.13. [How are actions carried out through triggers on a source replicated to a replica?](faqs-triggers.md#faq-mysql-how-triggers-source-replica)

|  |  |
| --- | --- |
| **A.5.1.** | Where can I find the documentation for MySQL 8.0 triggers? |
|  | See [Section 27.3, “Using Triggers”](triggers.md "27.3 Using Triggers"). |
| **A.5.2.** | Is there a discussion forum for MySQL Triggers? |
|  | Yes. It is available at <https://forums.mysql.com/list.php?99>. |
| **A.5.3.** | Does MySQL have statement-level or row-level triggers? |
|  | All triggers are `FOR EACH ROW`; that is, the trigger is activated for each row that is inserted, updated, or deleted. MySQL does not support triggers using `FOR EACH STATEMENT`. |
| **A.5.4.** | Are there any default triggers? |
|  | Not explicitly. MySQL does have specific special behavior for some [`TIMESTAMP`](datetime.md "13.2.2 The DATE, DATETIME, and TIMESTAMP Types") columns, as well as for columns which are defined using `AUTO_INCREMENT`. |
| **A.5.5.** | How are triggers managed in MySQL? |
|  | Triggers can be created using the [`CREATE TRIGGER`](create-trigger.md "15.1.22 CREATE TRIGGER Statement") statement, and dropped using [`DROP TRIGGER`](drop-trigger.md "15.1.34 DROP TRIGGER Statement"). See [Section 15.1.22, “CREATE TRIGGER Statement”](create-trigger.md "15.1.22 CREATE TRIGGER Statement"), and [Section 15.1.34, “DROP TRIGGER Statement”](drop-trigger.md "15.1.34 DROP TRIGGER Statement"), for more about these statements.  Information about triggers can be obtained by querying the [`INFORMATION_SCHEMA.TRIGGERS`](information-schema-triggers-table.md "28.3.45 The INFORMATION_SCHEMA TRIGGERS Table") table. See [Section 28.3.45, “The INFORMATION\_SCHEMA TRIGGERS Table”](information-schema-triggers-table.md "28.3.45 The INFORMATION_SCHEMA TRIGGERS Table"). |
| **A.5.6.** | Is there a way to view all triggers in a given database? |
|  | Yes. You can obtain a listing of all triggers defined on database `dbname` using a query on the [`INFORMATION_SCHEMA.TRIGGERS`](information-schema-triggers-table.md "28.3.45 The INFORMATION_SCHEMA TRIGGERS Table") table such as the one shown here:   ```sql SELECT TRIGGER_NAME, EVENT_MANIPULATION, EVENT_OBJECT_TABLE, ACTION_STATEMENT     FROM INFORMATION_SCHEMA.TRIGGERS     WHERE TRIGGER_SCHEMA='dbname'; ```   For more information about this table, see [Section 28.3.45, “The INFORMATION\_SCHEMA TRIGGERS Table”](information-schema-triggers-table.md "28.3.45 The INFORMATION_SCHEMA TRIGGERS Table").  You can also use the [`SHOW TRIGGERS`](show-triggers.md "15.7.7.40 SHOW TRIGGERS Statement") statement, which is specific to MySQL. See [Section 15.7.7.40, “SHOW TRIGGERS Statement”](show-triggers.md "15.7.7.40 SHOW TRIGGERS Statement"). |
| **A.5.7.** | Where are triggers stored? |
|  | Triggers are stored in the `mysql.triggers` system table, which is part of the data dictionary. |
| **A.5.8.** | Can a trigger call a stored procedure? |
|  | Yes. |
| **A.5.9.** | Can triggers access tables? |
|  | A trigger can access both old and new data in its own table. A trigger can also affect other tables, but it is not permitted to modify a table that is already being used (for reading or writing) by the statement that invoked the function or trigger. |
| **A.5.10.** | Can a table have multiple triggers with the same trigger event and action time? |
|  | In MySQL 8.0, it is possible to define multiple triggers for a given table that have the same trigger event and action time. For example, you can have two `BEFORE UPDATE` triggers for a table. By default, triggers that have the same trigger event and action time activate in the order they were created. To affect trigger order, specify a clause after `FOR EACH ROW` that indicates `FOLLOWS` or `PRECEDES` and the name of an existing trigger that also has the same trigger event and action time. With `FOLLOWS`, the new trigger activates after the existing trigger. With `PRECEDES`, the new trigger activates before the existing trigger. |
| **A.5.11.** | Is it possible for a trigger to update tables on a remote server? |
|  | Yes. A table on a remote server could be updated using the `FEDERATED` storage engine. (See [Section 18.8, “The FEDERATED Storage Engine”](federated-storage-engine.md "18.8 The FEDERATED Storage Engine")). |
| **A.5.12.** | Do triggers work with replication? |
|  | Yes. However, the way in which they work depends whether you are using MySQL's “classic” statement-based or row-based replication format.  When using statement-based replication, triggers on the replica are executed by statements that are executed on the source (and replicated to the replica).  When using row-based replication, triggers are not executed on the replica due to statements that were run on the source and then replicated to the replica. Instead, when using row-based replication, the changes caused by executing the trigger on the source are applied on the replica.  For more information, see [Section 19.5.1.36, “Replication and Triggers”](replication-features-triggers.md "19.5.1.36 Replication and Triggers"). |
| **A.5.13.** | How are actions carried out through triggers on a source replicated to a replica? |
|  | Again, this depends on whether you are using statement-based or row-based replication.  **Statement-based replication.** First, the triggers that exist on a source must be re-created on the replica server. Once this is done, the replication flow works as any other standard DML statement that participates in replication. For example, consider a table `EMP` that has an `AFTER` insert trigger, which exists on a replication source server. The same `EMP` table and `AFTER` insert trigger exist on the replica server as well. The replication flow would be:  1. An [`INSERT`](insert.md "15.2.7 INSERT Statement") statement is made    to `EMP`. 2. The `AFTER` trigger on    `EMP` activates. 3. The [`INSERT`](insert.md "15.2.7 INSERT Statement") statement is    written to the binary log. 4. The replica picks up the    [`INSERT`](insert.md "15.2.7 INSERT Statement") statement to    `EMP` and executes it. 5. The `AFTER` trigger on    `EMP` that exists on the replica activates.  **Row-based replication.** When you use row-based replication, the changes caused by executing the trigger on the source are applied on the replica. However, the triggers themselves are not actually executed on the replica under row-based replication. This is because, if both the source and the replica applied the changes from the source and, in addition, the trigger causing these changes were applied on the replica, the changes would in effect be applied twice on the replica, leading to different data on the source and the replica.  In most cases, the outcome is the same for both row-based and statement-based replication. However, if you use different triggers on the source and replica, you cannot use row-based replication. (This is because the row-based format replicates the changes made by triggers executing on the source to the replicas, rather than the statements that caused the triggers to execute, and the corresponding triggers on the replica are not executed.) Instead, any statements causing such triggers to be executed must be replicated using statement-based replication.  For more information, see [Section 19.5.1.36, “Replication and Triggers”](replication-features-triggers.md "19.5.1.36 Replication and Triggers"). |
