## 13.1 Numeric Data Types

[13.1.1 Numeric Data Type Syntax](numeric-type-syntax.md)

[13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT](integer-types.md)

[13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC](fixed-point-types.md)

[13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE](floating-point-types.md)

[13.1.5 Bit-Value Type - BIT](bit-type.md)

[13.1.6 Numeric Type Attributes](numeric-type-attributes.md)

[13.1.7 Out-of-Range and Overflow Handling](out-of-range-and-overflow.md)

MySQL supports all standard SQL numeric data types. These types
include the exact numeric data types
([`INTEGER`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT"),
[`SMALLINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT"),
[`DECIMAL`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC"), and
[`NUMERIC`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC")), as well as the
approximate numeric data types
([`FLOAT`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE"),
[`REAL`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE"), and
[`DOUBLE PRECISION`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE")). The keyword
[`INT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") is a synonym for
[`INTEGER`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT"), and the keywords
[`DEC`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") and
[`FIXED`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") are synonyms for
[`DECIMAL`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC"). MySQL treats
[`DOUBLE`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") as a synonym for
[`DOUBLE PRECISION`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") (a nonstandard
extension). MySQL also treats [`REAL`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE")
as a synonym for [`DOUBLE PRECISION`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE")
(a nonstandard variation), unless the
[`REAL_AS_FLOAT`](sql-mode.md#sqlmode_real_as_float) SQL mode is
enabled.

The [`BIT`](bit-type.md "13.1.5 Bit-Value Type - BIT") data type stores bit values
and is supported for [`MyISAM`](myisam-storage-engine.md "18.2 The MyISAM Storage Engine"),
[`MEMORY`](memory-storage-engine.md "18.3 The MEMORY Storage Engine"),
[`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"), and
[`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") tables.

For information about how MySQL handles assignment of out-of-range
values to columns and overflow during expression evaluation, see
[Section 13.1.7, “Out-of-Range and Overflow Handling”](out-of-range-and-overflow.md "13.1.7 Out-of-Range and Overflow Handling").

For information about storage requirements of the numeric data
types, see [Section 13.7, “Data Type Storage Requirements”](storage-requirements.md "13.7 Data Type Storage Requirements").

For descriptions of functions that operate on numeric values, see
[Section 14.6, “Numeric Functions and Operators”](numeric-functions.md "14.6 Numeric Functions and Operators"). The data type used for the
result of a calculation on numeric operands depends on the types
of the operands and the operations performed on them. For more
information, see [Section 14.6.1, “Arithmetic Operators”](arithmetic-functions.md "14.6.1 Arithmetic Operators").
