### 7.4.2 The Error Log

[7.4.2.1 Error Log Configuration](error-log-configuration.md)

[7.4.2.2 Default Error Log Destination Configuration](error-log-destination-configuration.md)

[7.4.2.3 Error Event Fields](error-log-event-fields.md)

[7.4.2.4 Types of Error Log Filtering](error-log-filtering.md)

[7.4.2.5 Priority-Based Error Log Filtering (log\_filter\_internal)](error-log-priority-based-filtering.md)

[7.4.2.6 Rule-Based Error Log Filtering (log\_filter\_dragnet)](error-log-rule-based-filtering.md)

[7.4.2.7 Error Logging in JSON Format](error-log-json.md)

[7.4.2.8 Error Logging to the System Log](error-log-syslog.md)

[7.4.2.9 Error Log Output Format](error-log-format.md)

[7.4.2.10 Error Log File Flushing and Renaming](error-log-rotation.md)

This section discusses how to configure the MySQL server for
logging of diagnostic messages to the error log. For information
about selecting the error message character set and language, see
[Section 12.6, “Error Message Character Set”](charset-errors.md "12.6 Error Message Character Set"), and
[Section 12.12, “Setting the Error Message Language”](error-message-language.md "12.12 Setting the Error Message Language").

The error log contains a record of [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")
startup and shutdown times. It also contains diagnostic messages
such as errors, warnings, and notes that occur during server
startup and shutdown, and while the server is running. For
example, if [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") notices that a table needs
to be automatically checked or repaired, it writes a message to
the error log.

Depending on error log configuration, error messages may also
populate the Performance Schema
[`error_log`](performance-schema-error-log-table.md "29.12.21.2 The error_log Table") table, to provide an SQL
interface to the log and enable its contents to be queried. See
[Section 29.12.21.2, “The error\_log Table”](performance-schema-error-log-table.md "29.12.21.2 The error_log Table").

On some operating systems, the error log contains a stack trace if
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") exits abnormally. The trace can be used
to determine where [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") exited. See
[Section 7.9, “Debugging MySQL”](debugging-mysql.md "7.9 Debugging MySQL").

If used to start [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"),
[**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") may write messages to the error
log. For example, when [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") notices
abnormal [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") exits, it restarts
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") and writes a `mysqld
restarted` message to the error log.

The following sections discuss aspects of configuring error
logging.
