__author__ = 'deadmanwalking'

import subprocess
import os
import json
import sys

abs_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(abs_path+'/../../../Database')

from DBinterface import *

class Config():
    """The main configuration file. Now its just a test version"""
    def __init__(self):
        return

    #Panoptic works only with python2
    def run(self, tool_input):
        """Runs the tool with parameters taken from parameters file and tool_input and stores the output in db.
        The output is first redirected to a file stdout , from which it is read and dumped in JSON format. To get
        the instance number , the file number is read , and the number incremented by 1 is written back to the file.

        Note :- When a string is to be passed as data_dict , it should be in the format '"string"'. This is to
        avoid putting double quotes around all arguments effectively converting them to strings ( Which is not our
        requirement.

        tool_input  -> The user input (Here -> website to scan)
        parameters                  -> List of parameters for subprocess.call(here python2,panoptic.py,-v,-a,-u,url)
        path                       -> Path to the file parameters
        os.chdir()                 -> Changes the current directory to the one where panoptic.py resides
        os.path.abspath(__file__)  -> Gets absolute path of current file
        os.path.dirname(file)      -> Gets the removes the filename from abspath , making it path to directory
        os.path.join               -> Joins 2 paths (Here it appends /Panoptic to the path)
        subproces.call(parameters , stdout = stdout) -> Executes the program and redirectes the output to stdout file.
        instance = int(file.readlines()[0])          -> converts the first line into an int and stores it in instance.
        file.seek(0)               -> Seek to the starting of the file.
        file.write(str(num))       -> Convert the incremented instance to string and write.
        """

        parameters = []
        parameters.append('python2')
        parameters.append('panoptic.py')
        i = 0
        path = os.path.join(os.path.dirname(__file__), 'parameters')
        with open(path, 'r') as file:
            for line in file:
                for word in line.split():
                    parameters.append(word)
        parameters.append(tool_input)
        os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Panoptic'))
        stdout = open("stdout", "wb")
        subprocess.call(parameters, stdout=stdout)
        with open('stdout', 'r+') as file:
            lines = file.readlines()
            file.close()
        #dump = json.dumps(lines)
        inter_obj = DbInterface()
        db_inter_obj = inter_obj.create_obj()
        with open('../number', 'r+') as file:
            instance = int(file.readlines()[0])
            file.seek(0)
            num = instance+1
            file.write(str(num))
            file.truncate()
            file.close()
        data_dict = {}
        data_dict["instance"] = instance
        data_dict["tool_name"] = '"panoptic"'
        data_dict["report_dump"] = lines
        db_inter_obj.insert_data(data_dict, "Report")
        db_inter_obj.commit_session()
        #print(parameters)