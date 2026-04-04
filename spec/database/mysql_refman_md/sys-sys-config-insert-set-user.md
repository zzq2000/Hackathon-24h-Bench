#### 30.4.2.2 The sys\_config\_insert\_set\_user Trigger

For rows added to the [`sys_config`](sys-sys-config.md "30.4.2.1 The sys_config Table")
table by `INSERT` statements, the
[`sys_config_insert_set_user`](sys-sys-config-insert-set-user.md "30.4.2.2 The sys_config_insert_set_user Trigger")
trigger sets the `set_by` column to the
current user.
