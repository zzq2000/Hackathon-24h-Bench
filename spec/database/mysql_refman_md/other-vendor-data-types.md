## 13.9 Using Data Types from Other Database Engines

To facilitate the use of code written for SQL implementations from
other vendors, MySQL maps data types as shown in the following
table. These mappings make it easier to import table definitions
from other database systems into MySQL.

| Other Vendor Type | MySQL Type |
| --- | --- |
| [`BOOL`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`TINYINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| [`BOOLEAN`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`TINYINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| `CHARACTER VARYING(M)` | `VARCHAR(M)` |
| [`FIXED`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") | [`DECIMAL`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") |
| [`FLOAT4`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") | [`FLOAT`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") |
| [`FLOAT8`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") | [`DOUBLE`](floating-point-types.md "13.1.4 Floating-Point Types (Approximate Value) - FLOAT, DOUBLE") |
| [`INT1`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`TINYINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| [`INT2`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`SMALLINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| [`INT3`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`MEDIUMINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| [`INT4`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`INT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| `INT8` | [`BIGINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| `LONG VARBINARY` | [`MEDIUMBLOB`](blob.md "13.3.4 The BLOB and TEXT Types") |
| `LONG VARCHAR` | [`MEDIUMTEXT`](blob.md "13.3.4 The BLOB and TEXT Types") |
| `LONG` | [`MEDIUMTEXT`](blob.md "13.3.4 The BLOB and TEXT Types") |
| [`MIDDLEINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") | [`MEDIUMINT`](integer-types.md "13.1.2 Integer Types (Exact Value) - INTEGER, INT, SMALLINT, TINYINT, MEDIUMINT, BIGINT") |
| [`NUMERIC`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") | [`DECIMAL`](fixed-point-types.md "13.1.3 Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC") |

Data type mapping occurs at table creation time, after which the
original type specifications are discarded. If you create a table
with types used by other vendors and then issue a
`DESCRIBE tbl_name`
statement, MySQL reports the table structure using the equivalent
MySQL types. For example:

```sql
mysql> CREATE TABLE t (a BOOL, b FLOAT8, c LONG VARCHAR, d NUMERIC);
Query OK, 0 rows affected (0.00 sec)

mysql> DESCRIBE t;
+-------+---------------+------+-----+---------+-------+
| Field | Type          | Null | Key | Default | Extra |
+-------+---------------+------+-----+---------+-------+
| a     | tinyint(1)    | YES  |     | NULL    |       |
| b     | double        | YES  |     | NULL    |       |
| c     | mediumtext    | YES  |     | NULL    |       |
| d     | decimal(10,0) | YES  |     | NULL    |       |
+-------+---------------+------+-----+---------+-------+
4 rows in set (0.01 sec)
```
