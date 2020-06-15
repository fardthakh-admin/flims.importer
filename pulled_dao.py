import pyodbc
from utility import Utility
from flims_entities import LabDepartmentManagerEntity, AnalysisCategoryEntity
from pulled_entities import DepartmentEntity, TestCategoryEntity, TestEntity, TestResultTypeEntity, TestPriceEntity, TestPriceEntity2, PulledPatientEntity, TransAmountDetailsEntity, ResultEntity
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

#Sample select query

from abc import ABC, abstractmethod

class AbstractDAO(ABC):
    
    __slots__ = ('_flims_configurations', '_database_engine', '_database_schema', '_username', '_password', '_database_url', '_database_port')#, '_model_schema_name')

    @abstractmethod
    def __init__(self, flims_configurations):
        self._flims_configurations = flims_configurations
        self._database_engine = flims_configurations["database_engine"]
        self._database_url = flims_configurations["database_host_url"]
        self._database_port = flims_configurations["database_port"]
        self._database_name = flims_configurations["database_name"]
        self._database_schema = flims_configurations["database_schema"]
        self._username = flims_configurations["database_username"]
        self._password = flims_configurations["database_password"]
        #self._model_schema_name = model_schema_name

    def getConnection(self):
        if(self._database_engine == "MSSQLServer2019"):
            return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._database_url+';DATABASE='+self._database_name+';UID='+self._username+';PWD='+ self._password)

    def generateWhereClause(self, defaultCriteriaDictionary, criteriaDictionary):
        whereClause = ""
        for criteria, defaultValue in defaultCriteriaDictionary.items():
            #print(criteria, criteriaDictionary[criteria])
            if(criteriaDictionary[criteria] != defaultValue):
                whereClause += " and " + criteria[1:] + " = " + str(criteriaDictionary[criteria])
        return whereClause

class DepartmentDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchDepartment(self, criteriaDictionary):
        departmentsList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, CatNumber, catnumber_new, CatName, catshort, Orders, iscats, Catnumber_no FROM IntegratedLAB.dbo.TestCats WHERE 1=1 "
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((DepartmentEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += ";"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                if row[1].strip().find("_") == -1:
                    departmentEntity = DepartmentEntity()
                    departmentEntity.id = row[1].strip()
                    departmentEntity.depname = row[3].strip()
                    departmentsList.append(departmentEntity)
                row = cursor.fetchone()
        return departmentsList

class TestCategoryDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTestCategory(self, criteriaDictionary):
        testCategoriesList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, CatNumber, catnumber_new, CatName, catshort, Orders, iscats, Catnumber_no FROM IntegratedLAB.dbo.TestCats"
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((TestCategoryEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += ";"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                if row[1].strip().find("_") == -1:
                    testCategoryEntity = TestCategoryEntity()
                    testCategoryEntity.CatNumber = row[1].strip()
                    testCategoryEntity.CatName = row[3].strip()
                    testCategoriesList.append(testCategoryEntity)
                row = cursor.fetchone()
        return testCategoriesList

class LabTestDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTests(self, criteriaDictionary):
        testsList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, TstNumber, testnumber, Tstlabid, TstName, tstshort, CatNumber, TstDuration, tstHrDuration, TstResultType, TstNotes, TstSpecimal1, TstSpecimal2, tstdword, testDesc, resulttype, testEquation, ShowPreviousresult FROM IntegratedLAB.dbo.LabTests WHERE 1 = 1" + super().generateWhereClause((TestEntity()).getCriteriaDictionary(), criteriaDictionary) + ";"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                testEntity = TestEntity()
                testEntity.ID = row[0]
                testEntity.TstNumber = row[1].strip()
                testEntity.testnumber = row[2]
                testEntity.Tstlabid = row[3].strip()
                testEntity.TstName = row[4].strip()
                testEntity.tstshort = row[5].strip()
                testEntity.CatNumber = row[6]
                testEntity.TstDuration = row[7].strip() if row[7] is not None else "0"
                testEntity.tstHrDuration = row[8].strip() if row[8] is not None else "0"
                testEntity.TstResultType = row[9].strip()
                testEntity.TstNotes = row[10].strip() if row[10] is not None else ""
                testEntity.TstSpecimal1 = row[11].strip() if row[11] is not None else ""
                testEntity.TstSpecimal2 = row[12].strip() if row[12] is not None else ""
                testEntity.tstdword = row[13].strip() if row[13] is not None else ""
                testEntity.testDesc = row[14].strip() if row[14] is not None else ""
                testEntity.resulttype = row[15].strip()
                testEntity.testEquation = row[16].strip() if row[16] is not None else ""
                testEntity.ShowPreviousresult = row[17] if row[17] is not None else 0
                testsList.append(testEntity)
                row = cursor.fetchone()
        return testsList

class TestResultTypeDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTestsResultTypes(self, criteriaDictionary):
        testResultTypesList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, TstNumber, testnumber, Tstgender, Tstagefrom, tstdayfrom, Tstageto, Tstdayto, Tstprefix, TstNormalFrom, TstNormalTo, Tstsufix, TstWord, TstDword, TstUnit, Tstfactor, Tstfacunit FROM IntegratedLAB.dbo.TestsResultTypes WHERE 1 = 1"
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((TestResultTypeEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += ";"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                testResultTypeEntity = TestResultTypeEntity()
                testResultTypeEntity.ID = row[0]
                testResultTypeEntity.TstNumber = row[1].strip()
                testResultTypeEntity.testnumber = row[2]
                testResultTypeEntity.Tstgender = row[3].strip() if row[3] is not None else ""
                testResultTypeEntity.Tstagefrom = row[4] if row[4] is not None else 0
                testResultTypeEntity.tstdayfrom = row[5].strip() if row[5] is not None else ""
                testResultTypeEntity.Tstageto = row[6] if row[6] is not None else 0
                testResultTypeEntity.Tstdayto = row[7].strip() if row[7] is not None else ""
                testResultTypeEntity.Tstprefix = row[8].strip() if row[8] is not None else ""
                testResultTypeEntity.TstNormalFrom = row[9].strip() if row[9] is not None else ""
                testResultTypeEntity.TstNormalTo = row[10].strip() if row[10] is not None else ""
                testResultTypeEntity.Tstsufix = row[11].strip() if row[11] is not None else ""
                testResultTypeEntity.TstWord = row[12].strip() if row[12] is not None else ""
                testResultTypeEntity.TstDword = row[13].strip() if row[13] is not None else ""
                testResultTypeEntity.TstUnit = row[14].strip() if row[14] is not None else ""
                testResultTypeEntity.Tstfactor = row[15] if row[15] is not None else 0
                testResultTypeEntity.Tstfacunit = row[16].strip() if row[16] is not None else ""
                testResultTypesList.append(testResultTypeEntity)
                row = cursor.fetchone()
        return testResultTypesList

class TestPriceDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTestPrices(self, criteriaDictionary):
        testsPricesList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT Idno, testname, [1995max] as max1995, [1995min] as min1995, [2008min] as min2008, [2008max] as max2008, F9, jam FROM IntegratedLAB.dbo.Testspricefinal WHERE 1 = 1"
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((TestPriceEntity()).getCriteriaDictionary(), criteriaDictionary) 
            selectStatement += ";"
            print (selectStatement)
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                testPriceEntity = TestPriceEntity()
                if row[1] != None:
                    testPriceEntity.Idno = row[0]
                    testPriceEntity.testname = row[1]
                    testPriceEntity.max1995 = str(row[2])
                    testPriceEntity.min1995 = str(row[3])
                    testPriceEntity.min2008 = str(row[4])
                    testPriceEntity.max2008 = str(row[5])
                    testPriceEntity.F9 = str(row[6])
                    testPriceEntity.jam = str(row[7])
                    testsPricesList.append(testPriceEntity)
                row = cursor.fetchone()
        return testsPricesList

class TestPriceDAO2(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTestPrices(self, criteriaDictionary):
        testsPricesList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, TstNumber, testnumber, TstPrice, PriceCatID FROM IntegratedLAB.dbo.TestPrices WHERE 1 = 1" + super().generateWhereClause((TestPriceEntity2()).getCriteriaDictionary(), criteriaDictionary) + ";"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                testPriceEntity = TestPriceEntity2()
                if row[2] != None:
                    testPriceEntity.ID = row[0]
                    testPriceEntity.TstNumber = row[1]
                    testPriceEntity.testname = row[2]
                    testPriceEntity.TstPrice = row[3]
                    testPriceEntity.PriceCatID = row[4]
                    testsPricesList.append(testPriceEntity)
                row = cursor.fetchone()
        return testsPricesList

class PatientDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchPatients(self, criteriaDictionary = None):
        patientsList = []
        if (self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT ID, PatNumber, PatName, PatarName, FORMAT (PatDateOfBirth, 'yyyy-MM-dd') as PatDateOfBirth, PatSex, PatTelephone, PatMobile, PatEmail, PatMaritalStatus FROM IntegratedLAB.dbo.Patient WHERE 1 = 1 "
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((PulledPatientEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += " ORDER BY PatNumber"
            selectStatement += " OFFSET 60 ROWS FETCH NEXT 7000 ROWS ONLY;"
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                pulledPatientEntity = PulledPatientEntity()
                pulledPatientEntity.ID = row[0]
                pulledPatientEntity.PatNumber = row[1]
                pulledPatientEntity.PatName = row[2].strip() if row[2] is not None else ""
                pulledPatientEntity.PatarName = row[3].strip() if row[3] is not None else ""
                pulledPatientEntity.PatDateOfBirth = row[4]
                pulledPatientEntity.PatSex = row[5].strip() if row[5] is not None else ""
                pulledPatientEntity.PatTelephone = row[6].strip() if row[6] is not None else ""
                pulledPatientEntity.PatMobile = row[7].strip() if row[7] is not None else ""
                pulledPatientEntity.PatEmail = row[8].strip() if row[8] is not None else ""
                pulledPatientEntity.PatMaritalStatus = row[9].strip() if row[9] is not None else ""

                patientsList.append(pulledPatientEntity)
                row = cursor.fetchone()
        return patientsList

class TransAmountDetailsDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchTransAmountDetails(self, criteriaDictionary = None):
        transAmountDetailsList = []
        if (self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT id_auto, pat_id, trano, FORMAT (datee, 'yyyy-MM-dd HH:MM') as datee, amount, p_type, balance, net_amount, status_pat, status_value, Coverage, inv_number, decount, PatCoverage, patCovValue, DiscountCompany FROM IntegratedLAB.dbo.trans_amount_details WHERE 1 = 1 and deleted IN (0) "
            print (criteriaDictionary)
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((TransAmountDetailsEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += " ORDER BY trano"
            #selectStatement += " OFFSET 4 ROWS FETCH NEXT 10 ROWS ONLY;"
            print (selectStatement)
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                transAmountDetailsEntity = TransAmountDetailsEntity()
                transAmountDetailsEntity.id_auto = row[0]
                transAmountDetailsEntity.pat_id = row[1]
                transAmountDetailsEntity.trano = row[2]
                transAmountDetailsEntity.datee = row[3].strip()
                transAmountDetailsEntity.amount = row[4]
                transAmountDetailsEntity.p_type = row[5] if row[5] is not None else 0
                transAmountDetailsEntity.balance = row[6] if row[6] is not None else 0
                transAmountDetailsEntity.net_amount = row[7] if row[7] is not None else 0
                transAmountDetailsEntity.status_pat = row[8] if row[8] is not None else 0
                transAmountDetailsEntity.status_value = row[9] if row[9] is not None else 0
                transAmountDetailsEntity.Coverage = row[10] if row[10] is not None else 0.0
                transAmountDetailsEntity.inv_number = row[11] if row[11] is not None else 0
                transAmountDetailsEntity.decount = row[12] if row[12] is not None else 0.0
                transAmountDetailsEntity.PatCoverage = row[13] if row[13] is not None else 0.0
                if transAmountDetailsEntity.PatCoverage == -1:
                    transAmountDetailsEntity.PatCoverage = 0
                transAmountDetailsEntity.patCovValue = row[14] if row[14] is not None else 0.0
                transAmountDetailsEntity.DiscountCompany = row[15] if row[15] is not None else 0.0
                transAmountDetailsList.append(transAmountDetailsEntity)
                row = cursor.fetchone()
        return transAmountDetailsList

class ResultDAO(AbstractDAO):

    def __init__(self, flims_configurations):
        super().__init__(flims_configurations)

    def searchResults(self, criteriaDictionary):
        resultsList = []
        if(self._database_engine == "MSSQLServer2019"):
            con = super().getConnection()
            cursor = con.cursor()
            selectStatement = "SELECT id, restrano, reststno, reststname, result_val, resunit, restxt, resspecial, resorganisim, resdirectform, rescolonycount, reskitid, resprofile, resorder, ressemen, gp, pendding, group1, Namegroup, Position_name, MICRO4, MICRO5, MICRO6, SelReportForm, Approved, ChildVisable, confirm_level1, user_level1, confirm_level2, user_level2, depno, comment, Interpretation, tstprice, tstlocation, offRange, ViewComment, ViewInterpretation, SampleNo, testnumber, ReadyDate, sendPSM, subtestno, printed FROM IntegratedLAB.dbo.[Result] WHERE 1 = 1 "
            if criteriaDictionary != None:
                selectStatement += super().generateWhereClause((ResultEntity()).getCriteriaDictionary(), criteriaDictionary)
            selectStatement += " AND reststname in (SELECT tstshort FROM IntegratedLAB.dbo.LabTests WHERE ShowPreviousresult IN (1)) AND TRIM(result_val) NOT LIKE '' AND result_val IS NOT NULL AND result_val NOT LIKE '%[A-Z]%' AND result_val NOT LIKE '%[:]%' AND result_val NOT LIKE '%[<]%' AND result_val NOT LIKE '%[>]%' AND result_val NOT LIKE '%[+]%' AND result_val NOT LIKE '%[-]%'"
            selectStatement += " ORDER BY id"
            selectStatement += " ;"
            print (selectStatement)
            cursor.execute(selectStatement)
            row = cursor.fetchone()
            while row:
                resultEntity = ResultEntity()
                resultEntity.id = row[0]
                resultEntity.restrano = row[1]
                resultEntity.reststno = row[2].strip() if row[2] is not None else ""
                resultEntity.reststname = row[3].strip() if row[3] is not None else ""
                resultEntity.result_val = row[4].strip() if row[4] is not None else ""
                resultsList.append(resultEntity)
                row = cursor.fetchone()
        return resultsList