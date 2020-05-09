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

    def getAttr(self, attribute):
        return getattr(self, attribute)


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
        self._Manager = LabDepartmentManagerEntity()

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

class RetentionPeriod(AbstractEntity):

    __slots__ = ('_days', '_hours', '_minutes')

    def __init__(self):
        self._days = 0
        self._hours = 0
        self._minutes = 0

    @property
    def days(self):
        return self._days
    
    @days.setter
    def days(self, days):
        self._days = days

    @property
    def hours(self):
        return self._hours
    
    @hours.setter
    def hours(self, hours):
        self._hours = hours

    @property
    def minutes(self):
        return self._minutes
    
    @minutes.setter
    def minutes(self, minutes):
        self._minutes = minutes

class AdmittedStickerTemplates(AbstractEntity):

    __slots__ = ('_admitted', '_small', '_large')

    def __init__(self):
        self._admitted = "Code_128_1x48mm.pt"
        self._small = "Code_128_1x48mm.pt"
        self._large = "Code_128_1x48mm.pt"

    @property
    def admitted(self):
        return self._admitted
    
    @property
    def small(self):
        return self._small
    
    @property
    def large(self):
        return self._large
    
class SampleTypeEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_description', '_RetentionPeriod', '_Prefix', '_MinimumVolume', '_AdmittedStickerTemplates')

    def __init__(self, portal_type = "SampleType"):
        self._portal_type = portal_type
        self._title = ""
        self._description = ""
        self._RetentionPeriod = RetentionPeriod()
        self._Prefix = ""
        self._MinimumVolume = ""
        self._AdmittedStickerTemplates = AdmittedStickerTemplates()

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
    def RetentionPeriod(self):
        return self._RetentionPeriod

    @RetentionPeriod.setter
    def RetentionPeriod(self, RetentionPeriod):
        self._RetentionPeriod = RetentionPeriod

    @property
    def Prefix(self):
        return self._Prefix

    @Prefix.setter
    def Prefix(self, Prefix):
        self._Prefix = Prefix

    @property
    def MinimumVolume(self):
        return self._MinimumVolume
    
    @MinimumVolume.setter
    def MinimumVolume(self, MinimumVolume):
        self._MinimumVolume = MinimumVolume

    @property
    def AdmittedStickerTemplates(self):
        return self._AdmittedStickerTemplates
    
    @AdmittedStickerTemplates.setter
    def AdmittedStickerTemplates(self, AdmittedStickerTemplates):
        self._AdmittedStickerTemplates = AdmittedStickerTemplates

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._title.value).encode())
        return hash_object.hexdigest()

class AnalysisSpec(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_description', '_Department')

    def __init__(self, portal_type = "AnalysisCategory"):
        self._portal_type = portal_type
        self._title = ""
        # self._description = ""
        # labDepartmentEntity = LabDepartmentEntity(None)
        # labDepartmentEntity.title = "Initial_Dept"
        # self._Department = labDepartmentEntity

class DynamicAnalysisSpecEntity(AbstractEntity):

    __slots__ = ('_Keyword', '_Gender', '_Age_From', '_Age_To', '_min', '_max')

    def __init__(self):
        self._Keyword = ""
        self._Gender = ""

    @property
    def Keyword(self):
        return self._Keyword
    
    @Keyword.setter
    def Keyword(self, Keyword):
        self._Keyword = Keyword

    @property
    def Gender(self):
        return self._Gender
    
    @Gender.setter
    def Gender(self, Gender):
        self._Gender = Gender
    
    @property
    def Age_From(self):
        return self._Age_From
    
    @Age_From.setter
    def Age_From(self, Age_From):
        self._Age_From = Age_From

    @property
    def Age_To(self):
        return self._Age_To

    @Age_To.setter
    def Age_To(self, Age_To):
        self._Age_To = Age_To
    
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, mini):
        self._min = mini

    @property
    def max(self):
        return self._max

    @max.setter
    def max(self, maxi):
        self._max = maxi

    def getDataAsList(self):
        return [self._Keyword, self._Gender, self._Age_From, self._Age_To, self._min, self._max]

    
# class DynamicAnalysisSpecEntity(AbstractEntity):

#     __slots__ = ('_portal_type', '_uid', '_title', '_Keyword', '_Department')

#     def __init__(self, portal_type = "AnalysisCategory"):
#         self._portal_type = portal_type
#         self._title = ""
#         # self._description = ""
#         # labDepartmentEntity = LabDepartmentEntity(None)
#         # labDepartmentEntity.title = "Initial_Dept"
#         # self._Department = labDepartmentEntity

class AnalysisCategoryEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_description', '_Department')

    def __init__(self, portal_type = "AnalysisCategory"):
        self._portal_type = portal_type
        self._title = ""
        self._description = ""
        labDepartmentEntity = LabDepartmentEntity(None)
        labDepartmentEntity.title = "Initial_Dept"
        self._Department = labDepartmentEntity

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

class UncertaintyEntity(AbstractEntity):

    __slots__ = ('_gender', '_age_from', '_age_to', '_intercept_min', '_intercept_max', '_errorvalue')

    def __init__(self):
        self._gender = "Male"
        self._errorvalue = 0

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def age_from(self):
        return self._age_from

    @age_from.setter
    def age_from(self, age_from):
        self._age_from = age_from

    @property
    def age_to(self):
        return self._age_to

    @age_to.setter
    def age_to(self, age_to):
        self._age_to = age_to

    @property
    def intercept_min(self):
        return self._intercept_min

    @intercept_min.setter
    def intercept_min(self, intercept_min):
        self._intercept_min = intercept_min

    @property
    def intercept_max(self):
        return self._intercept_max

    @intercept_max.setter
    def intercept_max(self, intercept_max):
        self._intercept_max = intercept_max

    @property
    def errorvalue(self):
        return self._errorvalue

    @errorvalue.setter
    def errorvalue(self, errorvalue):
        self._errorvalue = errorvalue

class MaxTimeAllowed(AbstractEntity):

    __slots__ = ('_days', '_hours', '_minutes')

    def __init__(self):
        self._days = 0
        self._hours = 0
        self._minutes = 0

    @property
    def days(self):
        return self._days
    
    @days.setter
    def days(self, days):
        self._days = days

    @property
    def hours(self):
        return self._hours
    
    @hours.setter
    def hours(self, hours):
        self._hours = hours

    @property
    def minutes(self):
        return self._minutes
    
    @minutes.setter
    def minutes(self, minutes):
        self._minutes = minutes

class AnalysisServiceEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_title', '_ShortTitle', '_SortKey', '_ScientificName', '_Unit', '_Factor', '_Precision', '_Keyword', '_Category', '_Department', '_Price', '_MaxPrice2008', '_MinPrice1995', '_MaxPrice1995', '_BulkPrice', '_description', '_MaxTimeAllowed', '_PointOfCapture', '_ExponentialFormatPrecision', '_Uncertainties', '_Department')

    def __init__(self, portal_type = "AnalysisService"):
        self._portal_type = portal_type
        self._title = ""
        self._Unit = ""
        self._Factor = 0
        self._Keyword = ""
        self._description = ""
        self._PointOfCapture = "PointOfCapture_2" #PointOfCapture_1 for field, PointOfCapture_2 for Lab
        self._ExponentialFormatPrecision = 7 # The defualt is 7
        self._Category = AnalysisCategoryEntity(None)
        self._Department = LabDepartmentEntity(None)
        self._MaxTimeAllowed = MaxTimeAllowed()

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
    def Factor(self):
        return self._Factor
    
    @Factor.setter
    def Factor(self, Factor):
        self._Factor = Factor

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
    def MaxPrice2008(self):
        return self._MaxPrice2008

    @MaxPrice2008.setter
    def MaxPrice2008(self, MaxPrice2008):
        self._MaxPrice2008 = MaxPrice2008

    @property
    def MinPrice1995(self):
        return self._MinPrice1995

    @MinPrice1995.setter
    def MinPrice1995(self, MinPrice1995):
        self._MinPrice1995 = MinPrice1995

    @property
    def MaxPrice1995(self):
        return self._MaxPrice1995

    @MaxPrice1995.setter
    def MaxPrice1995(self, MaxPrice1995):
        self._MaxPrice1995 = MaxPrice1995

    @property
    def AssociationPrice(self):
        return self._AssociationPrice

    @AssociationPrice.setter
    def AssociationPrice(self, AssociationPrice):
        self._AssociationPrice = AssociationPrice

    @property
    def LaboratoriesPrice(self):
        return self._LaboratoriesPrice

    @LaboratoriesPrice.setter
    def LaboratoriesPrice(self, LaboratoriesPrice):
        self._LaboratoriesPrice = LaboratoriesPrice

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

    @property
    def Uncertainties(self):
        return self._Uncertainties

    @Uncertainties.setter
    def Uncertainties(self, uncertaintyEntity):
        self._Uncertainties = uncertaintyEntity

    @property
    def Department(self):
        return self._Department

    @Department.setter
    def Department(self, Department):
        self._Department = Department
    
    def hash_code(self):

        import hashlib
        hash_object = hashlib.md5(str(self._title.value).encode())
        return hash_object.hexdigest()


class PatientEntity(AbstractEntity):

    __slots__ = ('_primaryReferrer', '_clientPatientID', '_salutation', '_firstname', '_middleinitial', '_middlename', '_surname', '_consentSMS', '_gender', '_birthDate', '_age_splitted_year', '_age_splitted_month', '_age_splitted_day', '_countryState_country', '_countryState_state', '_emailAddress', '_homePhone', '_mobilePhone', '_civilStatus', '_PatientCoverageRate')

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
        self._countryState_country = "Jordan"
        self._countryState_state = "Amman"
        self._emailAddress = ""
        self._homePhone = ""
        self._mobilePhone = ""
        self._civilStatus = "" # Single, Married, dk (for don't know)
        self._PatientCoverageRate = 0

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

    @property
    def PatientCoverageRate(self):
        return self._PatientCoverageRate
    
    @PatientCoverageRate.setter
    def PatientCoverageRate(self, PatientCoverageRate):
        self._PatientCoverageRate = PatientCoverageRate

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._clientPatientID.value).encode())
        return hash_object.hexdigest()

class AnalysisRequestEntity(AbstractEntity):

    __slots__ = ('_portal_type', '_uid', '_Client', '_Contact', '_Patient', '_DateSampled', '_SampleType', '_ClientSampleID','_InternalUse' )

    def __init__(self, portal_type = "AnalysisService"):
        self._portal_type = portal_type

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
    def Client(self):
        return self._Client
    
    @Client.setter
    def Client(self, Client):
        self._Client = Client

    @property
    def Contact(self):
        return self._Contact
    
    @Contact.setter
    def Contact(self, Contact):
        self._Contact = Contact

    @property
    def Patient(self):
        return self._Patient
    
    @Patient.setter
    def Patient(self, Patient):
        self._Patient = Patient

    @property
    def DateSampled(self):
        return self._DateSampled

    @DateSampled.setter
    def DateSampled(self, DateSampled):
        self._DateSampled = DateSampled

    @property
    def SampleType(self):
        return self._SampleType
    
    @SampleType.setter
    def SampleType(self, SampleType):
        self._SampleType = SampleType

    @property
    def ClientSampleID(self):
        return self._ClientSampleID
    
    @ClientSampleID.setter
    def ClientSampleID(self, ClientSampleID):
        self._ClientSampleID = ClientSampleID

    @property
    def InternalUse(self):
        return self._InternalUse
    
    @InternalUse.setter
    def InternalUse(self, InternalUse):
        self._InternalUse = InternalUse

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._clientPatientID.value).encode())
        return hash_object.hexdigest()