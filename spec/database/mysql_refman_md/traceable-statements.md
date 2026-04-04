### 10.15.3 Traceable Statements

Statements which are traceable are listed here:

- [`SELECT`](select.md "15.2.13 SELECT Statement")
- [`INSERT`](insert.md "15.2.7 INSERT Statement")
- [`REPLACE`](replace.md "15.2.12 REPLACE Statement")
- [`UPDATE`](update.md "15.2.17 UPDATE Statement")
- [`DELETE`](delete.md "15.2.2 DELETE Statement")
- [`EXPLAIN`](explain.md "15.8.2 EXPLAIN Statement") with any of the
  preceding statements
- [`SET`](set-statement.md "15.7.6 SET Statements")
- [`DO`](do.md "15.2.3 DO Statement")
- [`DECLARE`](declare.md "15.6.3 DECLARE Statement"),
  [`CASE`](case.md "15.6.5.1 CASE Statement"),
  [`IF`](if.md "15.6.5.2 IF Statement"), and
  [`RETURN`](return.md "15.6.5.7 RETURN Statement") as used in stored
  routines
- [`CALL`](call.md "15.2.1 CALL Statement")

Tracing is supported for both `INSERT` and
`REPLACE` statements using
`VALUES`, `VALUES ROW`, or
`SELECT`.

Traces of multi-table `UPDATE` and
`DELETE` statements are supported.

Tracing of `SET optimizer_trace` is not
supported.

For statements which are prepared and executed in separate steps,
preparation and execution are traced separately.
