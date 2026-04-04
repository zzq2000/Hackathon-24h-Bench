### 8.1.4 Security-Related mysqld Options and Variables

The following table shows [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") options and
system variables that affect security. For descriptions of each of
these, see [Section 7.1.7, “Server Command Options”](server-options.md "7.1.7 Server Command Options"), and
[Section 7.1.8, “Server System Variables”](server-system-variables.md "7.1.8 Server System Variables").

**Table 8.1 Security Option and Variable Summary**

| Name | Cmd-Line | Option File | System Var | Status Var | Var Scope | Dynamic |
| --- | --- | --- | --- | --- | --- | --- |
| [allow-suspicious-udfs](server-options.md#option_mysqld_allow-suspicious-udfs) | Yes | Yes |  |  |  |  |
| [automatic\_sp\_privileges](server-system-variables.md#sysvar_automatic_sp_privileges) | Yes | Yes | Yes |  | Global | Yes |
| [chroot](server-options.md#option_mysqld_chroot) | Yes | Yes |  |  |  |  |
| [local\_infile](server-system-variables.md#sysvar_local_infile) | Yes | Yes | Yes |  | Global | Yes |
| [safe-user-create](server-options.md#option_mysqld_safe-user-create) | Yes | Yes |  |  |  |  |
| [secure\_file\_priv](server-system-variables.md#sysvar_secure_file_priv) | Yes | Yes | Yes |  | Global | No |
| [skip-grant-tables](server-options.md#option_mysqld_skip-grant-tables) | Yes | Yes |  |  |  |  |
| [skip\_name\_resolve](server-system-variables.md#sysvar_skip_name_resolve) | Yes | Yes | Yes |  | Global | No |
| [skip\_networking](server-system-variables.md#sysvar_skip_networking) | Yes | Yes | Yes |  | Global | No |
| [skip\_show\_database](server-options.md#option_mysqld_skip-show-database) | Yes | Yes | Yes |  | Global | No |
