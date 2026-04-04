# Chapter 14 Functions and Operators

**Table of Contents**

[14.1 Built-In Function and Operator Reference](built-in-function-reference.md)

[14.2 Loadable Function Reference](loadable-function-reference.md)

[14.3 Type Conversion in Expression Evaluation](type-conversion.md)

[14.4 Operators](non-typed-operators.md)
:   [14.4.1 Operator Precedence](operator-precedence.md)

    [14.4.2 Comparison Functions and Operators](comparison-operators.md)

    [14.4.3 Logical Operators](logical-operators.md)

    [14.4.4 Assignment Operators](assignment-operators.md)

[14.5 Flow Control Functions](flow-control-functions.md)

[14.6 Numeric Functions and Operators](numeric-functions.md)
:   [14.6.1 Arithmetic Operators](arithmetic-functions.md)

    [14.6.2 Mathematical Functions](mathematical-functions.md)

[14.7 Date and Time Functions](date-and-time-functions.md)

[14.8 String Functions and Operators](string-functions.md)
:   [14.8.1 String Comparison Functions and Operators](string-comparison-functions.md)

    [14.8.2 Regular Expressions](regexp.md)

    [14.8.3 Character Set and Collation of Function Results](string-functions-charset.md)

[14.9 Full-Text Search Functions](fulltext-search.md)
:   [14.9.1 Natural Language Full-Text Searches](fulltext-natural-language.md)

    [14.9.2 Boolean Full-Text Searches](fulltext-boolean.md)

    [14.9.3 Full-Text Searches with Query Expansion](fulltext-query-expansion.md)

    [14.9.4 Full-Text Stopwords](fulltext-stopwords.md)

    [14.9.5 Full-Text Restrictions](fulltext-restrictions.md)

    [14.9.6 Fine-Tuning MySQL Full-Text Search](fulltext-fine-tuning.md)

    [14.9.7 Adding a User-Defined Collation for Full-Text Indexing](full-text-adding-collation.md)

    [14.9.8 ngram Full-Text Parser](fulltext-search-ngram.md)

    [14.9.9 MeCab Full-Text Parser Plugin](fulltext-search-mecab.md)

[14.10 Cast Functions and Operators](cast-functions.md)

[14.11 XML Functions](xml-functions.md)

[14.12 Bit Functions and Operators](bit-functions.md)

[14.13 Encryption and Compression Functions](encryption-functions.md)

[14.14 Locking Functions](locking-functions.md)

[14.15 Information Functions](information-functions.md)

[14.16 Spatial Analysis Functions](spatial-analysis-functions.md)
:   [14.16.1 Spatial Function Reference](spatial-function-reference.md)

    [14.16.2 Argument Handling by Spatial Functions](spatial-function-argument-handling.md)

    [14.16.3 Functions That Create Geometry Values from WKT Values](gis-wkt-functions.md)

    [14.16.4 Functions That Create Geometry Values from WKB Values](gis-wkb-functions.md)

    [14.16.5 MySQL-Specific Functions That Create Geometry Values](gis-mysql-specific-functions.md)

    [14.16.6 Geometry Format Conversion Functions](gis-format-conversion-functions.md)

    [14.16.7 Geometry Property Functions](gis-property-functions.md)

    [14.16.8 Spatial Operator Functions](spatial-operator-functions.md)

    [14.16.9 Functions That Test Spatial Relations Between Geometry Objects](spatial-relation-functions.md)

    [14.16.10 Spatial Geohash Functions](spatial-geohash-functions.md)

    [14.16.11 Spatial GeoJSON Functions](spatial-geojson-functions.md)

    [14.16.12 Spatial Aggregate Functions](spatial-aggregate-functions.md)

    [14.16.13 Spatial Convenience Functions](spatial-convenience-functions.md)

[14.17 JSON Functions](json-functions.md)
:   [14.17.1 JSON Function Reference](json-function-reference.md)

    [14.17.2 Functions That Create JSON Values](json-creation-functions.md)

    [14.17.3 Functions That Search JSON Values](json-search-functions.md)

    [14.17.4 Functions That Modify JSON Values](json-modification-functions.md)

    [14.17.5 Functions That Return JSON Value Attributes](json-attribute-functions.md)

    [14.17.6 JSON Table Functions](json-table-functions.md)

    [14.17.7 JSON Schema Validation Functions](json-validation-functions.md)

    [14.17.8 JSON Utility Functions](json-utility-functions.md)

[14.18 Replication Functions](replication-functions.md)
:   [14.18.1 Group Replication Functions](group-replication-functions.md)

    [14.18.2 Functions Used with Global Transaction Identifiers (GTIDs)](gtid-functions.md)

    [14.18.3 Asynchronous Replication Channel Failover Functions](replication-functions-async-failover.md)

    [14.18.4 Position-Based Synchronization Functions](replication-functions-synchronization.md)

[14.19 Aggregate Functions](aggregate-functions-and-modifiers.md)
:   [14.19.1 Aggregate Function Descriptions](aggregate-functions.md)

    [14.19.2 GROUP BY Modifiers](group-by-modifiers.md)

    [14.19.3 MySQL Handling of GROUP BY](group-by-handling.md)

    [14.19.4 Detection of Functional Dependence](group-by-functional-dependence.md)

[14.20 Window Functions](window-functions.md)
:   [14.20.1 Window Function Descriptions](window-function-descriptions.md)

    [14.20.2 Window Function Concepts and Syntax](window-functions-usage.md)

    [14.20.3 Window Function Frame Specification](window-functions-frames.md)

    [14.20.4 Named Windows](window-functions-named-windows.md)

    [14.20.5 Window Function Restrictions](window-function-restrictions.md)

[14.21 Performance Schema Functions](performance-schema-functions.md)

[14.22 Internal Functions](internal-functions.md)

[14.23 Miscellaneous Functions](miscellaneous-functions.md)

[14.24 Precision Math](precision-math.md)
:   [14.24.1 Types of Numeric Values](precision-math-numbers.md)

    [14.24.2 DECIMAL Data Type Characteristics](precision-math-decimal-characteristics.md)

    [14.24.3 Expression Handling](precision-math-expressions.md)

    [14.24.4 Rounding Behavior](precision-math-rounding.md)

    [14.24.5 Precision Math Examples](precision-math-examples.md)

Expressions can be used at several points in
[SQL](glossary.md#glos_sql "SQL") statements, such as in the
`ORDER BY` or `HAVING` clauses of
[`SELECT`](select.md "15.2.13 SELECT Statement") statements, in the
`WHERE` clause of a
[`SELECT`](select.md "15.2.13 SELECT Statement"),
[`DELETE`](delete.md "15.2.2 DELETE Statement"), or
[`UPDATE`](update.md "15.2.17 UPDATE Statement") statement, or in
[`SET`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment")
statements. Expressions can be written using values from several
sources, such as literal values, column values,
`NULL`, variables, built-in functions and
operators, loadable functions, and stored functions (a type of
stored object).

This chapter describes the built-in functions and operators that are
permitted for writing expressions in MySQL. For information about
loadable functions and stored functions, see
[Section 7.7, “MySQL Server Loadable Functions”](server-loadable-functions.md "7.7 MySQL Server Loadable Functions"), and
[Section 27.2, “Using Stored Routines”](stored-routines.md "27.2 Using Stored Routines"). For the rules describing how the
server interprets references to different kinds of functions, see
[Section 11.2.5, “Function Name Parsing and Resolution”](function-resolution.md "11.2.5 Function Name Parsing and Resolution").

An expression that contains `NULL` always produces
a `NULL` value unless otherwise indicated in the
documentation for a particular function or operator.

Note

By default, there must be no whitespace between a function name
and the parenthesis following it. This helps the MySQL parser
distinguish between function calls and references to tables or
columns that happen to have the same name as a function. However,
spaces around function arguments are permitted.

To tell the MySQL server to accept spaces after function names by
starting it with the
[`--sql-mode=IGNORE_SPACE`](server-options.md#option_mysqld_sql-mode) option.
(See [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes").) Individual client programs can
request this behavior by using the
`CLIENT_IGNORE_SPACE` option for
[`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/8.0/en/mysql-real-connect.html). In either
case, all function names become reserved words.

For the sake of brevity, some examples in this chapter display the
output from the [**mysql**](mysql.md "6.5.1 mysql — The MySQL Command-Line Client") program in abbreviated
form. Rather than showing examples in this format:

```sql
mysql> SELECT MOD(29,9);
+-----------+
| mod(29,9) |
+-----------+
|         2 |
+-----------+
1 rows in set (0.00 sec)
```

This format is used instead:

```sql
mysql> SELECT MOD(29,9);
        -> 2
```
