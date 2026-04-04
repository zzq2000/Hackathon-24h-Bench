### 12.14.4 Adding a UCA Collation to a Unicode Character Set

[12.14.4.1 Defining a UCA Collation Using LDML Syntax](ldml-collation-example.md)

[12.14.4.2 LDML Syntax Supported in MySQL](ldml-rules.md)

[12.14.4.3 Diagnostics During Index.xml Parsing](collation-diagnostics.md)

This section describes how to add a UCA collation for a Unicode
character set by writing the
`<collation>` element within a
`<charset>` character set description in
the MySQL `Index.xml` file. The procedure
described here does not require recompiling MySQL. It uses a
subset of the Locale Data Markup Language (LDML) specification,
which is available at
<http://www.unicode.org/reports/tr35/>. With this
method, you need not define the entire collation. Instead, you
begin with an existing “base” collation and
describe the new collation in terms of how it differs from the
base collation. The following table lists the base collations of
the Unicode character sets for which UCA collations can be
defined. It is not possible to create user-defined UCA
collations for `utf16le`; there is no
`utf16le_unicode_ci` collation that would serve
as the basis for such collations.

**Table 12.4 MySQL Character Sets Available for User-Defined UCA Collations**

| Character Set | Base Collation |
| --- | --- |
| `utf8mb4` | `utf8mb4_unicode_ci` |
| `ucs2` | `ucs2_unicode_ci` |
| `utf16` | `utf16_unicode_ci` |
| `utf32` | `utf32_unicode_ci` |

The following sections show how to add a collation that is
defined using LDML syntax, and provide a summary of LDML rules
supported in MySQL.
