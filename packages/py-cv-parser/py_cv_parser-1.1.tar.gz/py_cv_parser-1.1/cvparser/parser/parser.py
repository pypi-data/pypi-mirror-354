from abc import abstractmethod

from cvparser.utility.ult import *
class parser:
    """
    parser abstract class, to parse doc
    """
    def __init__(self,file,filetype):
        self.filetype = filetype
        self.filename=get_filename(file)
        self.filesize=get_filesize(file)
        self.file=file



    @abstractmethod
    def parse(self):
        """return a cv object presenting content of a cv"""
        pass
