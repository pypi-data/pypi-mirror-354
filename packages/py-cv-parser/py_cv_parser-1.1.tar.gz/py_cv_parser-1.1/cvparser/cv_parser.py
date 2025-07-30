import re
from pathlib import Path

from cvparser.factories.extractor_factory import ExtractorFactory
from cvparser.factories.parser_factory import *
from cvparser.Enum.filetype import *
from cvparser.parser.doc import Doc


class CvParser:
    @staticmethod
    def load(file:str):

        # if "\\" in file or "/" in file:
        #     file = re.sub(r"[/\\]+", "/", file)
        # file_path=Path(file).resolve(strict=False)
        # print(file_path)
        try:
         return ParserFactory.get_parser(str(file))
        except Exception as e:
            print(e)
            return None
    @staticmethod
    def extract(doc:Doc,country,language:Language=None):
       '''


       :param language: if this parameter is None, program will try to detect language

       '''
       return ExtractorFactory.get_extractor(doc,country,language).extract()


