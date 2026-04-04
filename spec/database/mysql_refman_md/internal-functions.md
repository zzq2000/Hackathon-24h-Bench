## 14.22 Internal Functions

**Table 14.32 Internal Functions**

| Name | Description | Introduced |
| --- | --- | --- |
| [`CAN_ACCESS_COLUMN()`](internal-functions.md#function_can-access-column) | Internal use only |  |
| [`CAN_ACCESS_DATABASE()`](internal-functions.md#function_can-access-database) | Internal use only |  |
| [`CAN_ACCESS_TABLE()`](internal-functions.md#function_can-access-table) | Internal use only |  |
| [`CAN_ACCESS_USER()`](internal-functions.md#function_can-access-user) | Internal use only | 8.0.22 |
| [`CAN_ACCESS_VIEW()`](internal-functions.md#function_can-access-view) | Internal use only |  |
| [`GET_DD_COLUMN_PRIVILEGES()`](internal-functions.md#function_get-dd-column-privileges) | Internal use only |  |
| [`GET_DD_CREATE_OPTIONS()`](internal-functions.md#function_get-dd-create-options) | Internal use only |  |
| [`GET_DD_INDEX_SUB_PART_LENGTH()`](internal-functions.md#function_get-dd-index-sub-part-length) | Internal use only |  |
| [`INTERNAL_AUTO_INCREMENT()`](internal-functions.md#function_internal-auto-increment) | Internal use only |  |
| [`INTERNAL_AVG_ROW_LENGTH()`](internal-functions.md#function_internal-avg-row-length) | Internal use only |  |
| [`INTERNAL_CHECK_TIME()`](internal-functions.md#function_internal-check-time) | Internal use only |  |
| [`INTERNAL_CHECKSUM()`](internal-functions.md#function_internal-checksum) | Internal use only |  |
| [`INTERNAL_DATA_FREE()`](internal-functions.md#function_internal-data-free) | Internal use only |  |
| [`INTERNAL_DATA_LENGTH()`](internal-functions.md#function_internal-data-length) | Internal use only |  |
| [`INTERNAL_DD_CHAR_LENGTH()`](internal-functions.md#function_internal-dd-char-length) | Internal use only |  |
| [`INTERNAL_GET_COMMENT_OR_ERROR()`](internal-functions.md#function_internal-get-comment-or-error) | Internal use only |  |
| [`INTERNAL_GET_ENABLED_ROLE_JSON()`](internal-functions.md#function_internal-get-enabled-role-json) | Internal use only | 8.0.19 |
| [`INTERNAL_GET_HOSTNAME()`](internal-functions.md#function_internal-get-hostname) | Internal use only | 8.0.19 |
| [`INTERNAL_GET_USERNAME()`](internal-functions.md#function_internal-get-username) | Internal use only | 8.0.19 |
| [`INTERNAL_GET_VIEW_WARNING_OR_ERROR()`](internal-functions.md#function_internal-get-view-warning-or-error) | Internal use only |  |
| [`INTERNAL_INDEX_COLUMN_CARDINALITY()`](internal-functions.md#function_internal-index-column-cardinality) | Internal use only |  |
| [`INTERNAL_INDEX_LENGTH()`](internal-functions.md#function_internal-index-length) | Internal use only |  |
| [`INTERNAL_IS_ENABLED_ROLE()`](internal-functions.md#function_internal-is-enabled-role) | Internal use only | 8.0.19 |
| [`INTERNAL_IS_MANDATORY_ROLE()`](internal-functions.md#function_internal-is-mandatory-role) | Internal use only | 8.0.19 |
| [`INTERNAL_KEYS_DISABLED()`](internal-functions.md#function_internal-keys-disabled) | Internal use only |  |
| [`INTERNAL_MAX_DATA_LENGTH()`](internal-functions.md#function_internal-max-data-length) | Internal use only |  |
| [`INTERNAL_TABLE_ROWS()`](internal-functions.md#function_internal-table-rows) | Internal use only |  |
| [`INTERNAL_UPDATE_TIME()`](internal-functions.md#function_internal-update-time) | Internal use only |  |

The functions listed in this section are intended only for
internal use by the server. Attempts by users to invoke them
result in an error.

- [`CAN_ACCESS_COLUMN(ARGS)`](internal-functions.md#function_can-access-column)
- [`CAN_ACCESS_DATABASE(ARGS)`](internal-functions.md#function_can-access-database)
- [`CAN_ACCESS_TABLE(ARGS)`](internal-functions.md#function_can-access-table)
- [`CAN_ACCESS_USER(ARGS)`](internal-functions.md#function_can-access-user)
- [`CAN_ACCESS_VIEW(ARGS)`](internal-functions.md#function_can-access-view)
- [`GET_DD_COLUMN_PRIVILEGES(ARGS)`](internal-functions.md#function_get-dd-column-privileges)
- [`GET_DD_CREATE_OPTIONS(ARGS)`](internal-functions.md#function_get-dd-create-options)
- [`GET_DD_INDEX_SUB_PART_LENGTH(ARGS)`](internal-functions.md#function_get-dd-index-sub-part-length)
- [`INTERNAL_AUTO_INCREMENT(ARGS)`](internal-functions.md#function_internal-auto-increment)
- [`INTERNAL_AVG_ROW_LENGTH(ARGS)`](internal-functions.md#function_internal-avg-row-length)
- [`INTERNAL_CHECK_TIME(ARGS)`](internal-functions.md#function_internal-check-time)
- [`INTERNAL_CHECKSUM(ARGS)`](internal-functions.md#function_internal-checksum)
- [`INTERNAL_DATA_FREE(ARGS)`](internal-functions.md#function_internal-data-free)
- [`INTERNAL_DATA_LENGTH(ARGS)`](internal-functions.md#function_internal-data-length)
- [`INTERNAL_DD_CHAR_LENGTH(ARGS)`](internal-functions.md#function_internal-dd-char-length)
- [`INTERNAL_GET_COMMENT_OR_ERROR(ARGS)`](internal-functions.md#function_internal-get-comment-or-error)
- [`INTERNAL_GET_ENABLED_ROLE_JSON(ARGS)`](internal-functions.md#function_internal-get-enabled-role-json)
- [`INTERNAL_GET_HOSTNAME(ARGS)`](internal-functions.md#function_internal-get-hostname)
- [`INTERNAL_GET_USERNAME(ARGS)`](internal-functions.md#function_internal-get-username)
- [`INTERNAL_GET_VIEW_WARNING_OR_ERROR(ARGS)`](internal-functions.md#function_internal-get-view-warning-or-error)
- [`INTERNAL_INDEX_COLUMN_CARDINALITY(ARGS)`](internal-functions.md#function_internal-index-column-cardinality)
- [`INTERNAL_INDEX_LENGTH(ARGS)`](internal-functions.md#function_internal-index-length)
- [`INTERNAL_IS_ENABLED_ROLE(ARGS)`](internal-functions.md#function_internal-is-enabled-role)
- [`INTERNAL_IS_MANDATORY_ROLE(ARGS)`](internal-functions.md#function_internal-is-mandatory-role)
- [`INTERNAL_KEYS_DISABLED(ARGS)`](internal-functions.md#function_internal-keys-disabled)
- [`INTERNAL_MAX_DATA_LENGTH(ARGS)`](internal-functions.md#function_internal-max-data-length)
- [`INTERNAL_TABLE_ROWS(ARGS)`](internal-functions.md#function_internal-table-rows)
- [`INTERNAL_UPDATE_TIME(ARGS)`](internal-functions.md#function_internal-update-time)
- [`IS_VISIBLE_DD_OBJECT(ARGS)`](internal-functions.md#function_is-visible-dd-object)
