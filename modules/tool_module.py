__author__ = 'deadmanwalking'

import os
import sys

"""For importing from DBinterface"""
abs_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abs_path+'/../Database')


from DBinterface import *


class ToolModule:
    """The main class"""

    def __init__(self):
        return

    def run_tool(self, tool_input, path):
        """Runs the tool on the by passing the tool_input to it.

        tool_input      -> Input to the tool
        path            -> Path of file
        tool_executer   -> The imported file from path
        config.py       -> File that takes the input , selects parameters and runs the tool
        config_obj      -> Object of the config class()

        sys.path.append -> Appends the path so that the module can be imported
        """
        sys.path.append(abs_path+'/../'+path)
        tool_executer = __import__('config')
        config_obj = tool_executer.Config()
        config_obj.run(tool_input)

    def get_path(self, tool_name):
        """Gets the path of the tool from the db uxf and returns it

        inter_obj    -> Main db interface class object
        db_inter_obj -> Object of the class which provides the API
        session      -> Session of db
        tool_name    -> A list whose first element is the category of tool and second is the tool name


        session.query(Uxf.path)            -> Returns all the path value of every row
        .filter(Uxf.path == tool_name[0])  -> Returns only those whose category matches one defined in tool_name[0]
        .filter(Uxf.name == tool_name[1])  -> Returns only those whose name matches one defined in tool_name[1]
        .all()                             -> [(path, )]   (where path is the required value)
        .all()[0]                          -> (path)
        .all()[0][0]                       -> path
        """

        inter_obj = DbInterface()
        db_inter_obj = inter_obj.create_obj()
        session = db_inter_obj.get_session()
        return session.query(Uxf.path).filter(Uxf.category == tool_name[0]).filter(Uxf.name == tool_name[1]).all()[0][0]

    def run(self, tool_input, tool_name):
        """This function calls the get_path to get the path and calls run_tool with the path and tool_input

        tool_name    -> A list whose first element is the category of tool and second is the tool name
        tool_input      -> Input to the tool
        """
        tool_path = self.get_path(tool_name)
        self.run_tool(tool_input, tool_path)

    def run_all(self, tool_input):
        """Runs all the tools with the tool_input

        session.query(Uxf.path).all()      -> Returns a list where each element is again a list with 0th element as path
        path                               -> List with 0th element as tool path
        real_path                          -> The real path of the tool

        The function calls run_tool() with each path and tool_input
        """
        inter_obj = DbInterface()
        db_inter_obj = inter_obj.create_obj()
        session = db_inter_obj.get_session()
        tool_paths = session.query(Uxf.path).all()
        for path in tool_paths:
            real_path = path[0]
            self.run_tool(tool_input, real_path)


def test():
    obj = ToolModule()
    tool_name = ['web', 'panoptic']
    print(obj.get_path(tool_name))
    #obj.run('http://www.securethelock.com', tool_name)
    obj.run_all('http://www.securethelock.com')

#test()