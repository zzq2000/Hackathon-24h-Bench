#### 8.4.5.8 Writing Audit Log Filter Definitions

Filter definitions are [`JSON`](json.md "13.5 The JSON Data Type")
values. For information about using
[`JSON`](json.md "13.5 The JSON Data Type") data in MySQL, see
[Section 13.5, “The JSON Data Type”](json.md "13.5 The JSON Data Type").

Filter definitions have this form, where
*`actions`* indicates how filtering takes
place:

```json
{ "filter": actions }
```

The following discussion describes permitted constructs in
filter definitions.

- [Logging All Events](audit-log-filter-definitions.md#audit-log-filtering-enabling-logging "Logging All Events")
- [Logging Specific Event Classes](audit-log-filter-definitions.md#audit-log-filtering-class-logging "Logging Specific Event Classes")
- [Logging Specific Event Subclasses](audit-log-filter-definitions.md#audit-log-filtering-subclass-logging "Logging Specific Event Subclasses")
- [Inclusive and Exclusive Logging](audit-log-filter-definitions.md#audit-log-filtering-inclusive-exclusive "Inclusive and Exclusive Logging")
- [Testing Event Field Values](audit-log-filter-definitions.md#audit-log-filtering-event-fields "Testing Event Field Values")
- [Blocking Execution of Specific Events](audit-log-filter-definitions.md#audit-log-filtering-blocking-events "Blocking Execution of Specific Events")
- [Logical Operators](audit-log-filter-definitions.md#audit-log-filtering-logical-operators "Logical Operators")
- [Referencing Predefined Variables](audit-log-filter-definitions.md#audit-log-filtering-predefined-variables "Referencing Predefined Variables")
- [Referencing Predefined Functions](audit-log-filter-definitions.md#audit-log-filtering-predefined-functions "Referencing Predefined Functions")
- [Replacement of Event Field Values](audit-log-filter-definitions.md#audit-log-filtering-field-replacement "Replacement of Event Field Values")
- [Replacing a User Filter](audit-log-filter-definitions.md#audit-log-filtering-filter-replacement "Replacing a User Filter")

##### Logging All Events

To explicitly enable or disable logging of all events, use a
`log` item in the filter:

```json
{
  "filter": { "log": true }
}
```

The `log` value can be either
`true` or `false`.

The preceding filter enables logging of all events. It is
equivalent to:

```json
{
  "filter": { }
}
```

Logging behavior depends on the `log` value
and whether `class` or
`event` items are specified:

- With `log` specified, its given value is
  used.
- Without `log` specified, logging is
  `true` if no `class` or
  `event` item is specified, and
  `false` otherwise (in which case,
  `class` or `event` can
  include their own `log` item).

##### Logging Specific Event Classes

To log events of a specific class, use a
`class` item in the filter, with its
`name` field denoting the name of the class
to log:

```json
{
  "filter": {
    "class": { "name": "connection" }
  }
}
```

The `name` value can be
`connection`, `general`, or
`table_access` to log connection, general, or
table-access events, respectively.

The preceding filter enables logging of events in the
`connection` class. It is equivalent to the
following filter with `log` items made
explicit:

```json
{
  "filter": {
    "log": false,
    "class": { "log": true,
               "name": "connection" }
  }
}
```

To enable logging of multiple classes, define the
`class` value as a
[`JSON`](json.md "13.5 The JSON Data Type") array element that names
the classes:

```json
{
  "filter": {
    "class": [
      { "name": "connection" },
      { "name": "general" },
      { "name": "table_access" }
    ]
  }
}
```

Note

When multiple instances of a given item appear at the same
level within a filter definition, the item values can be
combined into a single instance of that item within an array
value. The preceding definition can be written like this:

```json
{
  "filter": {
    "class": [
      { "name": [ "connection", "general", "table_access" ] }
    ]
  }
}
```

##### Logging Specific Event Subclasses

To select specific event subclasses, use an
`event` item containing a
`name` item that names the subclasses. The
default action for events selected by an
`event` item is to log them. For example,
this filter enables logging for the named event subclasses:

```json
{
  "filter": {
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect" },
          { "name": "disconnect" }
        ]
      },
      { "name": "general" },
      {
        "name": "table_access",
        "event": [
          { "name": "insert" },
          { "name": "delete" },
          { "name": "update" }
        ]
      }
    ]
  }
}
```

The `event` item can also contain explicit
`log` items to indicate whether to log
qualifying events. This `event` item selects
multiple events and explicitly indicates logging behavior for
them:

```json
"event": [
  { "name": "read", "log": false },
  { "name": "insert", "log": true },
  { "name": "delete", "log": true },
  { "name": "update", "log": true }
]
```

The `event` item can also indicate whether to
block qualifying events, if it contains an
`abort` item. For details, see
[Blocking Execution of Specific Events](audit-log-filter-definitions.md#audit-log-filtering-blocking-events "Blocking Execution of Specific Events").

[Table 8.35, “Event Class and Subclass Combinations”](audit-log-filter-definitions.md#audit-log-event-subclass-combinations "Table 8.35 Event Class and Subclass Combinations")
describes the permitted subclass values for each event class.

**Table 8.35 Event Class and Subclass Combinations**

| Event Class | Event Subclass | Description |
| --- | --- | --- |
| `connection` | `connect` | Connection initiation (successful or unsuccessful) |
| `connection` | `change_user` | User re-authentication with different user/password during session |
| `connection` | `disconnect` | Connection termination |
| `general` | `status` | General operation information |
| `message` | `internal` | Internally generated message |
| `message` | `user` | Message generated by [`audit_api_message_emit_udf()`](audit-api-message-emit.md#function_audit-api-message-emit-udf) |
| `table_access` | `read` | Table read statements, such as [`SELECT`](select.md "15.2.13 SELECT Statement") or [`INSERT INTO ... SELECT`](insert-select.md "15.2.7.1 INSERT ... SELECT Statement") |
| `table_access` | `delete` | Table delete statements, such as [`DELETE`](delete.md "15.2.2 DELETE Statement") or [`TRUNCATE TABLE`](truncate-table.md "15.1.37 TRUNCATE TABLE Statement") |
| `table_access` | `insert` | Table insert statements, such as [`INSERT`](insert.md "15.2.7 INSERT Statement") or [`REPLACE`](replace.md "15.2.12 REPLACE Statement") |
| `table_access` | `update` | Table update statements, such as [`UPDATE`](update.md "15.2.17 UPDATE Statement") |

[Table 8.36, “Log and Abort Characteristics Per Event Class and Subclass Combination”](audit-log-filter-definitions.md#audit-log-event-subclass-log-abort "Table 8.36 Log and Abort Characteristics Per Event Class and Subclass Combination") describes
for each event subclass whether it can be logged or aborted.

**Table 8.36 Log and Abort Characteristics Per Event Class and Subclass Combination**

| Event Class | Event Subclass | Can be Logged | Can be Aborted |
| --- | --- | --- | --- |
| `connection` | `connect` | Yes | No |
| `connection` | `change_user` | Yes | No |
| `connection` | `disconnect` | Yes | No |
| `general` | `status` | Yes | No |
| `message` | `internal` | Yes | Yes |
| `message` | `user` | Yes | Yes |
| `table_access` | `read` | Yes | Yes |
| `table_access` | `delete` | Yes | Yes |
| `table_access` | `insert` | Yes | Yes |
| `table_access` | `update` | Yes | Yes |

##### Inclusive and Exclusive Logging

A filter can be defined in inclusive or exclusive mode:

- Inclusive mode logs only explicitly specified items.
- Exclusive mode logs everything but explicitly specified
  items.

To perform inclusive logging, disable logging globally and
enable logging for specific classes. This filter logs
`connect` and `disconnect`
events in the `connection` class, and events
in the `general` class:

```json
{
  "filter": {
    "log": false,
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect", "log": true },
          { "name": "disconnect", "log": true }
        ]
      },
      { "name": "general", "log": true }
    ]
  }
}
```

To perform exclusive logging, enable logging globally and
disable logging for specific classes. This filter logs
everything except events in the `general`
class:

```json
{
  "filter": {
    "log": true,
    "class":
      { "name": "general", "log": false }
  }
}
```

This filter logs `change_user` events in the
`connection` class,
`message` events, and
`table_access` events, by virtue of
*not* logging everything else:

```json
{
  "filter": {
    "log": true,
    "class": [
      {
        "name": "connection",
        "event": [
          { "name": "connect", "log": false },
          { "name": "disconnect", "log": false }
        ]
      },
      { "name": "general", "log": false }
    ]
  }
}
```

##### Testing Event Field Values

To enable logging based on specific event field values,
specify a `field` item within the
`log` item that indicates the field name and
its expected value:

```json
{
  "filter": {
    "class": {
    "name": "general",
      "event": {
        "name": "status",
        "log": {
          "field": { "name": "general_command.str", "value": "Query" }
        }
      }
    }
  }
}
```

Each event contains event class-specific fields that can be
accessed from within a filter to perform custom filtering.

An event in the `connection` class indicates
when a connection-related activity occurs during a session,
such as a user connecting to or disconnecting from the server.
[Table 8.37, “Connection Event Fields”](audit-log-filter-definitions.md#audit-log-connection-event-fields "Table 8.37 Connection Event Fields") indicates
the permitted fields for `connection` events.

**Table 8.37 Connection Event Fields**

| Field Name | Field Type | Description |
| --- | --- | --- |
| `status` | integer | Event status:  0: OK  Otherwise: Failed |
| `connection_id` | unsigned integer | Connection ID |
| `user.str` | string | User name specified during authentication |
| `user.length` | unsigned integer | User name length |
| `priv_user.str` | string | Authenticated user name (account user name) |
| `priv_user.length` | unsigned integer | Authenticated user name length |
| `external_user.str` | string | External user name (provided by third-party authentication plugin) |
| `external_user.length` | unsigned integer | External user name length |
| `proxy_user.str` | string | Proxy user name |
| `proxy_user.length` | unsigned integer | Proxy user name length |
| `host.str` | string | Connected user host |
| `host.length` | unsigned integer | Connected user host length |
| `ip.str` | string | Connected user IP address |
| `ip.length` | unsigned integer | Connected user IP address length |
| `database.str` | string | Database name specified at connect time |
| `database.length` | unsigned integer | Database name length |
| `connection_type` | integer | Connection type:  0 or `"::undefined"`: Undefined  1 or `"::tcp/ip"`: TCP/IP  2 or `"::socket"`: Socket  3 or `"::named_pipe"`: Named pipe  4 or `"::ssl"`: TCP/IP with encryption  5 or `"::shared_memory"`: Shared memory |

The `"::xxx"`
values are symbolic pseudo-constants that may be given instead
of the literal numeric values. They must be quoted as strings
and are case-sensitive.

An event in the `general` class indicates the
status code of an operation and its details.
[Table 8.38, “General Event Fields”](audit-log-filter-definitions.md#audit-log-general-event-fields "Table 8.38 General Event Fields") indicates the
permitted fields for `general` events.

**Table 8.38 General Event Fields**

| Field Name | Field Type | Description |
| --- | --- | --- |
| `general_error_code` | integer | Event status:  0: OK  Otherwise: Failed |
| `general_thread_id` | unsigned integer | Connection/thread ID |
| `general_user.str` | string | User name specified during authentication |
| `general_user.length` | unsigned integer | User name length |
| `general_command.str` | string | Command name |
| `general_command.length` | unsigned integer | Command name length |
| `general_query.str` | string | SQL statement text |
| `general_query.length` | unsigned integer | SQL statement text length |
| `general_host.str` | string | Host name |
| `general_host.length` | unsigned integer | Host name length |
| `general_sql_command.str` | string | SQL command type name |
| `general_sql_command.length` | unsigned integer | SQL command type name length |
| `general_external_user.str` | string | External user name (provided by third-party authentication plugin) |
| `general_external_user.length` | unsigned integer | External user name length |
| `general_ip.str` | string | Connected user IP address |
| `general_ip.length` | unsigned integer | Connection user IP address length |

`general_command.str` indicates a command
name: `Query`, `Execute`,
`Quit`, or `Change user`.

A `general` event with the
`general_command.str` field set to
`Query` or `Execute`
contains `general_sql_command.str` set to a
value that specifies the type of SQL command:
`alter_db`,
`alter_db_upgrade`,
`admin_commands`, and so forth. The available
`general_sql_command.str` values can be seen
as the last components of the Performance Schema instruments
displayed by this statement:

```sql
mysql> SELECT NAME FROM performance_schema.setup_instruments
       WHERE NAME LIKE 'statement/sql/%' ORDER BY NAME;
+---------------------------------------+
| NAME                                  |
+---------------------------------------+
| statement/sql/alter_db                |
| statement/sql/alter_db_upgrade        |
| statement/sql/alter_event             |
| statement/sql/alter_function          |
| statement/sql/alter_instance          |
| statement/sql/alter_procedure         |
| statement/sql/alter_server            |
...
```

An event in the `table_access` class provides
information about a specific type of access to a table.
[Table 8.39, “Table-Access Event Fields”](audit-log-filter-definitions.md#audit-log-table-access-event-fields "Table 8.39 Table-Access Event Fields")
indicates the permitted fields for
`table_access` events.

**Table 8.39 Table-Access Event Fields**

| Field Name | Field Type | Description |
| --- | --- | --- |
| `connection_id` | unsigned integer | Event connection ID |
| `sql_command_id` | integer | SQL command ID |
| `query.str` | string | SQL statement text |
| `query.length` | unsigned integer | SQL statement text length |
| `table_database.str` | string | Database name associated with event |
| `table_database.length` | unsigned integer | Database name length |
| `table_name.str` | string | Table name associated with event |
| `table_name.length` | unsigned integer | Table name length |

The following list shows which statements produce which
table-access events:

- `read` event:

  - `SELECT`
  - `INSERT ... SELECT` (for tables
    referenced in `SELECT` clause)
  - `REPLACE ... SELECT` (for tables
    referenced in `SELECT` clause)
  - `UPDATE ... WHERE` (for tables
    referenced in `WHERE` clause)
  - `HANDLER ... READ`
- `delete` event:

  - `DELETE`
  - `TRUNCATE TABLE`
- `insert` event:

  - `INSERT`
  - `INSERT ... SELECT` (for table
    referenced in `INSERT` clause)
  - `REPLACE`
  - `REPLACE ... SELECT` (for table
    referenced in `REPLACE` clause
  - `LOAD DATA`
  - `LOAD XML`
- `update` event:

  - `UPDATE`
  - `UPDATE ... WHERE` (for tables
    referenced in `UPDATE` clause)

##### Blocking Execution of Specific Events

`event` items can include an
`abort` item that indicates whether to
prevent qualifying events from executing.
`abort` enables rules to be written that
block execution of specific SQL statements.

Important

It is theoretically possible for a user with sufficient
permissions to mistakenly create an `abort`
item in the audit log filter that prevents themselves and
other administrators from accessing the system. From MySQL
8.0.28, the
[`AUDIT_ABORT_EXEMPT`](privileges-provided.md#priv_audit-abort-exempt)
privilege is available to permit a user account’s queries
to always be executed even if an `abort`
item would block them. Accounts with this privilege can
therefore be used to regain access to a system following an
audit misconfiguration. The query is still logged in the
audit log, but instead of being rejected, it is permitted
due to the privilege.

Accounts created in MySQL 8.0.28 or later with the
[`SYSTEM_USER`](privileges-provided.md#priv_system-user) privilege have
the [`AUDIT_ABORT_EXEMPT`](privileges-provided.md#priv_audit-abort-exempt)
privilege assigned automatically when they are created. The
[`AUDIT_ABORT_EXEMPT`](privileges-provided.md#priv_audit-abort-exempt) privilege
is also assigned to existing accounts with the
[`SYSTEM_USER`](privileges-provided.md#priv_system-user)
privilege when you carry out an upgrade procedure with MySQL
8.0.28 or later, if no existing accounts have that privilege
assigned.

The `abort` item must appear within an
`event` item. For example:

```json
"event": {
  "name": qualifying event subclass names
  "abort": condition
}
```

For event subclasses selected by the `name`
item, the `abort` action is true or false,
depending on *`condition`* evaluation.
If the condition evaluates to true, the event is blocked.
Otherwise, the event continues executing.

The *`condition`* specification can be
as simple as `true` or
`false`, or it can be more complex such that
evaluation depends on event characteristics.

This filter blocks [`INSERT`](insert.md "15.2.7 INSERT Statement"),
[`UPDATE`](update.md "15.2.17 UPDATE Statement"), and
[`DELETE`](delete.md "15.2.2 DELETE Statement") statements:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": [ "insert", "update", "delete" ],
        "abort": true
      }
    }
  }
}
```

This more complex filter blocks the same statements, but only
for a specific table
(`finances.bank_account`):

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": [ "insert", "update", "delete" ],
        "abort": {
          "and": [
            { "field": { "name": "table_database.str", "value": "finances" } },
            { "field": { "name": "table_name.str", "value": "bank_account" } }
          ]
        }
      }
    }
  }
}
```

Statements matched and blocked by the filter return an error
to the client:

```none
ERROR 1045 (28000): Statement was aborted by an audit log filter
```

Not all events can be blocked (see
[Table 8.36, “Log and Abort Characteristics Per Event Class and Subclass Combination”](audit-log-filter-definitions.md#audit-log-event-subclass-log-abort "Table 8.36 Log and Abort Characteristics Per Event Class and Subclass Combination")). For an
event that cannot be blocked, the audit log writes a warning
to the error log rather than blocking it.

For attempts to define a filter in which the
`abort` item appears elsewhere than in an
`event` item, an error occurs.

##### Logical Operators

Logical operators (`and`,
`or`, `not`) permit
construction of complex conditions, enabling more advanced
filtering configurations to be written. The following
`log` item logs only
`general` events with
`general_command` fields having a specific
value and length:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "or": [
            {
              "and": [
                { "field": { "name": "general_command.str",    "value": "Query" } },
                { "field": { "name": "general_command.length", "value": 5 } }
              ]
            },
            {
              "and": [
                { "field": { "name": "general_command.str",    "value": "Execute" } },
                { "field": { "name": "general_command.length", "value": 7 } }
              ]
            }
          ]
        }
      }
    }
  }
}
```

##### Referencing Predefined Variables

To refer to a predefined variable in a `log`
condition, use a `variable` item, which takes
`name` and `value` items and
tests equality of the named variable against a given value:

```json
"variable": {
  "name": "variable_name",
  "value": comparison_value
}
```

This is true if *`variable_name`* has
the value *`comparison_value`*, false
otherwise.

Example:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "variable": {
            "name": "audit_log_connection_policy_value",
            "value": "::none"
          }
        }
      }
    }
  }
}
```

Each predefined variable corresponds to a system variable. By
writing a filter that tests a predefined variable, you can
modify filter operation by setting the corresponding system
variable, without having to redefine the filter. For example,
by writing a filter that tests the value of the
`audit_log_connection_policy_value`
predefined variable, you can modify filter operation by
changing the value of the
[`audit_log_connection_policy`](audit-log-reference.md#sysvar_audit_log_connection_policy)
system variable.

The
`audit_log_xxx_policy`
system variables are used for the deprecated legacy mode audit
log (see [Section 8.4.5.10, “Legacy Mode Audit Log Filtering”](audit-log-legacy-filtering.md "8.4.5.10 Legacy Mode Audit Log Filtering")). With
rule-based audit log filtering, those variables remain visible
(for example, using [`SHOW
VARIABLES`](show-variables.md "15.7.7.41 SHOW VARIABLES Statement")), but changes to them have no effect
unless you write filters containing constructs that refer to
them.

The following list describes the permitted predefined
variables for `variable` items:

- `audit_log_connection_policy_value`

  This variable corresponds to the value of the
  [`audit_log_connection_policy`](audit-log-reference.md#sysvar_audit_log_connection_policy)
  system variable. The value is an unsigned integer.
  [Table 8.40, “audit\_log\_connection\_policy\_value Values”](audit-log-filter-definitions.md#audit-log-connection-policy-value-values "Table 8.40 audit_log_connection_policy_value Values")
  shows the permitted values and the corresponding
  [`audit_log_connection_policy`](audit-log-reference.md#sysvar_audit_log_connection_policy)
  values.

  **Table 8.40 audit\_log\_connection\_policy\_value Values**

  | Value | Corresponding audit\_log\_connection\_policy Value |
  | --- | --- |
  | `0` or `"::none"` | `NONE` |
  | `1` or `"::errors"` | `ERRORS` |
  | `2` or `"::all"` | `ALL` |

  The `"::xxx"`
  values are symbolic pseudo-constants that may be given
  instead of the literal numeric values. They must be quoted
  as strings and are case-sensitive.
- `audit_log_policy_value`

  This variable corresponds to the value of the
  [`audit_log_policy`](audit-log-reference.md#sysvar_audit_log_policy) system
  variable. The value is an unsigned integer.
  [Table 8.41, “audit\_log\_policy\_value Values”](audit-log-filter-definitions.md#audit-log-policy-value-values "Table 8.41 audit_log_policy_value Values") shows the
  permitted values and the corresponding
  [`audit_log_policy`](audit-log-reference.md#sysvar_audit_log_policy) values.

  **Table 8.41 audit\_log\_policy\_value Values**

  | Value | Corresponding audit\_log\_policy Value |
  | --- | --- |
  | `0` or `"::none"` | `NONE` |
  | `1` or `"::logins"` | `LOGINS` |
  | `2` or `"::all"` | `ALL` |
  | `3` or `"::queries"` | `QUERIES` |

  The `"::xxx"`
  values are symbolic pseudo-constants that may be given
  instead of the literal numeric values. They must be quoted
  as strings and are case-sensitive.
- `audit_log_statement_policy_value`

  This variable corresponds to the value of the
  [`audit_log_statement_policy`](audit-log-reference.md#sysvar_audit_log_statement_policy)
  system variable. The value is an unsigned integer.
  [Table 8.42, “audit\_log\_statement\_policy\_value Values”](audit-log-filter-definitions.md#audit-log-statement-policy-value-values "Table 8.42 audit_log_statement_policy_value Values")
  shows the permitted values and the corresponding
  [`audit_log_statement_policy`](audit-log-reference.md#sysvar_audit_log_statement_policy)
  values.

  **Table 8.42 audit\_log\_statement\_policy\_value Values**

  | Value | Corresponding audit\_log\_statement\_policy Value |
  | --- | --- |
  | `0` or `"::none"` | `NONE` |
  | `1` or `"::errors"` | `ERRORS` |
  | `2` or `"::all"` | `ALL` |

  The `"::xxx"`
  values are symbolic pseudo-constants that may be given
  instead of the literal numeric values. They must be quoted
  as strings and are case-sensitive.

##### Referencing Predefined Functions

To refer to a predefined function in a `log`
condition, use a `function` item, which takes
`name` and `args` items to
specify the function name and its arguments, respectively:

```json
"function": {
  "name": "function_name",
  "args": arguments
}
```

The `name` item should specify the function
name only, without parentheses or the argument list.

The `args` item must satisfy these
conditions:

- If the function takes no arguments, no
  `args` item should be given.
- If the function does take arguments, an
  `args` item is needed, and the arguments
  must be given in the order listed in the function
  description. Arguments can refer to predefined variables,
  event fields, or string or numeric constants.

If the number of arguments is incorrect or the arguments are
not of the correct data types required by the function an
error occurs.

Example:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "log": {
          "function": {
            "name": "find_in_include_list",
            "args": [ { "string": [ { "field": "user.str" },
                                    { "string": "@"},
                                    { "field": "host.str" } ] } ]
          }
        }
      }
    }
  }
}
```

The preceding filter determines whether to log
`general` class `status`
events depending on whether the current user is found in the
[`audit_log_include_accounts`](audit-log-reference.md#sysvar_audit_log_include_accounts)
system variable. That user is constructed using fields in the
event.

The following list describes the permitted predefined
functions for `function` items:

- `audit_log_exclude_accounts_is_null()`

  Checks whether the
  [`audit_log_exclude_accounts`](audit-log-reference.md#sysvar_audit_log_exclude_accounts)
  system variable is `NULL`. This function
  can be helpful when defining filters that correspond to
  the legacy audit log implementation.

  Arguments:

  None.
- `audit_log_include_accounts_is_null()`

  Checks whether the
  [`audit_log_include_accounts`](audit-log-reference.md#sysvar_audit_log_include_accounts)
  system variable is `NULL`. This function
  can be helpful when defining filters that correspond to
  the legacy audit log implementation.

  Arguments:

  None.
- `debug_sleep(millisec)`

  Sleeps for the given number of milliseconds. This function
  is used during performance measurement.

  `debug_sleep()` is available for debug
  builds only.

  Arguments:

  - *`millisec`*: An unsigned
    integer that specifies the number of milliseconds to
    sleep.
- `find_in_exclude_list(account)`

  Checks whether an account string exists in the audit log
  exclude list (the value of the
  [`audit_log_exclude_accounts`](audit-log-reference.md#sysvar_audit_log_exclude_accounts)
  system variable).

  Arguments:

  - *`account`*: A string that
    specifies the user account name.
- `find_in_include_list(account)`

  Checks whether an account string exists in the audit log
  include list (the value of the
  [`audit_log_include_accounts`](audit-log-reference.md#sysvar_audit_log_include_accounts)
  system variable).

  Arguments:

  - *`account`*: A string that
    specifies the user account name.
- `query_digest([str])`

  This function has differing behavior depending on whether
  an argument is given:

  - With no argument, `query_digest`
    returns the statement digest value corresponding to
    the statement literal text in the current event.
  - With an argument, `query_digest`
    returns a Boolean indicating whether the argument is
    equal to the current statement digest.

  Arguments:

  - *`str`*: This argument is
    optional. If given, it specifies a statement digest to
    be compared against the digest for the statement in
    the current event.

  Examples:

  This `function` item includes no
  argument, so `query_digest` returns the
  current statement digest as a string:

  ```json
  "function": {
    "name": "query_digest"
  }
  ```

  This `function` item includes an
  argument, so `query_digest` returns a
  Boolean indicating whether the argument equals the current
  statement digest:

  ```json
  "function": {
    "name": "query_digest",
    "args": "SELECT ?"
  }
  ```

  This function was added in MySQL 8.0.26.
- `string_find(text, substr)`

  Checks whether the `substr` value is
  contained in the `text` value. This
  search is case-sensitive.

  Arguments:

  - *`text`*: The text string to
    search.
  - *`substr`*: The substring to
    search for in *`text`*.

##### Replacement of Event Field Values

As of MySQL 8.0.26, audit filter definitions support
replacement of certain audit event fields, so that logged
events contain the replacement value rather than the original
value. This capability enables logged audit records to include
statement digests rather than literal statements, which can be
useful for MySQL deployments for which statements may expose
sensitive values.

Field replacement in audit events works like this:

- Field replacements are specified in audit filter
  definitions, so audit log filtering must be enabled as
  described in [Section 8.4.5.7, “Audit Log Filtering”](audit-log-filtering.md "8.4.5.7 Audit Log Filtering").
- Not all fields can be replaced.
  [Table 8.43, “Event Fields Subject to Replacement”](audit-log-filter-definitions.md#audit-log-replaceable-event-fields "Table 8.43 Event Fields Subject to Replacement") shows
  which fields are replaceable in which event classes.

  **Table 8.43 Event Fields Subject to Replacement**

  | Event Class | Field Name |
  | --- | --- |
  | `general` | `general_query.str` |
  | `table_access` | `query.str` |
- Replacement is conditional. Each replacement specification
  in a filter definition includes a condition, enabling a
  replaceable field to be changed, or left unchanged,
  depending on the condition result.
- If replacement occurs, the replacement specification
  indicates the replacement value using a function that is
  permitted for that purpose.

As [Table 8.43, “Event Fields Subject to Replacement”](audit-log-filter-definitions.md#audit-log-replaceable-event-fields "Table 8.43 Event Fields Subject to Replacement") shows,
currently the only replaceable fields are those that contain
statement text (which occurs in events of the
`general` and `table_access`
classes). In addition, the only function permitted for
specifying the replacement value is
`query_digest`. This means that the only
permitted replacement operation is to replace statement
literal text by its corresponding digest.

Because field replacement occurs at an early auditing stage
(during filtering), the choice of whether to write statement
literal text or digest values applies regardless of log format
written later (that is, whether the audit log plugin produces
XML or JSON output).

Field replacement can take place at differing levels of event
granularity:

- To perform field replacement for all events in a class,
  filter events at the class level.
- To perform replacement on a more fine-grained basis,
  include additional event-selection items. For example, you
  can perform field replacement only for specific subclasses
  of a given event class, or only in events for which fields
  have certain characteristics.

Within a filter definition, specify field replacement by
including a `print` item, which has this
syntax:

```json
"print": {
  "field": {
    "name": "field_name",
    "print": condition,
    "replace": replacement_value
  }
}
```

Within the `print` item, its
`field` item takes these three items to
indicate how whether and how replacement occurs:

- `name`: The field for which replacement
  (potentially) occurs.
  *`field_name`* must be one of those
  shown in
  [Table 8.43, “Event Fields Subject to Replacement”](audit-log-filter-definitions.md#audit-log-replaceable-event-fields "Table 8.43 Event Fields Subject to Replacement").
- `print`: The condition that determines
  whether to retain the original field value or replace it:

  - If *`condition`* evaluates to
    `true`, the field remains unchanged.
  - If *`condition`* evaluates to
    `false`, replacement occurs, using
    the value of the `replace` item.

  To unconditionally replace a field, specify the condition
  like this:

  ```json
  "print": false
  ```
- `replace`: The replacement value to use
  when the `print` condition evaluates to
  `false`. Specify
  *`replacement_value`* using a
  `function` item.

For example, this filter definition applies to all events in
the `general` class, replacing the statement
literal text with its digest:

```json
{
  "filter": {
    "class": {
      "name": "general",
      "print": {
        "field": {
          "name": "general_query.str",
          "print": false,
          "replace": {
            "function": {
              "name": "query_digest"
            }
          }
        }
      }
    }
  }
}
```

The preceding filter uses this `print` item
to unconditionally replace the statement literal text
contained in `general_query.str` by its
digest value:

```json
"print": {
  "field": {
    "name": "general_query.str",
    "print": false,
    "replace": {
      "function": {
        "name": "query_digest"
      }
    }
  }
}
```

`print` items can be written different ways
to implement different replacement strategies. The
`replace` item just shown specifies the
replacement text using this `function`
construct to return a string representing the current
statement digest:

```json
"function": {
  "name": "query_digest"
}
```

The `query_digest` function can also be used
in another way, as a comparator that returns a Boolean, which
enables its use in the `print` condition. To
do this, provide an argument that specifies a comparison
statement digest:

```json
"function": {
  "name": "query_digest",
  "args": "digest"
}
```

In this case, `query_digest` returns
`true` or `false` depending
on whether the current statement digest is the same as the
comparison digest. Using `query_digest` this
way enables filter definitions to detect statements that match
particular digests. The condition in the following construct
is true only for statements that have a digest equal to
`SELECT ?`, thus effecting replacement only
for statements that do not match the digest:

```json
"print": {
  "field": {
    "name": "general_query.str",
    "print": {
      "function": {
        "name": "query_digest",
        "args": "SELECT ?"
      }
    },
    "replace": {
      "function": {
        "name": "query_digest"
      }
    }
  }
}
```

To perform replacement only for statements that do match the
digest, use `not` to invert the condition:

```json
"print": {
  "field": {
    "name": "general_query.str",
    "print": {
      "not": {
        "function": {
          "name": "query_digest",
          "args": "SELECT ?"
        }
      }
    },
    "replace": {
      "function": {
        "name": "query_digest"
      }
    }
  }
}
```

Suppose that you want the audit log to contain only statement
digests and not literal statements. To achieve this, you must
perform replacement on all events that contain statement text;
that is, events in the `general` and
`table_access` classes. An earlier filter
definition showed how to unconditionally replace statement
text for `general` events. To do the same for
`table_access` events, use a filter that is
similar but changes the class from `general`
to `table_access` and the field name from
`general_query.str` to
`query.str`:

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "print": {
        "field": {
          "name": "query.str",
          "print": false,
          "replace": {
            "function": {
              "name": "query_digest"
            }
          }
        }
      }
    }
  }
}
```

Combining the `general` and
`table_access` filters results in a single
filter that performs replacement for all statement
text-containing events:

```json
{
  "filter": {
    "class": [
      {
        "name": "general",
        "print": {
          "field": {
            "name": "general_query.str",
            "print": false,
            "replace": {
              "function": {
                "name": "query_digest"
              }
            }
          }
        }
      },
      {
        "name": "table_access",
        "print": {
          "field": {
            "name": "query.str",
            "print": false,
            "replace": {
              "function": {
                "name": "query_digest"
              }
            }
          }
        }
      }
    ]
  }
}
```

To perform replacement on only some events within a class, add
items to the filter that indicate more specifically when
replacement occurs. The following filter applies to events in
the `table_access` class, but performs
replacement only for `insert` and
`update` events (leaving
`read` and `delete` events
unchanged):

```json
{
  "filter": {
    "class": {
      "name": "table_access",
      "event": {
        "name": [
          "insert",
          "update"
        ],
        "print": {
          "field": {
            "name": "query.str",
            "print": false,
            "replace": {
              "function": {
                "name": "query_digest"
              }
            }
          }
        }
      }
    }
  }
}
```

This filter performs replacement for
`general` class events corresponding to the
listed account-management statements (the effect being to hide
credential and data values in the statements):

```json
{
  "filter": {
    "class": {
      "name": "general",
      "event": {
        "name": "status",
        "print": {
          "field": {
            "name": "general_query.str",
            "print": false,
            "replace": {
              "function": {
                "name": "query_digest"
              }
            }
          }
        },
        "log": {
          "or": [
            {
              "field": {
                "name": "general_sql_command.str",
                "value": "alter_user"
              }
            },
            {
              "field": {
                "name": "general_sql_command.str",
                "value": "alter_user_default_role"
              }
            },
            {
              "field": {
                "name": "general_sql_command.str",
                "value": "create_role"
              }
            },
            {
              "field": {
                "name": "general_sql_command.str",
                "value": "create_user"
              }
            }
          ]
        }
      }
    }
  }
}
```

For information about the possible
`general_sql_command.str` values, see
[Testing Event Field Values](audit-log-filter-definitions.md#audit-log-filtering-event-fields "Testing Event Field Values").

##### Replacing a User Filter

In some cases, the filter definition can be changed
dynamically. To do this, define a `filter`
configuration within an existing `filter`.
For example:

```json
{
  "filter": {
    "id": "main",
    "class": {
      "name": "table_access",
      "event": {
        "name": [ "update", "delete" ],
        "log": false,
        "filter": {
          "class": {
            "name": "general",
            "event" : { "name": "status",
                        "filter": { "ref": "main" } }
          },
          "activate": {
            "or": [
              { "field": { "name": "table_name.str", "value": "temp_1" } },
              { "field": { "name": "table_name.str", "value": "temp_2" } }
            ]
          }
        }
      }
    }
  }
}
```

A new filter is activated when the `activate`
item within a subfilter evaluates to `true`.
Using `activate` in a top-level
`filter` is not permitted.

A new filter can be replaced with the original one by using a
`ref` item inside the subfilter to refer to
the original filter `id`.

The filter shown operates like this:

- The `main` filter waits for
  `table_access` events, either
  `update` or `delete`.
- If the `update` or
  `delete` `table_access`
  event occurs on the `temp_1` or
  `temp_2` table, the filter is replaced
  with the internal one (without an `id`,
  since there is no need to refer to it explicitly).
- If the end of the command is signalled
  (`general` / `status`
  event), an entry is written to the audit log file and the
  filter is replaced with the `main`
  filter.

The filter is useful to log statements that update or delete
anything from the `temp_1` or
`temp_2` tables, such as this one:

```sql
UPDATE temp_1, temp_3 SET temp_1.a=21, temp_3.a=23;
```

The statement generates multiple
`table_access` events, but the audit log file
contains only `general` /
`status` entries.

Note

Any `id` values used in the definition are
evaluated with respect only to that definition. They have
nothing to do with the value of the
[`audit_log_filter_id`](audit-log-reference.md#sysvar_audit_log_filter_id) system
variable.
