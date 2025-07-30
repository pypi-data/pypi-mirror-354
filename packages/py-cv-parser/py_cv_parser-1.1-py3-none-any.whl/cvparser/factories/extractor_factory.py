from cvparser.Enum.language import Language
from cvparser.extracter.en_extractor import EnglishExtractor
from cvparser.parser.doc import Doc
from cvparser.utility.ult import language_detect


class ExtractorFactory:
    """
    for creating extractor
    """
    @staticmethod
    def get_extractor(doc:Doc,country,language:Language=None):
        try:
            if language is None:
                language = language_detect(doc.text)

            if language == Language.en.value:
                return EnglishExtractor(doc, country)

            else:
                raise NotImplementedError("language type not supported yet")

        except Exception as e:
            print(e)
            return None




