from abc import ABC

class AbstractEntity(ABC):

    def as_dictionary(self):
        temp = {}
        for s in self.__slots__:
            if hasattr(self, s) and getattr(self, s) != None:
                if type(getattr(self, s)).__module__ == 'builtins':
                    temp.update({s[1:]: getattr(self, s)})
                else:
                    temp.update({s[1:]: getattr(self, s).as_dictionary()})
        return temp


class LabDepartmentManagerEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_title')

    def __init__(self):
        self._portal_type = "LabContact"
        self._title = ""

    @property
    def portal_type(self):
        return self._portal_type

    @portal_type.setter
    def portal_type(self, portal_type):
        self._portal_type = portal_type

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    def as_dictionary(self):
        return {self._portal_type: self._title}

class LabDepartmentEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_Manager')

    def __init__(self, portal_type = "Department"):
        self._portal_type = portal_type
        self._title = ""

    @property
    def portal_type(self):
        return self._portal_type

    @portal_type.setter
    def portal_type(self, portal_type):
        self._portal_type = portal_type

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def Manager(self):
        return self._Manager

    @Manager.setter
    def Manager(self, managerEntity):
        self._Manager = managerEntity

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._title.value).encode())
        return hash_object.hexdigest()


class AnalysisCategoryEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_description', '_Department')

    def __init__(self, portal_type = "AnalysisCategory"):
        self._portal_type = portal_type
        self._title = ""

    @property
    def portal_type(self):
        return self._portal_type

    @portal_type.setter
    def portal_type(self, portal_type):
        self._portal_type = portal_type

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def Department(self):
        return self._Department

    @Department.setter
    def Department(self, departmentEntity):
        self._Department = departmentEntity

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._title.value).encode())
        return hash_object.hexdigest()

class AnalysisServiceEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_ShortTitle', '_SortKey', '_ScientificName', '_Unit', '_Precision', '_Keyword', '_Category', '_Department', '_Price', '_MinPrice', '_BulkPrice', '_description', '_MaxTimeAllowed', '_PointOfCapture', '_ExponentialFormatPrecision')

    def __init__(self, portal_type = "AnalysisService"):
        self._portal_type = portal_type
        self._title = ""
        self._Keyword = ""
        self._description = ""
        self._PointOfCapture = "PointOfCapture_2" #PointOfCapture_1 for field, PointOfCapture_2 for Lab
        self._ExponentialFormatPrecision = 7 # The defualt is 7

    @property
    def portal_type(self):
        return self._portal_type

    @portal_type.setter
    def portal_type(self, portal_type):
        self._portal_type = portal_type

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def ShortTitle(self):
        return self._ShortTitle

    @ShortTitle.setter
    def ShortTitle(self, shortTitle):
        self._ShortTitle = shortTitle

    @property
    def SortKey(self):
        return self._SortKey

    @SortKey.setter
    def SortKey(self, sortKey):
        self._SortKey = sortKey

    @property
    def ScientificName(self):
        return self._ScientificName

    @ScientificName.setter
    def ScientificName(self, scientificName):
        self._ScientificName = scientificName

    @property
    def Unit(self):
        return self._Unit

    @Unit.setter
    def Unit(self, unit):
        self._Unit = unit

    @property
    def Precision(self):
        return self._Precision

    @Precision.setter
    def Precision(self, precision):
        self._Precision = precision

    @property
    def Keyword(self):
        return self._Keyword

    @Keyword.setter
    def Keyword(self, keyword):
        self._Keyword = keyword

    @property
    def Category(self):
        return self._Category

    @Category.setter
    def Category(self, category):
        self._Category = category

    @property
    def Price(self):
        return self._Price

    @Price.setter
    def Price(self, price):
        self._Price = price

    @property
    def MinPrice(self):
        return self._MinPrice

    @MinPrice.setter
    def MinPrice(self, minPrice):
        self._MinPrice = minPrice

    @property
    def BulkPrice(self):
        return self._BulkPrice

    @BulkPrice.setter
    def BulkPrice(self, bulkPrice):
        self._BulkPrice = bulkPrice

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def MaxTimeAllowed(self):
        return self._MaxTimeAllowed

    @MaxTimeAllowed.setter
    def MaxTimeAllowed(self, MaxTimeAllowed):
        self._MaxTimeAllowed = MaxTimeAllowed

    @property
    def PointOfCapture(self):
        return self._PointOfCapture
    
    @PointOfCapture.setter
    def PointOfCapture(self, PointOfCapture):
        self._PointOfCapture = PointOfCapture

    @property
    def ExponentialFormatPrecision(self):
        return self._ExponentialFormatPrecision

    @ExponentialFormatPrecision.setter
    def ExponentialFormatPrecision(self, ExponentialFormatPrecision):
        self._ExponentialFormatPrecision = ExponentialFormatPrecision

    def hash_code(self):

        import hashlib
        hash_object = hashlib.md5(str(self._title.value).encode())
        return hash_object.hexdigest()


class PatientEntity(AbstractEntity):

    __slots__ = ('_primaryReferrer', '_clientPatientID', '_salutation', '_firstname', '_middleinitial', '_middlename', '_surname', '_consentSMS', '_gender', '_birthDate', '_age_splitted_year', '_age_splitted_month', '_age_splitted_day', '_countryState_country', '_countryState_state', '_emailAddress', '_homePhone', '_mobilePhone', '_civilStatus')

    def __init__(self):
        self._primaryReferrer = "GenoLab"
        self._clientPatientID = "GL"
        self._salutation = "Mr"
        self._firstname = ""
        self._middleinitial = ""
        self._middlename = ""
        self._surname = ""
        self._consentSMS = False
        self._gender = "male" # male, female, dk (for don't know)
        self._birthDate = ""
        self._age_splitted_year = ""
        self._age_splitted_month = ""
        self._age_splitted_day = ""
        self._countryState_country = ""
        self._countryState_state = ""
        self._emailAddress = ""
        self._homePhone = ""
        self._mobilePhone = ""
        self._civilStatus = "" # Single, Married, dk (for don't know)

    @property
    def primaryReferrer(self):
        return self._primaryReferrer

    @primaryReferrer.setter
    def primaryReferrer(self, primaryReferrer):
        self._primaryReferrer = primaryReferrer

    @property
    def clientPatientID(self):
        return self._clientPatientID

    @clientPatientID.setter
    def clientPatientID(self, clientPatientID):
        self._clientPatientID = clientPatientID

    @property
    def salutation(self):
        return self._salutation

    @salutation.setter
    def salutation(self, salutation):
        self._salutation = salutation

    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, firstname):
        self._firstname = firstname

    @property
    def middleinitial(self):
        return self._middleinitial

    @middleinitial.setter
    def middleinitial(self, middleinitial):
        self._middleinitial = middleinitial

    @property
    def middlename(self):
        return self._middlename

    @middlename.setter
    def middlename(self, middlename):
        self._middlename = middlename

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    @property
    def consentSMS(self):
        return self._consentSMS

    @consentSMS.setter
    def consentSMS(self, consentSMS):
        self._consentSMS = consentSMS

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def birthDate(self):
        return self._birthDate

    @birthDate.setter
    def birthDate(self, birthDate):
        self._birthDate = birthDate

    @property
    def age_splitted_year(self):
        return self._age_splitted_year

    @age_splitted_year.setter
    def age_splitted_year(self, age_splitted_year):
        self._age_splitted_year = age_splitted_year

    @property
    def age_splitted_month(self):
        return self._age_splitted_month

    @age_splitted_month.setter
    def age_splitted_month(self, age_splitted_month):
        self._age_splitted_month = age_splitted_month

    @property
    def age_splitted_day(self):
        return self._age_splitted_day

    @age_splitted_day.setter
    def age_splitted_day(self, age_splitted_day):
        self._age_splitted_day = age_splitted_day

    @property
    def countryState_country(self):
        return self._countryState_country

    @countryState_country.setter
    def countryState_country(self, countryState_country):
        self._countryState_country = countryState_country

    @property
    def countryState_state(self):
        return self._countryState_state

    @countryState_state.setter
    def countryState_state(self, countryState_state):
        self._countryState_state = countryState_state

    @property
    def emailAddress(self):
        return self._emailAddress

    @emailAddress.setter
    def emailAddress(self, emailAddress):
        self._emailAddress = emailAddress

    @property
    def homePhone(self):
        return self._homePhone

    @homePhone.setter
    def homePhone(self, homePhone):
        self._homePhone = homePhone

    @property
    def mobilePhone(self):
        return self._mobilePhone

    @mobilePhone.setter
    def mobilePhone(self, mobilePhone):
        self._mobilePhone = mobilePhone

    @property
    def civilStatus(self):
        return self._civilStatus

    @civilStatus.setter
    def civilStatus(self, civilStatus):
        self._civilStatus = civilStatus

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._clientPatientID.value).encode())
        return hash_object.hexdigest()