from abc import ABC, abstractmethod
import requests
import json
import mechanize
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
import csv
import time
from utility import Utility
from flims_entities import LabDepartmentEntity, SampleTypeEntity, AnalysisCategoryEntity, AnalysisServiceEntity, DynamicAnalysisSpecEntity, PatientEntity, AnalysisRequestEntity
from pulled_entities import DepartmentEntity, TestCategoryEntity, TestEntity, TestResultTypeEntity, TestPriceEntity, PulledPatientEntity, TransAmountDetailsEntity, ResultEntity
from pulled_dao import DepartmentDAO, TestCategoryDAO, LabTestDAO, TestResultTypeDAO, TestPriceDAO, PatientDAO, TransAmountDetailsDAO, ResultDAO

class AbstractService(ABC):

    __slots__ = ('_importer_configurations')

    @abstractmethod
    def __init__(self, importer_configurations):
        self._importer_configurations = importer_configurations

    def generateAPIUrl(self):
        flims_configurations = self._importer_configurations["flims_configurations"]
        return "http://" + flims_configurations["server_ip"] + ":" + flims_configurations["server_port"] + "/" + flims_configurations["server_path"] + "/@@API/senaite/v1/"

    def generateBrowserUrl(self):
        flims_configurations = self._importer_configurations["flims_configurations"]
        return "http://" + flims_configurations["server_ip"] + ":" + flims_configurations["server_port"] + "/" + flims_configurations["server_path"] + "/"

    def loginByAPI(self):
        session = requests.Session()
        data = {"__ac_name": "admin", "__ac_password": "admin"}
        session.post(self.generateAPIUrl() + "users/login", data).text
        return session

    def loginByMechanizeBrowser(self):
        url = self.generateBrowserUrl() + "/login_form"
        browser = mechanize.Browser()
        browser._factory.is_html = True
        browser.set_handle_robots(False) # ignore robots
        browser.open(url)
        browser.select_form(id="login_form")
        browser["__ac_name"] = "admin"
        browser["__ac_password"] = "admin"
        browser.submit()
        return browser

    def loginBySeleniumBrowser(self):
        WINDOW_SIZE = "1920,1080"
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.implicitly_wait(3)
        driver.get(self.generateBrowserUrl() + "/login_form")
        driver.find_element_by_id("__ac_name").send_keys("admin")
        driver.find_element_by_id("__ac_password").send_keys("admin")
        driver.find_element_by_name("submit").click()

        return driver

class LabDepartmentService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importLabDepartments(self):
        departmentDAO = DepartmentDAO(self._importer_configurations["database_configurations"])
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        departmentEntityForSearch = DepartmentEntity()
        departmentsList = departmentDAO.searchDepartment(departmentEntityForSearch.getCriteriaDictionary())
        for departmentEntity in departmentsList:
            response = session.get(super().generateAPIUrl() +  "department?title=" + requests.utils.quote(departmentEntity.depname), headers = headers)
            if len(response.json()["items"]) == 0:
                labDepartmentEntity = LabDepartmentEntity()
                labDepartmentEntity.title = departmentEntity.depname
                labDepartmentEntity.Manager.title = self._importer_configurations["flims_configurations"]["lab_contact_manager"]
                session.post(super().generateAPIUrl() + "create", data = json.dumps(labDepartmentEntity.as_dictionary()), headers = headers)
            else:
                print("Error: Can't add department ", departmentEntity.depname, ", it is already exist.")

class DynamicAnalysisSpecService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importDynamicAnalysisSpecs(self):
        sampeTypesList = {}
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        with open('data/SampleTypes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sampleTypeEntity = SampleTypeEntity()
                    sampleTypeEntity.title = row[0].strip()
                    sampleTypeEntity.Prefix = sampleTypeEntity.title
                    sampleTypeEntity.MinimumVolume = "0 ml"
                    sampleTypeEntity.RetentionPeriod.days = 1
                    response = session.get(super().generateAPIUrl() +  "sampletype?title=" + requests.utils.quote(sampleTypeEntity.title), headers = headers)
                    if len(response.json()["items"]) == 0:
                        session.post(super().generateAPIUrl() + "create", data = json.dumps(sampleTypeEntity.as_dictionary()), headers = headers)
                    else:
                        print("Error: Can't add sample type ", sampleTypeEntity.title, ", it is already exist.")
                line_count += 1

class SampleTypeService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importSampleTypes(self):
        sampeTypesList = {}
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        with open('data/SampleTypes.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count != 0:
                    sampleTypeEntity = SampleTypeEntity()
                    sampleTypeEntity.title = row[0].strip()
                    sampleTypeEntity.Prefix = sampleTypeEntity.title
                    sampleTypeEntity.MinimumVolume = "0 ml"
                    sampleTypeEntity.RetentionPeriod.days = 1
                    response = session.get(super().generateAPIUrl() +  "sampletype?title=" + requests.utils.quote(sampleTypeEntity.title), headers = headers)
                    if len(response.json()["items"]) == 0:
                        session.post(super().generateAPIUrl() + "create", data = json.dumps(sampleTypeEntity.as_dictionary()), headers = headers)
                    else:
                        print("Error: Can't add sample type ", sampleTypeEntity.title, ", it is already exist.")
                line_count += 1

class AnalysisCategoryService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importAnalysisCategories(self):
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        testCategoryDAO = TestCategoryDAO(self._importer_configurations["database_configurations"])
        testCategoryEntityForSearch = TestCategoryEntity()
        testCategoriesList = testCategoryDAO.searchTestCategory(testCategoryEntityForSearch.getCriteriaDictionary())
        for testCategoryEntity in testCategoriesList:
            response = session.get(super().generateAPIUrl() +  "analysiscategory?title=" + requests.utils.quote(testCategoryEntity.CatName), headers = headers)
            if len(response.json()["items"]) == 0:
                analysisCategoryEntity = AnalysisCategoryEntity()
                analysisCategoryEntity.title = testCategoryEntity.CatName
                analysisCategoryEntity.Department.title = testCategoryEntity.CatName
                session.post(super().generateAPIUrl() + "create", data = json.dumps(analysisCategoryEntity.as_dictionary()), headers = headers)
            else:
                print("Error: Can't add analysis category ", testCategoryEntity.CatName, ", it is already exist.")

class AnalysisServiceService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importAnalysisServices(self):
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        testCategoryEntityForSearch = TestCategoryEntity()
        testCategoryDAO = TestCategoryDAO(self._importer_configurations["database_configurations"])
        testCategoriesList = testCategoryDAO.searchTestCategory(testCategoryEntityForSearch.getCriteriaDictionary())
        labTestDAO = LabTestDAO(self._importer_configurations["database_configurations"])
        testResultTypeDAO = TestResultTypeDAO(self._importer_configurations["database_configurations"])
        testPriceDAO = TestPriceDAO(self._importer_configurations["database_configurations"])
        testEntityForSearch = TestEntity()
        testResultTypeEntityForSearch = TestResultTypeEntity()
        testPriceEntityForSearch = TestPriceEntity()
        for testCategoryEntity in testCategoriesList:
            testEntityForSearch.CatNumber = testCategoryEntity.CatNumber
            testsList = labTestDAO.searchTests(testEntityForSearch.getCriteriaDictionary())
            for testEntity in testsList:
                testResultTypeEntityForSearch.testnumber = testEntity.testnumber
                testResultTypesList = testResultTypeDAO.searchTestsResultTypes(testResultTypeEntityForSearch.getCriteriaDictionary())
                testPriceEntityForSearch.Idno = testEntity.testnumber
                if(testEntity.testnumber < 200):
                    print (testEntity.getCriteriaDictionary())
                testsPricesList = testPriceDAO.searchTestPrices(testPriceEntityForSearch.getCriteriaDictionary())
                #
                analysisServiceEntity = AnalysisServiceEntity()
                analysisServiceEntity.title = testEntity.TstName
                analysisServiceEntity.description = ""
                analysisServiceEntity.Keyword = testEntity.tstshort
                response = session.get(super().generateAPIUrl() +  "analysiscategory?title=" + requests.utils.quote(testCategoryEntity.CatName.strip()), headers = headers)
                if len(response.json()["items"]) != 0:
                    analysisServiceEntity.Category = response.json()["items"][0]["uid"]
                if len(testResultTypesList) == 0:
                    print("Error")
                else:
                    testResultTypeEntity = testResultTypesList[0]
                    analysisServiceEntity.Unit = testResultTypeEntity.TstUnit.strip() if testResultTypeEntity.TstUnit is not None else ""

                if len(testsPricesList) == 0:
                    analysisServiceEntity.Price = 0
                    analysisServiceEntity.MaxPrice2008 = 0
                    analysisServiceEntity.MinPrice1995 = 0
                    analysisServiceEntity.MaxPrice1995 = 0
                    analysisServiceEntity.AssociationPrice = 0
                    analysisServiceEntity.LaboratoriesPrice = 0
                else:
                    testsPricesEntity = testsPricesList[0]
                    analysisServiceEntity.Price = testsPricesEntity.min2008 if testsPricesEntity.min2008 is not None else 0
                    analysisServiceEntity.MaxPrice2008 = testsPricesEntity.max2008 if testsPricesEntity.max2008 is not None else 0
                    analysisServiceEntity.MinPrice1995 = testsPricesEntity.min1995 if testsPricesEntity.min1995 is not None else 0
                    analysisServiceEntity.MaxPrice1995 = testsPricesEntity.max1995 if testsPricesEntity.max1995 is not None else 0
                    analysisServiceEntity.AssociationPrice = testsPricesEntity.jam if testsPricesEntity.jam is not None else 0
                    analysisServiceEntity.LaboratoriesPrice = testsPricesEntity.F9 if testsPricesEntity.F9 is not None else 0

                analysisServiceEntity.MaxTimeAllowed.days = testEntity.TstDuration.strip() if testEntity.TstDuration is not None else "0"
                analysisServiceEntity.MaxTimeAllowed.hours = testEntity.tstHrDuration.strip() if testEntity.tstHrDuration is not None else "0"
                analysisServiceEntity.Factor = 1
                print(analysisServiceEntity.as_dictionary())
                z = session.post(super().generateAPIUrl() + "create", data = json.dumps(analysisServiceEntity.as_dictionary()), headers = headers)
                print(z.text)

class AnalysisSpecificationService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importAnalysisSpecifications(self):
        subtest_sample_spec_dictionary = {}
        dynamic_spec_dictionary_by_gender_age = {}
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        testCategoryDAO = TestCategoryDAO(self._importer_configurations["database_configurations"])
        testCategoryEntityForSearch = TestCategoryEntity()
        testCategoriesList = testCategoryDAO.searchTestCategory(testCategoryEntityForSearch.getCriteriaDictionary())
        labTestDAO = LabTestDAO(self._importer_configurations["database_configurations"])
        testResultTypeDAO = TestResultTypeDAO(self._importer_configurations["database_configurations"])
        testEntityForSearch = TestEntity()
        testResultTypeEntityForSearch = TestResultTypeEntity()
        for testCategoryEntity in testCategoriesList:
            testEntityForSearch.CatNumber = testCategoryEntity.CatNumber
            testsList = labTestDAO.searchTests(testEntityForSearch.getCriteriaDictionary())
            for testEntity in testsList:
                testResultTypeEntityForSearch.testnumber = testEntity.testnumber
                testResultTypesList = testResultTypeDAO.searchTestsResultTypes(testResultTypeEntityForSearch.getCriteriaDictionary())
                #
                if testEntity.TstSpecimal1 is not None and testEntity.TstSpecimal1 != "":
                    if testEntity.TstSpecimal1 not in dynamic_spec_dictionary_by_gender_age.keys():
                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1] = {}

                    for testResultTypeEntity in testResultTypesList:
                        if testResultTypeEntity.Tstgender is not None:
                            if testResultTypeEntity.Tstgender == "word":
                                continue
                            elif testResultTypeEntity.Tstgender == "Both" or testResultTypeEntity.Tstgender == "Male" or testResultTypeEntity.Tstgender == "Female":
                                age_in = "Year"
                                age_from = 0
                                age_to = 0
                                if testResultTypeEntity.tstdayfrom == "Day":
                                    age_from = round(float(testResultTypeEntity.Tstagefrom) / 365.0, 3)
                                elif testResultTypeEntity.tstdayfrom == "Month":
                                    age_from = round(float(testResultTypeEntity.Tstagefrom) / 12.0, 3)
                                elif testResultTypeEntity.tstdayfrom == "Year":
                                    age_from = round(float(testResultTypeEntity.Tstagefrom), 3)

                                if testResultTypeEntity.Tstdayto == "Day":
                                    age_to = round(float(testResultTypeEntity.Tstageto) / 365.0, 3)
                                elif testResultTypeEntity.Tstdayto == "Month":
                                    age_to = round(float(testResultTypeEntity.Tstageto) / 12.0, 3)
                                elif testResultTypeEntity.Tstdayto == "Year":
                                    age_to = round(float(testResultTypeEntity.Tstageto), 3)

                                minimum = 0
                                maximum = 0
                                if testResultTypeEntity.TstNormalFrom is not None and testResultTypeEntity.TstNormalFrom != "":
                                    testResultTypeEntity.TstNormalFrom = testResultTypeEntity.TstNormalFrom.replace(',', '')
                                    if testResultTypeEntity.TstNormalFrom.find("/") != -1:
                                        numerator = testResultTypeEntity.TstNormalFrom.split("/")[0]
                                        denominator = testResultTypeEntity.TstNormalFrom.split("/")[1]
                                        minimum = float(numerator) / float(denominator)
                                    elif not re.search("[A-Za-z<>:.].*", testResultTypeEntity.TstNormalFrom):
                                        minimum = float(testResultTypeEntity.TstNormalFrom)

                                if testResultTypeEntity.TstNormalTo is not None and testResultTypeEntity.TstNormalTo != "":
                                    testResultTypeEntity.TstNormalTo = testResultTypeEntity.TstNormalTo.replace(',', '')
                                    if testResultTypeEntity.TstNormalTo.find("/") != -1:
                                        numerator = testResultTypeEntity.TstNormalTo.split("/")[0]
                                        denominator = testResultTypeEntity.TstNormalTo.split("/")[1]
                                        maximum = float(numerator) / float(denominator)
                                    elif not re.search("[A-Za-z<>:.].*", testResultTypeEntity.TstNormalTo):
                                        maximum = float(testResultTypeEntity.TstNormalTo)
                            
                                gendersList = []
                                if testResultTypeEntity.Tstgender == "Both":
                                    gendersList = ["Male", "Female"]
                                elif testResultTypeEntity.Tstgender == "Male":
                                    gendersList = ["Male"]
                                elif testResultTypeEntity.Tstgender == "Female":
                                    gendersList = ["Female"]

                                for gender in gendersList:
                                    key = str(testEntity.tstshort) + gender + str(age_from) + str(age_to) + str(minimum) + str(maximum)
                                    if key not in dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1].keys():
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key] = DynamicAnalysisSpecEntity()
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].Keyword = testEntity.tstshort
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].Gender = gender
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].Age_From = age_from
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].Age_To = age_to
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].min = minimum
                                        dynamic_spec_dictionary_by_gender_age[testEntity.TstSpecimal1][key].max = maximum

                            elif testResultTypeEntity.Tstgender == "Spetial":
                                continue
        csvHeader = ["Keyword", "Gender", "Age_From", "Age_To", "min", "max"]
        for key in dynamic_spec_dictionary_by_gender_age:
            file_name = key.replace(',', '')
            file_name = file_name.replace('+', '')
            file_name = file_name.replace('/', ' ')
            f = open("data/" + file_name + '.csv', 'w')
            with f:
                writer = csv.writer(f)
                writer.writerow(csvHeader)
                print(dynamic_spec_dictionary_by_gender_age[key])
                for key2 in dynamic_spec_dictionary_by_gender_age[key]:
                    print(dynamic_spec_dictionary_by_gender_age[key][key2].getDataAsList())
                    writer.writerow(dynamic_spec_dictionary_by_gender_age[key][key2].getDataAsList())
        #print(dynamic_spec_dictionary_by_gender_age)
        return dynamic_spec_dictionary_by_gender_age

class PatientService(AbstractService):

    def __init__(self, importer_configurations):
        super().__init__(importer_configurations)

    def importPatients(self):
        session = super().loginByAPI()
        headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
        response = session.get(super().generateAPIUrl() + "client?title=" + self._importer_configurations["flims_configurations"]["client_name"], headers = headers)
        if response.json()["items"][0] == 0:
            print("Error: Client ", importer_configurations["client_name"], " was not found. Please be sure to create one or check the spelling. \
                \n Client is required to assign patients to it. Importing patients process will be terminated." )
        else:
            testCategoryDAO = TestCategoryDAO(self._importer_configurations["database_configurations"])
            testCategoryEntityForSearch = TestCategoryEntity()
            testCategoriesList = testCategoryDAO.searchTestCategory(testCategoryEntityForSearch.getCriteriaDictionary())
            testCategoriesMapByID = {}
            for testCategoryEntity in testCategoriesList:
                if testCategoryEntity not in testCategoriesMapByID:
                    testCategoriesMapByID[testCategoryEntity.CatNumber] = testCategoryEntity
            print (testCategoriesMapByID)
            labTestDAO = LabTestDAO(self._importer_configurations["database_configurations"])
            testEntityForSearch = TestEntity()
            testEntityForSearch.ShowPreviousresult = 1
            testsList = labTestDAO.searchTests(testEntityForSearch.getCriteriaDictionary())
            testsToShowHistory = {}
            for testEntity in testsList:
                if testEntity.tstshort not in testsToShowHistory:
                    testsToShowHistory[testEntity.tstshort] = testEntity
            print (len(testsToShowHistory))
            patientDAO = PatientDAO(self._importer_configurations["database_configurations"])
            transAmountDetailsDAO = TransAmountDetailsDAO(self._importer_configurations["database_configurations"])
            resultDAO = ResultDAO(self._importer_configurations["database_configurations"])
            pulledPatientsList = patientDAO.searchPatients()
            for pulledPatientEntity in pulledPatientsList:
                #
                patientEntity = PatientEntity()
                patientEntity.clientPatientID = str(patientEntity.clientPatientID) + "" + str(pulledPatientEntity.PatNumber)
                full_name = ""
                if pulledPatientEntity.PatarName == '':
                    full_name = pulledPatientEntity.PatName.split()
                else:
                    full_name = pulledPatientEntity.PatarName.split()
                if len(full_name) == 1:
                    patientEntity.firstname = full_name[0]
                elif len(full_name) == 2:
                    patientEntity.firstname = full_name[0]
                    patientEntity.surname = full_name[1]
                elif len(full_name) == 3:
                    patientEntity.firstname = full_name[0]
                    patientEntity.middlename = full_name[1]
                    patientEntity.surname = full_name[2]
                elif len(full_name) == 4:
                    patientEntity.firstname = full_name[0]
                    patientEntity.middlename = full_name[1] + " " + full_name[2]
                    patientEntity.surname = full_name[3]
                elif len(full_name) == 5:
                    patientEntity.firstname = full_name[0]
                    patientEntity.middlename = full_name[1] + " " + full_name[2] + " " + full_name[3]
                    patientEntity.surname = full_name[4]
                elif len(full_name) == 6:
                    patientEntity.firstname = full_name[0]
                    patientEntity.middlename = full_name[1] + " " + full_name[2] + " " + full_name[3]
                    patientEntity.surname = full_name[4] + " " + full_name[5]
                if pulledPatientEntity.PatSex == "Male":
                    patientEntity.salutation = "Mr"
                    patientEntity.gender = "male"
                elif pulledPatientEntity.PatSex == "Female":
                    patientEntity.salutation = "Mrs"
                    patientEntity.gender = "female"
                patientEntity.birthDate = pulledPatientEntity.PatDateOfBirth
                temp_birthdate = patientEntity.birthDate.split("-")
                age = Utility.calculate_age(int(temp_birthdate[2]), int(temp_birthdate[1]), int(temp_birthdate[0]))
                patientEntity.age_splitted_year = age[0]
                patientEntity.age_splitted_month = age[1]
                patientEntity.age_splitted_day = age[2]
                patientEntity.emailAddress = pulledPatientEntity.PatEmail
                patientEntity.homePhone = pulledPatientEntity.PatTelephone
                patientEntity.mobilePhone = pulledPatientEntity.PatMobile
                patientEntity.civilStatus = pulledPatientEntity.PatMaritalStatus

                #analysisRequestsList = []
                transAmountDetailsEntityForSearch = TransAmountDetailsEntity()
                transAmountDetailsEntityForSearch.pat_id = pulledPatientEntity.PatNumber
                transAmountDetailsList = transAmountDetailsDAO.searchTransAmountDetails(transAmountDetailsEntityForSearch.getCriteriaDictionary())
                for transAmountDetailsEntity in transAmountDetailsList:
                    if patientEntity.PatientCoverageRate < transAmountDetailsEntity.PatCoverage:
                        patientEntity.PatientCoverageRate = transAmountDetailsEntity.PatCoverage
                driver = super().loginBySeleniumBrowser()
                driver.get(super().generateBrowserUrl() + "patients/createObject?type_name=Patient")
                driver.find_element_by_id('PrimaryReferrer').send_keys(patientEntity.primaryReferrer)
                time.sleep(1)                
                driver.find_element_by_id('PrimaryReferrer').send_keys(Keys.TAB)
                driver.find_element_by_id('PrimaryReferrer').send_keys(Keys.TAB)
                driver.find_element_by_id('ClientPatientID').send_keys(patientEntity.clientPatientID);
                driver.find_element_by_id('Salutation').send_keys(patientEntity.salutation)
                driver.find_element_by_id('Firstname').send_keys(patientEntity.firstname)
                driver.find_element_by_id('Middleinitial').send_keys(patientEntity.middleinitial)
                driver.find_element_by_id('Middlename').send_keys(patientEntity.middlename)
                driver.find_element_by_id('Surname').send_keys(patientEntity.surname)
                time.sleep(1)
                driver.find_element_by_id('Gender').send_keys(patientEntity.gender)
                driver.find_element_by_id('Gender').click()
                driver.find_element_by_id('BirthDate').send_keys(patientEntity.birthDate)
                driver.find_element_by_id('BirthDate').send_keys(Keys.TAB)
                driver.find_element_by_id('CountryState.country').send_keys(patientEntity.countryState_country)
                driver.find_element_by_id('CountryState.country').click()
                driver.find_element_by_id('CountryState.state').send_keys(patientEntity.countryState_state)
                driver.find_element_by_id('CountryState.state').click()
                driver.find_element_by_id('fieldsetlegend-personal').click()
                driver.find_element_by_id('EmailAddress').send_keys(patientEntity.emailAddress)
                driver.find_element_by_id('HomePhone').send_keys(patientEntity.homePhone)
                driver.find_element_by_id('MobilePhone').send_keys(patientEntity.mobilePhone)
                driver.find_element_by_id('CivilStatus').send_keys(patientEntity.civilStatus)
                driver.find_element_by_name('form.button.save').click()

                for transAmountDetailsEntity in transAmountDetailsList:
                    resultEntityForSearch = ResultEntity()
                    resultEntityForSearch.restrano = transAmountDetailsEntity.trano
                    resultsList = resultDAO.searchResults(resultEntityForSearch.getCriteriaDictionary())
                    for resultEntity in resultsList:
                        analysisRequestEntity = AnalysisRequestEntity()
                        analysisRequestEntity.Client = patientEntity.primaryReferrer
                        analysisRequestEntity.Contact = self._importer_configurations["flims_configurations"]["lab_contact_manager"]
                        if pulledPatientEntity.PatarName == '':
                            analysisRequestEntity.Patient = pulledPatientEntity.PatName
                        else:
                            analysisRequestEntity.Patient = pulledPatientEntity.PatarName
                        analysisRequestEntity.DateSampled = transAmountDetailsEntity.datee
                        #analysisRequestEntity.InternalUse = "checked"
                        analysisRequestEntity.SampleType = testsToShowHistory[resultEntity.reststname].TstSpecimal1
                        analysisRequestEntity.ClientSampleID = resultEntity.reststname

                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/ar_add?ar_count=1")
                        driver.find_element_by_id('Patient-0').send_keys(patientEntity.clientPatientID)
                        time.sleep(1)
                        driver.find_element_by_id('Patient-0').send_keys(Keys.TAB)
                        time.sleep(1)
                        driver.find_element_by_id('DateSampled-0').send_keys(analysisRequestEntity.DateSampled)
                        driver.find_element_by_id('DateSampled-0').send_keys(Keys.TAB)
                        driver.find_element_by_id('SampleType-0').send_keys(analysisRequestEntity.SampleType)
                        time.sleep(2)
                        # driver.find_element_by_id('SampleType-0').send_keys(Keys.DOWN)
                        driver.find_element_by_id('SampleType-0').send_keys(Keys.ENTER)
                        driver.find_element_by_id('SampleType-0').send_keys(Keys.TAB)
                        time.sleep(2)
                        driver.find_element_by_id('ClientSampleID-0').send_keys(analysisRequestEntity.ClientSampleID)
                        #driver.find_element_by_id('SampleType-0').click()
                        driver.find_element_by_id('analyses-list').click()
                        time.sleep(2)
                        print ("Category name: ", testCategoriesMapByID[str(testsToShowHistory[resultEntity.reststname].CatNumber)].CatName)
                        response2 = session.get(super().generateAPIUrl() + "analysiscategory?title=" + requests.utils.quote(testCategoriesMapByID[str(testsToShowHistory[resultEntity.reststname].CatNumber)].CatName), headers = headers)

                        driver.find_element_by_id(response2.json()["items"][0]["id"]).click()
                        response2 = session.get(super().generateAPIUrl() + "analysisservice?title=" + requests.utils.quote(testsToShowHistory[resultEntity.reststname].TstName), headers = headers)
                        analysis_service_title = 'cb_0_' + response2.json()["items"][0]["uid"]
                        print (analysis_service_title)
                        driver.find_element_by_id(analysis_service_title).click()
                        time.sleep(3)
                        driver.find_element_by_name('save_button').click()
                        time.sleep(3)
                        #print (driver.current_url)
                        temp = driver.find_element_by_id("status_message").text
                        sample_id = temp[7:-26]
                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/" + sample_id + "/base_view")
                        print (driver.current_url)
                        driver.find_element_by_id("plone-contentmenu-workflow").click()
                        driver.find_element_by_id("workflow-transition-receive").click()
                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/" + sample_id + "/base_view")
                        print(driver.find_element_by_id("archetypes-fieldname-Contact").get_attribute("data-uid"))
                        response2 = session.get(super().generateAPIUrl() + "analysis/" + requests.utils.quote(driver.find_element_by_id("archetypes-fieldname-Contact").get_attribute("data-uid")), headers = headers)
                        vv = "Result." + response2.json()["items"][0]["Analyses"][0]["uid"] + ":records"
                        driver.find_element_by_name(vv).send_keys(resultEntity.result_val)
                        time.sleep(1)
                        driver.find_element_by_id("ajax_save_selection").click()
                        time.sleep(2)
                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/" + sample_id + "/base_view")
                        driver.find_element_by_name("uids:list").click()
                        time.sleep(1)
                        driver.find_element_by_id("submit_transition").click()
                        time.sleep(1)
                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/" + sample_id + "/base_view")
                        driver.find_element_by_name("uids:list").click()
                        time.sleep(1)
                        driver.find_element_by_id("verify_transition").click()
                        time.sleep(1)
                        driver.get(super().generateBrowserUrl() + "clients/" + response.json()["items"][0]["id"] + "/" + sample_id + "/base_view")
                        time.sleep(1)
                        driver.find_element_by_id("plone-contentmenu-workflow").click()
                        driver.find_element_by_id("workflow-transition-publish").click()
                        time.sleep(1)
                        driver.get(driver.current_url)
                        time.sleep(3)
                        driver.find_element_by_name("save").click()
                        time.sleep(3)