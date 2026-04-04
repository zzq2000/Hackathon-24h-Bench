### 14.17.1 JSON Function Reference

**Table 14.22 JSON Functions**

| Name | Description | Introduced | Deprecated |
| --- | --- | --- | --- |
| [`->`](json-search-functions.md#operator_json-column-path) | Return value from JSON column after evaluating path; equivalent to JSON\_EXTRACT(). |  |  |
| [`->>`](json-search-functions.md#operator_json-inline-path) | Return value from JSON column after evaluating path and unquoting the result; equivalent to JSON\_UNQUOTE(JSON\_EXTRACT()). |  |  |
| [`JSON_ARRAY()`](json-creation-functions.md#function_json-array) | Create JSON array |  |  |
| [`JSON_ARRAY_APPEND()`](json-modification-functions.md#function_json-array-append) | Append data to JSON document |  |  |
| [`JSON_ARRAY_INSERT()`](json-modification-functions.md#function_json-array-insert) | Insert into JSON array |  |  |
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
| [`MEMBER OF()`](json-search-functions.md#operator_member-of) | Returns true (1) if first operand matches any element of JSON array passed as second operand, otherwise returns false (0) | 8.0.17 |  |

MySQL supports two aggregate JSON functions
[`JSON_ARRAYAGG()`](aggregate-functions.md#function_json-arrayagg) and
[`JSON_OBJECTAGG()`](aggregate-functions.md#function_json-objectagg). See
[Section 14.19, “Aggregate Functions”](aggregate-functions-and-modifiers.md "14.19 Aggregate Functions"), for
descriptions of these.

MySQL also supports “pretty-printing” of JSON values
in an easy-to-read format, using the
[`JSON_PRETTY()`](json-utility-functions.md#function_json-pretty) function. You can see
how much storage space a given JSON value takes up, and how much
space remains for additional storage, using
[`JSON_STORAGE_SIZE()`](json-utility-functions.md#function_json-storage-size) and
[`JSON_STORAGE_FREE()`](json-utility-functions.md#function_json-storage-free), respectively.
For complete descriptions of these functions, see
[Section 14.17.8, “JSON Utility Functions”](json-utility-functions.md "14.17.8 JSON Utility Functions").
