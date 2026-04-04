### 2.8.7 MySQL Source-Configuration Options

The **CMake** program provides a great deal of
control over how you configure a MySQL source distribution.
Typically, you do this using options on the
**CMake** command line. For information about
options supported by **CMake**, run either of these
commands in the top-level source directory:

```terminal
$> cmake . -LH

$> ccmake .
```

You can also affect **CMake** using certain
environment variables. See
[Section 6.9, “Environment Variables”](environment-variables.md "6.9 Environment Variables").

For boolean options, the value may be specified as
`1` or `ON` to enable the
option, or as `0` or `OFF` to
disable the option.

Many options configure compile-time defaults that can be
overridden at server startup. For example, the
[`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix),
[`MYSQL_TCP_PORT`](source-configuration-options.md#option_cmake_mysql_tcp_port), and
[`MYSQL_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysql_unix_addr) options that
configure the default installation base directory location, TCP/IP
port number, and Unix socket file can be changed at server startup
with the [`--basedir`](server-system-variables.md#sysvar_basedir),
[`--port`](server-options.md#option_mysqld_port), and
[`--socket`](server-options.md#option_mysqld_socket) options for
[**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"). Where applicable, configuration option
descriptions indicate the corresponding [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server")
startup option.

The following sections provide more information about
**CMake** options.

- [CMake Option Reference](source-configuration-options.md#cmake-option-reference "CMake Option Reference")
- [General Options](source-configuration-options.md#cmake-general-options "General Options")
- [Installation Layout Options](source-configuration-options.md#cmake-installation-layout-options "Installation Layout Options")
- [Storage Engine Options](source-configuration-options.md#option_cmake_storage_engine_options "Storage Engine Options")
- [Feature Options](source-configuration-options.md#cmake-feature-options "Feature Options")
- [Compiler Flags](source-configuration-options.md#cmake-compiler-flags "Compiler Flags")
- [CMake Options for Compiling NDB Cluster](source-configuration-options.md#cmake-mysql-cluster-options "CMake Options for Compiling NDB Cluster")

#### CMake Option Reference

The following table shows the available **CMake**
options. In the `Default` column,
`PREFIX` stands for the value of the
[`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix) option, which
specifies the installation base directory. This value is used as
the parent location for several of the installation
subdirectories.

**Table 2.14 MySQL Source-Configuration Option Reference
(CMake)**

| Formats | Description | Default | Introduced | Removed |
| --- | --- | --- | --- | --- |
| [`ADD_GDB_INDEX`](source-configuration-options.md#option_cmake_add_gdb_index) | Whether to enable generation of .gdb\_index section in binaries |  | 8.0.18 |  |
| [`BUILD_CONFIG`](source-configuration-options.md#option_cmake_build_config) | Use same build options as official releases |  |  |  |
| [`BUNDLE_RUNTIME_LIBRARIES`](source-configuration-options.md#option_cmake_bundle_runtime_libraries) | Bundle runtime libraries with server MSI and Zip packages for Windows | `OFF` |  |  |
| [`CMAKE_BUILD_TYPE`](source-configuration-options.md#option_cmake_cmake_build_type) | Type of build to produce | `RelWithDebInfo` |  |  |
| [`CMAKE_CXX_FLAGS`](source-configuration-options.md#option_cmake_cmake_cxx_flags) | Flags for C++ Compiler |  |  |  |
| [`CMAKE_C_FLAGS`](source-configuration-options.md#option_cmake_cmake_c_flags) | Flags for C Compiler |  |  |  |
| [`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix) | Installation base directory | `/usr/local/mysql` |  |  |
| [`COMPILATION_COMMENT`](source-configuration-options.md#option_cmake_compilation_comment) | Comment about compilation environment |  |  |  |
| [`COMPILATION_COMMENT_SERVER`](source-configuration-options.md#option_cmake_compilation_comment_server) | Comment about compilation environment for use by mysqld |  | 8.0.14 |  |
| [`COMPRESS_DEBUG_SECTIONS`](source-configuration-options.md#option_cmake_compress_debug_sections) | Compress debug sections of binary executables | `OFF` | 8.0.22 |  |
| [`CPACK_MONOLITHIC_INSTALL`](source-configuration-options.md#option_cmake_cpack_monolithic_install) | Whether package build produces single file | `OFF` |  |  |
| [`DEFAULT_CHARSET`](source-configuration-options.md#option_cmake_default_charset) | The default server character set | `utf8mb4` |  |  |
| [`DEFAULT_COLLATION`](source-configuration-options.md#option_cmake_default_collation) | The default server collation | `utf8mb4_0900_ai_ci` |  |  |
| [`DISABLE_PSI_COND`](source-configuration-options.md#option_cmake_disable_psi_cond) | Exclude Performance Schema condition instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_DATA_LOCK`](source-configuration-options.md#option_cmake_disable_psi_data_lock) | Exclude the performance schema data lock instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_ERROR`](source-configuration-options.md#option_cmake_disable_psi_error) | Exclude the performance schema server error instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_FILE`](source-configuration-options.md#option_cmake_disable_psi_file) | Exclude Performance Schema file instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_IDLE`](source-configuration-options.md#option_cmake_disable_psi_idle) | Exclude Performance Schema idle instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_MEMORY`](source-configuration-options.md#option_cmake_disable_psi_memory) | Exclude Performance Schema memory instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_METADATA`](source-configuration-options.md#option_cmake_disable_psi_metadata) | Exclude Performance Schema metadata instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_MUTEX`](source-configuration-options.md#option_cmake_disable_psi_mutex) | Exclude Performance Schema mutex instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_PS`](source-configuration-options.md#option_cmake_disable_psi_ps) | Exclude the performance schema prepared statements | `OFF` |  |  |
| [`DISABLE_PSI_RWLOCK`](source-configuration-options.md#option_cmake_disable_psi_rwlock) | Exclude Performance Schema rwlock instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_SOCKET`](source-configuration-options.md#option_cmake_disable_psi_socket) | Exclude Performance Schema socket instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_SP`](source-configuration-options.md#option_cmake_disable_psi_sp) | Exclude Performance Schema stored program instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_STAGE`](source-configuration-options.md#option_cmake_disable_psi_stage) | Exclude Performance Schema stage instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_STATEMENT`](source-configuration-options.md#option_cmake_disable_psi_statement) | Exclude Performance Schema statement instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_STATEMENT_DIGEST`](source-configuration-options.md#option_cmake_disable_psi_statement_digest) | Exclude Performance Schema statements\_digest instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_TABLE`](source-configuration-options.md#option_cmake_disable_psi_table) | Exclude Performance Schema table instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_THREAD`](source-configuration-options.md#option_cmake_disable_psi_thread) | Exclude the performance schema thread instrumentation | `OFF` |  |  |
| [`DISABLE_PSI_TRANSACTION`](source-configuration-options.md#option_cmake_disable_psi_transaction) | Exclude the performance schema transaction instrumentation | `OFF` |  |  |
| [`DISABLE_SHARED`](source-configuration-options.md#option_cmake_disable_shared) | Do not build shared libraries, compile position-dependent code | `OFF` |  | 8.0.18 |
| [`DOWNLOAD_BOOST`](source-configuration-options.md#option_cmake_download_boost) | Whether to download the Boost library | `OFF` |  |  |
| [`DOWNLOAD_BOOST_TIMEOUT`](source-configuration-options.md#option_cmake_download_boost_timeout) | Timeout in seconds for downloading the Boost library | `600` |  |  |
| [`ENABLED_LOCAL_INFILE`](source-configuration-options.md#option_cmake_enabled_local_infile) | Whether to enable LOCAL for LOAD DATA | `OFF` |  |  |
| [`ENABLED_PROFILING`](source-configuration-options.md#option_cmake_enabled_profiling) | Whether to enable query profiling code | `ON` |  |  |
| [`ENABLE_DOWNLOADS`](source-configuration-options.md#option_cmake_enable_downloads) | Whether to download optional files | `OFF` |  | 8.0.26 |
| [`ENABLE_EXPERIMENTAL_SYSVARS`](source-configuration-options.md#option_cmake_enable_experimental_sysvars) | Whether to enabled experimental InnoDB system variables | `OFF` |  |  |
| [`ENABLE_GCOV`](source-configuration-options.md#option_cmake_enable_gcov) | Whether to include gcov support |  |  |  |
| [`ENABLE_GPROF`](source-configuration-options.md#option_cmake_enable_gprof) | Enable gprof (optimized Linux builds only) | `OFF` |  |  |
| [`FORCE_COLORED_OUTPUT`](source-configuration-options.md#option_cmake_force_colored_output) | Whether to colorize compiler output | `OFF` | 8.0.33 |  |
| [`FORCE_INSOURCE_BUILD`](source-configuration-options.md#option_cmake_force_insource_build) | Whether to force an in-source build | `OFF` | 8.0.14 |  |
| [`FORCE_UNSUPPORTED_COMPILER`](source-configuration-options.md#option_cmake_force_unsupported_compiler) | Whether to permit unsupported compilers | `OFF` |  |  |
| [`FPROFILE_GENERATE`](source-configuration-options.md#option_cmake_fprofile_generate) | Whether to generate profile guided optimization data | `OFF` | 8.0.19 |  |
| [`FPROFILE_USE`](source-configuration-options.md#option_cmake_fprofile_use) | Whether to use profile guided optimization data | `OFF` | 8.0.19 |  |
| [`HAVE_PSI_MEMORY_INTERFACE`](source-configuration-options.md#option_cmake_have_psi_memory_interface) | Enable performance schema memory tracing module for memory allocation functions used in dynamic storage of over-aligned types | `OFF` | 8.0.26 |  |
| [`IGNORE_AIO_CHECK`](source-configuration-options.md#option_cmake_ignore_aio_check) | With -DBUILD\_CONFIG=mysql\_release, ignore libaio check | `OFF` |  |  |
| [`INSTALL_BINDIR`](source-configuration-options.md#option_cmake_install_bindir) | User executables directory | `PREFIX/bin` |  |  |
| [`INSTALL_DOCDIR`](source-configuration-options.md#option_cmake_install_docdir) | Documentation directory | `PREFIX/docs` |  |  |
| [`INSTALL_DOCREADMEDIR`](source-configuration-options.md#option_cmake_install_docreadmedir) | README file directory | `PREFIX` |  |  |
| [`INSTALL_INCLUDEDIR`](source-configuration-options.md#option_cmake_install_includedir) | Header file directory | `PREFIX/include` |  |  |
| [`INSTALL_INFODIR`](source-configuration-options.md#option_cmake_install_infodir) | Info file directory | `PREFIX/docs` |  |  |
| [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout) | Select predefined installation layout | `STANDALONE` |  |  |
| [`INSTALL_LIBDIR`](source-configuration-options.md#option_cmake_install_libdir) | Library file directory | `PREFIX/lib` |  |  |
| [`INSTALL_MANDIR`](source-configuration-options.md#option_cmake_install_mandir) | Manual page directory | `PREFIX/man` |  |  |
| [`INSTALL_MYSQLKEYRINGDIR`](source-configuration-options.md#option_cmake_install_mysqlkeyringdir) | Directory for keyring\_file plugin data file | `platform specific` |  |  |
| [`INSTALL_MYSQLSHAREDIR`](source-configuration-options.md#option_cmake_install_mysqlsharedir) | Shared data directory | `PREFIX/share` |  |  |
| [`INSTALL_MYSQLTESTDIR`](source-configuration-options.md#option_cmake_install_mysqltestdir) | mysql-test directory | `PREFIX/mysql-test` |  |  |
| [`INSTALL_PKGCONFIGDIR`](source-configuration-options.md#option_cmake_install_pkgconfigdir) | Directory for mysqlclient.pc pkg-config file | `INSTALL_LIBDIR/pkgconfig` |  |  |
| [`INSTALL_PLUGINDIR`](source-configuration-options.md#option_cmake_install_plugindir) | Plugin directory | `PREFIX/lib/plugin` |  |  |
| [`INSTALL_PRIV_LIBDIR`](source-configuration-options.md#option_cmake_install_priv_libdir) | Installation private library directory |  | 8.0.18 |  |
| [`INSTALL_SBINDIR`](source-configuration-options.md#option_cmake_install_sbindir) | Server executable directory | `PREFIX/bin` |  |  |
| [`INSTALL_SECURE_FILE_PRIVDIR`](source-configuration-options.md#option_cmake_install_secure_file_privdir) | secure\_file\_priv default value | `platform specific` |  |  |
| [`INSTALL_SHAREDIR`](source-configuration-options.md#option_cmake_install_sharedir) | aclocal/mysql.m4 installation directory | `PREFIX/share` |  |  |
| [`INSTALL_STATIC_LIBRARIES`](source-configuration-options.md#option_cmake_install_static_libraries) | Whether to install static libraries | `ON` |  |  |
| [`INSTALL_SUPPORTFILESDIR`](source-configuration-options.md#option_cmake_install_supportfilesdir) | Extra support files directory | `PREFIX/support-files` |  |  |
| [`LINK_RANDOMIZE`](source-configuration-options.md#option_cmake_link_randomize) | Whether to randomize order of symbols in mysqld binary | `OFF` |  |  |
| [`LINK_RANDOMIZE_SEED`](source-configuration-options.md#option_cmake_link_randomize_seed) | Seed value for LINK\_RANDOMIZE option | `mysql` |  |  |
| [`MAX_INDEXES`](source-configuration-options.md#option_cmake_max_indexes) | Maximum indexes per table | `64` |  |  |
| [`MEMCACHED_HOME`](source-configuration-options.md#option_cmake_memcached_home) | Path to memcached; obsolete | `[none]` |  | 8.0.23 |
| [`MSVC_CPPCHECK`](source-configuration-options.md#option_cmake_msvc_cppcheck) | Enable MSVC code analysis. | `OFF` | 8.0.33 |  |
| [`MUTEX_TYPE`](source-configuration-options.md#option_cmake_mutex_type) | InnoDB mutex type | `event` |  |  |
| [`MYSQLX_TCP_PORT`](source-configuration-options.md#option_cmake_mysqlx_tcp_port) | TCP/IP port number used by X Plugin | `33060` |  |  |
| [`MYSQLX_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysqlx_unix_addr) | Unix socket file used by X Plugin | `/tmp/mysqlx.sock` |  |  |
| [`MYSQL_DATADIR`](source-configuration-options.md#option_cmake_mysql_datadir) | Data directory |  |  |  |
| [`MYSQL_MAINTAINER_MODE`](source-configuration-options.md#option_cmake_mysql_maintainer_mode) | Whether to enable MySQL maintainer-specific development environment | `OFF` |  |  |
| [`MYSQL_PROJECT_NAME`](source-configuration-options.md#option_cmake_mysql_project_name) | Windows/macOS project name | `MySQL` |  |  |
| [`MYSQL_TCP_PORT`](source-configuration-options.md#option_cmake_mysql_tcp_port) | TCP/IP port number | `3306` |  |  |
| [`MYSQL_UNIX_ADDR`](source-configuration-options.md#option_cmake_mysql_unix_addr) | Unix socket file | `/tmp/mysql.sock` |  |  |
| [`NDB_UTILS_LINK_DYNAMIC`](source-configuration-options.md#option_cmake_ndb_utils_link_dynamic) | Cause NDB tools to be dynamically linked to ndbclient |  | 8.0.22 |  |
| [`ODBC_INCLUDES`](source-configuration-options.md#option_cmake_odbc_includes) | ODBC includes directory |  |  |  |
| [`ODBC_LIB_DIR`](source-configuration-options.md#option_cmake_odbc_lib_dir) | ODBC library directory |  |  |  |
| [`OPTIMIZER_TRACE`](source-configuration-options.md#option_cmake_optimizer_trace) | Whether to support optimizer tracing |  |  |  |
| [`OPTIMIZE_SANITIZER_BUILDS`](source-configuration-options.md#option_cmake_optimize_sanitizer_builds) | Whether to optimize sanitizer builds | `ON` | 8.0.34 |  |
| [`REPRODUCIBLE_BUILD`](source-configuration-options.md#option_cmake_reproducible_build) | Take extra care to create a build result independent of build location and time |  |  |  |
| [`SHOW_SUPPRESSED_COMPILER_WARNING`](source-configuration-options.md#option_cmake_show_suppressed_compiler_warnings) | Whether to show suppressed compiler warnings and not fail with -Werror. | `OFF` | 8.0.30 |  |
| [`SYSCONFDIR`](source-configuration-options.md#option_cmake_sysconfdir) | Option file directory |  |  |  |
| [`SYSTEMD_PID_DIR`](source-configuration-options.md#option_cmake_systemd_pid_dir) | Directory for PID file under systemd | `/var/run/mysqld` |  |  |
| [`SYSTEMD_SERVICE_NAME`](source-configuration-options.md#option_cmake_systemd_service_name) | Name of MySQL service under systemd | `mysqld` |  |  |
| [`TMPDIR`](source-configuration-options.md#option_cmake_tmpdir) | tmpdir default value |  |  |  |
| [`USE_LD_GOLD`](source-configuration-options.md#option_cmake_use_ld_gold) | Whether to use GNU gold linker | `ON` |  | 8.0.31 |
| [`USE_LD_LLD`](source-configuration-options.md#option_cmake_use_ld_lld) | Whether to use LLVM lld linker | `ON` | 8.0.16 |  |
| [`WIN_DEBUG_NO_INLINE`](source-configuration-options.md#option_cmake_win_debug_no_inline) | Whether to disable function inlining | `OFF` |  |  |
| [`WITHOUT_SERVER`](source-configuration-options.md#option_cmake_without_server) | Do not build the server; internal use only | `OFF` |  |  |
| [`WITHOUT_xxx_STORAGE_ENGINE`](source-configuration-options.md#option_cmake_storage_engine_options "Storage Engine Options") | Exclude storage engine xxx from build |  |  |  |
| [`WITH_ANT`](source-configuration-options.md#option_cmake_with_ant) | Path to Ant for building GCS Java wrapper |  |  |  |
| [`WITH_ASAN`](source-configuration-options.md#option_cmake_with_asan) | Enable AddressSanitizer | `OFF` |  |  |
| [`WITH_ASAN_SCOPE`](source-configuration-options.md#option_cmake_with_asan_scope) | Enable AddressSanitizer -fsanitize-address-use-after-scope Clang flag | `OFF` |  |  |
| [`WITH_AUTHENTICATION_CLIENT_PLUGINS`](source-configuration-options.md#option_cmake_with_authentication_client_plugins) | Enabled automatically if any corresponding server authentication plugins are built |  | 8.0.26 |  |
| [`WITH_AUTHENTICATION_LDAP`](source-configuration-options.md#option_cmake_with_authentication_ldap) | Whether to report error if LDAP authentication plugins cannot be built | `OFF` |  |  |
| [`WITH_AUTHENTICATION_PAM`](source-configuration-options.md#option_cmake_with_authentication_pam) | Build PAM authentication plugin | `OFF` |  |  |
| [`WITH_AWS_SDK`](source-configuration-options.md#option_cmake_with_aws_sdk) | Location of Amazon Web Services software development kit |  |  |  |
| [`WITH_BOOST`](source-configuration-options.md#option_cmake_with_boost) | The location of the Boost library sources |  |  |  |
| [`WITH_BUILD_ID`](source-configuration-options.md#option_cmake_with_build_id) | On Linux systems, generate a unique build ID | `ON` | 8.0.31 |  |
| [`WITH_BUNDLED_LIBEVENT`](source-configuration-options.md#option_cmake_with_bundled_libevent) | Use bundled libevent when building ndbmemcache; obsolete | `ON` |  | 8.0.23 |
| [`WITH_BUNDLED_MEMCACHED`](source-configuration-options.md#option_cmake_with_bundled_memcached) | Use bundled memcached when building ndbmemcache; obsolete | `ON` |  | 8.0.23 |
| [`WITH_CLASSPATH`](source-configuration-options.md#option_cmake_with_classpath) | Classpath to use when building MySQL Cluster Connector for Java. Default is an empty string. |  |  |  |
| [`WITH_CLIENT_PROTOCOL_TRACING`](source-configuration-options.md#option_cmake_with_client_protocol_tracing) | Build client-side protocol tracing framework | `ON` |  |  |
| [`WITH_CURL`](source-configuration-options.md#option_cmake_with_curl) | Location of curl library |  |  |  |
| [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug) | Whether to include debugging support | `OFF` |  |  |
| [`WITH_DEFAULT_COMPILER_OPTIONS`](source-configuration-options.md#option_cmake_with_default_compiler_options) | Whether to use default compiler options | `ON` |  |  |
| [`WITH_DEFAULT_FEATURE_SET`](source-configuration-options.md#option_cmake_with_default_feature_set) | Whether to use default feature set | `ON` |  | 8.0.22 |
| [`WITH_DEVELOPER_ENTITLEMENTS`](source-configuration-options.md#option_cmake_with_developer_entitlements) | Whether to add the 'get-task-allow' entitlement to all executables on macOS to generate a core dump in the event of an unexpected server halt | `OFF` | 8.0.30 |  |
| [`WITH_EDITLINE`](source-configuration-options.md#option_cmake_with_editline) | Which libedit/editline library to use | `bundled` |  |  |
| [`WITH_ERROR_INSERT`](source-configuration-options.md#option_cmake_with_error_insert) | Enable error injection in the NDB storage engine. Should not be used for building binaries intended for production. | `OFF` |  |  |
| [`WITH_FIDO`](source-configuration-options.md#option_cmake_with_fido) | Type of FIDO library support | `bundled` | 8.0.27 |  |
| [`WITH_GMOCK`](source-configuration-options.md#option_cmake_with_gmock) | Path to googlemock distribution |  |  | 8.0.26 |
| [`WITH_ICU`](source-configuration-options.md#option_cmake_with_icu) | Type of ICU support | `bundled` |  |  |
| [`WITH_INNODB_EXTRA_DEBUG`](source-configuration-options.md#option_cmake_with_innodb_extra_debug) | Whether to include extra debugging support for InnoDB. | `OFF` |  |  |
| [`WITH_INNODB_MEMCACHED`](source-configuration-options.md#option_cmake_with_innodb_memcached) | Whether to generate memcached shared libraries. | `OFF` |  |  |
| [`WITH_JEMALLOC`](source-configuration-options.md#option_cmake_with_jemalloc) | Whether to link with -ljemalloc | `OFF` | 8.0.16 |  |
| [`WITH_KEYRING_TEST`](source-configuration-options.md#option_cmake_with_keyring_test) | Build the keyring test program | `OFF` |  |  |
| [`WITH_LIBEVENT`](source-configuration-options.md#option_cmake_with_libevent) | Which libevent library to use | `bundled` |  |  |
| [`WITH_LIBWRAP`](source-configuration-options.md#option_cmake_with_libwrap) | Whether to include libwrap (TCP wrappers) support | `OFF` |  |  |
| [`WITH_LOCK_ORDER`](source-configuration-options.md#option_cmake_with_lock_order) | Whether to enable LOCK\_ORDER tooling | `OFF` | 8.0.17 |  |
| [`WITH_LSAN`](source-configuration-options.md#option_cmake_with_lsan) | Whether to run LeakSanitizer, without AddressSanitizer | `OFF` | 8.0.16 |  |
| [`WITH_LTO`](source-configuration-options.md#option_cmake_with_lto) | Enable link-time optimizer | `OFF` | 8.0.13 |  |
| [`WITH_LZ4`](source-configuration-options.md#option_cmake_with_lz4) | Type of LZ4 library support | `bundled` |  |  |
| [`WITH_LZMA`](source-configuration-options.md#option_cmake_with_lzma) | Type of LZMA library support | `bundled` |  | 8.0.16 |
| [`WITH_MECAB`](source-configuration-options.md#option_cmake_with_mecab) | Compiles MeCab |  |  |  |
| [`WITH_MSAN`](source-configuration-options.md#option_cmake_with_msan) | Enable MemorySanitizer | `OFF` |  |  |
| [`WITH_MSCRT_DEBUG`](source-configuration-options.md#option_cmake_with_mscrt_debug) | Enable Visual Studio CRT memory leak tracing | `OFF` |  |  |
| [`WITH_MYSQLX`](source-configuration-options.md#option_cmake_with_mysqlx) | Whether to disable X Protocol | `ON` |  |  |
| [`WITH_NDB`](source-configuration-options.md#option_cmake_with_ndb) | Build MySQL NDB Cluster, including NDB storage engine and all NDB programs | `OFF` | 8.0.31 |  |
| [`WITH_NDBAPI_EXAMPLES`](source-configuration-options.md#option_cmake_with_ndbapi_examples) | Build API example programs. | `OFF` |  |  |
| [`WITH_NDBCLUSTER`](source-configuration-options.md#option_cmake_with_ndbcluster) | NDB 8.0.30 and earlier: Build NDB storage engine. NDB 8.0.31 and later: Deprecated; use WITH\_NDB instead | `OFF` |  |  |
| [`WITH_NDBCLUSTER_STORAGE_ENGINE`](source-configuration-options.md#option_cmake_with_ndbcluster_storage_engine) | Prior to NDB 8.0.31, this was for internal use only. NDB 8.0.31 and later: toggles (only) inclusion of NDBCLUSTER storage engine | `ON` |  |  |
| [`WITH_NDBMTD`](source-configuration-options.md#option_cmake_with_ndbmtd) | Build multithreaded data node binary | `ON` |  |  |
| [`WITH_NDB_DEBUG`](source-configuration-options.md#option_cmake_with_ndb_debug) | Produce a debug build for testing or troubleshooting. | `OFF` |  |  |
| [`WITH_NDB_JAVA`](source-configuration-options.md#option_cmake_with_ndb_java) | Enable building of Java and ClusterJ support. Enabled by default. Supported in MySQL Cluster only. | `ON` |  |  |
| [`WITH_NDB_PORT`](source-configuration-options.md#option_cmake_with_ndb_port) | Default port used by a management server built with this option. If this option was not used to build it, the management server's default port is 1186. | `[none]` |  |  |
| [`WITH_NDB_TEST`](source-configuration-options.md#option_cmake_with_ndb_test) | Include NDB API test programs. | `OFF` |  |  |
| [`WITH_NUMA`](source-configuration-options.md#option_cmake_with_numa) | Set NUMA memory allocation policy |  |  |  |
| [`WITH_PACKAGE_FLAGS`](source-configuration-options.md#option_cmake_with_package_flags) | For flags typically used for RPM/DEB packages, whether to add them to standalone builds on those platforms |  | 8.0.26 |  |
| [`WITH_PLUGIN_NDBCLUSTER`](source-configuration-options.md#option_cmake_with_plugin_ndbcluster) | For internal use; may not work as expected in all circumstances. Instead, users should employ WITH\_NDBCLUSTER |  | 8.0.13 | 8.0.31 |
| [`WITH_PROTOBUF`](source-configuration-options.md#option_cmake_with_protobuf) | Which Protocol Buffers package to use | `bundled` |  |  |
| [`WITH_RAPID`](source-configuration-options.md#option_cmake_with_rapid) | Whether to build rapid development cycle plugins | `ON` |  |  |
| [`WITH_RAPIDJSON`](source-configuration-options.md#option_cmake_with_rapidjson) | Type of RapidJSON support | `bundled` | 8.0.13 |  |
| [`WITH_RE2`](source-configuration-options.md#option_cmake_with_re2) | Type of RE2 library support | `bundled` |  | 8.0.18 |
| [`WITH_ROUTER`](source-configuration-options.md#option_cmake_with_router) | Whether to build MySQL Router | `ON` | 8.0.16 |  |
| [`WITH_SASL`](source-configuration-options.md#option_cmake_with_sasl) | Internal use only |  |  |  |
| [`WITH_SSL`](source-configuration-options.md#option_cmake_with_ssl) | Type of SSL support | `system` |  |  |
| [`WITH_SYSTEMD`](source-configuration-options.md#option_cmake_with_systemd) | Enable installation of systemd support files | `OFF` |  |  |
| [`WITH_SYSTEMD_DEBUG`](source-configuration-options.md#option_cmake_with_systemd_debug) | Enable additional systemd debug information | `OFF` | 8.0.22 |  |
| [`WITH_SYSTEM_LIBS`](source-configuration-options.md#option_cmake_with_system_libs) | Set system value of library options not set explicitly | `OFF` |  |  |
| [`WITH_TCMALLOC`](source-configuration-options.md#option_cmake_with_tcmalloc) | Whether to link with -ltcmalloc. BUNDLED is supported on Linux only | `OFF` | 8.0.22 |  |
| [`WITH_TEST_TRACE_PLUGIN`](source-configuration-options.md#option_cmake_with_test_trace_plugin) | Build test protocol trace plugin | `OFF` |  |  |
| [`WITH_TSAN`](source-configuration-options.md#option_cmake_with_tsan) | Enable ThreadSanitizer | `OFF` |  |  |
| [`WITH_UBSAN`](source-configuration-options.md#option_cmake_with_ubsan) | Enable Undefined Behavior Sanitizer | `OFF` |  |  |
| [`WITH_UNIT_TESTS`](source-configuration-options.md#option_cmake_with_unit_tests) | Compile MySQL with unit tests | `ON` |  |  |
| [`WITH_UNIXODBC`](source-configuration-options.md#option_cmake_with_unixodbc) | Enable unixODBC support | `OFF` |  |  |
| [`WITH_VALGRIND`](source-configuration-options.md#option_cmake_with_valgrind) | Whether to compile in Valgrind header files | `OFF` |  |  |
| [`WITH_WIN_JEMALLOC`](source-configuration-options.md#option_cmake_with_win_jemalloc) | Path to directory containing jemalloc.dll |  | 8.0.29 |  |
| [`WITH_ZLIB`](source-configuration-options.md#option_cmake_with_zlib) | Type of zlib support | `bundled` |  |  |
| [`WITH_ZSTD`](source-configuration-options.md#option_cmake_with_zstd) | Type of zstd support | `bundled` | 8.0.18 |  |
| [`WITH_xxx_STORAGE_ENGINE`](source-configuration-options.md#option_cmake_storage_engine_options "Storage Engine Options") | Compile storage engine xxx statically into server |  |  |  |

#### General Options

- [`-DBUILD_CONFIG=mysql_release`](source-configuration-options.md#option_cmake_build_config)

  This option configures a source distribution with the same
  build options used by Oracle to produce binary distributions
  for official MySQL releases.
- [`-DWITH_BUILD_ID=bool`](source-configuration-options.md#option_cmake_with_build_id)

  On Linux systems, generates a unique build ID which is used
  as the value of the
  [`build_id`](server-system-variables.md#sysvar_build_id) system variable
  and written to the MySQL server log on startup. Set this
  option to `OFF` to disable this feature.

  Added in MySQL 8.0.31, this option has no effect on
  platforms other than Linux.
- [`-DBUNDLE_RUNTIME_LIBRARIES=bool`](source-configuration-options.md#option_cmake_bundle_runtime_libraries)

  Whether to bundle runtime libraries with server MSI and Zip
  packages for Windows.
- [`-DCMAKE_BUILD_TYPE=type`](source-configuration-options.md#option_cmake_cmake_build_type)

  The type of build to produce:

  - `RelWithDebInfo`: Enable optimizations
    and generate debugging information. This is the default
    MySQL build type.
  - `Release`: Enable optimizations but
    omit debugging information to reduce the build size.
    This build type was added in MySQL 8.0.13.
  - `Debug`: Disable optimizations and
    generate debugging information. This build type is also
    used if the [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug)
    option is enabled. That is,
    [`-DWITH_DEBUG=1`](source-configuration-options.md#option_cmake_with_debug) has the
    same effect as
    [`-DCMAKE_BUILD_TYPE=Debug`](source-configuration-options.md#option_cmake_cmake_build_type).

  The option values `None` and
  `MinSizeRel` are not supported.
- [`-DCPACK_MONOLITHIC_INSTALL=bool`](source-configuration-options.md#option_cmake_cpack_monolithic_install)

  This option affects whether the **make
  package** operation produces multiple installation
  package files or a single file. If disabled, the operation
  produces multiple installation package files, which may be
  useful if you want to install only a subset of a full MySQL
  installation. If enabled, it produces a single file for
  installing everything.
- [`-DFORCE_INSOURCE_BUILD=bool`](source-configuration-options.md#option_cmake_force_insource_build)

  Defines whether to force an in-source build. Out-of-source
  builds are recommended, as they permit multiple builds from
  the same source, and cleanup can be performed quickly by
  removing the build directory. To force an in-source build,
  invoke **CMake** with
  [`-DFORCE_INSOURCE_BUILD=ON`](source-configuration-options.md#option_cmake_force_insource_build).
- [`-DFORCE_COLORED_OUTPUT=bool`](source-configuration-options.md#option_cmake_force_colored_output)

  Defines whether to enable colorized compiler output for
  **gcc** and **clang** when
  compiling on the command line. Defaults to
  `OFF`.

#### Installation Layout Options

The [`CMAKE_INSTALL_PREFIX`](source-configuration-options.md#option_cmake_cmake_install_prefix) option
indicates the base installation directory. Other options with
names of the form
`INSTALL_xxx` that
indicate component locations are interpreted relative to the
prefix and their values are relative pathnames. Their values
should not include the prefix.

- [`-DCMAKE_INSTALL_PREFIX=dir_name`](source-configuration-options.md#option_cmake_cmake_install_prefix)

  The installation base directory.

  This value can be set at server startup using the
  [`--basedir`](server-system-variables.md#sysvar_basedir) option.
- [`-DINSTALL_BINDIR=dir_name`](source-configuration-options.md#option_cmake_install_bindir)

  Where to install user programs.
- [`-DINSTALL_DOCDIR=dir_name`](source-configuration-options.md#option_cmake_install_docdir)

  Where to install documentation.
- [`-DINSTALL_DOCREADMEDIR=dir_name`](source-configuration-options.md#option_cmake_install_docreadmedir)

  Where to install `README` files.
- [`-DINSTALL_INCLUDEDIR=dir_name`](source-configuration-options.md#option_cmake_install_includedir)

  Where to install header files.
- [`-DINSTALL_INFODIR=dir_name`](source-configuration-options.md#option_cmake_install_infodir)

  Where to install Info files.
- [`-DINSTALL_LAYOUT=name`](source-configuration-options.md#option_cmake_install_layout)

  Select a predefined installation layout:

  - `STANDALONE`: Same layout as used for
    `.tar.gz` and
    `.zip` packages. This is the default.
  - `RPM`: Layout similar to RPM packages.
  - `SVR4`: Solaris package layout.
  - `DEB`: DEB package layout
    (experimental).

  You can select a predefined layout but modify individual
  component installation locations by specifying other
  options. For example:

  ```terminal
  cmake . -DINSTALL_LAYOUT=SVR4 -DMYSQL_DATADIR=/var/mysql/data
  ```

  The [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout) value
  determines the default value of the
  [`secure_file_priv`](server-system-variables.md#sysvar_secure_file_priv),
  [`keyring_encrypted_file_data`](keyring-system-variables.md#sysvar_keyring_encrypted_file_data),
  and [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data)
  system variables. See the descriptions of those variables in
  [Section 7.1.8, “Server System Variables”](server-system-variables.md "7.1.8 Server System Variables"), and
  [Section 8.4.4.19, “Keyring System Variables”](keyring-system-variables.md "8.4.4.19 Keyring System Variables").
- [`-DINSTALL_LIBDIR=dir_name`](source-configuration-options.md#option_cmake_install_libdir)

  Where to install library files.
- [`-DINSTALL_MANDIR=dir_name`](source-configuration-options.md#option_cmake_install_mandir)

  Where to install manual pages.
- [`-DINSTALL_MYSQLKEYRINGDIR=dir_path`](source-configuration-options.md#option_cmake_install_mysqlkeyringdir)

  The default directory to use as the location of the
  `keyring_file` plugin data file. The
  default value is platform specific and depends on the value
  of the [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout)
  **CMake** option; see the description of the
  [`keyring_file_data`](keyring-system-variables.md#sysvar_keyring_file_data) system
  variable in [Section 7.1.8, “Server System Variables”](server-system-variables.md "7.1.8 Server System Variables").
- [`-DINSTALL_MYSQLSHAREDIR=dir_name`](source-configuration-options.md#option_cmake_install_mysqlsharedir)

  Where to install shared data files.
- [`-DINSTALL_MYSQLTESTDIR=dir_name`](source-configuration-options.md#option_cmake_install_mysqltestdir)

  Where to install the `mysql-test`
  directory. To suppress installation of this directory,
  explicitly set the option to the empty value
  ([`-DINSTALL_MYSQLTESTDIR=`](source-configuration-options.md#option_cmake_install_mysqltestdir)).
- [`-DINSTALL_PKGCONFIGDIR=dir_name`](source-configuration-options.md#option_cmake_install_pkgconfigdir)

  The directory in which to install the
  `mysqlclient.pc` file for use by
  **pkg-config**. The default value is
  `INSTALL_LIBDIR/pkgconfig`, unless
  [`INSTALL_LIBDIR`](source-configuration-options.md#option_cmake_install_libdir) ends with
  `/mysql`, in which case that is removed
  first.
- [`-DINSTALL_PLUGINDIR=dir_name`](source-configuration-options.md#option_cmake_install_plugindir)

  The location of the plugin directory.

  This value can be set at server startup with the
  [`--plugin_dir`](server-system-variables.md#sysvar_plugin_dir) option.
- [`-DINSTALL_PRIV_LIBDIR=dir_name`](source-configuration-options.md#option_cmake_install_priv_libdir)

  The location of the dynamic library directory.

  **Default location.**
  For RPM builds, this is
  `/usr/lib64/mysql/private/`, for DEB it
  is `/usr/lib/mysql/private/`, and for
  TAR it is `lib/private/`.

  **Protobuf.**
  Because this is a private location, the loader (such as
  `ld-linux.so` on Linux) may not find
  the `libprotobuf.so` files without
  help. To guide the loader,
  `RPATH=$ORIGIN/../$INSTALL_PRIV_LIBDIR`
  is added to [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") and
  **mysqlxtest**. This works for most cases
  but when using the
  [Resource Group](resource-groups.md "7.1.16 Resource Groups")
  feature, [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") is
  `setsuid`, and the loader ignores any
  `RPATH` which contains
  `$ORIGIN`. To overcome this, an explicit
  full path to the directory is set in the DEB and RPM
  versions of [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server"), since the target
  destination is known. For tarball installs, patching of
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with a tool like
  **patchelf** is required.

  This option was added in MySQL 8.0.18.
- [`-DINSTALL_SBINDIR=dir_name`](source-configuration-options.md#option_cmake_install_sbindir)

  Where to install the [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") server.
- [`-DINSTALL_SECURE_FILE_PRIVDIR=dir_name`](source-configuration-options.md#option_cmake_install_secure_file_privdir)

  The default value for the
  [`secure_file_priv`](server-system-variables.md#sysvar_secure_file_priv) system
  variable. The default value is platform specific and depends
  on the value of the
  [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout)
  **CMake** option; see the description of the
  [`secure_file_priv`](server-system-variables.md#sysvar_secure_file_priv) system
  variable in [Section 7.1.8, “Server System Variables”](server-system-variables.md "7.1.8 Server System Variables").
- [`-DINSTALL_SHAREDIR=dir_name`](source-configuration-options.md#option_cmake_install_sharedir)

  Where to install `aclocal/mysql.m4`.
- [`-DINSTALL_STATIC_LIBRARIES=bool`](source-configuration-options.md#option_cmake_install_static_libraries)

  Whether to install static libraries. The default is
  `ON`. If set to `OFF`,
  these library files are not installed:
  `libmysqlclient.a`,
  `libmysqlservices.a`.
- [`-DINSTALL_SUPPORTFILESDIR=dir_name`](source-configuration-options.md#option_cmake_install_supportfilesdir)

  Where to install extra support files.
- [`-DLINK_RANDOMIZE=bool`](source-configuration-options.md#option_cmake_link_randomize)

  Whether to randomize the order of symbols in the
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") binary. The default is
  `OFF`. This option should be enabled only
  for debugging purposes.
- [`-DLINK_RANDOMIZE_SEED=val`](source-configuration-options.md#option_cmake_link_randomize_seed)

  Seed value for the
  [`LINK_RANDOMIZE`](source-configuration-options.md#option_cmake_link_randomize) option. The
  value is a string. The default is `mysql`,
  an arbitrary choice.
- [`-DMYSQL_DATADIR=dir_name`](source-configuration-options.md#option_cmake_mysql_datadir)

  The location of the MySQL data directory.

  This value can be set at server startup with the
  [`--datadir`](server-system-variables.md#sysvar_datadir) option.
- [`-DODBC_INCLUDES=dir_name`](source-configuration-options.md#option_cmake_odbc_includes)

  The location of the ODBC includes directory, which may be
  used while configuring Connector/ODBC.
- [`-DODBC_LIB_DIR=dir_name`](source-configuration-options.md#option_cmake_odbc_lib_dir)

  The location of the ODBC library directory, which may be
  used while configuring Connector/ODBC.
- [`-DSYSCONFDIR=dir_name`](source-configuration-options.md#option_cmake_sysconfdir)

  The default `my.cnf` option file
  directory.

  This location cannot be set at server startup, but you can
  start the server with a given option file using the
  [`--defaults-file=file_name`](option-file-options.md#option_general_defaults-file)
  option, where *`file_name`* is the
  full path name to the file.
- [`-DSYSTEMD_PID_DIR=dir_name`](source-configuration-options.md#option_cmake_systemd_pid_dir)

  The name of the directory in which to create the PID file
  when MySQL is managed by systemd. The default is
  `/var/run/mysqld`; this might be changed
  implicitly according to the
  [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout) value.

  This option is ignored unless
  [`WITH_SYSTEMD`](source-configuration-options.md#option_cmake_with_systemd) is enabled.
- [`-DSYSTEMD_SERVICE_NAME=name`](source-configuration-options.md#option_cmake_systemd_service_name)

  The name of the MySQL service to use when MySQL is managed
  by **systemd**. The default is
  `mysqld`; this might be changed implicitly
  according to the
  [`INSTALL_LAYOUT`](source-configuration-options.md#option_cmake_install_layout) value.

  This option is ignored unless
  [`WITH_SYSTEMD`](source-configuration-options.md#option_cmake_with_systemd) is enabled.
- [`-DTMPDIR=dir_name`](source-configuration-options.md#option_cmake_tmpdir)

  The default location to use for the
  [`tmpdir`](server-system-variables.md#sysvar_tmpdir) system variable. If
  unspecified, the value defaults to
  `P_tmpdir` in
  `<stdio.h>`.

#### Storage Engine Options

Storage engines are built as plugins. You can build a plugin as
a static module (compiled into the server) or a dynamic module
(built as a dynamic library that must be installed into the
server using the [`INSTALL PLUGIN`](install-plugin.md "15.7.4.4 INSTALL PLUGIN Statement")
statement or the [`--plugin-load`](server-options.md#option_mysqld_plugin-load)
option before it can be used). Some plugins might not support
static or dynamic building.

The [`InnoDB`](innodb-storage-engine.md "Chapter 17 The InnoDB Storage Engine"),
[`MyISAM`](myisam-storage-engine.md "18.2 The MyISAM Storage Engine"),
[`MERGE`](merge-storage-engine.md "18.7 The MERGE Storage Engine"),
[`MEMORY`](memory-storage-engine.md "18.3 The MEMORY Storage Engine"), and
[`CSV`](csv-storage-engine.md "18.4 The CSV Storage Engine") engines are mandatory (always
compiled into the server) and need not be installed explicitly.

To compile a storage engine statically into the server, use
`-DWITH_engine_STORAGE_ENGINE=1`.
Some permissible *`engine`* values are
`ARCHIVE`, `BLACKHOLE`,
`EXAMPLE`, and `FEDERATED`.
Examples:

```ini
-DWITH_ARCHIVE_STORAGE_ENGINE=1
-DWITH_BLACKHOLE_STORAGE_ENGINE=1
```

To build MySQL with support for NDB Cluster, use the
[`WITH_NDB`](source-configuration-options.md#option_cmake_with_ndb) option. (*NDB
8.0.30 and earlier*: Use
[`WITH_NDBCLUSTER`](source-configuration-options.md#option_cmake_with_ndbcluster).)

Note

It is not possible to compile without Performance Schema
support. If it is desired to compile without particular types
of instrumentation, that can be done with the following
**CMake** options:

```simple
DISABLE_PSI_COND
DISABLE_PSI_DATA_LOCK
DISABLE_PSI_ERROR
DISABLE_PSI_FILE
DISABLE_PSI_IDLE
DISABLE_PSI_MEMORY
DISABLE_PSI_METADATA
DISABLE_PSI_MUTEX
DISABLE_PSI_PS
DISABLE_PSI_RWLOCK
DISABLE_PSI_SOCKET
DISABLE_PSI_SP
DISABLE_PSI_STAGE
DISABLE_PSI_STATEMENT
DISABLE_PSI_STATEMENT_DIGEST
DISABLE_PSI_TABLE
DISABLE_PSI_THREAD
DISABLE_PSI_TRANSACTION
```

For example, to compile without mutex instrumentation,
configure MySQL using
[`-DDISABLE_PSI_MUTEX=1`](source-configuration-options.md#option_cmake_disable_psi_mutex).

To exclude a storage engine from the build, use
`-DWITH_engine_STORAGE_ENGINE=0`.
Examples:

```ini
-DWITH_ARCHIVE_STORAGE_ENGINE=0
-DWITH_EXAMPLE_STORAGE_ENGINE=0
-DWITH_FEDERATED_STORAGE_ENGINE=0
```

It is also possible to exclude a storage engine from the build
using
`-DWITHOUT_engine_STORAGE_ENGINE=1`
(but
`-DWITH_engine_STORAGE_ENGINE=0`
is preferred). Examples:

```ini
-DWITHOUT_ARCHIVE_STORAGE_ENGINE=1
-DWITHOUT_EXAMPLE_STORAGE_ENGINE=1
-DWITHOUT_FEDERATED_STORAGE_ENGINE=1
```

If neither
`-DWITH_engine_STORAGE_ENGINE`
nor
`-DWITHOUT_engine_STORAGE_ENGINE`
are specified for a given storage engine, the engine is built as
a shared module, or excluded if it cannot be built as a shared
module.

#### Feature Options

- [`-DADD_GDB_INDEX=bool`](source-configuration-options.md#option_cmake_add_gdb_index)

  This option determines whether to enable generation of a
  `.gdb_index` section in binaries, which
  makes loading them in a debugger faster. The option is
  disabled by default. **lld** linker is used,
  and is disabled by It has no effect if a linker other than
  **lld** or GNU **gold** is
  used.

  This option was added in MySQL 8.0.18.
- [`-DCOMPILATION_COMMENT=string`](source-configuration-options.md#option_cmake_compilation_comment)

  A descriptive comment about the compilation environment. As
  of MySQL 8.0.14, [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") uses
  [`COMPILATION_COMMENT_SERVER`](source-configuration-options.md#option_cmake_compilation_comment_server).
  Other programs continue to use
  [`COMPILATION_COMMENT`](source-configuration-options.md#option_cmake_compilation_comment).
- [`-DCOMPRESS_DEBUG_SECTIONS=bool`](source-configuration-options.md#option_cmake_compress_debug_sections)

  Whether to compress the debug sections of binary executables
  (Linux only). Compressing executable debug sections saves
  space at the cost of extra CPU time during the build
  process.

  The default is `OFF`. If this option is not
  set explicitly but the
  `COMPRESS_DEBUG_SECTIONS` environment
  variable is set, the option takes its value from that
  variable.

  This option was added in MySQL 8.0.22.
- [`-DCOMPILATION_COMMENT_SERVER=string`](source-configuration-options.md#option_cmake_compilation_comment_server)

  A descriptive comment about the compilation environment for
  use by [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") (for example, to set the
  [`version_comment`](server-system-variables.md#sysvar_version_comment) system
  variable). This option was added in MySQL 8.0.14. Prior to
  8.0.14, the server uses
  [`COMPILATION_COMMENT`](source-configuration-options.md#option_cmake_compilation_comment).
- [`-DDEFAULT_CHARSET=charset_name`](source-configuration-options.md#option_cmake_default_charset)

  The server character set. By default, MySQL uses the
  `utf8mb4` character set.

  *`charset_name`* may be one of
  `binary`, `armscii8`,
  `ascii`, `big5`,
  `cp1250`, `cp1251`,
  `cp1256`, `cp1257`,
  `cp850`, `cp852`,
  `cp866`, `cp932`,
  `dec8`, `eucjpms`,
  `euckr`, `gb2312`,
  `gbk`, `geostd8`,
  `greek`, `hebrew`,
  `hp8`, `keybcs2`,
  `koi8r`, `koi8u`,
  `latin1`, `latin2`,
  `latin5`, `latin7`,
  `macce`, `macroman`,
  `sjis`, `swe7`,
  `tis620`, `ucs2`,
  `ujis`, `utf8mb3`,
  `utf8mb4`, `utf16`,
  `utf16le`, `utf32`.

  This value can be set at server startup with the
  [`--character-set-server`](server-system-variables.md#sysvar_character_set_server)
  option.
- [`-DDEFAULT_COLLATION=collation_name`](source-configuration-options.md#option_cmake_default_collation)

  The server collation. By default, MySQL uses
  `utf8mb4_0900_ai_ci`. Use the
  [`SHOW COLLATION`](show-collation.md "15.7.7.4 SHOW COLLATION Statement") statement to
  determine which collations are available for each character
  set.

  This value can be set at server startup with the
  [`--collation_server`](server-system-variables.md#sysvar_collation_server) option.
- [`-DDISABLE_PSI_COND=bool`](source-configuration-options.md#option_cmake_disable_psi_cond)

  Whether to exclude the Performance Schema condition
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_FILE=bool`](source-configuration-options.md#option_cmake_disable_psi_file)

  Whether to exclude the Performance Schema file
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_IDLE=bool`](source-configuration-options.md#option_cmake_disable_psi_idle)

  Whether to exclude the Performance Schema idle
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_MEMORY=bool`](source-configuration-options.md#option_cmake_disable_psi_memory)

  Whether to exclude the Performance Schema memory
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_METADATA=bool`](source-configuration-options.md#option_cmake_disable_psi_metadata)

  Whether to exclude the Performance Schema metadata
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_MUTEX=bool`](source-configuration-options.md#option_cmake_disable_psi_mutex)

  Whether to exclude the Performance Schema mutex
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_RWLOCK=bool`](source-configuration-options.md#option_cmake_disable_psi_rwlock)

  Whether to exclude the Performance Schema rwlock
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_SOCKET=bool`](source-configuration-options.md#option_cmake_disable_psi_socket)

  Whether to exclude the Performance Schema socket
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_SP=bool`](source-configuration-options.md#option_cmake_disable_psi_sp)

  Whether to exclude the Performance Schema stored program
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_STAGE=bool`](source-configuration-options.md#option_cmake_disable_psi_stage)

  Whether to exclude the Performance Schema stage
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_STATEMENT=bool`](source-configuration-options.md#option_cmake_disable_psi_statement)

  Whether to exclude the Performance Schema statement
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_STATEMENT_DIGEST=bool`](source-configuration-options.md#option_cmake_disable_psi_statement_digest)

  Whether to exclude the Performance Schema statement digest
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_TABLE=bool`](source-configuration-options.md#option_cmake_disable_psi_table)

  Whether to exclude the Performance Schema table
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_SHARED=bool`](source-configuration-options.md#option_cmake_disable_shared)

  Whether to disable building build shared libraries and
  compile position-dependent code. The default is
  `OFF` (compile position-independent code).

  This option is unused, and was removed in MySQL 8.0.18.
- [`-DDISABLE_PSI_PS=bool`](source-configuration-options.md#option_cmake_disable_psi_ps)

  Exclude the Performance Schema prepared statements instances
  instrumentation. The default is `OFF`
  (include).
- [`-DDISABLE_PSI_THREAD=bool`](source-configuration-options.md#option_cmake_disable_psi_thread)

  Exclude the Performance Schema thread instrumentation. The
  default is `OFF` (include).

  Only disable threads when building without any
  instrumentation, because other instrumentations have a
  dependency on threads.
- [`-DDISABLE_PSI_TRANSACTION=bool`](source-configuration-options.md#option_cmake_disable_psi_transaction)

  Exclude the Performance Schema transaction instrumentation.
  The default is `OFF` (include).
- [`-DDISABLE_PSI_DATA_LOCK=bool`](source-configuration-options.md#option_cmake_disable_psi_data_lock)

  Exclude the performance schema data lock instrumentation.
  The default is `OFF` (include).
- [`-DDISABLE_PSI_ERROR=bool`](source-configuration-options.md#option_cmake_disable_psi_error)

  Exclude the performance schema server error instrumentation.
  The default is `OFF` (include).
- [`-DDOWNLOAD_BOOST=bool`](source-configuration-options.md#option_cmake_download_boost)

  Whether to download the Boost library. The default is
  `OFF`.

  See the [`WITH_BOOST`](source-configuration-options.md#option_cmake_with_boost) option for
  additional discussion about using Boost.
- [`-DDOWNLOAD_BOOST_TIMEOUT=seconds`](source-configuration-options.md#option_cmake_download_boost_timeout)

  The timeout in seconds for downloading the Boost library.
  The default is 600 seconds.

  See the [`WITH_BOOST`](source-configuration-options.md#option_cmake_with_boost) option for
  additional discussion about using Boost.
- [`-DENABLE_DOWNLOADS=bool`](source-configuration-options.md#option_cmake_enable_downloads)

  Whether to download optional files. For example, with this
  option enabled, **CMake** downloads the
  Google Test distribution that is used by the test suite to
  run unit tests, or Ant and JUnit, required for building the
  GCS Java wrapper.

  As of MySQL 8.0.26, MySQL source distributions bundle the
  Google Test source code used to run unit tests.
  Consequently, as of that version the
  [`WITH_GMOCK`](source-configuration-options.md#option_cmake_with_gmock) and
  [`ENABLE_DOWNLOADS`](source-configuration-options.md#option_cmake_enable_downloads)
  **CMake** options are removed and are ignored
  if specified.
- [`-DENABLE_EXPERIMENTAL_SYSVARS=bool`](source-configuration-options.md#option_cmake_enable_experimental_sysvars)

  Whether to enable experimental `InnoDB`
  system variables. Experimental system variables are intended
  for those engaged in MySQL development, should only be used
  in a development or test environment, and may be removed
  without notice in a future MySQL release. For information
  about experimental system variables, refer to
  `/storage/innobase/handler/ha_innodb.cc`
  in the MySQL source tree. Experimental system variables can
  be identified by searching for
  “PLUGIN\_VAR\_EXPERIMENTAL”.
- [`-DENABLE_GCOV=bool`](source-configuration-options.md#option_cmake_enable_gcov)

  Whether to include **gcov** support (Linux
  only).
- [`-DENABLE_GPROF=bool`](source-configuration-options.md#option_cmake_enable_gprof)

  Whether to enable **gprof** (optimized Linux
  builds only).
- [`-DENABLED_LOCAL_INFILE=bool`](source-configuration-options.md#option_cmake_enabled_local_infile)

  This option controls the compiled-in default
  `LOCAL` capability for the MySQL client
  library. Clients that make no explicit arrangements
  therefore have `LOCAL` capability disabled
  or enabled according to the
  [`ENABLED_LOCAL_INFILE`](source-configuration-options.md#option_cmake_enabled_local_infile) setting
  specified at MySQL build time.

  By default, the client library in MySQL binary distributions
  is compiled with
  [`ENABLED_LOCAL_INFILE`](source-configuration-options.md#option_cmake_enabled_local_infile) disabled.
  If you compile MySQL from source, configure it with
  [`ENABLED_LOCAL_INFILE`](source-configuration-options.md#option_cmake_enabled_local_infile) disabled
  or enabled based on whether clients that make no explicit
  arrangements should have `LOCAL` capability
  disabled or enabled, respectively.

  [`ENABLED_LOCAL_INFILE`](source-configuration-options.md#option_cmake_enabled_local_infile) controls
  the default for client-side `LOCAL`
  capability. For the server, the
  [`local_infile`](server-system-variables.md#sysvar_local_infile) system
  variable controls server-side `LOCAL`
  capability. To explicitly cause the server to refuse or
  permit [`LOAD DATA
  LOCAL`](load-data.md "15.2.9 LOAD DATA Statement") statements (regardless of how client
  programs and libraries are configured at build time or
  runtime), start [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with
  [`--local-infile`](server-system-variables.md#sysvar_local_infile) disabled or
  enabled, respectively.
  [`local_infile`](server-system-variables.md#sysvar_local_infile) can also be
  set at runtime. See
  [Section 8.1.6, “Security Considerations for LOAD DATA LOCAL”](load-data-local-security.md "8.1.6 Security Considerations for LOAD DATA LOCAL").
- [`-DENABLED_PROFILING=bool`](source-configuration-options.md#option_cmake_enabled_profiling)

  Whether to enable query profiling code (for the
  [`SHOW PROFILE`](show-profile.md "15.7.7.30 SHOW PROFILE Statement") and
  [`SHOW PROFILES`](show-profiles.md "15.7.7.31 SHOW PROFILES Statement") statements).
- [`-DFORCE_UNSUPPORTED_COMPILER=bool`](source-configuration-options.md#option_cmake_force_unsupported_compiler)

  By default, **CMake** checks for minimum
  versions of
  [supported
  compilers](source-installation-prerequisites.md "2.8.2 Source Installation Prerequisites"); to disable this check, use
  [`-DFORCE_UNSUPPORTED_COMPILER=ON`](source-configuration-options.md#option_cmake_force_unsupported_compiler).
- [`-DFPROFILE_GENERATE=bool`](source-configuration-options.md#option_cmake_fprofile_generate)

  Whether to generate profile guided optimization (PGO) data.
  This option is available for experimenting with PGO with
  GCC. See `cmake/fprofile.cmake` in the
  MySQL source distribution for information about using
  [`FPROFILE_GENERATE`](source-configuration-options.md#option_cmake_fprofile_generate) and
  [`FPROFILE_USE`](source-configuration-options.md#option_cmake_fprofile_use). These options
  have been tested with GCC 8 and 9.

  This option was added in MySQL 8.0.19.
- [`-DFPROFILE_USE=bool`](source-configuration-options.md#option_cmake_fprofile_use)

  Whether to use profile guided optimization (PGO) data. This
  option is available for experimenting with PGO with GCC. See
  the `cmake/fprofile.cmake` file in a
  MySQL source distribution for information about using
  [`FPROFILE_GENERATE`](source-configuration-options.md#option_cmake_fprofile_generate) and
  [`FPROFILE_USE`](source-configuration-options.md#option_cmake_fprofile_use). These options
  have been tested with GCC 8 and 9.

  Enabling [`FPROFILE_USE`](source-configuration-options.md#option_cmake_fprofile_use) also
  enables [`WITH_LTO`](source-configuration-options.md#option_cmake_with_lto).

  This option was added in MySQL 8.0.19.
- [`-DHAVE_PSI_MEMORY_INTERFACE=bool`](source-configuration-options.md#option_cmake_have_psi_memory_interface)

  Whether to enable the performance schema memory tracing
  module for memory allocation functions
  (`ut::aligned_name`
  library functions) used in dynamic storage of over-aligned
  types.
- [`-DIGNORE_AIO_CHECK=bool`](source-configuration-options.md#option_cmake_ignore_aio_check)

  If the
  [`-DBUILD_CONFIG=mysql_release`](source-configuration-options.md#option_cmake_build_config)
  option is given on Linux, the `libaio`
  library must be linked in by default. If you do not have
  `libaio` or do not want to install it, you
  can suppress the check for it by specifying
  [`-DIGNORE_AIO_CHECK=1`](source-configuration-options.md#option_cmake_ignore_aio_check).
- [`-DMAX_INDEXES=num`](source-configuration-options.md#option_cmake_max_indexes)

  The maximum number of indexes per table. The default is 64.
  The maximum is 255. Values smaller than 64 are ignored and
  the default of 64 is used.
- [`-DMYSQL_MAINTAINER_MODE=bool`](source-configuration-options.md#option_cmake_mysql_maintainer_mode)

  Whether to enable a MySQL maintainer-specific development
  environment. If enabled, this option causes compiler
  warnings to become errors.
- [`-DWITH_DEVELOPER_ENTITLEMENTS=bool`](source-configuration-options.md#option_cmake_with_developer_entitlements)

  Whether to add the `get-task-allow`
  entitlement to all executables to generate a core dump in
  the event of an unexpected server halt.

  On macOS 11+, core dumps are limited to processes with the
  `com.apple.security.get-task-allow`
  entitlement, which this CMake option enables. The
  entitlement allows other processes to attach and read/modify
  the processes memory, and allows
  [`--core-file`](server-options.md#option_mysqld_core-file) to function as
  expected.

  This option was added in MySQL 8.0.30.
- [`-DMUTEX_TYPE=type`](source-configuration-options.md#option_cmake_mutex_type)

  The mutex type used by `InnoDB`. Options
  include:

  - `event`: Use event mutexes. This is the
    default value and the original `InnoDB`
    mutex implementation.
  - `sys`: Use POSIX mutexes on UNIX
    systems. Use `CRITICAL_SECTION` objects
    on Windows, if available.
  - `futex`: Use Linux futexes instead of
    condition variables to schedule waiting threads.
- [`-DMYSQLX_TCP_PORT=port_num`](source-configuration-options.md#option_cmake_mysqlx_tcp_port)

  The port number on which X Plugin listens for TCP/IP
  connections. The default is 33060.

  This value can be set at server startup with the
  [`mysqlx_port`](x-plugin-options-system-variables.md#sysvar_mysqlx_port) system
  variable.
- [`-DMYSQLX_UNIX_ADDR=file_name`](source-configuration-options.md#option_cmake_mysqlx_unix_addr)

  The Unix socket file path on which the server listens for
  X Plugin socket connections. This must be an absolute path
  name. The default is `/tmp/mysqlx.sock`.

  This value can be set at server startup with the
  [`mysqlx_port`](x-plugin-options-system-variables.md#sysvar_mysqlx_port) system
  variable.
- [`-DMYSQL_PROJECT_NAME=name`](source-configuration-options.md#option_cmake_mysql_project_name)

  For Windows or macOS, the project name to incorporate into
  the project file name.
- [`-DMYSQL_TCP_PORT=port_num`](source-configuration-options.md#option_cmake_mysql_tcp_port)

  The port number on which the server listens for TCP/IP
  connections. The default is 3306.

  This value can be set at server startup with the
  [`--port`](server-options.md#option_mysqld_port) option.
- [`-DMYSQL_UNIX_ADDR=file_name`](source-configuration-options.md#option_cmake_mysql_unix_addr)

  The Unix socket file path on which the server listens for
  socket connections. This must be an absolute path name. The
  default is `/tmp/mysql.sock`.

  This value can be set at server startup with the
  [`--socket`](server-options.md#option_mysqld_socket) option.
- [`-DOPTIMIZER_TRACE=bool`](source-configuration-options.md#option_cmake_optimizer_trace)

  Whether to support optimizer tracing. See
  [Section 10.15, “Tracing the Optimizer”](optimizer-tracing.md "10.15 Tracing the Optimizer").
- [`-DREPRODUCIBLE_BUILD=bool`](source-configuration-options.md#option_cmake_reproducible_build)

  For builds on Linux systems, this option controls whether to
  take extra care to create a build result independent of
  build location and time.

  This option was added in MySQL 8.0.11. As of MySQL 8.0.12,
  it defaults to `ON` for
  `RelWithDebInfo` builds.
- [`-DSHOW_SUPPRESSED_COMPILER_WARNINGS=bool`](source-configuration-options.md#option_cmake_show_suppressed_compiler_warnings)

  Show suppressed compiler warnings, and do so without failing
  with `-Werror`. Defaults to
  `OFF`.

  This option was added in MySQL 8.0.30.
- [`-DUSE_LD_GOLD=bool`](source-configuration-options.md#option_cmake_use_ld_gold)

  GNU **gold** linker support was removed in
  MySQL 8.0.31; this CMake option was also removed.

  **CMake** causes the build process to link
  with the GNU **gold** linker if it is
  available and not explicitly disabled. To disable use of
  this linker, specify the
  [`-DUSE_LD_GOLD=OFF`](source-configuration-options.md#option_cmake_use_ld_gold) option.
- [`-DUSE_LD_LLD=bool`](source-configuration-options.md#option_cmake_use_ld_lld)

  **CMake** causes the build process to link
  using the LLVM **lld** linker for Clang if it
  is available and not explicitly disabled. To disable use of
  this linker, specify the
  [`-DUSE_LD_LLD=OFF`](source-configuration-options.md#option_cmake_use_ld_lld) option.

  This option was added in MySQL 8.0.16.
- [`-DWIN_DEBUG_NO_INLINE=bool`](source-configuration-options.md#option_cmake_win_debug_no_inline)

  Whether to disable function inlining on Windows. The default
  is `OFF` (inlining enabled).
- [`-DWITH_ANT=path_name`](source-configuration-options.md#option_cmake_with_ant)

  Set the path to Ant, required when building GCS Java
  wrapper. Set [`WITH_ANT`](source-configuration-options.md#option_cmake_with_ant) to the
  path of a directory where the Ant tarball or unpacked
  archive is saved. When
  [`WITH_ANT`](source-configuration-options.md#option_cmake_with_ant) is not set, or is set
  with the special value `system`, the build
  process assumes a binary `ant` exists in
  `$PATH`.
- [`-DWITH_ASAN=bool`](source-configuration-options.md#option_cmake_with_asan)

  Whether to enable the AddressSanitizer, for compilers that
  support it. The default is `OFF`.
- [`-DWITH_ASAN_SCOPE=bool`](source-configuration-options.md#option_cmake_with_asan_scope)

  Whether to enable the AddressSanitizer
  `-fsanitize-address-use-after-scope` Clang
  flag for use-after-scope detection. The default is off. To
  use this option, `-DWITH_ASAN`
  must also be enabled.
- [`-DWITH_AUTHENTICATION_CLIENT_PLUGINS=bool`](source-configuration-options.md#option_cmake_with_authentication_client_plugins)

  This option is enabled automatically if any corresponding
  server authentication plugins are built. Its value thus
  depends on other **CMake** options and it
  should not be set explicitly.

  This option was added in MySQL 8.0.26.
- [`-DWITH_AUTHENTICATION_LDAP=bool`](source-configuration-options.md#option_cmake_with_authentication_ldap)

  Whether to report an error if the LDAP authentication
  plugins cannot be built:

  - If this option is disabled (the default), the LDAP
    plugins are built if the required header files and
    libraries are found. If they are not,
    **CMake** displays a note about it.
  - If this option is enabled, a failure to find the
    required header file and libraries causes CMake to
    produce an error, preventing the server from being
    built.

  For information about LDAP authentication, see
  [Section 8.4.1.7, “LDAP Pluggable Authentication”](ldap-pluggable-authentication.md "8.4.1.7 LDAP Pluggable Authentication").
- [`-DWITH_AUTHENTICATION_PAM=bool`](source-configuration-options.md#option_cmake_with_authentication_pam)

  Whether to build the PAM authentication plugin, for source
  trees that include this plugin. (See
  [Section 8.4.1.5, “PAM Pluggable Authentication”](pam-pluggable-authentication.md "8.4.1.5 PAM Pluggable Authentication").) If this
  option is specified and the plugin cannot be compiled, the
  build fails.
- [`-DWITH_AWS_SDK=path_name`](source-configuration-options.md#option_cmake_with_aws_sdk)

  The location of the Amazon Web Services software development
  kit.
- [`-DWITH_BOOST=path_name`](source-configuration-options.md#option_cmake_with_boost)

  The Boost library is required to build MySQL. These
  **CMake** options enable control over the
  library source location, and whether to download it
  automatically:

  - [`-DWITH_BOOST=path_name`](source-configuration-options.md#option_cmake_with_boost)
    specifies the Boost library directory location. It is
    also possible to specify the Boost location by setting
    the `BOOST_ROOT` or
    `WITH_BOOST` environment variable.

    [`-DWITH_BOOST=system`](source-configuration-options.md#option_cmake_with_boost) is
    also permitted and indicates that the correct version of
    Boost is installed on the compilation host in the
    standard location. In this case, the installed version
    of Boost is used rather than any version included with a
    MySQL source distribution.
  - [`-DDOWNLOAD_BOOST=bool`](source-configuration-options.md#option_cmake_download_boost)
    specifies whether to download the Boost source if it is
    not present in the specified location. The default is
    `OFF`.
  - [`-DDOWNLOAD_BOOST_TIMEOUT=seconds`](source-configuration-options.md#option_cmake_download_boost_timeout)
    the timeout in seconds for downloading the Boost
    library. The default is 600 seconds.

  For example, if you normally build MySQL placing the object
  output in the `bld` subdirectory of your
  MySQL source tree, you can build with Boost like this:

  ```terminal
  mkdir bld
  cd bld
  cmake .. -DDOWNLOAD_BOOST=ON -DWITH_BOOST=$HOME/my_boost
  ```

  This causes Boost to be downloaded into the
  `my_boost` directory under your home
  directory. If the required Boost version is already there,
  no download is done. If the required Boost version changes,
  the newer version is downloaded.

  If Boost is already installed locally and your compiler
  finds the Boost header files on its own, it may not be
  necessary to specify the preceding **CMake**
  options. However, if the version of Boost required by MySQL
  changes and the locally installed version has not been
  upgraded, you may have build problems. Using the
  **CMake** options should give you a
  successful build.

  With the above settings that allow Boost download into a
  specified location, when the required Boost version changes,
  you need to remove the `bld` folder,
  recreate it, and perform the **cmake** step
  again. Otherwise, the new Boost version might not get
  downloaded, and compilation might fail.
- [`-DWITH_CLIENT_PROTOCOL_TRACING=bool`](source-configuration-options.md#option_cmake_with_client_protocol_tracing)

  Whether to build the client-side protocol tracing framework
  into the client library. By default, this option is enabled.

  For information about writing protocol trace client plugins,
  see [Writing Protocol Trace Plugins](https://dev.mysql.com/doc/extending-mysql/8.0/en/writing-protocol-trace-plugins.html).

  See also the
  [`WITH_TEST_TRACE_PLUGIN`](source-configuration-options.md#option_cmake_with_test_trace_plugin) option.
- [`-DWITH_CURL=curl_type`](source-configuration-options.md#option_cmake_with_curl)

  The location of the `curl` library.
  *`curl_type`* can be
  `system` (use the system
  `curl` library) or a path name to the
  `curl` library.
- [`-DWITH_DEBUG=bool`](source-configuration-options.md#option_cmake_with_debug)

  Whether to include debugging support.

  Configuring MySQL with debugging support enables you to use
  the [`--debug="d,parser_debug"`](server-options.md#option_mysqld_debug)
  option when you start the server. This causes the Bison
  parser that is used to process SQL statements to dump a
  parser trace to the server's standard error output.
  Typically, this output is written to the error log.

  Sync debug checking for the `InnoDB`
  storage engine is defined under
  `UNIV_DEBUG` and is available when
  debugging support is compiled in using the
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug) option. When
  debugging support is compiled in, the
  [`innodb_sync_debug`](innodb-parameters.md#sysvar_innodb_sync_debug)
  configuration option can be used to enable or disable
  `InnoDB` sync debug checking.

  Enabling [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug) also
  enables Debug Sync. This facility is used for testing and
  debugging. When compiled in, Debug Sync is disabled by
  default at runtime. To enable it, start
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server") with the
  [`--debug-sync-timeout=N`](server-options.md#option_mysqld_debug-sync-timeout)
  option, where *`N`* is a timeout
  value greater than 0. (The default value is 0, which
  disables Debug Sync.) *`N`* becomes
  the default timeout for individual synchronization points.

  Sync debug checking for the `InnoDB`
  storage engine is available when debugging support is
  compiled in using the
  [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug) option.

  For a description of the Debug Sync facility and how to use
  synchronization points, see
  [MySQL
  Internals: Test Synchronization](https://dev.mysql.com/doc/internals/en/test-synchronization.html).
- [`-DWITH_DEFAULT_FEATURE_SET=bool`](source-configuration-options.md#option_cmake_with_default_feature_set)

  Whether to use the flags from
  `cmake/build_configurations/feature_set.cmake`.
  This option was removed in MySQL 8.0.22.
- [`-DWITH_EDITLINE=value`](source-configuration-options.md#option_cmake_with_editline)

  Which `libedit`/`editline`
  library to use. The permitted values are
  `bundled` (the default) and
  `system`.
- [`-DWITH_FIDO=fido_type`](source-configuration-options.md#option_cmake_with_fido)

  The `authentication_fido` authentication
  plugin is implemented using a FIDO library (see
  [Section 8.4.1.11, “FIDO Pluggable Authentication”](fido-pluggable-authentication.md "8.4.1.11 FIDO Pluggable Authentication")). The
  [`WITH_FIDO`](source-configuration-options.md#option_cmake_with_fido) option indicates the
  source of FIDO support:

  - `bundled`: Use the FIDO library bundled
    with the distribution. This is the default.

    As of MySQL 8.0.30, MySQL includes
    `fido2` version 1.8.0. (Prior releases
    used `fido2` 1.5.0).
  - `system`: Use the system FIDO library.

  [`WITH_FIDO`](source-configuration-options.md#option_cmake_with_fido) is disabled (set to
  `none`) if all authentication plugins are
  disabled.

  This option was added in MySQL 8.0.27.
- [`-DWITH_GMOCK=path_name`](source-configuration-options.md#option_cmake_with_gmock)

  The path to the googlemock distribution, for use with Google
  Test-based unit tests. The option value is the path to the
  distribution zip file. Alternatively, set the
  `WITH_GMOCK` environment variable to the
  path name. It is also possible to use
  `-DENABLE_DOWNLOADS=1`, so that CMake
  downloads the distribution from GitHub.

  If you build MySQL without the Google Test unit tests (by
  configuring without
  [`WITH_GMOCK`](source-configuration-options.md#option_cmake_with_gmock)), CMake displays a
  message indicating how to download it.

  As of MySQL 8.0.26, MySQL source distributions bundle the
  Google Test source code. Consequently, as of that version,
  the [`WITH_GMOCK`](source-configuration-options.md#option_cmake_with_gmock) and
  [`ENABLE_DOWNLOADS`](source-configuration-options.md#option_cmake_enable_downloads) CMake options
  are removed and are ignored if specified.
- [`-DWITH_ICU={icu_type|path_name}`](source-configuration-options.md#option_cmake_with_icu)

  MySQL uses International Components for Unicode (ICU) to
  support regular expression operations. The
  `WITH_ICU` option indicates the type of ICU
  support to include or the path name to the ICU installation
  to use.

  - *`icu_type`* can be one of the
    following values:

    - `bundled`: Use the ICU library
      bundled with the distribution. This is the default,
      and is the only supported option for Windows.
    - `system`: Use the system ICU
      library.
  - *`path_name`* is the path name to
    the ICU installation to use. This can be preferable to
    using the *`icu_type`* value of
    `system` because it can prevent CMake
    from detecting and using an older or incorrect ICU
    version installed on the system. (Another permitted way
    to do the same thing is to set `WITH_ICU`
    to `system` and set the
    `CMAKE_PREFIX_PATH` option to
    *`path_name`*.)
- [`-DWITH_INNODB_EXTRA_DEBUG=bool`](source-configuration-options.md#option_cmake_with_innodb_extra_debug)

  Whether to include extra InnoDB debugging support.

  Enabling `WITH_INNODB_EXTRA_DEBUG` turns on
  extra InnoDB debug checks. This option can only be enabled
  when [`WITH_DEBUG`](source-configuration-options.md#option_cmake_with_debug) is enabled.
- [`-DWITH_INNODB_MEMCACHED=bool`](source-configuration-options.md#option_cmake_with_innodb_memcached)

  Whether to generate memcached shared libraries
  (`libmemcached.so` and
  `innodb_engine.so`).
- [`-DWITH_JEMALLOC=bool`](source-configuration-options.md#option_cmake_with_jemalloc)

  Whether to link with `-ljemalloc`. If
  enabled, built-in `malloc()`,
  `calloc()`, `realloc()`,
  and `free()` routines are disabled. The
  default is `OFF`.

  [`WITH_JEMALLOC`](source-configuration-options.md#option_cmake_with_jemalloc) and
  [`WITH_TCMALLOC`](source-configuration-options.md#option_cmake_with_tcmalloc) are mutually
  exclusive.

  This option was added in MySQL 8.0.16.
- [`-DWITH_KEYRING_TEST=bool`](source-configuration-options.md#option_cmake_with_keyring_test)

  Whether to build the test program that accompanies the
  `keyring_file` plugin. The default is
  `OFF`. Test file source code is located in
  the `plugin/keyring/keyring-test`
  directory.
- [`-DWITH_LIBEVENT=string`](source-configuration-options.md#option_cmake_with_libevent)

  Which `libevent` library to use. Permitted
  values are `bundled` (default) and
  `system`. Prior to MySQL 8.0.21, if you
  specify `system`, the system
  `libevent` library is used if present, and
  an error occurs otherwise. In MySQL 8.0.21 and later, if
  `system` is specified and no system
  `libevent` library can be found, an error
  occurs regardless, and the bundled
  `libevent` is not used.

  The `libevent` library is required by
  `InnoDB` memcached, X Plugin, and
  MySQL Router.
- [`-DWITH_LIBWRAP=bool`](source-configuration-options.md#option_cmake_with_libwrap)

  Whether to include `libwrap` (TCP wrappers)
  support.
- [`-DWITH_LOCK_ORDER=bool`](source-configuration-options.md#option_cmake_with_lock_order)

  Whether to enable LOCK\_ORDER tooling. By default, this
  option is disabled and server builds contain no tooling. If
  tooling is enabled, the LOCK\_ORDER tool is available and can
  be used as described in [Section 7.9.3, “The LOCK\_ORDER Tool”](lock-order-tool.md "7.9.3 The LOCK_ORDER Tool").

  Note

  With the [`WITH_LOCK_ORDER`](source-configuration-options.md#option_cmake_with_lock_order)
  option enabled, MySQL builds require the
  **flex** program.

  This option was added in MySQL 8.0.17.
- [`-DWITH_LSAN=bool`](source-configuration-options.md#option_cmake_with_lsan)

  Whether to run LeakSanitizer, without AddressSanitizer. The
  default is `OFF`.

  This option was added in MySQL 8.0.16.
- [`-DWITH_LTO=bool`](source-configuration-options.md#option_cmake_with_lto)

  Whether to enable the link-time optimizer, if the compiler
  supports it. The default is `OFF` unless
  [`FPROFILE_USE`](source-configuration-options.md#option_cmake_fprofile_use) is enabled.

  This option was added in MySQL 8.0.13.
- [`-DWITH_LZ4=lz4_type`](source-configuration-options.md#option_cmake_with_lz4)

  The [`WITH_LZ4`](source-configuration-options.md#option_cmake_with_lz4) option indicates
  the source of `zlib` support:

  - `bundled`: Use the
    `lz4` library bundled with the
    distribution. This is the default.
  - `system`: Use the system
    `lz4` library. If
    [`WITH_LZ4`](source-configuration-options.md#option_cmake_with_lz4) is set to this
    value, the [**lz4\_decompress**](lz4-decompress.md "6.8.1 lz4_decompress — Decompress mysqlpump LZ4-Compressed Output") utility is
    not built. In this case, the system
    **lz4** command can be used instead.
- [`-DWITH_LZMA=lzma_type`](source-configuration-options.md#option_cmake_with_lzma)

  The type of LZMA library support to include.
  *`lzma_type`* can be one of the
  following values:

  - `bundled`: Use the LZMA library bundled
    with the distribution. This is the default.
  - `system`: Use the system LZMA library.

  This option was removed in MySQL 8.0.16.
- [`-DWITH_MECAB={disabled|system|path_name}`](source-configuration-options.md#option_cmake_with_mecab)

  Use this option to compile the MeCab parser. If you have
  installed MeCab to its default installation directory, set
  `-DWITH_MECAB=system`. The
  `system` option applies to MeCab
  installations performed from source or from binaries using a
  native package management utility. If you installed MeCab to
  a custom installation directory, specify the path to the
  MeCab installation, for example,
  `-DWITH_MECAB=/opt/mecab`. If the
  `system` option does not work, specifying
  the MeCab installation path should work in all cases.

  For related information, see
  [Section 14.9.9, “MeCab Full-Text Parser Plugin”](fulltext-search-mecab.md "14.9.9 MeCab Full-Text Parser Plugin").
- [`-DWITH_MSAN=bool`](source-configuration-options.md#option_cmake_with_msan)

  Whether to enable MemorySanitizer, for compilers that
  support it. The default is off.

  For this option to have an effect if enabled, all libraries
  linked to MySQL must also have been compiled with the option
  enabled.
- [`-DWITH_MSCRT_DEBUG=bool`](source-configuration-options.md#option_cmake_with_mscrt_debug)

  Whether to enable Visual Studio CRT memory leak tracing. The
  default is `OFF`.
- [`-DMSVC_CPPCHECK=bool`](source-configuration-options.md#option_cmake_msvc_cppcheck)

  Whether to enable MSVC code analysis. The default is
  `OFF`.
- [`-DWITH_MYSQLX=bool`](source-configuration-options.md#option_cmake_with_mysqlx)

  Whether to build with support for X Plugin. The default is
  `ON`. See [Chapter 22, *Using MySQL as a Document Store*](document-store.md "Chapter 22 Using MySQL as a Document Store").
- [`-DWITH_NUMA=bool`](source-configuration-options.md#option_cmake_with_numa)

  Explicitly set the NUMA memory allocation policy.
  **CMake** sets the default
  [`WITH_NUMA`](source-configuration-options.md#option_cmake_with_numa) value based on
  whether the current platform has `NUMA`
  support. For platforms without NUMA support,
  **CMake** behaves as follows:

  - With no NUMA option (the normal case),
    **CMake** continues normally, producing
    only this warning: NUMA library missing or
    required version not available.
  - With [`-DWITH_NUMA=ON`](source-configuration-options.md#option_cmake_with_numa),
    **CMake** aborts with this error:
    NUMA library missing or required version not
    available.
- [`-DWITH_PACKAGE_FLAGS=bool`](source-configuration-options.md#option_cmake_with_package_flags)

  For flags typically used for RPM and Debian packages,
  whether to add them to standalone builds on those platforms.
  The default is `ON` for nondebug builds.

  This option was added in MySQL 8.0.26.
- [`-DWITH_PROTOBUF=protobuf_type`](source-configuration-options.md#option_cmake_with_protobuf)

  Which Protocol Buffers package to use.
  *`protobuf_type`* can be one of the
  following values:

  - `bundled`: Use the package bundled with
    the distribution. This is the default. Optionally use
    [`INSTALL_PRIV_LIBDIR`](source-configuration-options.md#option_cmake_install_priv_libdir) to
    modify the dynamic Protobuf library directory.
  - `system`: Use the package installed on
    the system.

  Other values are ignored, with a fallback to
  `bundled`.
- [`-DWITH_RAPID=bool`](source-configuration-options.md#option_cmake_with_rapid)

  Whether to build the rapid development cycle plugins. When
  enabled, a `rapid` directory is created
  in the build tree containing these plugins. When disabled,
  no `rapid` directory is created in the
  build tree. The default is `ON`, unless the
  `rapid` directory is removed from the
  source tree, in which case the default becomes
  `OFF`.
- [`-DWITH_RAPIDJSON=rapidjson_type`](source-configuration-options.md#option_cmake_with_rapidjson)

  The type of RapidJSON library support to include.
  *`rapidjson_type`* can be one of the
  following values:

  - `bundled`: Use the RapidJSON library
    bundled with the distribution. This is the default.
  - `system`: Use the system RapidJSON
    library. Version 1.1.0 or later is required.

  This option was added in MySQL 8.0.13.
- [`-DWITH_RE2=re2_type`](source-configuration-options.md#option_cmake_with_re2)

  The type of RE2 library support to include.
  *`re2_type`* can be one of the
  following values:

  - `bundled`: Use the RE2 library bundled
    with the distribution. This is the default.
  - `system`: Use the system RE2 library.

  As of MySQL 8.0.18, MySQL no longer uses the RE2 library,
  and this option has been removed.
- [`-DWITH_ROUTER=bool`](source-configuration-options.md#option_cmake_with_router)

  Whether to build MySQL Router. The default is
  `ON`.

  This option was added in MySQL 8.0.16.
- [`-DWITH_SASL=value`](source-configuration-options.md#option_cmake_with_sasl)

  Internal use only. This option was added in 8.0.20. Not
  supported on Windows.
- [`-DWITH_SSL={ssl_type`](source-configuration-options.md#option_cmake_with_ssl)|*`path_name`*}

  For support of encrypted connections, entropy for random
  number generation, and other encryption-related operations,
  MySQL must be built using an SSL library. This option
  specifies which SSL library to use.

  - *`ssl_type`* can be one of the
    following values:

    - `system`: Use the system OpenSSL
      library. This is the default.

      On macOS and Windows, using
      `system` configures MySQL to build
      as if CMake was invoked with
      *`path_name`* points to a
      manually installed OpenSSL library. This is because
      they do not have system SSL libraries. On macOS,
      *brew install openssl* installs
      to `/usr/local/opt/openssl` so
      that `system` can find it. On
      Windows, it checks
      `%ProgramFiles%/OpenSSL`,
      `%ProgramFiles%/OpenSSL-Win32`,
      `%ProgramFiles%/OpenSSL-Win64`,
      `C:/OpenSSL`,
      `C:/OpenSSL-Win32`, and
      `C:/OpenSSL-Win64`.
    - `yes`: This is a synonym for
      `system`.
    - `opensslversion`:
      (*MySQL 8.0.30 and later:*) Use
      an alternate OpenSSL system package such as
      `openssl11` on EL7, or
      `openssl3` on EL8.

      Authentication plugins, such as LDAP and Kerberos,
      are disabled as they do not support these
      alternative versions of OpenSSL.
  - *`path_name`* is the path name to
    the OpenSSL installation to use. This can be preferable
    to using the *`ssl_type`* value
    of `system` because it can prevent
    CMake from detecting and using an older or incorrect
    OpenSSL version installed on the system. (Another
    permitted way to do the same thing is to set
    `WITH_SSL` to `system`
    and set the `CMAKE_PREFIX_PATH` option to
    *`path_name`*.)

  For additional information about configuring the SSL
  library, see
  [Section 2.8.6, “Configuring SSL Library Support”](source-ssl-library-configuration.md "2.8.6 Configuring SSL Library Support").
- [`-DWITH_SYSTEMD=bool`](source-configuration-options.md#option_cmake_with_systemd)

  Whether to enable installation of **systemd**
  support files. By default, this option is disabled. When
  enabled, **systemd** support files are
  installed, and scripts such as
  [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") and the System V
  initialization script are not installed. On platforms where
  **systemd** is not available, enabling
  [`WITH_SYSTEMD`](source-configuration-options.md#option_cmake_with_systemd) results in an
  error from **CMake**.

  For more information about using **systemd**,
  see [Section 2.5.9, “Managing MySQL Server with systemd”](using-systemd.md "2.5.9 Managing MySQL Server with systemd"). That section also
  includes information about specifying options otherwise
  specified in `[mysqld_safe]` option groups.
  Because [**mysqld\_safe**](mysqld-safe.md "6.3.2 mysqld_safe — MySQL Server Startup Script") is not installed when
  **systemd** is used, such options must be
  specified another way.
- [`-DWITH_SYSTEM_LIBS=bool`](source-configuration-options.md#option_cmake_with_system_libs)

  This option serves as an “umbrella” option to
  set the `system` value of any of the
  following **CMake** options that are not set
  explicitly: [`WITH_CURL`](source-configuration-options.md#option_cmake_with_curl),
  [`WITH_EDITLINE`](source-configuration-options.md#option_cmake_with_editline),
  [`WITH_FIDO`](source-configuration-options.md#option_cmake_with_fido),
  [`WITH_ICU`](source-configuration-options.md#option_cmake_with_icu),
  [`WITH_LIBEVENT`](source-configuration-options.md#option_cmake_with_libevent),
  [`WITH_LZ4`](source-configuration-options.md#option_cmake_with_lz4),
  [`WITH_LZMA`](source-configuration-options.md#option_cmake_with_lzma),
  [`WITH_PROTOBUF`](source-configuration-options.md#option_cmake_with_protobuf),
  [`WITH_RE2`](source-configuration-options.md#option_cmake_with_re2),
  [`WITH_SSL`](source-configuration-options.md#option_cmake_with_ssl),
  [`WITH_ZSTD`](source-configuration-options.md#option_cmake_with_zstd).

  [`WITH_ZLIB`](source-configuration-options.md#option_cmake_with_zlib) was included here
  priot MySQL 8.0.30.
- [`-DWITH_SYSTEMD_DEBUG=bool`](source-configuration-options.md#option_cmake_with_systemd_debug)

  Whether to produce additional **systemd**
  debugging information, for platforms on which
  **systemd** is used to run MySQL. The default
  is `OFF`.

  This option was added in MySQL 8.0.22.
- [`-DWITH_TCMALLOC=bool`](source-configuration-options.md#option_cmake_with_tcmalloc)

  Whether to link with `-ltcmalloc`. If
  enabled, built-in `malloc()`,
  `calloc()`, `realloc()`,
  and `free()` routines are disabled. The
  default is `OFF`.

  Beginning with MySQL 8.0.38, a `tcmalloc`
  library is included in the source; you can cause the build
  to use the bundled version by setting this option to
  `BUNDLED`. `BUNDLED` is
  supported on Linux systems only.

  [`WITH_TCMALLOC`](source-configuration-options.md#option_cmake_with_tcmalloc) and
  [`WITH_JEMALLOC`](source-configuration-options.md#option_cmake_with_jemalloc) are mutually
  exclusive.

  This option was added in MySQL 8.0.22.
- [`-DWITH_TEST_TRACE_PLUGIN=bool`](source-configuration-options.md#option_cmake_with_test_trace_plugin)

  Whether to build the test protocol trace client plugin (see
  [Using the Test Protocol Trace Plugin](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.html)). By default,
  this option is disabled. Enabling this option has no effect
  unless the
  [`WITH_CLIENT_PROTOCOL_TRACING`](source-configuration-options.md#option_cmake_with_client_protocol_tracing)
  option is enabled. If MySQL is configured with both options
  enabled, the `libmysqlclient` client
  library is built with the test protocol trace plugin built
  in, and all the standard MySQL clients load the plugin.
  However, even when the test plugin is enabled, it has no
  effect by default. Control over the plugin is afforded using
  environment variables; see
  [Using the Test Protocol Trace Plugin](https://dev.mysql.com/doc/extending-mysql/8.0/en/test-protocol-trace-plugin.html).

  Note

  Do *not* enable the
  [`WITH_TEST_TRACE_PLUGIN`](source-configuration-options.md#option_cmake_with_test_trace_plugin)
  option if you want to use your own protocol trace plugins
  because only one such plugin can be loaded at a time and
  an error occurs for attempts to load a second one. If you
  have already built MySQL with the test protocol trace
  plugin enabled to see how it works, you must rebuild MySQL
  without it before you can use your own plugins.

  For information about writing trace plugins, see
  [Writing Protocol Trace Plugins](https://dev.mysql.com/doc/extending-mysql/8.0/en/writing-protocol-trace-plugins.html).
- [`-DWITH_TSAN=bool`](source-configuration-options.md#option_cmake_with_tsan)

  Whether to enable the ThreadSanitizer, for compilers that
  support it. The default is off.
- [`-DWITH_UBSAN=bool`](source-configuration-options.md#option_cmake_with_ubsan)

  Whether to enable the Undefined Behavior Sanitizer, for
  compilers that support it. The default is off.
- [`-DWITH_UNIT_TESTS={ON|OFF}`](source-configuration-options.md#option_cmake_with_unit_tests)

  If enabled, compile MySQL with unit tests. The default is
  `ON` unless the server is not being
  compiled.
- [`-DWITH_UNIXODBC=1`](source-configuration-options.md#option_cmake_with_unixodbc)

  Enables unixODBC support, for Connector/ODBC.
- [`-DWITH_VALGRIND=bool`](source-configuration-options.md#option_cmake_with_valgrind)

  Whether to compile in the Valgrind header files, which
  exposes the Valgrind API to MySQL code. The default is
  `OFF`.

  To generate a Valgrind-aware debug build,
  [`-DWITH_VALGRIND=1`](source-configuration-options.md#option_cmake_with_valgrind) normally is
  combined with [`-DWITH_DEBUG=1`](source-configuration-options.md#option_cmake_with_debug).
  See
  [Building
  Debug Configurations](https://dev.mysql.com/doc/internals/en/debug-configurations.html).
- [`-DWITH_WIN_JEMALLOC=string`](source-configuration-options.md#option_cmake_with_win_jemalloc)

  On Windows, pass in a path to a directory containing
  `jemalloc.dll` to enable jemalloc
  functionality. The build system copies
  `jemalloc.dll` to the same directory as
  `mysqld.exe` and/or
  `mysqld-debug.exe` and utilizes it for
  memory management operations. Standard memory functions are
  used if `jemalloc.dll` is not found or
  does not export the required functions. An INFORMATION level
  log message records whether or not jemalloc is found and
  used.

  This option is enabled for official MySQL binaries for
  Windows.

  This option was added in MySQL 8.0.29.
- [`-DWITH_ZLIB=zlib_type`](source-configuration-options.md#option_cmake_with_zlib)

  Some features require that the server be built with
  compression library support, such as the
  [`COMPRESS()`](encryption-functions.md#function_compress) and
  [`UNCOMPRESS()`](encryption-functions.md#function_uncompress) functions, and
  compression of the client/server protocol. The
  [`WITH_ZLIB`](source-configuration-options.md#option_cmake_with_zlib) option indicates the
  source of `zlib` support:

  In MYSQL 8.0.32 and later, the minimum supported version of
  `zlib` is 1.2.13.

  - `bundled`: Use the
    `zlib` library bundled with the
    distribution. This is the default.
  - `system`: Use the system
    `zlib` library. If
    [`WITH_ZLIB`](source-configuration-options.md#option_cmake_with_zlib) is set to this
    value, the [**zlib\_decompress**](zlib-decompress.md "6.8.3 zlib_decompress — Decompress mysqlpump ZLIB-Compressed Output") utility is
    not built. In this case, the system **openssl
    zlib** command can be used instead.
- [`-DWITH_ZSTD=zstd_type`](source-configuration-options.md#option_cmake_with_zstd)

  Connection compression using the `zstd`
  algorithm (see
  [Section 6.2.8, “Connection Compression Control”](connection-compression-control.md "6.2.8 Connection Compression Control")) requires
  that the server be built with `zstd`
  library support. The [`WITH_ZSTD`](source-configuration-options.md#option_cmake_with_zstd)
  option indicates the source of `zstd`
  support:

  - `bundled`: Use the
    `zstd` library bundled with the
    distribution. This is the default.
  - `system`: Use the system
    `zstd` library.

  This option was added in MySQL 8.0.18.
- [`-DWITHOUT_SERVER=bool`](source-configuration-options.md#option_cmake_without_server)

  Whether to build without MySQL Server. The default is OFF,
  which does build the server.

  This is considered an experimental option; it is preferred
  to build with the server.

  This option also prevents building of the
  [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine or any
  `NDB` binaries including management and
  data node programs.

#### Compiler Flags

- [`-DCMAKE_C_FLAGS="flags`](source-configuration-options.md#option_cmake_cmake_c_flags)"

  Flags for the C compiler.
- [`-DCMAKE_CXX_FLAGS="flags`](source-configuration-options.md#option_cmake_cmake_cxx_flags)"

  Flags for the C++ compiler.
- [`-DWITH_DEFAULT_COMPILER_OPTIONS=bool`](source-configuration-options.md#option_cmake_with_default_compiler_options)

  Whether to use the flags from
  `cmake/build_configurations/compiler_options.cmake`.

  Note

  All optimization flags are carefully chosen and tested by
  the MySQL build team. Overriding them can lead to
  unexpected results and is done at your own risk.
- [`-DOPTIMIZE_SANITIZER_BUILDS=bool`](source-configuration-options.md#option_cmake_optimize_sanitizer_builds)

  Whether to add `-O1 -fno-inline` to sanitizer
  builds. The default is `ON`.

To specify your own C and C++ compiler flags, for flags that do
not affect optimization, use the
[`CMAKE_C_FLAGS`](source-configuration-options.md#option_cmake_cmake_c_flags) and
[`CMAKE_CXX_FLAGS`](source-configuration-options.md#option_cmake_cmake_cxx_flags) CMake options.

When providing your own compiler flags, you might want to
specify [`CMAKE_BUILD_TYPE`](source-configuration-options.md#option_cmake_cmake_build_type) as well.

For example, to create a 32-bit release build on a 64-bit Linux
machine, do this:

```terminal
$> mkdir build
$> cd build
$> cmake .. -DCMAKE_C_FLAGS=-m32 \
  -DCMAKE_CXX_FLAGS=-m32 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo
```

If you set flags that affect optimization
(`-Onumber`), you must
set the
`CMAKE_C_FLAGS_build_type`
and/or
`CMAKE_CXX_FLAGS_build_type`
options, where *`build_type`* corresponds
to the [`CMAKE_BUILD_TYPE`](source-configuration-options.md#option_cmake_cmake_build_type) value. To
specify a different optimization for the default build type
(`RelWithDebInfo`) set the
`CMAKE_C_FLAGS_RELWITHDEBINFO` and
`CMAKE_CXX_FLAGS_RELWITHDEBINFO` options. For
example, to compile on Linux with `-O3` and with
debug symbols, do this:

```terminal
$> cmake .. -DCMAKE_C_FLAGS_RELWITHDEBINFO="-O3 -g" \
  -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-O3 -g"
```

#### CMake Options for Compiling NDB Cluster

To compile with support for NDB Cluster, you can use
[`-DWITH_NDB`](source-configuration-options.md#option_cmake_with_ndb), which causes the build
to include the NDB storage engine and all NDB programs. This
option is enabled by default. To prevent building of the NDB
storage engine plugin, use
[`-DWITH_NDBCLUSTER_STORAGE_ENGINE=OFF`](source-configuration-options.md#option_cmake_with_ndbcluster_storage_engine).
Other aspects of the build can be controlled using the other
options listed in this section.

The following options apply when building the MySQL sources with
NDB Cluster support.

- [`-DMEMCACHED_HOME=dir_name`](source-configuration-options.md#option_cmake_memcached_home)

  `NDB` support for memcached was removed in
  NDB 8.0.23; thus, this option is no longer supported for
  building `NDB` in this or later versions.
- [`-DNDB_UTILS_LINK_DYNAMIC={ON|OFF}`](source-configuration-options.md#option_cmake_ndb_utils_link_dynamic)

  Controls whether NDB utilities such as
  [**ndb\_drop\_table**](mysql-cluster-programs-ndb-drop-table.md "25.5.11 ndb_drop_table — Drop an NDB Table") are linked with
  `ndbclient` statically
  (`OFF`) or dynamically
  (`ON`); `OFF` (static
  linking) is the default. Normally static linking is used
  when building these to avoid problems with
  `LD_LIBRARY_PATH`, or when multiple
  versions of `ndbclient` are installed. This
  option is intended for creating Docker images and possibly
  other cases in which the target environment is subject to
  precise control and it is desirable to reduce image size.

  Added in NDB 8.0.22.
- [`-DWITH_BUNDLED_LIBEVENT={ON|OFF}`](source-configuration-options.md#option_cmake_with_bundled_libevent)

  `NDB` support for memcached was removed in
  NDB 8.0.23; thus, this option is no longer supported for
  building `NDB` in this or later versions.
- [`-DWITH_BUNDLED_MEMCACHED={ON|OFF}`](source-configuration-options.md#option_cmake_with_bundled_memcached)

  `NDB` support for memcached was removed in
  NDB 8.0.23; thus, this option is no longer supported for
  building `NDB` in this or later versions.
- [`-DWITH_CLASSPATH=path`](source-configuration-options.md#option_cmake_with_classpath)

  Sets the classpath for building MySQL NDB Cluster Connector for Java. The default is
  empty. This option is ignored if
  [`-DWITH_NDB_JAVA=OFF`](source-configuration-options.md#option_cmake_with_ndb_java) is used.
- [`-DWITH_ERROR_INSERT={ON|OFF}`](source-configuration-options.md#option_cmake_with_error_insert)

  Enables error injection in the
  [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") kernel. For testing only;
  not intended for use in building production binaries. The
  default is `OFF`.
- [`-DWITH_NDB={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndb)

  Build MySQL NDB Cluster; build the NDB plugin and all NDB
  Cluster programs.

  Added in NDB 8.0.31.
- [`-DWITH_NDBAPI_EXAMPLES={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndbapi_examples)

  Build NDB API example programs in
  `storage/ndb/ndbapi-examples/`. See
  [NDB API Examples](https://dev.mysql.com/doc/ndbapi/en/ndb-examples.html), for information about these.
- [`-DWITH_NDBCLUSTER_STORAGE_ENGINE={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndbcluster_storage_engine)

  *NDB 8.0.30 and earlier*: For internal
  use only; may not always work as expected. To build with
  `NDB` support, use
  [`WITH_NDBCLUSTER`](source-configuration-options.md#option_cmake_with_ndbcluster) instead.

  *NDB 8.0.31 and later*: Controls (only)
  whether the `NDBCLUSTER` storage engine is
  included in the build;
  [`WITH_NDB`](source-configuration-options.md#option_cmake_with_ndb) enables this option
  automatically, so it is recommended that you use
  `WITH_NDB` instead.
- [`-DWITH_NDBCLUSTER={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndbcluster)
  (DEPRECATED)

  Build and link in support for the
  [`NDB`](mysql-cluster.md "Chapter 25 MySQL NDB Cluster 8.0") storage engine in
  [**mysqld**](mysqld.md "6.3.1 mysqld — The MySQL Server").

  This option is deprecated as of NDB 8.0.31, and subject to
  eventual removal; use [`WITH_NDB`](source-configuration-options.md#option_cmake_with_ndb)
  instead.
- [`-DWITH_NDBMTD={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndbmtd)

  Build the multithreaded data node executable
  [**ndbmtd**](mysql-cluster-programs-ndbmtd.md "25.5.3 ndbmtd — The NDB Cluster Data Node Daemon (Multi-Threaded)"). The default is
  `ON`.
- [`-DWITH_NDB_DEBUG={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndb_debug)

  Enable building the debug versions of the NDB Cluster
  binaries. This is `OFF` by default.
- [`-DWITH_NDB_JAVA={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndb_java)

  Enable building NDB Cluster with Java support, including
  support for ClusterJ (see [MySQL NDB Cluster Connector for Java](https://dev.mysql.com/doc/ndbapi/en/mccj.html)).

  This option is `ON` by default. If you do
  not wish to compile NDB Cluster with Java support, you must
  disable it explicitly by specifying
  `-DWITH_NDB_JAVA=OFF` when running
  **CMake**. Otherwise, if Java cannot be
  found, configuration of the build fails.
- [`-DWITH_NDB_PORT=port`](source-configuration-options.md#option_cmake_with_ndb_port)

  Causes the NDB Cluster management server
  ([**ndb\_mgmd**](mysql-cluster-programs-ndb-mgmd.md "25.5.4 ndb_mgmd — The NDB Cluster Management Server Daemon")) that is built to use this
  *`port`* by default. If this option
  is unset, the resulting management server tries to use port
  1186 by default.
- [`-DWITH_NDB_TEST={ON|OFF}`](source-configuration-options.md#option_cmake_with_ndb_test)

  If enabled, include a set of NDB API test programs. The
  default is `OFF`.
- [`-DWITH_PLUGIN_NDBCLUSTER={ON|OFF}`](source-configuration-options.md#option_cmake_with_plugin_ndbcluster)

  For internal use only; may not always work as expected. This
  option was removed in NDB 8.0.31; use
  [`WITH_NDB`](source-configuration-options.md#option_cmake_with_ndb) instead to build
  MySQL NDB Cluster. (*NDB 8.0.30 and
  earlier*: Use
  [`WITH_NDBCLUSTER`](source-configuration-options.md#option_cmake_with_ndbcluster).)
