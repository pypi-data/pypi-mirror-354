import re
from pathlib import Path
from cvparser.factories.parser_factory import *
from cvparser.Enum.filetype import *


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


