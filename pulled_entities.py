from abc import ABC

class AbstractEntity(ABC, object):

    def getCriteriaDictionary(self):
        criteriaDictionary = {}
        for s in self.__slots__:
            if hasattr(self, s) and getattr(self, s) != None:
                if type(getattr(self, s)).__module__ == 'builtins' or type(getattr(self, s)).__module__ == 'decimal':
                    criteriaDictionary.update({s: getattr(self, s)})
                else:
                    criteriaDictionary.update({s: getattr(self, s).getCriteriaDictionary()})
        return criteriaDictionary

class DepartmentEntity(AbstractEntity):

    __slots__ = ('_id', '_depname')

    def __init__(self):
        self._id = 0
        self._depname = ""

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id

    @property
    def depname(self):
        return self._depname
    
    @depname.setter
    def depname(self, depname):
        self._depname = depname

class TestCategoryEntity(AbstractEntity):

    __slots__ = ('_CatNumber', '_CatName')

    def __init__(self):
        self._CatNumber = 0
        self._CatName = ""

    @property
    def CatNumber(self):
        return self._CatNumber

    @CatNumber.setter
    def CatNumber(self, CatNumber):
        self._CatNumber = CatNumber

    @property
    def CatName(self):
        return self._CatName

    @CatName.setter
    def CatName(self, CatName):
        self._CatName = CatName

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._CatNumber.value).encode())
        return hash_object.hexdigest()

class TestEntity(AbstractEntity):

    __slots__ = ('_ID', '_TstNumber', '_testnumber', '_TstName', '_tstshort', '_CatNumber', '_TstDuration', '_tstHrDuration', '_TstResultType', '_TstNotes', '_TstSpecimal1', '_TstSpecimal2', '_tstdword', '_testDesc', '_resulttype', '_testEquation', '_ShowPreviousresult')

    def __init__(self):
        self._CatNumber = 0
        self._ShowPreviousresult = -1

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def TstNumber(self):
        return self._TstNumber

    @TstNumber.setter
    def TstNumber(self, TstNumber):
        self._TstNumber = TstNumber

    @property
    def testnumber(self):
        return self._testnumber

    @testnumber.setter
    def testnumber(self, testnumber):
        self._testnumber = testnumber

    @property
    def TstName(self):
        return self._TstName

    @TstName.setter
    def TstName(self, TstName):
        self._TstName = TstName

    @property
    def tstshort(self):
        return self._tstshort

    @tstshort.setter
    def tstshort(self, tstshort):
        self._tstshort = tstshort

    @property
    def CatNumber(self):
        return self._CatNumber

    @CatNumber.setter
    def CatNumber(self, CatNumber):
        self._CatNumber = CatNumber

    @property
    def TstDuration(self):
        return self._TstDuration

    @TstDuration.setter
    def TstDuration(self, TstDuration):
        self._TstDuration = TstDuration

    @property
    def tstHrDuration(self):
        return self._tstHrDuration

    @tstHrDuration.setter
    def tstHrDuration(self, tstHrDuration):
        self._tstHrDuration = tstHrDuration

    @property
    def TstResultType(self):
        return self._TstResultType

    @TstResultType.setter
    def TstResultType(self, TstResultType):
        self._TstResultType = TstResultType

    @property
    def TstNotes(self):
        return self._TstNotes

    @TstNotes.setter
    def TstNotes(self, TstNotes):
        self._TstNotes = TstNotes

    @property
    def TstSpecimal1(self):
        return self._TstSpecimal1

    @TstSpecimal1.setter
    def TstSpecimal1(self, TstSpecimal1):
        self._TstSpecimal1 = TstSpecimal1

    @property
    def TstSpecimal2(self):
        return self._TstSpecimal2

    @TstSpecimal2.setter
    def TstSpecimal2(self, TstSpecimal2):
        self._TstSpecimal2 = TstSpecimal2

    @property
    def tstdword(self):
        return self._tstdword

    @tstdword.setter
    def tstdword(self, tstdword):
        self._tstdword = tstdword

    @property
    def testDesc(self):
        return self._testDesc

    @testDesc.setter
    def testDesc(self, testDesc):
        self._testDesc = testDesc

    @property
    def resulttype(self):
        return self._resulttype

    @resulttype.setter
    def resulttype(self, resulttype):
        self._resulttype = resulttype

    @property
    def testEquation(self):
        return self._testEquation

    @testEquation.setter
    def testEquation(self, testEquation):
        self._testEquation = testEquation

    @property
    def ShowPreviousresult(self):
        return self._ShowPreviousresult
    
    @ShowPreviousresult.setter
    def ShowPreviousresult(self, ShowPreviousresult):
        self._ShowPreviousresult = ShowPreviousresult
    
    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()

class TestResultTypeEntity(AbstractEntity):

    __slots__ = ('_ID', '_TstNumber', '_testnumber', '_Tstgender', '_Tstagefrom', '_tstdayfrom', '_Tstageto', '_Tstdayto', '_Tstprefix', '_TstNormalFrom', '_TstNormalTo', '_Tstsufix', '_TstWord', '_TstDword', '_TstUnit', '_Tstfactor', '_Tstfacunit')

    def __init__(self):
        self._testnumber = 0

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def TstNumber(self):
        return self._TstNumber

    @TstNumber.setter
    def TstNumber(self, TstNumber):
        self._TstNumber = TstNumber

    @property
    def testnumber(self):
        return self._testnumber

    @testnumber.setter
    def testnumber(self, testnumber):
        self._testnumber = testnumber

    @property
    def Tstgender(self):
        return self._Tstgender

    @Tstgender.setter
    def Tstgender(self, Tstgender):
        self._Tstgender = Tstgender

    @property
    def Tstagefrom(self):
        return self._Tstagefrom

    @Tstagefrom.setter
    def Tstagefrom(self, Tstagefrom):
        self._Tstagefrom = Tstagefrom

    @property
    def tstdayfrom(self):
        return self._tstdayfrom

    @tstdayfrom.setter
    def tstdayfrom(self, tstdayfrom):
        self._tstdayfrom = tstdayfrom

    @property
    def Tstageto(self):
        return self._Tstageto

    @Tstageto.setter
    def Tstageto(self, Tstageto):
        self._Tstageto = Tstageto

    @property
    def Tstdayto(self):
        return self._Tstdayto

    @Tstdayto.setter
    def Tstdayto(self, Tstdayto):
        self._Tstdayto = Tstdayto

    @property
    def Tstprefix(self):
        return self._Tstprefix
    
    @Tstprefix.setter
    def Tstprefix(self, Tstprefix):
        self._Tstprefix = Tstprefix

    @property
    def TstNormalFrom(self):
        return self._TstNormalFrom
    
    @TstNormalFrom.setter
    def TstNormalFrom(self, TstNormalFrom):
        self._TstNormalFrom = TstNormalFrom

    @property
    def TstNormalTo(self):
        return self._TstNormalTo
    
    @TstNormalTo.setter
    def TstNormalTo(self, TstNormalTo):
        self._TstNormalTo = TstNormalTo

    @property
    def Tstsufix(self):
        return self._Tstsufix

    @Tstsufix.setter
    def Tstsufix(self, Tstsufix):
        self._Tstsufix = Tstsufix

    @property
    def TstWord(self):
        return self._TstWord
    
    @TstWord.setter
    def TstWord(self, TstWord)  :
        self._TstWord = TstWord

    @property
    def TstDword(self):
        return self._TstDword
    
    @TstDword.setter
    def TstDword(self, TstDword):
        self._TstDword = TstDword

    @property
    def TstUnit(self):
        return self._TstUnit

    @TstUnit.setter
    def TstUnit(self, TstUnit):
        self._TstUnit = TstUnit

    @property
    def Tstfactor(self):
        return self._Tstfactor

    @Tstfactor.setter
    def Tstfactor(self, Tstfactor):
        self._Tstfactor = Tstfactor

    @property
    def Tstfacunit(self):
        return self._Tstfacunit
    
    @Tstfacunit.setter
    def Tstfacunit(self, Tstfacunit):
        self._Tstfacunit = Tstfacunit

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()

class TestPriceEntity(AbstractEntity):

    __slots__ = ('_Idno', '_testname', '_min1995', '_max1995', '_min2008', '_max2008', '_F9', '_jam')

    def __init__(self):
        self._Idno = 0

    @property
    def Idno(self):
        return self._Idno

    @Idno.setter
    def Idno(self, Idno):
        self._Idno = Idno

    @property
    def testname(self):
        return self._testname

    @testname.setter
    def testname(self, testname):
        self._testname = testname

    @property
    def min1995(self):
        return self._min1995

    @min1995.setter
    def min1995(self, min1995):
        self._min1995 = min1995

    @property
    def max1995(self):
        return self._max1995

    @max1995.setter
    def max1995(self, max1995):
        self._max1995 = max1995

    @property
    def min2008(self):
        return self._min2008

    @min2008.setter
    def min2008(self, min2008):
        self._min2008 = min2008

    @property
    def max2008(self):
        return self._max2008

    @max2008.setter
    def max2008(self, max2008):
        self._max2008 = max2008

    @property
    def F9(self):
        return self._F9

    @F9.setter
    def F9(self, F9):
        self._F9 = F9

    @property
    def jam(self):
        return self._jam

    @jam.setter
    def jam(self, jam):
        self._jam = jam

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._Idno.value).encode())
        return hash_object.hexdigest()

class TestPriceEntity2(AbstractEntity):

    __slots__ = ('_ID', '_TstNumber', '_testnumber', '_TstPrice', '_PriceCatID')

    def __init__(self):
        self._ID = 0
        self._TstNumber = ""
        self._testnumber = 0
        self._TstPrice = 0.0
        self._PriceCatID = 0

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def TstNumber(self):
        return self._TstNumber

    @TstNumber.setter
    def TstNumber(self, TstNumber):
        self._TstNumber = TstNumber

    @property
    def testnumber(self):
        return self._testnumber

    @testnumber.setter
    def testnumber(self, testnumber):
        self._testnumber = testnumber

    @property
    def TstPrice(self):
        return self._TstPrice
    
    @TstPrice.setter
    def TstPrice(self, TstPrice):
        self._TstPrice = TstPrice

    @property
    def PriceCatID(self):
        return self._PriceCatID

    @PriceCatID.setter
    def PriceCatID(self, PriceCatID):
        self._PriceCatID = PriceCatID

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()

class PulledPatientEntity(AbstractEntity):

    __slots__ = ('_ID', '_PatNumber', '_PatName', '_PatarName', '_PatDateOfBirth', '_PatSex', '_PatTelephone', '_PatMobile', '_PatEmail', '_PatMaritalStatus')

    def __init__(self):
        self._ID = 0

    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, ID):
        self._ID = ID

    @property
    def PatNumber(self):
        return self._PatNumber
    
    @PatNumber.setter
    def PatNumber(self, PatNumber):
        self._PatNumber = PatNumber

    @property
    def PatName(self):
        return self._PatName
    
    @PatName.setter
    def PatName(self, PatName):
        self._PatName = PatName

    @property
    def PatarName(self):
        return self._PatarName
    
    @PatarName.setter
    def PatarName(self, PatarName):
        self._PatarName = PatarName

    @property
    def PatDateOfBirth(self):
        return self._PatDateOfBirth
    
    @PatDateOfBirth.setter
    def PatDateOfBirth(self, PatDateOfBirth):
        self._PatDateOfBirth = PatDateOfBirth

    @property
    def PatSex(self):
        return self._PatSex
    
    @PatSex.setter
    def PatSex(self, PatSex):
        self._PatSex = PatSex

    @property
    def PatTelephone(self):
        return self._PatTelephone
    
    @PatTelephone.setter
    def PatTelephone(self, PatTelephone):
        self._PatTelephone = PatTelephone

    @property
    def PatMobile(self):
        return self._PatMobile
    
    @PatMobile.setter
    def PatMobile(self, PatMobile):
        self._PatMobile = PatMobile

    @property
    def PatEmail(self):
        return self._PatEmail
    
    @PatEmail.setter
    def PatEmail(self, PatEmail):
        self._PatEmail = PatEmail

    @property
    def PatMaritalStatus(self):
        return self._PatMaritalStatus
    
    @PatMaritalStatus.setter
    def PatMaritalStatus(self, PatMaritalStatus):
        self._PatMaritalStatus = PatMaritalStatus

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()

class TransAmountDetailsEntity(AbstractEntity):

    __slots__ = ('_id_auto', '_pat_id', '_trano', '_datee', '_amount', '_p_type', '_balance', '_net_amount', '_status_pat', '_status_value', '_Coverage', '_inv_number', '_decount', '_PatCoverage', '_patCovValue', '_DiscountCompany')

    def __init__(self):
        self._ID = 0
        self._pat_id = 0

    @property
    def id_auto(self):
        return self._id_auto
    
    @id_auto.setter
    def id_auto(self, id_auto):
        self._id_auto = id_auto

    @property
    def pat_id(self):
        return self._pat_id
    
    @pat_id.setter
    def pat_id(self, pat_id):
        self._pat_id = pat_id

    @property
    def trano(self):
        return self._trano
    
    @trano.setter
    def trano(self, trano):
        self._trano = trano

    @property
    def datee(self):
        return self._datee
    
    @datee.setter
    def datee(self, datee):
        self._datee = datee

    @property
    def amount(self):
        return self._amount
    
    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def p_type(self):
        return self._p_type
    
    @p_type.setter
    def p_type(self, p_type):
        self._p_type = p_type

    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, balance):
        self._balance = balance

    @property
    def net_amount(self):
        return self._net_amount
    
    @net_amount.setter
    def net_amount(self, net_amount):
        self._net_amount = net_amount

    @property
    def status_pat(self):
        return self._status_pat
    
    @status_pat.setter
    def status_pat(self, status_pat):
        self._status_pat = status_pat

    @property
    def status_value(self):
        return self._status_value
    
    @status_value.setter
    def status_value(self, status_value):
        self._status_value = status_value

    @property
    def Coverage(self):
        return self._Coverage

    @Coverage.setter
    def Coverage(self, Coverage):
        self._Coverage = Coverage

    @property
    def inv_number(self):
        return self._inv_number
    
    @inv_number.setter
    def inv_number(self, inv_number):
        self._inv_number = inv_number

    @property
    def decount(self):
        return self._decount

    @decount.setter
    def decount(self, decount):
        self._decount = decount

    @property
    def PatCoverage(self):
        return self._PatCoverage
    
    @PatCoverage.setter
    def PatCoverage(self, PatCoverage):
        self._PatCoverage = PatCoverage

    @property
    def patCovValue(self):
        return self._patCovValue
    
    @patCovValue.setter
    def patCovValue(self, patCovValue):
        self._patCovValue = patCovValue

    @property
    def DiscountCompany(self):
        return self._DiscountCompany
    
    @DiscountCompany.setter
    def DiscountCompany(self, DiscountCompany):
        self._DiscountCompany = DiscountCompany


    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()

class ResultEntity(AbstractEntity):

    __slots__ = ('_id', '_restrano', '_reststno', '_reststname', '_result_val', '_resspecial', '_resorganisim', '_resdirectform', '_rescolonycount', '_pendding', '_Position_name', '_MICRO4', '_MICRO5', '_MICRO6', '_Approved', '_comment', '_Interpretation', '_tstprice', '_tstlocation', '_offRange', '_ViewComment', '_ViewInterpretation', '_SampleNo', '_testnumber', '_ReadyDate', '_sendPSM', '_subtestno', '_printed')

    def __init__(self):
        self._id = 0
        self._restrano = 0

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def restrano(self):
        return self._restrano
    
    @restrano.setter
    def restrano(self, restrano):
        self._restrano = restrano

    @property
    def reststno(self):
        return self._reststno
    
    @reststno.setter
    def reststno(self, reststno):
        self._reststno = reststno

    @property
    def reststname(self):
        return self._reststname
    
    @reststname.setter
    def reststname(self, reststname):
        self._reststname = reststname

    @property
    def result_val(self):
        return self._result_val
    
    @result_val.setter
    def result_val(self, result_val):
        self._result_val = result_val

    def hash_code(self):
        import hashlib
        hash_object = hashlib.md5(str(self._ID.value).encode())
        return hash_object.hexdigest()