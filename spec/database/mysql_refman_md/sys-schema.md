# Chapter 30 MySQL sys Schema

**Table of Contents**

[30.1 Prerequisites for Using the sys Schema](sys-schema-prerequisites.md)

[30.2 Using the sys Schema](sys-schema-usage.md)

[30.3 sys Schema Progress Reporting](sys-schema-progress-reporting.md)

[30.4 sys Schema Object Reference](sys-schema-reference.md)
:   [30.4.1 sys Schema Object Index](sys-schema-object-index.md)

    [30.4.2 sys Schema Tables and Triggers](sys-schema-tables.md)

    [30.4.3 sys Schema Views](sys-schema-views.md)

    [30.4.4 sys Schema Stored Procedures](sys-schema-procedures.md)

    [30.4.5 sys Schema Stored Functions](sys-schema-functions.md)

MySQL 8.0 includes the
[`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema, a set of objects that
helps DBAs and developers interpret data collected by the
Performance Schema. [`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema objects
can be used for typical tuning and diagnosis use cases. Objects in
this schema include:

- Views that summarize Performance Schema data into more easily
  understandable form.
- Stored procedures that perform operations such as Performance
  Schema configuration and generating diagnostic reports.
- Stored functions that query Performance Schema configuration and
  provide formatting services.

For new installations, the [`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema
is installed by default during data directory initialization if you
use [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with the
[`--initialize`](server-options.md#option_mysqld_initialize) or
[`--initialize-insecure`](server-options.md#option_mysqld_initialize-insecure) option. If this
is not desired, you can drop the [`sys`](sys-schema.md "Chapter 30 MySQL sys Schema")
schema manually after initialization if it is unneeded.

The MySQL upgrade procedure produces an error if a
[`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema exists but has no
[`version`](sys-version.md "30.4.3.47 The version View") view, on the assumption that
absence of this view indicates a user-created `sys`
schema. To upgrade in this case, remove or rename the existing
[`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema first.

[`sys`](sys-schema.md "Chapter 30 MySQL sys Schema") schema objects have a
`DEFINER` of
`'mysql.sys'@'localhost'`. Use of the dedicated
`mysql.sys` account avoids problems that occur if a
DBA renames or removes the `root` account.
