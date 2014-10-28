__author__ = 'Anirudh Anand (lucif3r)'

"""
.. module:: core run script
    :platform: Linux
    :synopsis: A module for Initializing Framework

.. module author:: Anirudh Anand <anirudh.anand@owasp.org>

This is the main file which initialize the framework.
"""

import sys
import os

"""For importing from tool_module"""
abs_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abs_path + '/modules')
sys.path.append(abs_path + '/Database')

from tool_module import ToolModule
from DBinterface import *
import json

class Initialize:

    def display_result(self, tool_name):
        """Gets the result of the last instance of the tool(indicted by tool_name) from the db and displays it.

        tool_name                         -> name of the tool.
        instance=int(file.readlines()[0]) -> converts the first line into an int and stores it in instance.
        instance-1          -> The instance value is incremented before writing . Current instance will be one less.
        lines               -> The output in list format.
        """
        inter_obj = DbInterface()
        db_inter_obj = inter_obj.create_obj()
        session = db_inter_obj.get_session()
        path = os.path.join(abs_path, session.query(Uxf.path).filter(Uxf.name == tool_name).all()[0][0], 'number')
        with open(path, 'r') as file:
            instance = int(file.readlines()[0])
        instance = instance-1
        lines = session.query(Report.report_dump).filter(Report.tool_name == tool_name).filter(Report.instance == instance).all()[0][0]
        print(str(lines))
        #lines = json.loads(str(json_lines))
        i = 0
        while i < len(lines):
            print(lines[i], end='')
            i = i+1

    def run_command(self, command):
        os.system(command)

    def launch(self):
        self.run_command("toilet -f mono12 -F metal UxF")

    def db_init(self):
        inter_obj = DbInterface()
        db_inter_obj = inter_obj.create_obj()
        db_inter_obj.create_tables_all()
        fp = os.path.join(os.path.dirname(__file__), 'Database', 'DBdata')
        try:
            db_inter_obj.insert_data_file(fp, "Uxf")
            db_inter_obj.commit_session()
        except:
            print("Skipping insertion..")

    def check_args(self):
        """
        Checking if the framework is initializing with required number of Arguments
        """
        if(len(sys.argv)) < 2:
            print("Invalid Number of Arguments: \nUsage:- Python3.4 uxf.py target URL")
            exit()

    def launch_tools(self):
        """
        Creating an object of class ToolModule from modules/tool_module which maintains the list of tools as different
        modules
        """
        obj = ToolModule()
        obj.run_all(sys.argv[1])


if __name__ == "__main__":
    initialize = Initialize()
    initialize.check_args()
    initialize.launch()
    initialize.db_init()
    initialize.launch_tools()
    initialize.display_result("panoptic")