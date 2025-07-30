from cvparser.cv import CV
from cvparser.extracter.extractor import Extractor
import spacy
import re
from datetime import datetime

class EnglishExtractor(Extractor):
    def __init__(self, doc,country):
        super().__init__(doc,country)


    def extract(self)->CV:
        name,schools,companies,address,schools_with_date,companies_with_date,skills=[None]*7
        try:
            nlp = spacy.load('en_core_web_trf')
            nlp_doc = nlp(self.doc.text)
            name = self.get_person_name(nlp_doc)
            schools = self.__get_school_list(nlp_doc)
            companies = self.__get_company_list(nlp_doc)
            address = self.get_address_list(nlp_doc)
            schools_with_date = self.__get_education_date(nlp_doc)
            companies_with_date = self.__get_work_date_company(nlp_doc)
            skills=self.__get_skill(nlp_doc)
        except Exception as e:
            print(e)
        email,phone,age=[None]*3
        try:
            email = self.get_email_addresses()
            phone = self.get_phone_numbers()
            age = self.__calculate_age_from_year_str(self.__get_year_from_text())
        except Exception as e:
            print(e)


        return CV(name=name,email=email,phone=phone,address=address,age=age,schools=schools,companies=companies,schools_with_date=schools_with_date,companies_with_date=companies_with_date,skills=skills)


    def __get_school_list(self, nlp_doc):
        school_list=[]
        orglist=self.get_org_name(nlp_doc)
        for o in orglist:
            match=re.search(r".+?school|.+?college|.+?university", o,re.IGNORECASE)
            if match is not None:
               school_list.append(match.group())

        return school_list

    def __get_company_list(self, nlp_doc):
        company_list=[]
        pattern=r"\b[A-Za-z\s\-\(\)]+(?:Inc\.|Corporation|Limited|Group|Co\.|LLC|PLC|AG|SE|Company|Holdings|LLP)\b"
        orglist = self.get_org_name(nlp_doc)
        for o in orglist:
            match=re.search(pattern, o, re.IGNORECASE)
            if match is not None:
                company_list.append(match.group())

        return company_list

    def __is_company(self,text):
        pattern = r"\b[A-Za-z\s\-\(\)]+(?:Inc\.|Corporation|Limited|Group|Co\.|LLC|PLC|AG|SE|Company|Holdings|LLP)\b"
        if re.search(pattern, text, re.IGNORECASE):
            return True
        return False


    def __get_work_date_company(self, nlp_doc):
        work_date_company={}
        ents = nlp_doc.ents
        ents_list=[]
        for ent in ents:
            if ent.label_ == 'DATE' or ent.label_ == 'ORG':
                ents_list.append(ent)
        for i in range(len(ents_list)):
            if self.__is_company(ents_list[i].text) and i+1 < len(ents_list) and ents_list[i+1].label_ == 'DATE':
                work_date_company.update({ents_list[i].text: ents_list[i+1].text})

        return work_date_company

    def __is_school(self,text):
        pattern=r".+?school|.+?college|.+?university"
        if re.search(pattern, text, re.IGNORECASE):
            return True
        return False


    def __get_education_date(self, nlp_doc):
        education_date={}
        ents = nlp_doc.ents
        ents_list = []
        for ent in ents:
            if ent.label_ == 'DATE' or ent.label_ == 'ORG':
                ents_list.append(ent)

        for i in range(len(ents_list)):
            if self.__is_school(ents_list[i].text) and i+1 < len(ents_list) and ents_list[i+1].label_ == 'DATE':
                education_date.update({ents_list[i].text: ents_list[i+1].text})


        return education_date

    def __get_age(self):
        """
        expired

        """

        pattern=r"(?:Birth Year|Year of Birth|Born in|Graduated in|from|Birth Date)\s*[:\-]?[ \t]*(?:19|20)\d{2}"

        age_res=re.search(pattern, self.doc.text, re.IGNORECASE).group()

        res=re.search(r"\w*(\d+)",age_res,re.IGNORECASE).group()

        return res

    def __get_year_from_text(self):  # 函数名修改为更准确的描述
        """
        Attempts to extract a 4-digit year (19xx or 20xx) associated with
        keywords like "Birth Year", "Born in", etc.
        Also includes "Graduated in" as per original, be mindful of its meaning.
        """

        pattern = r"(?:Birth Year|Year of Birth|Born in|Graduated in|from|Birth Date)\s*[:\-]?[ \t]*((?:19|20)\d{2})"

        match = re.search(pattern, self.doc.text, re.IGNORECASE)

        if match:
            # group(1) 返回第一个捕获组的内容，即 ((?:19|20)\d{2}) 匹配到的年份
            year_str = match.group(1)
            return year_str

        return None  # 如果没有找到匹配，返回 None

    def __calculate_age_from_year_str(self, year_str):
        """
        Calculates age given a birth year string.
        Returns age as an integer or None if conversion/calculation fails.
        """
        if year_str:
            try:
                birth_year = int(year_str)
                current_year = datetime.now().year
                age = current_year - birth_year
                # 可以加一些年龄的合理性校验
                if 0 <= age <= 130:  # 例如，年龄在0到130岁之间
                    return age
                else:
                    # 年龄超出合理范围
                    return None
            except ValueError:
                # 年份字符串无法转换为整数
                return None
        return None

    def __get_company_discription(self,nlp_doc):
          raise NotImplementedError


    def __get_skill(self,nlp_doc):
        skills=[]
        for ent in nlp_doc.ents:
            if ent.label_ == 'PRODUCT':
                skills.append(ent.text)

        return skills



























