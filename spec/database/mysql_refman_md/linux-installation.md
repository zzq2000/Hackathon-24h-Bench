## 2.5 Installing MySQL on Linux

[2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository](linux-installation-yum-repo.md)

[2.5.2 Installing MySQL on Linux Using the MySQL APT Repository](linux-installation-apt-repo.md)

[2.5.3 Installing MySQL on Linux Using the MySQL SLES Repository](linux-installation-sles-repo.md)

[2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle](linux-installation-rpm.md)

[2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle](linux-installation-debian.md)

[2.5.6 Deploying MySQL on Linux with Docker Containers](linux-installation-docker.md)

[2.5.7 Installing MySQL on Linux from the Native Software Repositories](linux-installation-native.md)

[2.5.8 Installing MySQL on Linux with Juju](linux-installation-juju.md)

[2.5.9 Managing MySQL Server with systemd](using-systemd.md)

Linux supports a number of different solutions for installing MySQL.
We recommend that you use one of the distributions from Oracle, for
which several methods for installation are available:

**Table 2.8 Linux Installation Methods and Information**

| Type | Setup Method | Additional Information |
| --- | --- | --- |
| Apt | Enable the [MySQL Apt repository](https://dev.mysql.com/downloads/repo/apt/) | [Documentation](linux-installation-apt-repo.md "2.5.2 Installing MySQL on Linux Using the MySQL APT Repository") |
| Yum | Enable the [MySQL Yum repository](https://dev.mysql.com/downloads/repo/yum/) | [Documentation](linux-installation-yum-repo.md "2.5.1 Installing MySQL on Linux Using the MySQL Yum Repository") |
| Zypper | Enable the [MySQL SLES repository](https://dev.mysql.com/downloads/repo/suse/) | [Documentation](linux-installation-sles-repo.md "2.5.3 Installing MySQL on Linux Using the MySQL SLES Repository") |
| RPM | [Download](https://dev.mysql.com/downloads/mysql/) a specific package | [Documentation](linux-installation-rpm.md "2.5.4 Installing MySQL on Linux Using RPM Packages from Oracle") |
| DEB | [Download](https://dev.mysql.com/downloads/mysql/) a specific package | [Documentation](linux-installation-debian.md "2.5.5 Installing MySQL on Linux Using Debian Packages from Oracle") |
| Generic | [Download](https://dev.mysql.com/downloads/mysql/) a generic package | [Documentation](binary-installation.md "2.2 Installing MySQL on Unix/Linux Using Generic Binaries") |
| Source | Compile from [source](https://dev.mysql.com/downloads/mysql/) | [Documentation](source-installation.md "2.8 Installing MySQL from Source") |
| Docker | Use the [Oracle Container Registry](https://container-registry.oracle.com/). You can also use [My Oracle Support](https://support.oracle.com/) for the MySQL Enterprise Edition. | [Documentation](linux-installation-docker.md "2.5.6 Deploying MySQL on Linux with Docker Containers") |
| Oracle Unbreakable Linux Network | Use ULN channels | [Documentation](uln-installation.md "2.6 Installing MySQL Using Unbreakable Linux Network (ULN)") |

As an alternative, you can use the package manager on your system to
automatically download and install MySQL with packages from the
native software repositories of your Linux distribution. These
native packages are often several versions behind the currently
available release. You are also normally unable to install
innovation releases, since these are not usually made available in
the native repositories. For more information on using the native
package installers, see [Section 2.5.7, “Installing MySQL on Linux from the Native Software Repositories”](linux-installation-native.md "2.5.7 Installing MySQL on Linux from the Native Software Repositories").

Note

For many Linux installations, you want to set up MySQL to be
started automatically when your machine starts. Many of the native
package installations perform this operation for you, but for
source, binary and RPM solutions you may need to set this up
separately. The required script, [**mysql.server**](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script"),
can be found in the `support-files` directory
under the MySQL installation directory or in a MySQL source tree.
You can install it as `/etc/init.d/mysql` for
automatic MySQL startup and shutdown. See
[Section 6.3.3, “mysql.server — MySQL Server Startup Script”](mysql-server.md "6.3.3 mysql.server — MySQL Server Startup Script").
