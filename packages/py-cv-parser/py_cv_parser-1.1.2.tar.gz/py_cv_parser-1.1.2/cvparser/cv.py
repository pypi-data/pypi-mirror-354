class CV:
      def __init__(self,name,age,phone,email,schools,schools_with_date,companies,companies_with_date,address,skills):
          self.name=name
          self.age=age
          self.phone=phone
          self.email=email
          self.schools=schools
          self.schools_with_date=schools_with_date
          self.companies=companies
          self.companies_with_date=companies_with_date
          self.address=address
          self.skills=skills


      def __repr__(self):
          return (f"name:{self.name},age:{self.age},phone:{self.phone},email:{self.email},"
                  f"schools:{self.schools},schools_with_date:{self.schools_with_date},"
                  f"companies:{self.companies},"
                  f"companies_with_date:{self.companies_with_date},"
                  f"address:{self.address}),"
                  f"skills:{self.skills})"
                  )


