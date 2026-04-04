#### 15.7.2.3 DROP RESOURCE GROUP Statement

```sql
DROP RESOURCE GROUP group_name [FORCE]
```

[`DROP RESOURCE GROUP`](drop-resource-group.md "15.7.2.3 DROP RESOURCE GROUP Statement") is used for
resource group management (see
[Section 7.1.16, “Resource Groups”](resource-groups.md "7.1.16 Resource Groups")). This statement drops a
resource group. It requires the
[`RESOURCE_GROUP_ADMIN`](privileges-provided.md#priv_resource-group-admin) privilege.

*`group_name`* identifies which resource
group to drop. If the group does not exist, an error occurs.

The `FORCE` modifier determines statement
behavior if the resource group has any threads assigned to it:

- If `FORCE` is not given and any threads are
  assigned to the group, an error occurs.
- If `FORCE` is given, existing threads in
  the group are moved to their respective default group
  (system threads to `SYS_default`, user
  threads to `USR_default`).

Examples:

- Drop a group, failing if the group contains any threads:

  ```sql
  DROP RESOURCE GROUP rg1;
  ```
- Drop a group and move existing threads to the default
  groups:

  ```sql
  DROP RESOURCE GROUP rg2 FORCE;
  ```

Resource group management is local to the server on which it
occurs. [`DROP RESOURCE GROUP`](drop-resource-group.md "15.7.2.3 DROP RESOURCE GROUP Statement")
statements are not written to the binary log and are not
replicated.
