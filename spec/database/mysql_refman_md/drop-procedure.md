### 15.1.29 DROP PROCEDURE and DROP FUNCTION Statements

```sql
DROP {PROCEDURE | FUNCTION} [IF EXISTS] sp_name
```

These statements are used to drop a stored routine (a stored
procedure or function). That is, the specified routine is removed
from the server. (`DROP FUNCTION` is also used to
drop loadable functions; see
[Section 15.7.4.2, “DROP FUNCTION Statement for Loadable Functions”](drop-function-loadable.md "15.7.4.2 DROP FUNCTION Statement for Loadable Functions").)

To drop a stored routine, you must have the
[`ALTER ROUTINE`](privileges-provided.md#priv_alter-routine) privilege for it. (If
the [`automatic_sp_privileges`](server-system-variables.md#sysvar_automatic_sp_privileges)
system variable is enabled, that privilege and
[`EXECUTE`](privileges-provided.md#priv_execute) are granted automatically
to the routine creator when the routine is created and dropped
from the creator when the routine is dropped. See
[Section 27.2.2, “Stored Routines and MySQL Privileges”](stored-routines-privileges.md "27.2.2 Stored Routines and MySQL Privileges").)

In addition, if the definer of the routine has the
[`SYSTEM_USER`](privileges-provided.md#priv_system-user) privilege, the user
dropping it must also have this privilege. This is enforced in
MySQL 8.0.16 and later.

The `IF EXISTS` clause is a MySQL extension. It
prevents an error from occurring if the procedure or function does
not exist. A warning is produced that can be viewed with
[`SHOW WARNINGS`](show-warnings.md "15.7.7.42 SHOW WARNINGS Statement").

[`DROP FUNCTION`](drop-function.md "15.1.26 DROP FUNCTION Statement") is also used to drop
loadable functions (see [Section 15.7.4.2, “DROP FUNCTION Statement for Loadable Functions”](drop-function-loadable.md "15.7.4.2 DROP FUNCTION Statement for Loadable Functions")).
