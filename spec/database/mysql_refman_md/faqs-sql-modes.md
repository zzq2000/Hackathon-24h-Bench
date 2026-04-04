## A.3 MySQL 8.0 FAQ: Server SQL Mode

A.3.1. [What are server SQL modes?](faqs-sql-modes.md#faq-mysql-what-sql-modes)

A.3.2. [How many server SQL modes are there?](faqs-sql-modes.md#faq-mysql-count-sql-modes)

A.3.3. [How do you determine the server SQL mode?](faqs-sql-modes.md#faq-mysql-how-see-sql-mode)

A.3.4. [Is the mode dependent on the database or connection?](faqs-sql-modes.md#faq-mysql-sql-mode-dependency)

A.3.5. [Can the rules for strict mode be extended?](faqs-sql-modes.md#faq-mysql-extend-strict-mode)

A.3.6. [Does strict mode impact performance?](faqs-sql-modes.md#faq-mysql-strict-impact)

A.3.7. [What is the default server SQL mode when MySQL 8.0 is installed?](faqs-sql-modes.md#faq-mysql-what-default-mode)

|  |  |
| --- | --- |
| **A.3.1.** | What are server SQL modes? |
|  | Server SQL modes define what SQL syntax MySQL should support and what kind of data validation checks it should perform. This makes it easier to use MySQL in different environments and to use MySQL together with other database servers. The MySQL Server apply these modes individually to different clients. For more information, see [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes"). |
| **A.3.2.** | How many server SQL modes are there? |
|  | Each mode can be independently switched on and off. See [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes"), for a complete list of available modes. |
| **A.3.3.** | How do you determine the server SQL mode? |
|  | You can set the default SQL mode (for [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") startup) with the [`--sql-mode`](server-options.md#option_mysqld_sql-mode) option. Using the statement [`SET [GLOBAL|SESSION] sql_mode='modes'`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment"), you can change the settings from within a connection, either locally to the connection, or to take effect globally. You can retrieve the current mode by issuing a `SELECT @@sql_mode` statement. |
| **A.3.4.** | Is the mode dependent on the database or connection? |
|  | A mode is not linked to a particular database. Modes can be set locally to the session (connection), or globally for the server. you can change these settings using [`SET [GLOBAL|SESSION] sql_mode='modes'`](set-variable.md "15.7.6.1 SET Syntax for Variable Assignment"). |
| **A.3.5.** | Can the rules for strict mode be extended? |
|  | When we refer to *strict mode*, we mean a mode where at least one of the modes [`TRADITIONAL`](sql-mode.md#sqlmode_traditional), [`STRICT_TRANS_TABLES`](sql-mode.md#sqlmode_strict_trans_tables), or [`STRICT_ALL_TABLES`](sql-mode.md#sqlmode_strict_all_tables) is enabled. Options can be combined, so you can add restrictions to a mode. See [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes"), for more information. |
| **A.3.6.** | Does strict mode impact performance? |
|  | The intensive validation of input data that some settings requires more time than if the validation is not done. While the performance impact is not that great, if you do not require such validation (perhaps your application already handles all of this), then MySQL gives you the option of leaving strict mode disabled. However, if you do require it, strict mode can provide such validation. |
| **A.3.7.** | What is the default server SQL mode when MySQL 8.0 is installed? |
|  | The default SQL mode in MySQL 8.0 includes these modes: [`ONLY_FULL_GROUP_BY`](sql-mode.md#sqlmode_only_full_group_by), [`STRICT_TRANS_TABLES`](sql-mode.md#sqlmode_strict_trans_tables), [`NO_ZERO_IN_DATE`](sql-mode.md#sqlmode_no_zero_in_date), [`NO_ZERO_DATE`](sql-mode.md#sqlmode_no_zero_date), [`ERROR_FOR_DIVISION_BY_ZERO`](sql-mode.md#sqlmode_error_for_division_by_zero), and [`NO_ENGINE_SUBSTITUTION`](sql-mode.md#sqlmode_no_engine_substitution).  For information about all available modes and default MySQL behavior, see [Section 7.1.11, “Server SQL Modes”](sql-mode.md "7.1.11 Server SQL Modes"). |
