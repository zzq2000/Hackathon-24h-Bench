### 17.1.3 Verifying that InnoDB is the Default Storage Engine

Issue the [`SHOW ENGINES`](show-engines.md "15.7.7.16 SHOW ENGINES Statement") statement to
view the available MySQL storage engines. Look for
`DEFAULT` in the `SUPPORT`
column.

```sql
mysql> SHOW ENGINES;
```

Alternatively, query the Information Schema
[`ENGINES`](information-schema-engines-table.md "28.3.13 The INFORMATION_SCHEMA ENGINES Table") table.

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.ENGINES;
```
