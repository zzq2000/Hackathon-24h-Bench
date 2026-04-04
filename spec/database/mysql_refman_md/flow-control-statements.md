### 15.6.5 Flow Control Statements

[15.6.5.1 CASE Statement](case.md)

[15.6.5.2 IF Statement](if.md)

[15.6.5.3 ITERATE Statement](iterate.md)

[15.6.5.4 LEAVE Statement](leave.md)

[15.6.5.5 LOOP Statement](loop.md)

[15.6.5.6 REPEAT Statement](repeat.md)

[15.6.5.7 RETURN Statement](return.md)

[15.6.5.8 WHILE Statement](while.md)

MySQL supports the [`IF`](if.md "15.6.5.2 IF Statement"),
[`CASE`](case.md "15.6.5.1 CASE Statement"),
[`ITERATE`](iterate.md "15.6.5.3 ITERATE Statement"),
[`LEAVE`](leave.md "15.6.5.4 LEAVE Statement")
[`LOOP`](loop.md "15.6.5.5 LOOP Statement"),
[`WHILE`](while.md "15.6.5.8 WHILE Statement"), and
[`REPEAT`](repeat.md "15.6.5.6 REPEAT Statement") constructs for flow control
within stored programs. It also supports
[`RETURN`](return.md "15.6.5.7 RETURN Statement") within stored functions.

Many of these constructs contain other statements, as indicated by
the grammar specifications in the following sections. Such
constructs may be nested. For example, an
[`IF`](if.md "15.6.5.2 IF Statement") statement might contain a
[`WHILE`](while.md "15.6.5.8 WHILE Statement") loop, which itself contains a
[`CASE`](case.md "15.6.5.1 CASE Statement") statement.

MySQL does not support `FOR` loops.
