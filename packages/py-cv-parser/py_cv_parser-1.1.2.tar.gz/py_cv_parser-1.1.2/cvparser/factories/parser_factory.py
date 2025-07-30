from cvparser.Enum.filetype import *
from cvparser.Enum.language import *
from cvparser.parser.pdf_parser import Pdfparser
from cvparser.utility.ult import filetype_detect


class ParserFactory:
    @staticmethod
    def get_parser(file):
        _filetype = filetype_detect(file)

        if _filetype == FileType.PDF.value:
                return Pdfparser(file, _filetype)
        else:
            raise NotImplementedError("File types not supported yet")





