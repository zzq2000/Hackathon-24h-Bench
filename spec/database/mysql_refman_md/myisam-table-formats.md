### 18.2.3 MyISAM Table Storage Formats

[18.2.3.1 Static (Fixed-Length) Table Characteristics](static-format.md)

[18.2.3.2 Dynamic Table Characteristics](dynamic-format.md)

[18.2.3.3 Compressed Table Characteristics](compressed-format.md)

`MyISAM` supports three different storage
formats. Two of them, fixed and dynamic format, are chosen
automatically depending on the type of columns you are using. The
third, compressed format, can be created only with the
[**myisampack**](myisampack.md "6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables") utility (see
[Section 6.6.6, “myisampack — Generate Compressed, Read-Only MyISAM Tables”](myisampack.md "6.6.6 myisampack — Generate Compressed, Read-Only MyISAM Tables")).

When you use [`CREATE TABLE`](create-table.md "15.1.20 CREATE TABLE Statement") or
[`ALTER TABLE`](alter-table.md "15.1.9 ALTER TABLE Statement") for a table that has no
[`BLOB`](blob.md "13.3.4 The BLOB and TEXT Types") or
[`TEXT`](blob.md "13.3.4 The BLOB and TEXT Types") columns, you can force the
table format to `FIXED` or
`DYNAMIC` with the `ROW_FORMAT`
table option.

See [Section 15.1.20, “CREATE TABLE Statement”](create-table.md "15.1.20 CREATE TABLE Statement"), for information about
`ROW_FORMAT`.

You can decompress (unpack) compressed `MyISAM`
tables using [**myisamchk**](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility")
[`--unpack`](myisamchk-repair-options.md#option_myisamchk_unpack); see
[Section 6.6.4, “myisamchk — MyISAM Table-Maintenance Utility”](myisamchk.md "6.6.4 myisamchk — MyISAM Table-Maintenance Utility"), for more information.
