#### 12.10.7.1 The cp932 Character Set

**Why is `cp932`
needed?**

In MySQL, the `sjis` character set
corresponds to the `Shift_JIS` character set
defined by IANA, which supports JIS X0201 and JIS X0208
characters. (See
<http://www.iana.org/assignments/character-sets>.)

However, the meaning of “SHIFT JIS” as a
descriptive term has become very vague and it often includes
the extensions to `Shift_JIS` that are
defined by various vendors.

For example, “SHIFT JIS” used in Japanese Windows
environments is a Microsoft extension of
`Shift_JIS` and its exact name is
`Microsoft Windows Codepage : 932` or
`cp932`. In addition to the characters
supported by `Shift_JIS`,
`cp932` supports extension characters such as
NEC special characters, NEC selected—IBM extended
characters, and IBM selected characters.

Many Japanese users have experienced problems using these
extension characters. These problems stem from the following
factors:

- MySQL automatically converts character sets.
- Character sets are converted using Unicode
  (`ucs2`).
- The `sjis` character set does not support
  the conversion of these extension characters.
- There are several conversion rules from so-called
  “SHIFT JIS” to Unicode, and some characters
  are converted to Unicode differently depending on the
  conversion rule. MySQL supports only one of these rules
  (described later).

The MySQL `cp932` character set is designed
to solve these problems.

Because MySQL supports character set conversion, it is
important to separate IANA `Shift_JIS` and
`cp932` into two different character sets
because they provide different conversion rules.

**How does `cp932` differ
from `sjis`?**

The `cp932` character set differs from
`sjis` in the following ways:

- `cp932` supports NEC special characters,
  NEC selected—IBM extended characters, and IBM
  selected characters.
- Some `cp932` characters have two
  different code points, both of which convert to the same
  Unicode code point. When converting from Unicode back to
  `cp932`, one of the code points must be
  selected. For this “round trip conversion,”
  the rule recommended by Microsoft is used. (See
  <http://support.microsoft.com/kb/170559/EN-US/>.)

  The conversion rule works like this:

  - If the character is in both JIS X 0208 and NEC special
    characters, use the code point of JIS X 0208.
  - If the character is in both NEC special characters and
    IBM selected characters, use the code point of NEC
    special characters.
  - If the character is in both IBM selected characters
    and NEC selected—IBM extended characters, use
    the code point of IBM extended characters.

  The table shown at
  <https://msdn.microsoft.com/en-us/goglobal/cc305152.aspx>
  provides information about the Unicode values of
  `cp932` characters. For
  `cp932` table entries with characters
  under which a four-digit number appears, the number
  represents the corresponding Unicode
  (`ucs2`) encoding. For table entries with
  an underlined two-digit value appears, there is a range of
  `cp932` character values that begin with
  those two digits. Clicking such a table entry takes you to
  a page that displays the Unicode value for each of the
  `cp932` characters that begin with those
  digits.

  The following links are of special interest. They
  correspond to the encodings for the following sets of
  characters:

  - NEC special characters (lead byte
    `0x87`):

    ```html
    https://msdn.microsoft.com/en-us/goglobal/gg674964
    ```
  - NEC selected—IBM extended characters (lead byte
    `0xED` and `0xEE`):

    ```html
    https://msdn.microsoft.com/en-us/goglobal/gg671837
    https://msdn.microsoft.com/en-us/goglobal/gg671838
    ```
  - IBM selected characters (lead byte
    `0xFA`, `0xFB`,
    `0xFC`):

    ```html
    https://msdn.microsoft.com/en-us/goglobal/gg671839
    https://msdn.microsoft.com/en-us/goglobal/gg671840
    https://msdn.microsoft.com/en-us/goglobal/gg671841
    ```
- `cp932` supports conversion of
  user-defined characters in combination with
  `eucjpms`, and solves the problems with
  `sjis`/`ujis`
  conversion. For details, please refer to
  <http://www.sljfaq.org/afaq/encodings.html>.

For some characters, conversion to and from
`ucs2` is different for
`sjis` and `cp932`. The
following tables illustrate these differences.

Conversion to `ucs2`:

| `sjis`/`cp932` Value | `sjis` -> `ucs2` Conversion | `cp932` -> `ucs2` Conversion |
| --- | --- | --- |
| 5C | 005C | 005C |
| 7E | 007E | 007E |
| 815C | 2015 | 2015 |
| 815F | 005C | FF3C |
| 8160 | 301C | FF5E |
| 8161 | 2016 | 2225 |
| 817C | 2212 | FF0D |
| 8191 | 00A2 | FFE0 |
| 8192 | 00A3 | FFE1 |
| 81CA | 00AC | FFE2 |

Conversion from `ucs2`:

| `ucs2` value | `ucs2` -> `sjis` Conversion | `ucs2` -> `cp932` Conversion |
| --- | --- | --- |
| 005C | 815F | 5C |
| 007E | 7E | 7E |
| 00A2 | 8191 | 3F |
| 00A3 | 8192 | 3F |
| 00AC | 81CA | 3F |
| 2015 | 815C | 815C |
| 2016 | 8161 | 3F |
| 2212 | 817C | 3F |
| 2225 | 3F | 8161 |
| 301C | 8160 | 3F |
| FF0D | 3F | 817C |
| FF3C | 3F | 815F |
| FF5E | 3F | 8160 |
| FFE0 | 3F | 8191 |
| FFE1 | 3F | 8192 |
| FFE2 | 3F | 81CA |

Users of any Japanese character sets should be aware that
using
[`--character-set-client-handshake`](server-options.md#option_mysqld_character-set-client-handshake)
(or
[`--skip-character-set-client-handshake`](server-options.md#option_mysqld_character-set-client-handshake))
has an important effect. See [Section 7.1.7, “Server Command Options”](server-options.md "7.1.7 Server Command Options").
