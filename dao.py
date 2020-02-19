import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

#Sample select query

class FlimsImporterDAO():
    
    __slots__ = ('_flims_configurations', '_database_engine', '_database_schema', '_username', '_password', '_database_url', '_database_port', '_model_schema_name')
    # define 
    def __init__(self, flims_configurations, model_schema_name):
        self._flims_configurations = flims_configurations
        self._database_engine = flims_configurations["database_engine"]
        self._database_url = flims_configurations["database_host_url"]
        self._database_port = flims_configurations["database_port"]
        self._database_schema = flims_configurations["database_schema"]
        self._username = flims_configurations["database_username"]
        self._password = flims_configurations["database_password"]
        self._model_schema_name = model_schema_name


    def get_data(self):

        data_list = []

        def get_lab_departments(self):
            nonlocal data_list

            if(self._database_engine == "MSSQLServer2019"):
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._database_url+';DATABASE='+self._database_schema+';UID='+self._username+';PWD='+ self._password)
                cursor = cnxn.cursor()
                cursor.execute("SELECT id, catnumber, depname, prtname FROM IntegratedLAB.dbo.DepAndPrt;")
                row = cursor.fetchone()
                from flims_entities import LabDepartmentEntity, LabDepartmentManagerEntity

                while row:
                    labDepartmentEntity = LabDepartmentEntity()
                    labDepartmentEntity.title = row[2]
                    labDepartmentEntity.portal_type = "Department"
                    labDepartmentManagerEntity = LabDepartmentManagerEntity()
                    labDepartmentManagerEntity.title = self._flims_configurations["lab_contact_manager"]
                    labDepartmentEntity.Manager = labDepartmentManagerEntity
                    data_list.append(labDepartmentEntity)
                    row = cursor.fetchone()

        def get_analysis_categories(self):
            nonlocal data_list
        	
            if(self._database_engine == "MSSQLServer2019"):
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._database_url+';DATABASE='+self._database_schema+';UID='+self._username+';PWD='+ self._password)
                cursor = cnxn.cursor()
                cursor.execute("SELECT ID, CatNumber, catnumber_new, CatName, catshort, Orders, iscats, Catnumber_no, 'Initial_Dept' as department FROM IntegratedLAB.dbo.TestCats;")
                row = cursor.fetchone()
                from flims_entities import AnalysisCategoryEntity, LabDepartmentEntity
                while row:
                    analysisCategoryEntity = AnalysisCategoryEntity()
                    analysisCategoryEntity.title = row[3].strip()
                    analysisCategoryEntity.description = "Keyword: " + str(row[4]) + "\n" + "Category Number(old-new): (" + str(row[1]) + " - " + str(row[2]) + ")"
                    labDepartmentEntity = LabDepartmentEntity(None)
                    labDepartmentEntity.title = row[8]
                    analysisCategoryEntity.Department = labDepartmentEntity
                    data_list.append(analysisCategoryEntity)
                    row = cursor.fetchone()

        def get_analysis_services(self):
            nonlocal data_list
            
            if(self._database_engine == "MSSQLServer2019"):
                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._database_url+';DATABASE='+self._database_schema+';UID='+self._username+';PWD='+ self._password)
                cursor = cnxn.cursor()
                cursor.execute("SELECT lt.TstNumber, lt.testnumber, lt.Tstlabid, lt.TstName, tpf.testname, lt.tstshort, lt.CatNumber, tc.catnumber_new, tc.CatName, tpf.[2008min] AS MinPrice, tpf.[2008max] AS MaxPrice, lt.TstDuration, lt.Tstworknight, lt.TstResultType, lt.TstNotes, lt.TstSpecimal1, lt.TstSpecimal2, lt.tstorder FROM IntegratedLAB.dbo.LabTests lt FULL OUTER JOIN IntegratedLAB.dbo.TestCats AS tc ON lt.CatNumber = tc.catnumber_new FULL OUTER JOIN IntegratedLAB.dbo.Testspricefinal AS tpf ON lt.testnumber = tpf.Idno;")
                row = cursor.fetchone()
                from flims_entities import AnalysisServiceEntity, AnalysisCategoryEntity
                while row:
                    temp_description = ""
                    analysisServiceEntity = AnalysisServiceEntity()
                    if not (row[3] == None and row[4] == None):
                        if row[3] != None:
                            analysisServiceEntity.title = str(row[3])
                            if row[4] != None:
                                temp_description += "\nTitle: " + row[4]
                            else:
                                temp_description += "\nTitle: " + row[3]
                        else:
                            analysisServiceEntity.title = str(row[4])
                            temp_description += "\nTitle: " + row[4]

                        temp_description += "\n Test Number: " + str(row[0])
                        temp_description += "\n Test Number: " + str(row[1])
                        temp_description += "\n Test Lab ID: " + str(row[2])
                        analysisServiceEntity.Keyword = str(row[5] if row[5] is not None else "")
                        analysisCategoryEntity = AnalysisCategoryEntity(None)
                        analysisCategoryEntity.title = str(row[8] if row[8] is not None else "")
                        analysisServiceEntity.Category = analysisCategoryEntity
                        analysisServiceEntity.Price = str(row[10]) if row[10] is not None else "0"
                        analysisServiceEntity.MinPrice = str(row[9]) if row[9] is not None else "0"
                        analysisServiceEntity.description = temp_description
                        analysisServiceEntity.MaxTimeAllowed = row[11].strip() if row[11] is not None else "0"
                        data_list.append(analysisServiceEntity)
                    row = cursor.fetchone()

        def get_patients(self):
            nonlocal data_list
            if self._database_engine == "MSSQLServer2019":

                cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+self._database_url+';DATABASE='+self._database_schema+';UID='+self._username+';PWD='+ self._password)
                cursor = cnxn.cursor()
                cursor.execute("SELECT ID, PatNumber, PatName, PatarName, FORMAT (PatDateOfBirth, 'yyyy-MM-dd') as dateOfBirth, PatAge, Patday, PatSex, PatTelephone, PatMobile, PatFax, PatEmail, PatPOBox, PatLocation, PatNationality, PatProfesion, PatMaritalStatus, RefNumber, PatCredit, PatPOCode, PatReg, PatState, PatpClass, PatDiscount, Patsend, patnano, Patpassword, medInfo, macaddress, usernames, notess, med_free_txt, patregdate, PatRefranse, branch_code, UpdateData, ViewNote, patreferral, fromserver, status FROM IntegratedLAB.dbo.Patient;")
                row = cursor.fetchone()
                from utility import Utility
                from flims_entities import PatientEntity
                while row:
                    patientEntity = PatientEntity()
                    patientEntity.clientPatientID = row[1]
                    if row[7] == "Female":
                        patientEntity.salutation = "Mrs"
                    full_name = row[3].split()
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
                    patientEntity.gender = "male" if row[7] == "Male" else "female"
                    patientEntity.birthDate = row[4]
                    temp_birthdate = patientEntity.birthDate.split("-")
                    age = Utility.calculate_age(int(temp_birthdate[2]), int(temp_birthdate[1]), int(temp_birthdate[0]))
                    patientEntity.age_splitted_year = age[0]
                    patientEntity.age_splitted_month = age[1]
                    patientEntity.age_splitted_day = age[2]
                    patientEntity.countryState_country = row[14]
                    patientEntity.emailAddress = row[11]
                    patientEntity.homePhone = row[8]
                    patientEntity.mobilePhone = row[9]
                    patientEntity.civilStatus = row[16]

                    data_list.append(patientEntity)
                    row = cursor.fetchone()
            
        get_from_model = {
            'Lab_Department' : get_lab_departments,
            'Analysis_Category' : get_analysis_categories,
            'Analysis_Service' : get_analysis_services,
            'Patient' : get_patients
        }[self._model_schema_name](self)

        return data_list