# Chapter 2 Installing MySQL

**Table of Contents**

[2.1 General Installation Guidance](general-installation-issues.md)
:   [2.1.1 Supported Platforms](platform-support.md)

    [2.1.2 Which MySQL Version and Distribution to Install](which-version.md)

    [2.1.3 How to Get MySQL](getting-mysql.md)

    [2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG](verifying-package-integrity.md)

    [2.1.5 Installation Layouts](installation-layouts.md)

    [2.1.6 Compiler-Specific Build Characteristics](compiler-characteristics.md)

[2.2 Installing MySQL on Unix/Linux Using Generic Binaries](binary-installation.md)

[2.3 Installing MySQL on Microsoft Windows](windows-installation.md)
:   [2.3.1 MySQL Installation Layout on Microsoft Windows](windows-installation-layout.md)

    [2.3.2 Choosing an Installation Package](windows-choosing-package.md)

    [2.3.3 MySQL Installer for Windows](mysql-installer.md)

    [2.3.4 Installing MySQL on Microsoft Windows Using a `noinstall` ZIP Archive](windows-install-archive.md)

    [2.3.5 Troubleshooting a Microsoft Windows MySQL Server Installation](windows-troubleshooting.md)

    [2.3.6 Windows Postinstallation Procedures](windows-postinstallation.md)

    [2.3.7 Windows Platform Restrictions](windows-restrictions.md)

[2.4 Installing MySQL on macOS](macos-installation.md)
:   [2.4.1 General Notes on Installing MySQL on macOS](macos-installation-notes.md)

    [2.4.2 Installing MySQL on macOS Using Native Packages](macos-installation-pkg.md)

    [2.4.3 Installing and Using the MySQL Launch Daemon](macos-installation-launchd.md)

    [2.4.4 Installing and Using the MySQL Preference Pane](macos-installation-prefpane.md)

[2.5 Installing MySQL on Linux](linux-installation.md)
:   [2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository](linux-installation-yum-repo.md)

    [2.5.2 Installing MySQL on Linux Using the MySQL APT Repository](linux-installation-apt-repo.md)

    [2.5.3 Installing MySQL on Linux Using the MySQL SLES Repository](linux-installation-sles-repo.md)

    [2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle](linux-installation-rpm.md)

    [2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle](linux-installation-debian.md)

    [2.5.6 Deploying MySQL on Linux with Docker Containers](linux-installation-docker.md)

    [2.5.7 Installing MySQL on Linux from the Native Software Repositories](linux-installation-native.md)

    [2.5.8 Installing MySQL on Linux with Juju](linux-installation-juju.md)

    [2.5.9 Managing MySQL Server with systemd](using-systemd.md)

[2.6 Installing MySQL Using Unbreakable Linux Network (ULN)](uln-installation.md)

[2.7 Installing MySQL on Solaris](solaris-installation.md)
:   [2.7.1 Installing MySQL on Solaris Using a Solaris PKG](solaris-installation-pkg.md)

[2.8 Installing MySQL from Source](source-installation.md)
:   [2.8.1 Source Installation Methods](source-installation-methods.md)

    [2.8.2 Source Installation Prerequisites](source-installation-prerequisites.md)

    [2.8.3 MySQL Layout for Source Installation](source-installation-layout.md)

    [2.8.4 Installing MySQL Using a Standard Source Distribution](installing-source-distribution.md)

    [2.8.5 Installing MySQL Using a Development Source Tree](installing-development-tree.md)

    [2.8.6 Configuring SSL Library Support](source-ssl-library-configuration.md)

    [2.8.7 MySQL Source-Configuration Options](source-configuration-options.md)

    [2.8.8 Dealing with Problems Compiling MySQL](compilation-problems.md)

    [2.8.9 MySQL Configuration and Third-Party Tools](source-configuration-third-party.md)

    [2.8.10 Generating MySQL Doxygen Documentation Content](source-installation-doxygen.md)

[2.9 Postinstallation Setup and Testing](postinstallation.md)
:   [2.9.1 Initializing the Data Directory](data-directory-initialization.md)

    [2.9.2 Starting the Server](starting-server.md)

    [2.9.3 Testing the Server](testing-server.md)

    [2.9.4 Securing the Initial MySQL Account](default-privileges.md)

    [2.9.5 Starting and Stopping MySQL Automatically](automatic-start.md)

[2.10 Perl Installation Notes](perl-support.md)
:   [2.10.1 Installing Perl on Unix](perl-installation.md)

    [2.10.2 Installing ActiveState Perl on Windows](activestate-perl.md)

    [2.10.3 Problems Using the Perl DBI/DBD Interface](perl-support-problems.md)

This chapter describes how to obtain and install MySQL. A summary of
the procedure follows and later sections provide the details. If you
plan to upgrade an existing version of MySQL to a newer version
rather than install MySQL for the first time, see
[Chapter 3, *Upgrading MySQL*](upgrading.md "Chapter 3 Upgrading MySQL"), for information about upgrade
procedures and about issues that you should consider before
upgrading.

If you are interested in migrating to MySQL from another database
system, see [Section A.8, “MySQL 8.0 FAQ: Migration”](faqs-migration.md "A.8 MySQL 8.0 FAQ: Migration"), which contains answers
to some common questions concerning migration issues.

Installation of MySQL generally follows the steps outlined here:

1. **Determine whether MySQL runs and is
   supported on your platform.**

   Please note that not all platforms are equally suitable for
   running MySQL, and that not all platforms on which MySQL is
   known to run are officially supported by Oracle Corporation. For
   information about those platforms that are officially supported,
   see <https://www.mysql.com/support/supportedplatforms/database.html> on the MySQL
   website.
2. **Choose which distribution to
   install.**

   Several versions of MySQL are available, and most are available
   in several distribution formats. You can choose from
   pre-packaged distributions containing binary (precompiled)
   programs or source code. When in doubt, use a binary
   distribution. Oracle also provides access to the MySQL source
   code for those who want to see recent developments and test new
   code. To determine which version and type of distribution you
   should use, see [Section 2.1.2, “Which MySQL Version and Distribution to Install”](which-version.md "2.1.2 Which MySQL Version and Distribution to Install").
3. **Choose which track to install.**

   MySQL offers a bugfix track (such as MySQL
   8.4), and an innovation track (today it's MySQL
   9.6) and each track addresses different
   use cases. Both tracks are considered production-ready and
   include bug fixes, while innovation releases also include new
   features and potential for modified behavior.

   A bugfix track upgrade includes point releases, such as MySQL
   8.4.*`x`* upgrading to
   8.4.*`y`*, while
   innovation track releases typically only have minor releases,
   such as MySQL 9.6.0 upgrading to
   9.7.0. However, an innovation track does
   have the occasional point release.
4. **Download the distribution that you want to
   install.**

   For instructions, see [Section 2.1.3, “How to Get MySQL”](getting-mysql.md "2.1.3 How to Get MySQL"). To verify
   the integrity of the distribution, use the instructions in
   [Section 2.1.4, “Verifying Package Integrity Using MD5 Checksums or GnuPG”](verifying-package-integrity.md "2.1.4 Verifying Package Integrity Using MD5 Checksums or GnuPG").
5. **Install the distribution.**

   To install MySQL from a binary distribution, use the
   instructions in [Section 2.2, “Installing MySQL on Unix/Linux Using Generic Binaries”](binary-installation.md "2.2 Installing MySQL on Unix/Linux Using Generic Binaries").
   Alternatively, use the
   [Secure
   Deployment Guide](https://dev.mysql.com/doc/mysql-secure-deployment-guide/8.0/en/), which provides procedures for
   deploying a generic binary distribution of MySQL Enterprise Edition Server with
   features for managing the security of your MySQL installation.

   To install MySQL from a source distribution or from the current
   development source tree, use the instructions in
   [Section 2.8, “Installing MySQL from Source”](source-installation.md "2.8 Installing MySQL from Source").
6. **Perform any necessary postinstallation
   setup.**

   After installing MySQL, see [Section 2.9, “Postinstallation Setup and Testing”](postinstallation.md "2.9 Postinstallation Setup and Testing")
   for information about making sure the MySQL server is working
   properly. Also refer to the information provided in
   [Section 2.9.4, “Securing the Initial MySQL Account”](default-privileges.md "2.9.4 Securing the Initial MySQL Account"). This section describes how
   to secure the initial MySQL `root` user
   account, *which has no password* until you
   assign one. The section applies whether you install MySQL using
   a binary or source distribution.
7. If you want to run the MySQL benchmark scripts, Perl support for
   MySQL must be available. See [Section 2.10, “Perl Installation Notes”](perl-support.md "2.10 Perl Installation Notes").

Instructions for installing MySQL on different platforms and
environments is available on a platform by platform basis:

- **Unix, Linux**

  For instructions on installing MySQL on most Linux and Unix
  platforms using a generic binary (for example, a
  `.tar.gz` package), see
  [Section 2.2, “Installing MySQL on Unix/Linux Using Generic Binaries”](binary-installation.md "2.2 Installing MySQL on Unix/Linux Using Generic Binaries").

  For information on building MySQL entirely from the source code
  distributions or the source code repositories, see
  [Section 2.8, “Installing MySQL from Source”](source-installation.md "2.8 Installing MySQL from Source")

  For specific platform help on installation, configuration, and
  building from source see the corresponding platform section:

  - Linux, including notes on distribution specific methods, see
    [Section 2.5, “Installing MySQL on Linux”](linux-installation.md "2.5 Installing MySQL on Linux").
  - IBM AIX, see [Section 2.7, “Installing MySQL on Solaris”](solaris-installation.md "2.7 Installing MySQL on Solaris").
- **Microsoft Windows**

  For instructions on installing MySQL on Microsoft Windows, using
  either the MySQL Installer or Zipped binary, see
  [Section 2.3, “Installing MySQL on Microsoft Windows”](windows-installation.md "2.3 Installing MySQL on Microsoft Windows").

  For details and instructions on building MySQL from source code
  using Microsoft Visual Studio, see
  [Section 2.8, “Installing MySQL from Source”](source-installation.md "2.8 Installing MySQL from Source").
- **macOS**

  For installation on macOS, including using both the binary
  package and native PKG formats, see
  [Section 2.4, “Installing MySQL on macOS”](macos-installation.md "2.4 Installing MySQL on macOS").

  For information on making use of an macOS Launch Daemon to
  automatically start and stop MySQL, see
  [Section 2.4.3, “Installing and Using the MySQL Launch Daemon”](macos-installation-launchd.md "2.4.3 Installing and Using the MySQL Launch Daemon").

  For information on the MySQL Preference Pane, see
  [Section 2.4.4, “Installing and Using the MySQL Preference Pane”](macos-installation-prefpane.md "2.4.4 Installing and Using the MySQL Preference Pane").
