__author__ = 'Anirudh Anand (lucif3r)'

"""
.. module:: Install Script
    :platform: Linux
    :synopsis: A module for Installing essentials

.. module author:: Anirudh Anand <anirudh.anand@owasp.org>
"""

import os


class InstallTools(object):
    """This file should be run once by every user to ensure that all the
    modules required for working of the tool are installed in the system"""

    def __init__(self, RootDir):
        self.RootDir = RootDir
        self.Pid = os.getpid()
        """Getting the right file location to install tools and setting up db

        *ostools.uxf    ->    Necessary OS tools
        *piptools.uxf   ->    Necessary python-pip tools
        *dbsetup.sh     ->    db configuration file
        *os.path.join   ->    Join one or more path components
        """

        self.ostools = os.path.join(RootDir, "ostools.uxf")
        self.piptools = os.path.join(RootDir, "piptools.uxf")
        self.dbsetup = os.path.join(RootDir, "db_setup.sh")


    def run_command(self, command):
        """Instead of calling os.system() in multiple places, it is better to have
        it as a function and use it """

        print("* Running the command %s" % command)
        os.system(command)

    def install_piptools(self, tools):
        """This will install the necessary python-pip tools. We are saving a list
        of tools to be installed with just the name. Advantages of doing this are:

        * Adding a new tool later to the install script will be very easy (just add
        the name on the next line in piptools.uxf

        *Removing can also be done in the similar way
        """
        self.run_command("sudo -E pip3 install --upgrade %s" % tools)

    def install_ostools(self, tools):
        self.run_command("sudo apt-get install %s" % tools)

    def setupdb(self):
        self.run_command("sh %s" % self.dbsetup)

    def install(self):
        """
        This function will make sure that:

        * All the pip and OS tools are installed from corresponding files
        * Postgresql db has been setup with required credentials
        """
        tools_pip = open(self.piptools, 'r')
        print("* Installing necessary python-pip tools")
        for i in tools_pip.readlines():
            self.install_piptools(i)

        tools_os = open(self.ostools, 'r')
        print("* Installing necessary OS tools")
        for i in tools_os.readlines():
            self.install_ostools(i)

        print("* Setting up the db and creating the user ")
        self.setupdb()


if __name__ == "__main__":
    RootDir = os.path.dirname(os.path.realpath(__file__))
    install = InstallTools(RootDir)
    install.install()