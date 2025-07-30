from abc import abstractmethod
import re
import phonenumbers
from phonenumbers import PhoneNumberFormat
import country_converter
class Extractor(object):
    """
    extract critical information from Doc object
    """
    def __init__(self, doc,country):
        self.doc = doc
        self.country = country


    @abstractmethod
    def extract(self):
        pass

    def get_person_name(self, nlp_doc):
        for token in nlp_doc.ents:
            if token.label_ == 'PERSON':
                return token.text

        return None


    def get_org_name(self, nlp_doc):
        orglist=[]
        for token in nlp_doc.ents:
            if token.label_ == 'ORG':
                orglist.append(token.text)

        return  orglist


    def get_address_list(self, nlp_doc):
        address_list=[]
        for token in nlp_doc.ents:
            if token.label_ == 'GPE' or token.label_ == 'FAC' or token.label_ == 'LOC':
                address_list.append(token.text)

        return address_list


    def get_email_addresses(self):
        """
    get mail addr
        """
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        return list(set(email_pattern.findall(self.doc.text)))  # 使用 set 去重

    def get_phone_numbers(self):
        found_numbers = set()  # 使用 set 去重

        phone_pattern = re.compile(
            r'(?:(?:\+\d{1,3}[-.\s]*)?  (e.g., +1, +86)(?:(?:\(\d{1,4}\)|\d{1,4})[-.\s]*)? \d{2,4}[-.\s]* ){2,}\d{2,4} | \b\d{7,15}\b ',
            re.VERBOSE)

        for match in phone_pattern.finditer(self.doc.text):
            potential_number_str = match.group(0)

            try:
                standard_name=country_converter.convert(names=self.country,to='iso2')

                parsed_number = phonenumbers.parse(potential_number_str,standard_name)


                if phonenumbers.is_valid_number(parsed_number) and phonenumbers.is_possible_number(parsed_number):

                    formatted_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                    found_numbers.add(formatted_number)

            except phonenumbers.NumberParseException:

                print(f"Failed to parse: {potential_number_str}")
                pass

        return list(found_numbers)
