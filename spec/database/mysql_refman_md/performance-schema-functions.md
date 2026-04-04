## 14.21 Performance Schema Functions

As of MySQL 8.0.16, MySQL includes built-in SQL functions that
format or retrieve Performance Schema data, and that may be used
as equivalents for the corresponding `sys` schema
stored functions. The built-in functions can be invoked in any
schema and require no qualifier, unlike the `sys`
functions, which require either a `sys.` schema
qualifier or that `sys` be the current schema.

**Table 14.31 Performance Schema Functions**

| Name | Description | Introduced |
| --- | --- | --- |
| [`FORMAT_BYTES()`](performance-schema-functions.md#function_format-bytes) | Convert byte count to value with units | 8.0.16 |
| [`FORMAT_PICO_TIME()`](performance-schema-functions.md#function_format-pico-time) | Convert time in picoseconds to value with units | 8.0.16 |
| [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id) | Performance Schema thread ID for current thread | 8.0.16 |
| [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) | Performance Schema thread ID for given thread | 8.0.16 |

The built-in functions supersede the corresponding
`sys` functions, which are deprecated; expect
them to be removed in a future version of MySQL. Applications that
use the `sys` functions should be adjusted to use
the built-in functions instead, keeping in mind some minor
differences between the `sys` functions and the
built-in functions. For details about these differences, see the
function descriptions in this section.

- [`FORMAT_BYTES(count)`](performance-schema-functions.md#function_format-bytes)

  Given a numeric byte count, converts it to human-readable
  format and returns a string consisting of a value and a units
  indicator. The string contains the number of bytes rounded to
  2 decimal places and a minimum of 3 significant digits.
  Numbers less than 1024 bytes are represented as whole numbers
  and are not rounded. Returns `NULL` if
  *`count`* is `NULL`.

  The units indicator depends on the size of the byte-count
  argument as shown in the following table.

  | Argument Value | Result Units | Result Units Indicator |
  | --- | --- | --- |
  | Up to 1023 | bytes | bytes |
  | Up to 10242 − 1 | kibibytes | KiB |
  | Up to 10243 − 1 | mebibytes | MiB |
  | Up to 10244 − 1 | gibibytes | GiB |
  | Up to 10245 − 1 | tebibytes | TiB |
  | Up to 10246 − 1 | pebibytes | PiB |
  | 10246 and up | exbibytes | EiB |

  ```sql
  mysql> SELECT FORMAT_BYTES(512), FORMAT_BYTES(18446644073709551615);
  +-------------------+------------------------------------+
  | FORMAT_BYTES(512) | FORMAT_BYTES(18446644073709551615) |
  +-------------------+------------------------------------+
  |  512 bytes        | 16.00 EiB                          |
  +-------------------+------------------------------------+
  ```

  [`FORMAT_BYTES()`](performance-schema-functions.md#function_format-bytes) was added in
  MySQL 8.0.16. It may be used instead of the
  `sys` schema
  [`format_bytes()`](sys-format-bytes.md "30.4.5.3 The format_bytes() Function") function, keeping
  in mind this difference:

  - [`FORMAT_BYTES()`](performance-schema-functions.md#function_format-bytes) uses the
    `EiB` units indicator.
    [`sys.format_bytes()`](sys-format-bytes.md "30.4.5.3 The format_bytes() Function") does not.
- [`FORMAT_PICO_TIME(time_val)`](performance-schema-functions.md#function_format-pico-time)

  Given a numeric Performance Schema latency or wait time in
  picoseconds, converts it to human-readable format and returns
  a string consisting of a value and a units indicator. The
  string contains the decimal time rounded to 2 decimal places
  and a minimum of 3 significant digits. Times under 1
  nanosecond are represented as whole numbers and are not
  rounded.

  If *`time_val`* is
  `NULL`, this function returns
  `NULL`.

  The units indicator depends on the size of the time-value
  argument as shown in the following table.

  | Argument Value | Result Units | Result Units Indicator |
  | --- | --- | --- |
  | Up to 103 − 1 | picoseconds | ps |
  | Up to 106 − 1 | nanoseconds | ns |
  | Up to 109 − 1 | microseconds | us |
  | Up to 1012 − 1 | milliseconds | ms |
  | Up to 60×1012 − 1 | seconds | s |
  | Up to 3.6×1015 − 1 | minutes | min |
  | Up to 8.64×1016 − 1 | hours | h |
  | 8.64×1016 and up | days | d |

  ```sql
  mysql> SELECT FORMAT_PICO_TIME(3501), FORMAT_PICO_TIME(188732396662000);
  +------------------------+-----------------------------------+
  | FORMAT_PICO_TIME(3501) | FORMAT_PICO_TIME(188732396662000) |
  +------------------------+-----------------------------------+
  | 3.50 ns                | 3.15 min                          |
  +------------------------+-----------------------------------+
  ```

  [`FORMAT_PICO_TIME()`](performance-schema-functions.md#function_format-pico-time) was added in
  MySQL 8.0.16. It may be used instead of the
  `sys` schema
  [`format_time()`](sys-format-time.md "30.4.5.6 The format_time() Function") function, keeping
  in mind these differences:

  - To indicate minutes,
    [`sys.format_time()`](sys-format-time.md "30.4.5.6 The format_time() Function") uses the
    `m` units indicator, whereas
    [`FORMAT_PICO_TIME()`](performance-schema-functions.md#function_format-pico-time) uses
    `min`.
  - [`sys.format_time()`](sys-format-time.md "30.4.5.6 The format_time() Function") uses the
    `w` (weeks) units indicator.
    [`FORMAT_PICO_TIME()`](performance-schema-functions.md#function_format-pico-time) does
    not.
- [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id)

  Returns a `BIGINT UNSIGNED` value
  representing the Performance Schema thread ID assigned to the
  current connection.

  The thread ID return value is a value of the type given in the
  `THREAD_ID` column of Performance Schema
  tables.

  Performance Schema configuration affects
  [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id) the same
  way as for [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id). For
  details, see the description of that function.

  ```sql
  mysql> SELECT PS_CURRENT_THREAD_ID();
  +------------------------+
  | PS_CURRENT_THREAD_ID() |
  +------------------------+
  |                     52 |
  +------------------------+
  mysql> SELECT PS_THREAD_ID(CONNECTION_ID());
  +-------------------------------+
  | PS_THREAD_ID(CONNECTION_ID()) |
  +-------------------------------+
  |                            52 |
  +-------------------------------+
  ```

  [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id) was
  added in MySQL 8.0.16. It may be used as a shortcut for
  invoking the `sys` schema
  [`ps_thread_id()`](sys-ps-thread-id.md "30.4.5.15 The ps_thread_id() Function") function with an
  argument of `NULL` or
  [`CONNECTION_ID()`](information-functions.md#function_connection-id).
- [`PS_THREAD_ID(connection_id)`](performance-schema-functions.md#function_ps-thread-id)

  Given a connection ID, returns a `BIGINT
  UNSIGNED` value representing the Performance Schema
  thread ID assigned to the connection ID, or
  `NULL` if no thread ID exists for the
  connection ID. The latter can occur for threads that are not
  instrumented, or if *`connection_id`*
  is `NULL`.

  The connection ID argument is a value of the type given in the
  `PROCESSLIST_ID` column of the Performance
  Schema [`threads`](performance-schema-threads-table.md "29.12.21.8 The threads Table") table or the
  `Id` column of [`SHOW
  PROCESSLIST`](show-processlist.md "15.7.7.29 SHOW PROCESSLIST Statement") output.

  The thread ID return value is a value of the type given in the
  `THREAD_ID` column of Performance Schema
  tables.

  Performance Schema configuration affects
  [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) operation as
  follows. (These remarks also apply to
  [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id).)

  - Disabling the `thread_instrumentation`
    consumer disables statistics from being collected and
    aggregated at the thread level, but has no effect on
    [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id).
  - If
    [`performance_schema_max_thread_instances`](performance-schema-system-variables.md#sysvar_performance_schema_max_thread_instances)
    is not 0, the Performance Schema allocates memory for
    thread statistics and assigns an internal ID to each
    thread for which instance memory is available. If there
    are threads for which instance memory is not available,
    [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) returns
    `NULL`; in this case,
    [`Performance_schema_thread_instances_lost`](performance-schema-status-variables.md#statvar_Performance_schema_thread_instances_lost)
    is nonzero.
  - If
    [`performance_schema_max_thread_instances`](performance-schema-system-variables.md#sysvar_performance_schema_max_thread_instances)
    is 0, the Performance Schema allocates no thread memory
    and [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) returns
    `NULL`.
  - If the Performance Schema itself is disabled,
    [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) produces an
    error.

  ```sql
  mysql> SELECT PS_THREAD_ID(6);
  +-----------------+
  | PS_THREAD_ID(6) |
  +-----------------+
  |              45 |
  +-----------------+
  ```

  [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) was added in
  MySQL 8.0.16. It may be used instead of the
  `sys` schema
  [`ps_thread_id()`](sys-ps-thread-id.md "30.4.5.15 The ps_thread_id() Function") function, keeping
  in mind this difference:

  - With an argument of `NULL`,
    [`sys.ps_thread_id()`](sys-ps-thread-id.md "30.4.5.15 The ps_thread_id() Function") returns
    the thread ID for the current connection, whereas
    [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) returns
    `NULL`. To obtain the current connection
    thread ID, use
    [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id)
    instead.
