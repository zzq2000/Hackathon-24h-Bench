## 14.1 Built-In Function and Operator Reference

The following table lists each built-in (native) function and
operator and provides a short description of each one. For a table
listing functions that are loadable at runtime, see
[Section 14.2, “Loadable Function Reference”](loadable-function-reference.md "14.2 Loadable Function Reference").

**Table 14.1 Built-In Functions and Operators**

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
| [`ABS()`](mathematical-functions.md#function_abs) | Return the absolute value |  |  |
| [`ACOS()`](mathematical-functions.md#function_acos) | Return the arc cosine |  |  |
| [`ADDDATE()`](date-and-time-functions.md#function_adddate) | Add time values (intervals) to a date value |  |  |
| [`ADDTIME()`](date-and-time-functions.md#function_addtime) | Add time |  |  |
| [`AES_DECRYPT()`](encryption-functions.md#function_aes-decrypt) | Decrypt using AES |  |  |
| [`AES_ENCRYPT()`](encryption-functions.md#function_aes-encrypt) | Encrypt using AES |  |  |
| [`AND`, `&&`](logical-operators.md#operator_and) | Logical AND |  |  |
| [`ANY_VALUE()`](miscellaneous-functions.md#function_any-value) | Suppress ONLY\_FULL\_GROUP\_BY value rejection |  |  |
| [`ASCII()`](string-functions.md#function_ascii) | Return numeric value of left-most character |  |  |
| [`ASIN()`](mathematical-functions.md#function_asin) | Return the arc sine |  |  |
| [`asynchronous_connection_failover_add_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-managed) | Add group member source server configuration information to a replication channel source list | 8.0.23 |  |
| [`asynchronous_connection_failover_add_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-add-source) | Add source server configuration information server to a replication channel source list | 8.0.22 |  |
| [`asynchronous_connection_failover_delete_managed()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-managed) | Remove a managed group from a replication channel source list | 8.0.23 |  |
| [`asynchronous_connection_failover_delete_source()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-delete-source) | Remove a source server from a replication channel source list | 8.0.22 |  |
| [`asynchronous_connection_failover_reset()`](replication-functions-async-failover.md#function_asynchronous-connection-failover-reset) | Remove all settings relating to group replication asynchronous failover | 8.0.27 |  |
| [`ATAN()`](mathematical-functions.md#function_atan) | Return the arc tangent |  |  |
| [`ATAN2()`, `ATAN()`](mathematical-functions.md#function_atan2) | Return the arc tangent of the two arguments |  |  |
| [`AVG()`](aggregate-functions.md#function_avg) | Return the average value of the argument |  |  |
| [`BENCHMARK()`](information-functions.md#function_benchmark) | Repeatedly execute an expression |  |  |
| [`BETWEEN ... AND ...`](comparison-operators.md#operator_between) | Whether a value is within a range of values |  |  |
| [`BIN()`](string-functions.md#function_bin) | Return a string containing binary representation of a number |  |  |
| [`BIN_TO_UUID()`](miscellaneous-functions.md#function_bin-to-uuid) | Convert binary UUID to string |  |  |
| [`BINARY`](cast-functions.md#operator_binary) | Cast a string to a binary string |  | 8.0.27 |
| [`BIT_AND()`](aggregate-functions.md#function_bit-and) | Return bitwise AND |  |  |
| [`BIT_COUNT()`](bit-functions.md#function_bit-count) | Return the number of bits that are set |  |  |
| [`BIT_LENGTH()`](string-functions.md#function_bit-length) | Return length of argument in bits |  |  |
| [`BIT_OR()`](aggregate-functions.md#function_bit-or) | Return bitwise OR |  |  |
| [`BIT_XOR()`](aggregate-functions.md#function_bit-xor) | Return bitwise XOR |  |  |
| [`CAN_ACCESS_COLUMN()`](internal-functions.md#function_can-access-column) | Internal use only |  |  |
| [`CAN_ACCESS_DATABASE()`](internal-functions.md#function_can-access-database) | Internal use only |  |  |
| [`CAN_ACCESS_TABLE()`](internal-functions.md#function_can-access-table) | Internal use only |  |  |
| [`CAN_ACCESS_USER()`](internal-functions.md#function_can-access-user) | Internal use only | 8.0.22 |  |
| [`CAN_ACCESS_VIEW()`](internal-functions.md#function_can-access-view) | Internal use only |  |  |
| [`CASE`](flow-control-functions.md#operator_case) | Case operator |  |  |
| [`CAST()`](cast-functions.md#function_cast) | Cast a value as a certain type |  |  |
| [`CEIL()`](mathematical-functions.md#function_ceil) | Return the smallest integer value not less than the argument |  |  |
| [`CEILING()`](mathematical-functions.md#function_ceiling) | Return the smallest integer value not less than the argument |  |  |
| [`CHAR()`](string-functions.md#function_char) | Return the character for each integer passed |  |  |
| [`CHAR_LENGTH()`](string-functions.md#function_char-length) | Return number of characters in argument |  |  |
| [`CHARACTER_LENGTH()`](string-functions.md#function_character-length) | Synonym for CHAR\_LENGTH() |  |  |
| [`CHARSET()`](information-functions.md#function_charset) | Return the character set of the argument |  |  |
| [`COALESCE()`](comparison-operators.md#function_coalesce) | Return the first non-NULL argument |  |  |
| [`COERCIBILITY()`](information-functions.md#function_coercibility) | Return the collation coercibility value of the string argument |  |  |
| [`COLLATION()`](information-functions.md#function_collation) | Return the collation of the string argument |  |  |
| [`COMPRESS()`](encryption-functions.md#function_compress) | Return result as a binary string |  |  |
| [`CONCAT()`](string-functions.md#function_concat) | Return concatenated string |  |  |
| [`CONCAT_WS()`](string-functions.md#function_concat-ws) | Return concatenate with separator |  |  |
| [`CONNECTION_ID()`](information-functions.md#function_connection-id) | Return the connection ID (thread ID) for the connection |  |  |
| [`CONV()`](mathematical-functions.md#function_conv) | Convert numbers between different number bases |  |  |
| [`CONVERT()`](cast-functions.md#function_convert) | Cast a value as a certain type |  |  |
| [`CONVERT_TZ()`](date-and-time-functions.md#function_convert-tz) | Convert from one time zone to another |  |  |
| [`COS()`](mathematical-functions.md#function_cos) | Return the cosine |  |  |
| [`COT()`](mathematical-functions.md#function_cot) | Return the cotangent |  |  |
| [`COUNT()`](aggregate-functions.md#function_count) | Return a count of the number of rows returned |  |  |
| [`COUNT(DISTINCT)`](aggregate-functions.md#function_count-distinct) | Return the count of a number of different values |  |  |
| [`CRC32()`](mathematical-functions.md#function_crc32) | Compute a cyclic redundancy check value |  |  |
| [`CUME_DIST()`](window-function-descriptions.md#function_cume-dist) | Cumulative distribution value |  |  |
| [`CURDATE()`](date-and-time-functions.md#function_curdate) | Return the current date |  |  |
| [`CURRENT_DATE()`, `CURRENT_DATE`](date-and-time-functions.md#function_current-date) | Synonyms for CURDATE() |  |  |
| [`CURRENT_ROLE()`](information-functions.md#function_current-role) | Return the current active roles |  |  |
| [`CURRENT_TIME()`, `CURRENT_TIME`](date-and-time-functions.md#function_current-time) | Synonyms for CURTIME() |  |  |
| [`CURRENT_TIMESTAMP()`, `CURRENT_TIMESTAMP`](date-and-time-functions.md#function_current-timestamp) | Synonyms for NOW() |  |  |
| [`CURRENT_USER()`, `CURRENT_USER`](information-functions.md#function_current-user) | The authenticated user name and host name |  |  |
| [`CURTIME()`](date-and-time-functions.md#function_curtime) | Return the current time |  |  |
| [`DATABASE()`](information-functions.md#function_database) | Return the default (current) database name |  |  |
| [`DATE()`](date-and-time-functions.md#function_date) | Extract the date part of a date or datetime expression |  |  |
| [`DATE_ADD()`](date-and-time-functions.md#function_date-add) | Add time values (intervals) to a date value |  |  |
| [`DATE_FORMAT()`](date-and-time-functions.md#function_date-format) | Format date as specified |  |  |
| [`DATE_SUB()`](date-and-time-functions.md#function_date-sub) | Subtract a time value (interval) from a date |  |  |
| [`DATEDIFF()`](date-and-time-functions.md#function_datediff) | Subtract two dates |  |  |
| [`DAY()`](date-and-time-functions.md#function_day) | Synonym for DAYOFMONTH() |  |  |
| [`DAYNAME()`](date-and-time-functions.md#function_dayname) | Return the name of the weekday |  |  |
| [`DAYOFMONTH()`](date-and-time-functions.md#function_dayofmonth) | Return the day of the month (0-31) |  |  |
| [`DAYOFWEEK()`](date-and-time-functions.md#function_dayofweek) | Return the weekday index of the argument |  |  |
| [`DAYOFYEAR()`](date-and-time-functions.md#function_dayofyear) | Return the day of the year (1-366) |  |  |
| [`DEFAULT()`](miscellaneous-functions.md#function_default) | Return the default value for a table column |  |  |
| [`DEGREES()`](mathematical-functions.md#function_degrees) | Convert radians to degrees |  |  |
| [`DENSE_RANK()`](window-function-descriptions.md#function_dense-rank) | Rank of current row within its partition, without gaps |  |  |
| [`DIV`](arithmetic-functions.md#operator_div) | Integer division |  |  |
| [`ELT()`](string-functions.md#function_elt) | Return string at index number |  |  |
| [`EXISTS()`](comparison-operators.md#operator_exists) | Whether the result of a query contains any rows |  |  |
| [`EXP()`](mathematical-functions.md#function_exp) | Raise to the power of |  |  |
| [`EXPORT_SET()`](string-functions.md#function_export-set) | Return a string such that for every bit set in the value bits, you get an on string and for every unset bit, you get an off string |  |  |
| [`EXTRACT()`](date-and-time-functions.md#function_extract) | Extract part of a date |  |  |
| [`ExtractValue()`](xml-functions.md#function_extractvalue) | Extract a value from an XML string using XPath notation |  |  |
| [`FIELD()`](string-functions.md#function_field) | Index (position) of first argument in subsequent arguments |  |  |
| [`FIND_IN_SET()`](string-functions.md#function_find-in-set) | Index (position) of first argument within second argument |  |  |
| [`FIRST_VALUE()`](window-function-descriptions.md#function_first-value) | Value of argument from first row of window frame |  |  |
| [`FLOOR()`](mathematical-functions.md#function_floor) | Return the largest integer value not greater than the argument |  |  |
| [`FORMAT()`](string-functions.md#function_format) | Return a number formatted to specified number of decimal places |  |  |
| [`FORMAT_BYTES()`](performance-schema-functions.md#function_format-bytes) | Convert byte count to value with units | 8.0.16 |  |
| [`FORMAT_PICO_TIME()`](performance-schema-functions.md#function_format-pico-time) | Convert time in picoseconds to value with units | 8.0.16 |  |
| [`FOUND_ROWS()`](information-functions.md#function_found-rows) | For a SELECT with a LIMIT clause, the number of rows that would be returned were there no LIMIT clause |  |  |
| [`FROM_BASE64()`](string-functions.md#function_from-base64) | Decode base64 encoded string and return result |  |  |
| [`FROM_DAYS()`](date-and-time-functions.md#function_from-days) | Convert a day number to a date |  |  |
| [`FROM_UNIXTIME()`](date-and-time-functions.md#function_from-unixtime) | Format Unix timestamp as a date |  |  |
| [`GeomCollection()`](gis-mysql-specific-functions.md#function_geomcollection) | Construct geometry collection from geometries |  |  |
| [`GeometryCollection()`](gis-mysql-specific-functions.md#function_geometrycollection) | Construct geometry collection from geometries |  |  |
| [`GET_DD_COLUMN_PRIVILEGES()`](internal-functions.md#function_get-dd-column-privileges) | Internal use only |  |  |
| [`GET_DD_CREATE_OPTIONS()`](internal-functions.md#function_get-dd-create-options) | Internal use only |  |  |
| [`GET_DD_INDEX_SUB_PART_LENGTH()`](internal-functions.md#function_get-dd-index-sub-part-length) | Internal use only |  |  |
| [`GET_FORMAT()`](date-and-time-functions.md#function_get-format) | Return a date format string |  |  |
| [`GET_LOCK()`](locking-functions.md#function_get-lock) | Get a named lock |  |  |
| [`GREATEST()`](comparison-operators.md#function_greatest) | Return the largest argument |  |  |
| [`GROUP_CONCAT()`](aggregate-functions.md#function_group-concat) | Return a concatenated string |  |  |
| [`group_replication_disable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-disable-member-action) | Disable member action for event specified | 8.0.26 |  |
| [`group_replication_enable_member_action()`](group-replication-functions-for-member-actions.md#function_group-replication-enable-member-action) | Enable member action for event specified | 8.0.26 |  |
| [`group_replication_get_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-get-communication-protocol) | Get version of group replication communication protocol currently in use | 8.0.16 |  |
| [`group_replication_get_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-get-write-concurrency) | Get maximum number of consensus instances currently set for group | 8.0.13 |  |
| [`group_replication_reset_member_actions()`](group-replication-functions-for-member-actions.md#function_group-replication-reset-member-actions) | Reset all member actions to defaults and configuration version number to 1 | 8.0.26 |  |
| [`group_replication_set_as_primary()`](group-replication-functions-for-new-primary.md#function_group-replication-set-as-primary) | Make a specific group member the primary | 8.0.29 |  |
| [`group_replication_set_communication_protocol()`](group-replication-functions-for-communication-protocol.md#function_group-replication-set-communication-protocol) | Set version for group replication communication protocol to use | 8.0.16 |  |
| [`group_replication_set_write_concurrency()`](group-replication-functions-for-maximum-consensus.md#function_group-replication-set-write-concurrency) | Set maximum number of consensus instances that can be executed in parallel | 8.0.13 |  |
| [`group_replication_switch_to_multi_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-multi-primary-mode) | Changes the mode of a group running in single-primary mode to multi-primary mode | 8.0.13 |  |
| [`group_replication_switch_to_single_primary_mode()`](group-replication-functions-for-mode.md#function_group-replication-switch-to-single-primary-mode) | Changes the mode of a group running in multi-primary mode to single-primary mode | 8.0.13 |  |
| [`GROUPING()`](miscellaneous-functions.md#function_grouping) | Distinguish super-aggregate ROLLUP rows from regular rows |  |  |
| [`GTID_SUBSET()`](gtid-functions.md#function_gtid-subset) | Return true if all GTIDs in subset are also in set; otherwise false. |  |  |
| [`GTID_SUBTRACT()`](gtid-functions.md#function_gtid-subtract) | Return all GTIDs in set that are not in subset. |  |  |
| [`HEX()`](string-functions.md#function_hex) | Hexadecimal representation of decimal or string value |  |  |
| [`HOUR()`](date-and-time-functions.md#function_hour) | Extract the hour |  |  |
| [`ICU_VERSION()`](information-functions.md#function_icu-version) | ICU library version |  |  |
| [`IF()`](flow-control-functions.md#function_if) | If/else construct |  |  |
| [`IFNULL()`](flow-control-functions.md#function_ifnull) | Null if/else construct |  |  |
| [`IN()`](comparison-operators.md#operator_in) | Whether a value is within a set of values |  |  |
| [`INET_ATON()`](miscellaneous-functions.md#function_inet-aton) | Return the numeric value of an IP address |  |  |
| [`INET_NTOA()`](miscellaneous-functions.md#function_inet-ntoa) | Return the IP address from a numeric value |  |  |
| [`INET6_ATON()`](miscellaneous-functions.md#function_inet6-aton) | Return the numeric value of an IPv6 address |  |  |
| [`INET6_NTOA()`](miscellaneous-functions.md#function_inet6-ntoa) | Return the IPv6 address from a numeric value |  |  |
| [`INSERT()`](string-functions.md#function_insert) | Insert substring at specified position up to specified number of characters |  |  |
| [`INSTR()`](string-functions.md#function_instr) | Return the index of the first occurrence of substring |  |  |
| [`INTERNAL_AUTO_INCREMENT()`](internal-functions.md#function_internal-auto-increment) | Internal use only |  |  |
| [`INTERNAL_AVG_ROW_LENGTH()`](internal-functions.md#function_internal-avg-row-length) | Internal use only |  |  |
| [`INTERNAL_CHECK_TIME()`](internal-functions.md#function_internal-check-time) | Internal use only |  |  |
| [`INTERNAL_CHECKSUM()`](internal-functions.md#function_internal-checksum) | Internal use only |  |  |
| [`INTERNAL_DATA_FREE()`](internal-functions.md#function_internal-data-free) | Internal use only |  |  |
| [`INTERNAL_DATA_LENGTH()`](internal-functions.md#function_internal-data-length) | Internal use only |  |  |
| [`INTERNAL_DD_CHAR_LENGTH()`](internal-functions.md#function_internal-dd-char-length) | Internal use only |  |  |
| [`INTERNAL_GET_COMMENT_OR_ERROR()`](internal-functions.md#function_internal-get-comment-or-error) | Internal use only |  |  |
| [`INTERNAL_GET_ENABLED_ROLE_JSON()`](internal-functions.md#function_internal-get-enabled-role-json) | Internal use only | 8.0.19 |  |
| [`INTERNAL_GET_HOSTNAME()`](internal-functions.md#function_internal-get-hostname) | Internal use only | 8.0.19 |  |
| [`INTERNAL_GET_USERNAME()`](internal-functions.md#function_internal-get-username) | Internal use only | 8.0.19 |  |
| [`INTERNAL_GET_VIEW_WARNING_OR_ERROR()`](internal-functions.md#function_internal-get-view-warning-or-error) | Internal use only |  |  |
| [`INTERNAL_INDEX_COLUMN_CARDINALITY()`](internal-functions.md#function_internal-index-column-cardinality) | Internal use only |  |  |
| [`INTERNAL_INDEX_LENGTH()`](internal-functions.md#function_internal-index-length) | Internal use only |  |  |
| [`INTERNAL_IS_ENABLED_ROLE()`](internal-functions.md#function_internal-is-enabled-role) | Internal use only | 8.0.19 |  |
| [`INTERNAL_IS_MANDATORY_ROLE()`](internal-functions.md#function_internal-is-mandatory-role) | Internal use only | 8.0.19 |  |
| [`INTERNAL_KEYS_DISABLED()`](internal-functions.md#function_internal-keys-disabled) | Internal use only |  |  |
| [`INTERNAL_MAX_DATA_LENGTH()`](internal-functions.md#function_internal-max-data-length) | Internal use only |  |  |
| [`INTERNAL_TABLE_ROWS()`](internal-functions.md#function_internal-table-rows) | Internal use only |  |  |
| [`INTERNAL_UPDATE_TIME()`](internal-functions.md#function_internal-update-time) | Internal use only |  |  |
| [`INTERVAL()`](comparison-operators.md#function_interval) | Return the index of the argument that is less than the first argument |  |  |
| [`IS`](comparison-operators.md#operator_is) | Test a value against a boolean |  |  |
| [`IS_FREE_LOCK()`](locking-functions.md#function_is-free-lock) | Whether the named lock is free |  |  |
| [`IS_IPV4()`](miscellaneous-functions.md#function_is-ipv4) | Whether argument is an IPv4 address |  |  |
| [`IS_IPV4_COMPAT()`](miscellaneous-functions.md#function_is-ipv4-compat) | Whether argument is an IPv4-compatible address |  |  |
| [`IS_IPV4_MAPPED()`](miscellaneous-functions.md#function_is-ipv4-mapped) | Whether argument is an IPv4-mapped address |  |  |
| [`IS_IPV6()`](miscellaneous-functions.md#function_is-ipv6) | Whether argument is an IPv6 address |  |  |
| [`IS NOT`](comparison-operators.md#operator_is-not) | Test a value against a boolean |  |  |
| [`IS NOT NULL`](comparison-operators.md#operator_is-not-null) | NOT NULL value test |  |  |
| [`IS NULL`](comparison-operators.md#operator_is-null) | NULL value test |  |  |
| [`IS_USED_LOCK()`](locking-functions.md#function_is-used-lock) | Whether the named lock is in use; return connection identifier if true |  |  |
| [`IS_UUID()`](miscellaneous-functions.md#function_is-uuid) | Whether argument is a valid UUID |  |  |
| [`ISNULL()`](comparison-operators.md#function_isnull) | Test whether the argument is NULL |  |  |
| [`JSON_ARRAY()`](json-creation-functions.md#function_json-array) | Create JSON array |  |  |
| [`JSON_ARRAY_APPEND()`](json-modification-functions.md#function_json-array-append) | Append data to JSON document |  |  |
| [`JSON_ARRAY_INSERT()`](json-modification-functions.md#function_json-array-insert) | Insert into JSON array |  |  |
| [`JSON_ARRAYAGG()`](aggregate-functions.md#function_json-arrayagg) | Return result set as a single JSON array |  |  |
| [`JSON_CONTAINS()`](json-search-functions.md#function_json-contains) | Whether JSON document contains specific object at path |  |  |
| [`JSON_CONTAINS_PATH()`](json-search-functions.md#function_json-contains-path) | Whether JSON document contains any data at path |  |  |
| [`JSON_DEPTH()`](json-attribute-functions.md#function_json-depth) | Maximum depth of JSON document |  |  |
| [`JSON_EXTRACT()`](json-search-functions.md#function_json-extract) | Return data from JSON document |  |  |
| [`JSON_INSERT()`](json-modification-functions.md#function_json-insert) | Insert data into JSON document |  |  |
| [`JSON_KEYS()`](json-search-functions.md#function_json-keys) | Array of keys from JSON document |  |  |
| [`JSON_LENGTH()`](json-attribute-functions.md#function_json-length) | Number of elements in JSON document |  |  |
| [`JSON_MERGE()`](json-modification-functions.md#function_json-merge) | Merge JSON documents, preserving duplicate keys. Deprecated synonym for JSON\_MERGE\_PRESERVE() |  | Yes |
| [`JSON_MERGE_PATCH()`](json-modification-functions.md#function_json-merge-patch) | Merge JSON documents, replacing values of duplicate keys |  |  |
| [`JSON_MERGE_PRESERVE()`](json-modification-functions.md#function_json-merge-preserve) | Merge JSON documents, preserving duplicate keys |  |  |
| [`JSON_OBJECT()`](json-creation-functions.md#function_json-object) | Create JSON object |  |  |
| [`JSON_OBJECTAGG()`](aggregate-functions.md#function_json-objectagg) | Return result set as a single JSON object |  |  |
| [`JSON_OVERLAPS()`](json-search-functions.md#function_json-overlaps) | Compares two JSON documents, returns TRUE (1) if these have any key-value pairs or array elements in common, otherwise FALSE (0) | 8.0.17 |  |
| [`JSON_PRETTY()`](json-utility-functions.md#function_json-pretty) | Print a JSON document in human-readable format |  |  |
| [`JSON_QUOTE()`](json-creation-functions.md#function_json-quote) | Quote JSON document |  |  |
| [`JSON_REMOVE()`](json-modification-functions.md#function_json-remove) | Remove data from JSON document |  |  |
| [`JSON_REPLACE()`](json-modification-functions.md#function_json-replace) | Replace values in JSON document |  |  |
| [`JSON_SCHEMA_VALID()`](json-validation-functions.md#function_json-schema-valid) | Validate JSON document against JSON schema; returns TRUE/1 if document validates against schema, or FALSE/0 if it does not | 8.0.17 |  |
| [`JSON_SCHEMA_VALIDATION_REPORT()`](json-validation-functions.md#function_json-schema-validation-report) | Validate JSON document against JSON schema; returns report in JSON format on outcome on validation including success or failure and reasons for failure | 8.0.17 |  |
| [`JSON_SEARCH()`](json-search-functions.md#function_json-search) | Path to value within JSON document |  |  |
| [`JSON_SET()`](json-modification-functions.md#function_json-set) | Insert data into JSON document |  |  |
| [`JSON_STORAGE_FREE()`](json-utility-functions.md#function_json-storage-free) | Freed space within binary representation of JSON column value following partial update |  |  |
| [`JSON_STORAGE_SIZE()`](json-utility-functions.md#function_json-storage-size) | Space used for storage of binary representation of a JSON document |  |  |
| [`JSON_TABLE()`](json-table-functions.md#function_json-table) | Return data from a JSON expression as a relational table |  |  |
| [`JSON_TYPE()`](json-attribute-functions.md#function_json-type) | Type of JSON value |  |  |
| [`JSON_UNQUOTE()`](json-modification-functions.md#function_json-unquote) | Unquote JSON value |  |  |
| [`JSON_VALID()`](json-attribute-functions.md#function_json-valid) | Whether JSON value is valid |  |  |
| [`JSON_VALUE()`](json-search-functions.md#function_json-value) | Extract value from JSON document at location pointed to by path provided; return this value as VARCHAR(512) or specified type | 8.0.21 |  |
| [`LAG()`](window-function-descriptions.md#function_lag) | Value of argument from row lagging current row within partition |  |  |
| [`LAST_DAY`](date-and-time-functions.md#function_last-day) | Return the last day of the month for the argument |  |  |
| [`LAST_INSERT_ID()`](information-functions.md#function_last-insert-id) | Value of the AUTOINCREMENT column for the last INSERT |  |  |
| [`LAST_VALUE()`](window-function-descriptions.md#function_last-value) | Value of argument from last row of window frame |  |  |
| [`LCASE()`](string-functions.md#function_lcase) | Synonym for LOWER() |  |  |
| [`LEAD()`](window-function-descriptions.md#function_lead) | Value of argument from row leading current row within partition |  |  |
| [`LEAST()`](comparison-operators.md#function_least) | Return the smallest argument |  |  |
| [`LEFT()`](string-functions.md#function_left) | Return the leftmost number of characters as specified |  |  |
| [`LENGTH()`](string-functions.md#function_length) | Return the length of a string in bytes |  |  |
| [`LIKE`](string-comparison-functions.md#operator_like) | Simple pattern matching |  |  |
| [`LineString()`](gis-mysql-specific-functions.md#function_linestring) | Construct LineString from Point values |  |  |
| [`LN()`](mathematical-functions.md#function_ln) | Return the natural logarithm of the argument |  |  |
| [`LOAD_FILE()`](string-functions.md#function_load-file) | Load the named file |  |  |
| [`LOCALTIME()`, `LOCALTIME`](date-and-time-functions.md#function_localtime) | Synonym for NOW() |  |  |
| [`LOCALTIMESTAMP`, `LOCALTIMESTAMP()`](date-and-time-functions.md#function_localtimestamp) | Synonym for NOW() |  |  |
| [`LOCATE()`](string-functions.md#function_locate) | Return the position of the first occurrence of substring |  |  |
| [`LOG()`](mathematical-functions.md#function_log) | Return the natural logarithm of the first argument |  |  |
| [`LOG10()`](mathematical-functions.md#function_log10) | Return the base-10 logarithm of the argument |  |  |
| [`LOG2()`](mathematical-functions.md#function_log2) | Return the base-2 logarithm of the argument |  |  |
| [`LOWER()`](string-functions.md#function_lower) | Return the argument in lowercase |  |  |
| [`LPAD()`](string-functions.md#function_lpad) | Return the string argument, left-padded with the specified string |  |  |
| [`LTRIM()`](string-functions.md#function_ltrim) | Remove leading spaces |  |  |
| [`MAKE_SET()`](string-functions.md#function_make-set) | Return a set of comma-separated strings that have the corresponding bit in bits set |  |  |
| [`MAKEDATE()`](date-and-time-functions.md#function_makedate) | Create a date from the year and day of year |  |  |
| [`MAKETIME()`](date-and-time-functions.md#function_maketime) | Create time from hour, minute, second |  |  |
| [`MASTER_POS_WAIT()`](replication-functions-synchronization.md#function_master-pos-wait) | Block until the replica has read and applied all updates up to the specified position |  | 8.0.26 |
| [`MATCH()`](fulltext-search.md#function_match) | Perform full-text search |  |  |
| [`MAX()`](aggregate-functions.md#function_max) | Return the maximum value |  |  |
| [`MBRContains()`](spatial-relation-functions-mbr.md#function_mbrcontains) | Whether MBR of one geometry contains MBR of another |  |  |
| [`MBRCoveredBy()`](spatial-relation-functions-mbr.md#function_mbrcoveredby) | Whether one MBR is covered by another |  |  |
| [`MBRCovers()`](spatial-relation-functions-mbr.md#function_mbrcovers) | Whether one MBR covers another |  |  |
| [`MBRDisjoint()`](spatial-relation-functions-mbr.md#function_mbrdisjoint) | Whether MBRs of two geometries are disjoint |  |  |
| [`MBREquals()`](spatial-relation-functions-mbr.md#function_mbrequals) | Whether MBRs of two geometries are equal |  |  |
| [`MBRIntersects()`](spatial-relation-functions-mbr.md#function_mbrintersects) | Whether MBRs of two geometries intersect |  |  |
| [`MBROverlaps()`](spatial-relation-functions-mbr.md#function_mbroverlaps) | Whether MBRs of two geometries overlap |  |  |
| [`MBRTouches()`](spatial-relation-functions-mbr.md#function_mbrtouches) | Whether MBRs of two geometries touch |  |  |
| [`MBRWithin()`](spatial-relation-functions-mbr.md#function_mbrwithin) | Whether MBR of one geometry is within MBR of another |  |  |
| [`MD5()`](encryption-functions.md#function_md5) | Calculate MD5 checksum |  |  |
| [`MEMBER OF()`](json-search-functions.md#operator_member-of) | Returns true (1) if first operand matches any element of JSON array passed as second operand, otherwise returns false (0) | 8.0.17 |  |
| [`MICROSECOND()`](date-and-time-functions.md#function_microsecond) | Return the microseconds from argument |  |  |
| [`MID()`](string-functions.md#function_mid) | Return a substring starting from the specified position |  |  |
| [`MIN()`](aggregate-functions.md#function_min) | Return the minimum value |  |  |
| [`MINUTE()`](date-and-time-functions.md#function_minute) | Return the minute from the argument |  |  |
| [`MOD()`](mathematical-functions.md#function_mod) | Return the remainder |  |  |
| [`MONTH()`](date-and-time-functions.md#function_month) | Return the month from the date passed |  |  |
| [`MONTHNAME()`](date-and-time-functions.md#function_monthname) | Return the name of the month |  |  |
| [`MultiLineString()`](gis-mysql-specific-functions.md#function_multilinestring) | Contruct MultiLineString from LineString values |  |  |
| [`MultiPoint()`](gis-mysql-specific-functions.md#function_multipoint) | Construct MultiPoint from Point values |  |  |
| [`MultiPolygon()`](gis-mysql-specific-functions.md#function_multipolygon) | Construct MultiPolygon from Polygon values |  |  |
| [`NAME_CONST()`](miscellaneous-functions.md#function_name-const) | Cause the column to have the given name |  |  |
| [`NOT`, `!`](logical-operators.md#operator_not) | Negates value |  |  |
| [`NOT BETWEEN ... AND ...`](comparison-operators.md#operator_not-between) | Whether a value is not within a range of values |  |  |
| [`NOT EXISTS()`](comparison-operators.md#operator_not-exists) | Whether the result of a query contains no rows |  |  |
| [`NOT IN()`](comparison-operators.md#operator_not-in) | Whether a value is not within a set of values |  |  |
| [`NOT LIKE`](string-comparison-functions.md#operator_not-like) | Negation of simple pattern matching |  |  |
| [`NOT REGEXP`](regexp.md#operator_not-regexp) | Negation of REGEXP |  |  |
| [`NOW()`](date-and-time-functions.md#function_now) | Return the current date and time |  |  |
| [`NTH_VALUE()`](window-function-descriptions.md#function_nth-value) | Value of argument from N-th row of window frame |  |  |
| [`NTILE()`](window-function-descriptions.md#function_ntile) | Bucket number of current row within its partition. |  |  |
| [`NULLIF()`](flow-control-functions.md#function_nullif) | Return NULL if expr1 = expr2 |  |  |
| [`OCT()`](string-functions.md#function_oct) | Return a string containing octal representation of a number |  |  |
| [`OCTET_LENGTH()`](string-functions.md#function_octet-length) | Synonym for LENGTH() |  |  |
| [`OR`, `||`](logical-operators.md#operator_or) | Logical OR |  |  |
| [`ORD()`](string-functions.md#function_ord) | Return character code for leftmost character of the argument |  |  |
| [`PERCENT_RANK()`](window-function-descriptions.md#function_percent-rank) | Percentage rank value |  |  |
| [`PERIOD_ADD()`](date-and-time-functions.md#function_period-add) | Add a period to a year-month |  |  |
| [`PERIOD_DIFF()`](date-and-time-functions.md#function_period-diff) | Return the number of months between periods |  |  |
| [`PI()`](mathematical-functions.md#function_pi) | Return the value of pi |  |  |
| [`Point()`](gis-mysql-specific-functions.md#function_point) | Construct Point from coordinates |  |  |
| [`Polygon()`](gis-mysql-specific-functions.md#function_polygon) | Construct Polygon from LineString arguments |  |  |
| [`POSITION()`](string-functions.md#function_position) | Synonym for LOCATE() |  |  |
| [`POW()`](mathematical-functions.md#function_pow) | Return the argument raised to the specified power |  |  |
| [`POWER()`](mathematical-functions.md#function_power) | Return the argument raised to the specified power |  |  |
| [`PS_CURRENT_THREAD_ID()`](performance-schema-functions.md#function_ps-current-thread-id) | Performance Schema thread ID for current thread | 8.0.16 |  |
| [`PS_THREAD_ID()`](performance-schema-functions.md#function_ps-thread-id) | Performance Schema thread ID for given thread | 8.0.16 |  |
| [`QUARTER()`](date-and-time-functions.md#function_quarter) | Return the quarter from a date argument |  |  |
| [`QUOTE()`](string-functions.md#function_quote) | Escape the argument for use in an SQL statement |  |  |
| [`RADIANS()`](mathematical-functions.md#function_radians) | Return argument converted to radians |  |  |
| [`RAND()`](mathematical-functions.md#function_rand) | Return a random floating-point value |  |  |
| [`RANDOM_BYTES()`](encryption-functions.md#function_random-bytes) | Return a random byte vector |  |  |
| [`RANK()`](window-function-descriptions.md#function_rank) | Rank of current row within its partition, with gaps |  |  |
| [`REGEXP`](regexp.md#operator_regexp) | Whether string matches regular expression |  |  |
| [`REGEXP_INSTR()`](regexp.md#function_regexp-instr) | Starting index of substring matching regular expression |  |  |
| [`REGEXP_LIKE()`](regexp.md#function_regexp-like) | Whether string matches regular expression |  |  |
| [`REGEXP_REPLACE()`](regexp.md#function_regexp-replace) | Replace substrings matching regular expression |  |  |
| [`REGEXP_SUBSTR()`](regexp.md#function_regexp-substr) | Return substring matching regular expression |  |  |
| [`RELEASE_ALL_LOCKS()`](locking-functions.md#function_release-all-locks) | Release all current named locks |  |  |
| [`RELEASE_LOCK()`](locking-functions.md#function_release-lock) | Release the named lock |  |  |
| [`REPEAT()`](string-functions.md#function_repeat) | Repeat a string the specified number of times |  |  |
| [`REPLACE()`](string-functions.md#function_replace) | Replace occurrences of a specified string |  |  |
| [`REVERSE()`](string-functions.md#function_reverse) | Reverse the characters in a string |  |  |
| [`RIGHT()`](string-functions.md#function_right) | Return the specified rightmost number of characters |  |  |
| [`RLIKE`](regexp.md#operator_regexp) | Whether string matches regular expression |  |  |
| [`ROLES_GRAPHML()`](information-functions.md#function_roles-graphml) | Return a GraphML document representing memory role subgraphs |  |  |
| [`ROUND()`](mathematical-functions.md#function_round) | Round the argument |  |  |
| [`ROW_COUNT()`](information-functions.md#function_row-count) | The number of rows updated |  |  |
| [`ROW_NUMBER()`](window-function-descriptions.md#function_row-number) | Number of current row within its partition |  |  |
| [`RPAD()`](string-functions.md#function_rpad) | Append string the specified number of times |  |  |
| [`RTRIM()`](string-functions.md#function_rtrim) | Remove trailing spaces |  |  |
| [`SCHEMA()`](information-functions.md#function_schema) | Synonym for DATABASE() |  |  |
| [`SEC_TO_TIME()`](date-and-time-functions.md#function_sec-to-time) | Converts seconds to 'hh:mm:ss' format |  |  |
| [`SECOND()`](date-and-time-functions.md#function_second) | Return the second (0-59) |  |  |
| [`SESSION_USER()`](information-functions.md#function_session-user) | Synonym for USER() |  |  |
| [`SHA1()`, `SHA()`](encryption-functions.md#function_sha1) | Calculate an SHA-1 160-bit checksum |  |  |
| [`SHA2()`](encryption-functions.md#function_sha2) | Calculate an SHA-2 checksum |  |  |
| [`SIGN()`](mathematical-functions.md#function_sign) | Return the sign of the argument |  |  |
| [`SIN()`](mathematical-functions.md#function_sin) | Return the sine of the argument |  |  |
| [`SLEEP()`](miscellaneous-functions.md#function_sleep) | Sleep for a number of seconds |  |  |
| [`SOUNDEX()`](string-functions.md#function_soundex) | Return a soundex string |  |  |
| [`SOUNDS LIKE`](string-functions.md#operator_sounds-like) | Compare sounds |  |  |
| [`SOURCE_POS_WAIT()`](replication-functions-synchronization.md#function_source-pos-wait) | Block until the replica has read and applied all updates up to the specified position | 8.0.26 |  |
| [`SPACE()`](string-functions.md#function_space) | Return a string of the specified number of spaces |  |  |
| [`SQRT()`](mathematical-functions.md#function_sqrt) | Return the square root of the argument |  |  |
| [`ST_Area()`](gis-polygon-property-functions.md#function_st-area) | Return Polygon or MultiPolygon area |  |  |
| [`ST_AsBinary()`, `ST_AsWKB()`](gis-format-conversion-functions.md#function_st-asbinary) | Convert from internal geometry format to WKB |  |  |
| [`ST_AsGeoJSON()`](spatial-geojson-functions.md#function_st-asgeojson) | Generate GeoJSON object from geometry |  |  |
| [`ST_AsText()`, `ST_AsWKT()`](gis-format-conversion-functions.md#function_st-astext) | Convert from internal geometry format to WKT |  |  |
| [`ST_Buffer()`](spatial-operator-functions.md#function_st-buffer) | Return geometry of points within given distance from geometry |  |  |
| [`ST_Buffer_Strategy()`](spatial-operator-functions.md#function_st-buffer-strategy) | Produce strategy option for ST\_Buffer() |  |  |
| [`ST_Centroid()`](gis-polygon-property-functions.md#function_st-centroid) | Return centroid as a point |  |  |
| [`ST_Collect()`](spatial-aggregate-functions.md#function_st-collect) | Aggregate spatial values into collection | 8.0.24 |  |
| [`ST_Contains()`](spatial-relation-functions-object-shapes.md#function_st-contains) | Whether one geometry contains another |  |  |
| [`ST_ConvexHull()`](spatial-operator-functions.md#function_st-convexhull) | Return convex hull of geometry |  |  |
| [`ST_Crosses()`](spatial-relation-functions-object-shapes.md#function_st-crosses) | Whether one geometry crosses another |  |  |
| [`ST_Difference()`](spatial-operator-functions.md#function_st-difference) | Return point set difference of two geometries |  |  |
| [`ST_Dimension()`](gis-general-property-functions.md#function_st-dimension) | Dimension of geometry |  |  |
| [`ST_Disjoint()`](spatial-relation-functions-object-shapes.md#function_st-disjoint) | Whether one geometry is disjoint from another |  |  |
| [`ST_Distance()`](spatial-relation-functions-object-shapes.md#function_st-distance) | The distance of one geometry from another |  |  |
| [`ST_Distance_Sphere()`](spatial-convenience-functions.md#function_st-distance-sphere) | Minimum distance on earth between two geometries |  |  |
| [`ST_EndPoint()`](gis-linestring-property-functions.md#function_st-endpoint) | End Point of LineString |  |  |
| [`ST_Envelope()`](gis-general-property-functions.md#function_st-envelope) | Return MBR of geometry |  |  |
| [`ST_Equals()`](spatial-relation-functions-object-shapes.md#function_st-equals) | Whether one geometry is equal to another |  |  |
| [`ST_ExteriorRing()`](gis-polygon-property-functions.md#function_st-exteriorring) | Return exterior ring of Polygon |  |  |
| [`ST_FrechetDistance()`](spatial-relation-functions-object-shapes.md#function_st-frechetdistance) | The discrete Fréchet distance of one geometry from another | 8.0.23 |  |
| [`ST_GeoHash()`](spatial-geohash-functions.md#function_st-geohash) | Produce a geohash value |  |  |
| [`ST_GeomCollFromText()`, `ST_GeometryCollectionFromText()`, `ST_GeomCollFromTxt()`](gis-wkt-functions.md#function_st-geomcollfromtext) | Return geometry collection from WKT |  |  |
| [`ST_GeomCollFromWKB()`, `ST_GeometryCollectionFromWKB()`](gis-wkb-functions.md#function_st-geomcollfromwkb) | Return geometry collection from WKB |  |  |
| [`ST_GeometryN()`](gis-geometrycollection-property-functions.md#function_st-geometryn) | Return N-th geometry from geometry collection |  |  |
| [`ST_GeometryType()`](gis-general-property-functions.md#function_st-geometrytype) | Return name of geometry type |  |  |
| [`ST_GeomFromGeoJSON()`](spatial-geojson-functions.md#function_st-geomfromgeojson) | Generate geometry from GeoJSON object |  |  |
| [`ST_GeomFromText()`, `ST_GeometryFromText()`](gis-wkt-functions.md#function_st-geomfromtext) | Return geometry from WKT |  |  |
| [`ST_GeomFromWKB()`, `ST_GeometryFromWKB()`](gis-wkb-functions.md#function_st-geomfromwkb) | Return geometry from WKB |  |  |
| [`ST_HausdorffDistance()`](spatial-relation-functions-object-shapes.md#function_st-hausdorffdistance) | The discrete Hausdorff distance of one geometry from another | 8.0.23 |  |
| [`ST_InteriorRingN()`](gis-polygon-property-functions.md#function_st-interiorringn) | Return N-th interior ring of Polygon |  |  |
| [`ST_Intersection()`](spatial-operator-functions.md#function_st-intersection) | Return point set intersection of two geometries |  |  |
| [`ST_Intersects()`](spatial-relation-functions-object-shapes.md#function_st-intersects) | Whether one geometry intersects another |  |  |
| [`ST_IsClosed()`](gis-linestring-property-functions.md#function_st-isclosed) | Whether a geometry is closed and simple |  |  |
| [`ST_IsEmpty()`](gis-general-property-functions.md#function_st-isempty) | Whether a geometry is empty |  |  |
| [`ST_IsSimple()`](gis-general-property-functions.md#function_st-issimple) | Whether a geometry is simple |  |  |
| [`ST_IsValid()`](spatial-convenience-functions.md#function_st-isvalid) | Whether a geometry is valid |  |  |
| [`ST_LatFromGeoHash()`](spatial-geohash-functions.md#function_st-latfromgeohash) | Return latitude from geohash value |  |  |
| [`ST_Latitude()`](gis-point-property-functions.md#function_st-latitude) | Return latitude of Point | 8.0.12 |  |
| [`ST_Length()`](gis-linestring-property-functions.md#function_st-length) | Return length of LineString |  |  |
| [`ST_LineFromText()`, `ST_LineStringFromText()`](gis-wkt-functions.md#function_st-linefromtext) | Construct LineString from WKT |  |  |
| [`ST_LineFromWKB()`, `ST_LineStringFromWKB()`](gis-wkb-functions.md#function_st-linefromwkb) | Construct LineString from WKB |  |  |
| [`ST_LineInterpolatePoint()`](spatial-operator-functions.md#function_st-lineinterpolatepoint) | The point a given percentage along a LineString | 8.0.24 |  |
| [`ST_LineInterpolatePoints()`](spatial-operator-functions.md#function_st-lineinterpolatepoints) | The points a given percentage along a LineString | 8.0.24 |  |
| [`ST_LongFromGeoHash()`](spatial-geohash-functions.md#function_st-longfromgeohash) | Return longitude from geohash value |  |  |
| [`ST_Longitude()`](gis-point-property-functions.md#function_st-longitude) | Return longitude of Point | 8.0.12 |  |
| [`ST_MakeEnvelope()`](spatial-convenience-functions.md#function_st-makeenvelope) | Rectangle around two points |  |  |
| [`ST_MLineFromText()`, `ST_MultiLineStringFromText()`](gis-wkt-functions.md#function_st-mlinefromtext) | Construct MultiLineString from WKT |  |  |
| [`ST_MLineFromWKB()`, `ST_MultiLineStringFromWKB()`](gis-wkb-functions.md#function_st-mlinefromwkb) | Construct MultiLineString from WKB |  |  |
| [`ST_MPointFromText()`, `ST_MultiPointFromText()`](gis-wkt-functions.md#function_st-mpointfromtext) | Construct MultiPoint from WKT |  |  |
| [`ST_MPointFromWKB()`, `ST_MultiPointFromWKB()`](gis-wkb-functions.md#function_st-mpointfromwkb) | Construct MultiPoint from WKB |  |  |
| [`ST_MPolyFromText()`, `ST_MultiPolygonFromText()`](gis-wkt-functions.md#function_st-mpolyfromtext) | Construct MultiPolygon from WKT |  |  |
| [`ST_MPolyFromWKB()`, `ST_MultiPolygonFromWKB()`](gis-wkb-functions.md#function_st-mpolyfromwkb) | Construct MultiPolygon from WKB |  |  |
| [`ST_NumGeometries()`](gis-geometrycollection-property-functions.md#function_st-numgeometries) | Return number of geometries in geometry collection |  |  |
| [`ST_NumInteriorRing()`, `ST_NumInteriorRings()`](gis-polygon-property-functions.md#function_st-numinteriorrings) | Return number of interior rings in Polygon |  |  |
| [`ST_NumPoints()`](gis-linestring-property-functions.md#function_st-numpoints) | Return number of points in LineString |  |  |
| [`ST_Overlaps()`](spatial-relation-functions-object-shapes.md#function_st-overlaps) | Whether one geometry overlaps another |  |  |
| [`ST_PointAtDistance()`](spatial-operator-functions.md#function_st-pointatdistance) | The point a given distance along a LineString | 8.0.24 |  |
| [`ST_PointFromGeoHash()`](spatial-geohash-functions.md#function_st-pointfromgeohash) | Convert geohash value to POINT value |  |  |
| [`ST_PointFromText()`](gis-wkt-functions.md#function_st-pointfromtext) | Construct Point from WKT |  |  |
| [`ST_PointFromWKB()`](gis-wkb-functions.md#function_st-pointfromwkb) | Construct Point from WKB |  |  |
| [`ST_PointN()`](gis-linestring-property-functions.md#function_st-pointn) | Return N-th point from LineString |  |  |
| [`ST_PolyFromText()`, `ST_PolygonFromText()`](gis-wkt-functions.md#function_st-polyfromtext) | Construct Polygon from WKT |  |  |
| [`ST_PolyFromWKB()`, `ST_PolygonFromWKB()`](gis-wkb-functions.md#function_st-polyfromwkb) | Construct Polygon from WKB |  |  |
| [`ST_Simplify()`](spatial-convenience-functions.md#function_st-simplify) | Return simplified geometry |  |  |
| [`ST_SRID()`](gis-general-property-functions.md#function_st-srid) | Return spatial reference system ID for geometry |  |  |
| [`ST_StartPoint()`](gis-linestring-property-functions.md#function_st-startpoint) | Start Point of LineString |  |  |
| [`ST_SwapXY()`](gis-format-conversion-functions.md#function_st-swapxy) | Return argument with X/Y coordinates swapped |  |  |
| [`ST_SymDifference()`](spatial-operator-functions.md#function_st-symdifference) | Return point set symmetric difference of two geometries |  |  |
| [`ST_Touches()`](spatial-relation-functions-object-shapes.md#function_st-touches) | Whether one geometry touches another |  |  |
| [`ST_Transform()`](spatial-operator-functions.md#function_st-transform) | Transform coordinates of geometry | 8.0.13 |  |
| [`ST_Union()`](spatial-operator-functions.md#function_st-union) | Return point set union of two geometries |  |  |
| [`ST_Validate()`](spatial-convenience-functions.md#function_st-validate) | Return validated geometry |  |  |
| [`ST_Within()`](spatial-relation-functions-object-shapes.md#function_st-within) | Whether one geometry is within another |  |  |
| [`ST_X()`](gis-point-property-functions.md#function_st-x) | Return X coordinate of Point |  |  |
| [`ST_Y()`](gis-point-property-functions.md#function_st-y) | Return Y coordinate of Point |  |  |
| [`STATEMENT_DIGEST()`](encryption-functions.md#function_statement-digest) | Compute statement digest hash value |  |  |
| [`STATEMENT_DIGEST_TEXT()`](encryption-functions.md#function_statement-digest-text) | Compute normalized statement digest |  |  |
| [`STD()`](aggregate-functions.md#function_std) | Return the population standard deviation |  |  |
| [`STDDEV()`](aggregate-functions.md#function_stddev) | Return the population standard deviation |  |  |
| [`STDDEV_POP()`](aggregate-functions.md#function_stddev-pop) | Return the population standard deviation |  |  |
| [`STDDEV_SAMP()`](aggregate-functions.md#function_stddev-samp) | Return the sample standard deviation |  |  |
| [`STR_TO_DATE()`](date-and-time-functions.md#function_str-to-date) | Convert a string to a date |  |  |
| [`STRCMP()`](string-comparison-functions.md#function_strcmp) | Compare two strings |  |  |
| [`SUBDATE()`](date-and-time-functions.md#function_subdate) | Synonym for DATE\_SUB() when invoked with three arguments |  |  |
| [`SUBSTR()`](string-functions.md#function_substr) | Return the substring as specified |  |  |
| [`SUBSTRING()`](string-functions.md#function_substring) | Return the substring as specified |  |  |
| [`SUBSTRING_INDEX()`](string-functions.md#function_substring-index) | Return a substring from a string before the specified number of occurrences of the delimiter |  |  |
| [`SUBTIME()`](date-and-time-functions.md#function_subtime) | Subtract times |  |  |
| [`SUM()`](aggregate-functions.md#function_sum) | Return the sum |  |  |
| [`SYSDATE()`](date-and-time-functions.md#function_sysdate) | Return the time at which the function executes |  |  |
| [`SYSTEM_USER()`](information-functions.md#function_system-user) | Synonym for USER() |  |  |
| [`TAN()`](mathematical-functions.md#function_tan) | Return the tangent of the argument |  |  |
| [`TIME()`](date-and-time-functions.md#function_time) | Extract the time portion of the expression passed |  |  |
| [`TIME_FORMAT()`](date-and-time-functions.md#function_time-format) | Format as time |  |  |
| [`TIME_TO_SEC()`](date-and-time-functions.md#function_time-to-sec) | Return the argument converted to seconds |  |  |
| [`TIMEDIFF()`](date-and-time-functions.md#function_timediff) | Subtract time |  |  |
| [`TIMESTAMP()`](date-and-time-functions.md#function_timestamp) | With a single argument, this function returns the date or datetime expression; with two arguments, the sum of the arguments |  |  |
| [`TIMESTAMPADD()`](date-and-time-functions.md#function_timestampadd) | Add an interval to a datetime expression |  |  |
| [`TIMESTAMPDIFF()`](date-and-time-functions.md#function_timestampdiff) | Return the difference of two datetime expressions, using the units specified |  |  |
| [`TO_BASE64()`](string-functions.md#function_to-base64) | Return the argument converted to a base-64 string |  |  |
| [`TO_DAYS()`](date-and-time-functions.md#function_to-days) | Return the date argument converted to days |  |  |
| [`TO_SECONDS()`](date-and-time-functions.md#function_to-seconds) | Return the date or datetime argument converted to seconds since Year 0 |  |  |
| [`TRIM()`](string-functions.md#function_trim) | Remove leading and trailing spaces |  |  |
| [`TRUNCATE()`](mathematical-functions.md#function_truncate) | Truncate to specified number of decimal places |  |  |
| [`UCASE()`](string-functions.md#function_ucase) | Synonym for UPPER() |  |  |
| [`UNCOMPRESS()`](encryption-functions.md#function_uncompress) | Uncompress a string compressed |  |  |
| [`UNCOMPRESSED_LENGTH()`](encryption-functions.md#function_uncompressed-length) | Return the length of a string before compression |  |  |
| [`UNHEX()`](string-functions.md#function_unhex) | Return a string containing hex representation of a number |  |  |
| [`UNIX_TIMESTAMP()`](date-and-time-functions.md#function_unix-timestamp) | Return a Unix timestamp |  |  |
| [`UpdateXML()`](xml-functions.md#function_updatexml) | Return replaced XML fragment |  |  |
| [`UPPER()`](string-functions.md#function_upper) | Convert to uppercase |  |  |
| [`USER()`](information-functions.md#function_user) | The user name and host name provided by the client |  |  |
| [`UTC_DATE()`](date-and-time-functions.md#function_utc-date) | Return the current UTC date |  |  |
| [`UTC_TIME()`](date-and-time-functions.md#function_utc-time) | Return the current UTC time |  |  |
| [`UTC_TIMESTAMP()`](date-and-time-functions.md#function_utc-timestamp) | Return the current UTC date and time |  |  |
| [`UUID()`](miscellaneous-functions.md#function_uuid) | Return a Universal Unique Identifier (UUID) |  |  |
| [`UUID_SHORT()`](miscellaneous-functions.md#function_uuid-short) | Return an integer-valued universal identifier |  |  |
| [`UUID_TO_BIN()`](miscellaneous-functions.md#function_uuid-to-bin) | Convert string UUID to binary |  |  |
| [`VALIDATE_PASSWORD_STRENGTH()`](encryption-functions.md#function_validate-password-strength) | Determine strength of password |  |  |
| [`VALUES()`](miscellaneous-functions.md#function_values) | Define the values to be used during an INSERT |  |  |
| [`VAR_POP()`](aggregate-functions.md#function_var-pop) | Return the population standard variance |  |  |
| [`VAR_SAMP()`](aggregate-functions.md#function_var-samp) | Return the sample variance |  |  |
| [`VARIANCE()`](aggregate-functions.md#function_variance) | Return the population standard variance |  |  |
| [`VERSION()`](information-functions.md#function_version) | Return a string that indicates the MySQL server version |  |  |
| [`WAIT_FOR_EXECUTED_GTID_SET()`](gtid-functions.md#function_wait-for-executed-gtid-set) | Wait until the given GTIDs have executed on the replica. |  |  |
| [`WAIT_UNTIL_SQL_THREAD_AFTER_GTIDS()`](gtid-functions.md#function_wait-until-sql-thread-after-gtids) | Use `WAIT_FOR_EXECUTED_GTID_SET()`. |  | 8.0.18 |
| [`WEEK()`](date-and-time-functions.md#function_week) | Return the week number |  |  |
| [`WEEKDAY()`](date-and-time-functions.md#function_weekday) | Return the weekday index |  |  |
| [`WEEKOFYEAR()`](date-and-time-functions.md#function_weekofyear) | Return the calendar week of the date (1-53) |  |  |
| [`WEIGHT_STRING()`](string-functions.md#function_weight-string) | Return the weight string for a string |  |  |
| [`XOR`](logical-operators.md#operator_xor) | Logical XOR |  |  |
| [`YEAR()`](date-and-time-functions.md#function_year) | Return the year |  |  |
| [`YEARWEEK()`](date-and-time-functions.md#function_yearweek) | Return the year and week |  |  |
| [`|`](bit-functions.md#operator_bitwise-or) | Bitwise OR |  |  |
| [`~`](bit-functions.md#operator_bitwise-invert) | Bitwise inversion |  |  |
