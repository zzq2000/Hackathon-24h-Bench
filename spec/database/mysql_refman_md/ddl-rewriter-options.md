#### 7.6.5.2 ddl\_rewriter Plugin Options

This section describes the command options that control
operation of the `ddl_rewriter` plugin. If
values specified at startup time are incorrect, the
`ddl_rewriter` plugin may fail to initialize
properly and the server does not load it.

To control activation of the `ddl_rewriter`
plugin, use this option:

- [`--ddl-rewriter[=value]`](ddl-rewriter-options.md#option_mysqld_ddl-rewriter)

  |  |  |
  | --- | --- |
  | Command-Line Format | `--ddl-rewriter[=value]` |
  | Introduced | 8.0.16 |
  | Type | Enumeration |
  | Default Value | `ON` |
  | Valid Values | `ON`  `OFF`  `FORCE`  `FORCE_PLUS_PERMANENT` |

  This option controls how the server loads the
  `ddl_rewriter` plugin at startup. It is
  available only if the plugin has been previously registered
  with [`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement") or is
  loaded with [`--plugin-load`](server-options.md#option_mysqld_plugin-load) or
  [`--plugin-load-add`](server-options.md#option_mysqld_plugin-load-add). See
  [Section 7.6.5.1, “Installing or Uninstalling ddl\_rewriter”](ddl-rewriter-installation.md "7.6.5.1 Installing or Uninstalling ddl_rewriter").

  The option value should be one of those available for
  plugin-loading options, as described in
  [Section 7.6.1, “Installing and Uninstalling Plugins”](plugin-loading.md "7.6.1 Installing and Uninstalling Plugins"). For example,
  [`--ddl-rewriter=OFF`](ddl-rewriter-options.md#option_mysqld_ddl-rewriter) disables
  the plugin at server startup.
