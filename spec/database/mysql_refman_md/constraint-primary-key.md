#### 1.6.3.1 PRIMARY KEY and UNIQUE Index Constraints

Normally, errors occur for data-change statements (such as
[`INSERT`](insert.md "15.2.7 INSERT Statement") or
[`UPDATE`](update.md "15.2.17 UPDATE Statement")) that would violate
primary-key, unique-key, or foreign-key constraints. If you
are using a transactional storage engine such as
`InnoDB`, MySQL automatically rolls back the
statement. If you are using a nontransactional storage engine,
MySQL stops processing the statement at the row for which the
error occurred and leaves any remaining rows unprocessed.

MySQL supports an `IGNORE` keyword for
[`INSERT`](insert.md "15.2.7 INSERT Statement"),
[`UPDATE`](update.md "15.2.17 UPDATE Statement"), and so forth. If you
use it, MySQL ignores primary-key or unique-key violations and
continues processing with the next row. See the section for
the statement that you are using ([Section 15.2.7, “INSERT Statement”](insert.md "15.2.7 INSERT Statement"),
[Section 15.2.17, “UPDATE Statement”](update.md "15.2.17 UPDATE Statement"), and so forth).

You can get information about the number of rows actually
inserted or updated with the
[`mysql_info()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-info.html) C API function.
You can also use the [`SHOW
WARNINGS`](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement") statement. See
[mysql\_info()](https://dev.mysql.com/doc/c-api/8.0/en/mysql-info.html), and
[Section 15.7.7.42, “SHOW WARNINGS Statement”](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement").

`InnoDB` and `NDB` tables
support foreign keys. See
[Section 1.6.3.2, “FOREIGN KEY Constraints”](constraint-foreign-key.md "1.6.3.2 FOREIGN KEY Constraints").
