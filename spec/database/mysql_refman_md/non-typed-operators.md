## 14.4 Operators

[14.4.1 Operator Precedence](operator-precedence.md)

[14.4.2 Comparison Functions and Operators](comparison-operators.md)

[14.4.3 Logical Operators](logical-operators.md)

[14.4.4 Assignment Operators](assignment-operators.md)

**Table 14.3 Operators**

| Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [`&`](bit-functions.md#operator_bitwise-and) | Bitwise AND |  |  |
| [`>`](comparison-operators.md#operator_greater-than) | Greater than operator |  |  |
| [`>>`](bit-functions.md#operator_right-shift) | Right shift |  |  |
| [`>=`](comparison-operators.md#operator_greater-than-or-equal) | Greater than or equal operator |  |  |
| [`<`](comparison-operators.md#operator_less-than) | Less than operator |  |  |
| [`<>`, `!=`](comparison-operators.md#operator_not-equal) | Not equal operator |  |  |
| [`<<`](bit-functions.md#operator_left-shift) | Left shift |  |  |
| [`<=`](comparison-operators.md#operator_less-than-or-equal) | Less than or equal operator |  |  |
| [`<=>`](comparison-operators.md#operator_equal-to) | NULL-safe equal to operator |  |  |
| [`%`, `MOD`](arithmetic-functions.md#operator_mod) | Modulo operator |  |  |
| [`*`](arithmetic-functions.md#operator_times) | Multiplication operator |  |  |
| [`+`](arithmetic-functions.md#operator_plus) | Addition operator |  |  |
| [`-`](arithmetic-functions.md#operator_minus) | Minus operator |  |  |
| [`-`](arithmetic-functions.md#operator_unary-minus) | Change the sign of the argument |  |  |
| [`->`](json-search-functions.md#operator_json-column-path) | Return value from JSON column after evaluating path; equivalent to JSON\_EXTRACT(). |  |  |
| [`->>`](json-search-functions.md#operator_json-inline-path) | Return value from JSON column after evaluating path and unquoting the result; equivalent to JSON\_UNQUOTE(JSON\_EXTRACT()). |  |  |
| [`/`](arithmetic-functions.md#operator_divide) | Division operator |  |  |
| [`:=`](assignment-operators.md#operator_assign-value) | Assign a value |  |  |
| [`=`](assignment-operators.md#operator_assign-equal) | Assign a value (as part of a [`SET`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment") statement, or as part of the `SET` clause in an [`UPDATE`](update.md "15.2.17 UPDATE Statement") statement) |  |  |
| [`=`](comparison-operators.md#operator_equal) | Equal operator |  |  |
| [`^`](bit-functions.md#operator_bitwise-xor) | Bitwise XOR |  |  |
| [`AND`, `&&`](logical-operators.md#operator_and) | Logical AND |  |  |
| [`BETWEEN ... AND ...`](comparison-operators.md#operator_between) | Whether a value is within a range of values |  |  |
| [`BINARY`](cast-functions.md#operator_binary) | Cast a string to a binary string |  | 8.0.27 |
| [`CASE`](flow-control-functions.md#operator_case) | Case operator |  |  |
| [`DIV`](arithmetic-functions.md#operator_div) | Integer division |  |  |
| [`EXISTS()`](comparison-operators.md#operator_exists) | Whether the result of a query contains any rows |  |  |
| [`IN()`](comparison-operators.md#operator_in) | Whether a value is within a set of values |  |  |
| [`IS`](comparison-operators.md#operator_is) | Test a value against a boolean |  |  |
| [`IS NOT`](comparison-operators.md#operator_is-not) | Test a value against a boolean |  |  |
| [`IS NOT NULL`](comparison-operators.md#operator_is-not-null) | NOT NULL value test |  |  |
| [`IS NULL`](comparison-operators.md#operator_is-null) | NULL value test |  |  |
| [`LIKE`](string-comparison-functions.md#operator_like) | Simple pattern matching |  |  |
| [`MEMBER OF()`](json-search-functions.md#operator_member-of) | Returns true (1) if first operand matches any element of JSON array passed as second operand, otherwise returns false (0) | 8.0.17 |  |
| [`NOT`, `!`](logical-operators.md#operator_not) | Negates value |  |  |
| [`NOT BETWEEN ... AND ...`](comparison-operators.md#operator_not-between) | Whether a value is not within a range of values |  |  |
| [`NOT EXISTS()`](comparison-operators.md#operator_not-exists) | Whether the result of a query contains no rows |  |  |
| [`NOT IN()`](comparison-operators.md#operator_not-in) | Whether a value is not within a set of values |  |  |
| [`NOT LIKE`](string-comparison-functions.md#operator_not-like) | Negation of simple pattern matching |  |  |
| [`NOT REGEXP`](regexp.md#operator_not-regexp) | Negation of REGEXP |  |  |
| [`OR`, `||`](logical-operators.md#operator_or) | Logical OR |  |  |
| [`REGEXP`](regexp.md#operator_regexp) | Whether string matches regular expression |  |  |
| [`RLIKE`](regexp.md#operator_regexp) | Whether string matches regular expression |  |  |
| [`SOUNDS LIKE`](string-functions.md#operator_sounds-like) | Compare sounds |  |  |
| [`XOR`](logical-operators.md#operator_xor) | Logical XOR |  |  |
| [`|`](bit-functions.md#operator_bitwise-or) | Bitwise OR |  |  |
| [`~`](bit-functions.md#operator_bitwise-invert) | Bitwise inversion |  |  |
