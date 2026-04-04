### 14.8.3 Character Set and Collation of Function Results

MySQL has many operators and functions that return a string.
This section answers the question: What is the character set and
collation of such a string?

For simple functions that take string input and return a string
result as output, the output's character set and collation are
the same as those of the principal input value. For example,
[`UPPER(X)`](string-functions.md#function_upper)
returns a string with the same character string and collation as
*`X`*. The same applies for
[`INSTR()`](string-functions.md#function_instr),
[`LCASE()`](string-functions.md#function_lcase),
[`LOWER()`](string-functions.md#function_lower),
[`LTRIM()`](string-functions.md#function_ltrim),
[`MID()`](string-functions.md#function_mid),
[`REPEAT()`](string-functions.md#function_repeat),
[`REPLACE()`](string-functions.md#function_replace),
[`REVERSE()`](string-functions.md#function_reverse),
[`RIGHT()`](string-functions.md#function_right),
[`RPAD()`](string-functions.md#function_rpad),
[`RTRIM()`](string-functions.md#function_rtrim),
[`SOUNDEX()`](string-functions.md#function_soundex),
[`SUBSTRING()`](string-functions.md#function_substring),
[`TRIM()`](string-functions.md#function_trim),
[`UCASE()`](string-functions.md#function_ucase), and
[`UPPER()`](string-functions.md#function_upper).

Note

The [`REPLACE()`](string-functions.md#function_replace) function, unlike
all other functions, always ignores the collation of the
string input and performs a case-sensitive comparison.

If a string input or function result is a binary string, the
string has the `binary` character set and
collation. This can be checked by using the
[`CHARSET()`](information-functions.md#function_charset) and
[`COLLATION()`](information-functions.md#function_collation) functions, both of
which return `binary` for a binary string
argument:

```sql
mysql> SELECT CHARSET(BINARY 'a'), COLLATION(BINARY 'a');
+---------------------+-----------------------+
| CHARSET(BINARY 'a') | COLLATION(BINARY 'a') |
+---------------------+-----------------------+
| binary              | binary                |
+---------------------+-----------------------+
```

For operations that combine multiple string inputs and return a
single string output, the “aggregation rules” of
standard SQL apply for determining the collation of the result:

- If an explicit `COLLATE
  Y` occurs, use
  *`Y`*.
- If explicit `COLLATE
  Y` and `COLLATE
  Z` occur, raise an
  error.
- Otherwise, if all collations are
  *`Y`*, use
  *`Y`*.
- Otherwise, the result has no collation.

For example, with `CASE ... WHEN a THEN b WHEN b THEN c
COLLATE X END`, the
resulting collation is *`X`*. The same
applies for [`UNION`](union.md "15.2.18 UNION Clause"),
[`||`](logical-operators.md#operator_or),
[`CONCAT()`](string-functions.md#function_concat),
[`ELT()`](string-functions.md#function_elt),
[`GREATEST()`](comparison-operators.md#function_greatest),
[`IF()`](flow-control-functions.md#function_if), and
[`LEAST()`](comparison-operators.md#function_least).

For operations that convert to character data, the character set
and collation of the strings that result from the operations are
defined by the
[`character_set_connection`](server-system-variables.md#sysvar_character_set_connection) and
[`collation_connection`](server-system-variables.md#sysvar_collation_connection) system
variables that determine the default connection character set
and collation (see [Section 12.4, “Connection Character Sets and Collations”](charset-connection.md "12.4 Connection Character Sets and Collations")). This
applies only to [`BIN_TO_UUID()`](miscellaneous-functions.md#function_bin-to-uuid),
[`CAST()`](cast-functions.md#function_cast),
[`CONV()`](mathematical-functions.md#function_conv),
[`FORMAT()`](string-functions.md#function_format),
[`HEX()`](string-functions.md#function_hex), and
[`SPACE()`](string-functions.md#function_space).

An exception to the preceding principle occurs for expressions
for virtual generated columns. In such expressions, the table
character set is used for
[`BIN_TO_UUID()`](miscellaneous-functions.md#function_bin-to-uuid),
[`CONV()`](mathematical-functions.md#function_conv), or
[`HEX()`](string-functions.md#function_hex) results, regardless of
connection character set.

If there is any question about the character set or collation of
the result returned by a string function, use the
[`CHARSET()`](information-functions.md#function_charset) or
[`COLLATION()`](information-functions.md#function_collation) function to find out:

```sql
mysql> SELECT USER(), CHARSET(USER()), COLLATION(USER());
+----------------+-----------------+--------------------+
| USER()         | CHARSET(USER()) | COLLATION(USER())  |
+----------------+-----------------+--------------------+
| test@localhost | utf8mb3         | utf8mb3_general_ci |
+----------------+-----------------+--------------------+
mysql> SELECT CHARSET(COMPRESS('abc')), COLLATION(COMPRESS('abc'));
+--------------------------+----------------------------+
| CHARSET(COMPRESS('abc')) | COLLATION(COMPRESS('abc')) |
+--------------------------+----------------------------+
| binary                   | binary                     |
+--------------------------+----------------------------+
```
