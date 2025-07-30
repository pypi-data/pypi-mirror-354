from xml.dom.minidom import Document

from cvparser.parser.doc import Doc
from cvparser.parser.parser import parser
from pdfminer.high_level import *
from cvparser.utility.ult import *
class Pdfparser(parser):
    """
    parse pdf doc
    """
    def __init__(self,file,filetype):
        super().__init__(file,filetype)



    def parse(self):
        try:
            output_string = StringIO()
            with open(self.file, 'rb') as fin:
                extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='text', codec='utf-8')


            text = clean_text(output_string.getvalue().strip())
            count = count_words(text)
            return Doc(text, count)
        except Exception as e:
             print(e)
             return None


