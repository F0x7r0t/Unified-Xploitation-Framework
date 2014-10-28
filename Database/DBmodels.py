__author__ = 'deadmanwalking'

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import TypeDecorator, VARCHAR
import json

Base = declarative_base()

""" This is where all the mappings for tables are put """


class JSONEncodedDict(TypeDecorator):
    """Class for processiong JSON values .
    """

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value



class Uxf(Base):
    __tablename__ = "tool_paths"

    id = Column(Integer, primary_key=True)
    category = Column(String)
    name = Column(String)
    path = Column(String)


class Report(Base):
    """Table for storing the output of the tool.
    Instance     -> Which instance of the tool is stored.
    tool_name    -> Name of the tool.
    report_dump  -> Output of the tool in JSON format.
    """
    __tablename__ = "report"

    instance = Column(Integer, primary_key=True)
    tool_name = Column(String)
    report_dump = Column(JSONEncodedDict())

