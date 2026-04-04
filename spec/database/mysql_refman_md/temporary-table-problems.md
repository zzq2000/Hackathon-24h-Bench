#### B.3.6.2 TEMPORARY Table Problems

Temporary tables created with
[`CREATE TEMPORARY
TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") have the following limitations:

- `TEMPORARY` tables are supported only by
  the `InnoDB`, `MEMORY`,
  `MyISAM`, and `MERGE`
  storage engines.
- Temporary tables are not supported for NDB Cluster.
- The [`SHOW TABLES`](show-tables.md "15.7.7.39 SHOW TABLES Statement") statement
  does not list `TEMPORARY` tables.
- To rename `TEMPORARY` tables,
  `RENAME TABLE` does not work. Use
  [`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement") instead:

  ```sql
  ALTER TABLE old_name RENAME new_name;
  ```
- You cannot refer to a `TEMPORARY` table
  more than once in the same query. For example, the
  following does not work:

  ```sql
  SELECT * FROM temp_table JOIN temp_table AS t2;
  ```

  The statement produces this error:

  ```none
  ERROR 1137: Can't reopen table: 'temp_table'
  ```

  You can work around this issue if your query permits use
  of a common table expression (CTE) rather than a
  `TEMPORARY` table. For example, this
  fails with the Can't reopen table
  error:

  ```sql
  CREATE TEMPORARY TABLE t SELECT 1 AS col_a, 2 AS col_b;
  SELECT * FROM t AS t1 JOIN t AS t2;
  ```

  To avoid the error, use a
  [`WITH`](with.md "15.2.20 WITH (Common Table Expressions)") clause that defines a
  CTE, rather than the `TEMPORARY` table:

  ```sql
  WITH cte AS (SELECT 1 AS col_a, 2 AS col_b)
  SELECT * FROM cte AS t1 JOIN cte AS t2;
  ```
- The Can't reopen table error also
  occurs if you refer to a temporary table multiple times in
  a stored function under different aliases, even if the
  references occur in different statements within the
  function. It may occur for temporary tables created
  outside stored functions and referred to across multiple
  calling and callee functions.
- If a `TEMPORARY` is created with the same
  name as an existing non-`TEMPORARY`
  table, the non-`TEMPORARY` table is
  hidden until the `TEMPORARY` table is
  dropped, even if the tables use different storage engines.
- There are known issues in using temporary tables with
  replication. See
  [Section 19.5.1.31, “Replication and Temporary Tables”](replication-features-temptables.md "19.5.1.31 Replication and Temporary Tables"), for
  more information.
