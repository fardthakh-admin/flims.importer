import flims_zodb_dao as FLIMS_DAO

flims_configurations = {
    "database_engine" : "MSSQLServer2019",
    "database_host_url" : "localhost",
    "database_port" : "1433",
    "database_username" : "sa",
    "database_password" : "123456",
    "database_schema" : "IntegratedLAB",
    "lab_contact_manager" : "Ayman Abu Awwad",
    "client_name" : "GenoLab",
    "flims_system_ip" : "localhost",
    "flims_system_port" : "8080",
    "flims_system_path" : "flims"
    }

def config_flims(operation, **kwargs):

    def set_database_engine(**kwargs):
        for key, value in kwargs.items():
            if (key == "database_engine"):
                flims_configurations["database_engine"] = value

    def set_database_connection_settings():
        print ("Database Connection Settings:")
        flims_configurations["database_host_url"] = input('Host(URL): ')
        flims_configurations["database_port"] = input('Port: ')
        flims_configurations["database_username"] = input('Username: ')
        flims_configurations["database_password"] = input('Password: ')

    def set_flims_system_server_configurations():
        print ("FLIMS System Server Config:")
        flims_configurations["flims_system_ip"] = input('Server IP: ')
        flims_configurations["flims_system_port"] = input('Server Port: ')
        flims_configurations["flims_system_path"] = input('FLIMS web path: ')

    def set_client_name():
        flims_configurations["client_name"] = input('Enter Client Name: ')

    def set_lab_contact_manager():
        flims_configurations["lab_contact_manager"] = input('Enter LabContact Manager Full Name: ')

    def get_flims_configurations():
        for k, v in flims_configurations.items():
            print(k, ":", v)
        print("\n\n")

    # map the inputs to the function blocks
    config_type = {
        'database_engine' : set_database_engine,
        'database_connection_settings' : set_database_connection_settings,
        'flims_system_server_configurations' : set_flims_system_server_configurations,
        'lab_contact_manager' : set_lab_contact_manager,
        'get_flims_configurations' : get_flims_configurations
    }[operation](**kwargs)        

def flims_services(operation, **kwargs):

    def import_lab_departments():
        print ("importing lab departments...\n")
        from dao import FlimsImporterDAO
        flimsImporterDAO = FlimsImporterDAO(flims_configurations, "Lab_Department")
        labDepartmentsList = flimsImporterDAO.get_data()
        from flims_entities import LabDepartmentEntity, LabDepartmentManagerEntity
        labDepartmentEntity = LabDepartmentEntity()
        labDepartmentEntity.title = "Initial_Dept"
        labDepartmentEntity.portal_type = "Department"
        labDepartmentManagerEntity = LabDepartmentManagerEntity()
        labDepartmentManagerEntity.title = flims_configurations["lab_contact_manager"]
        labDepartmentEntity.Manager = labDepartmentManagerEntity
        labDepartmentsList.append(labDepartmentEntity)
        FLIMS_DAO.insert_lab_department(labDepartmentsList, flims_configurations)

    def import_analysis_categories():
        print ("importing lab departments...\n")
        from dao import FlimsImporterDAO
        flimsImporterDAO = FlimsImporterDAO(flims_configurations, "Analysis_Category")
        analysisCategoriesList = flimsImporterDAO.get_data()
        from flims_entities import AnalysisCategoryEntity, LabDepartmentEntity
        analysisCategoryEntity = AnalysisCategoryEntity()
        analysisCategoryEntity.title = "Initial_Analysis_Category"
        labDepartmentEntity = LabDepartmentEntity(None)
        labDepartmentEntity.title = "Initial_Dept"
        analysisCategoryEntity.Department = labDepartmentEntity
        analysisCategoriesList.append(analysisCategoryEntity)
        FLIMS_DAO.insert_analysis_category(analysisCategoriesList, flims_configurations)
    
    def import_analysis_services():
        print ("importing Analysis_services...\n")
        from dao import FlimsImporterDAO
        flimsImporterDAO = FlimsImporterDAO(flims_configurations, "Analysis_Service")
        analysisServicesList = flimsImporterDAO.get_data()
        from flims_entities import AnalysisServiceEntity, AnalysisCategoryEntity
        analysisCategoryEntity = AnalysisCategoryEntity(None)
        analysisCategoryEntity.title = "Initial_Analysis_Category"
        for analysisServiceEntity in analysisServicesList:
            if analysisServiceEntity.Category.title is None:
                analysisServiceEntity.Category = analysisCategoryEntity
        FLIMS_DAO.insert_analysis_services(analysisServicesList, flims_configurations)

    def import_patients():
        print ("importing patients...\n")
        from dao import FlimsImporterDAO
        flimsImporterDAO = FlimsImporterDAO(flims_configurations, "Patient")
        patientsList = flimsImporterDAO.get_data()
        FLIMS_DAO.insert_patients(patientsList, flims_configurations)

    # map the inputs to the function blocks
    services = {
        'import_lab_departments' : import_lab_departments,
        'import_analysis_categories' : import_analysis_categories,
        'import_analysis_services' : import_analysis_services,
        'import_patients' : import_patients
    }[operation](**kwargs)

commands_list = {
    '1' : {
        '?' : "FLIMS Importer Configurations",
        'has_function' : False,
        'function' : None,
        'args' : None,
        'sub_command' :{
            '1' : {
                '?' : "Change database engine",
                'has_function' : False,
                'function' : None,
                'args' : None,
                'sub_command' :{
                    '1' : {
                        '?' : "MSSQLServer2019",
                        'has_function' : True,
                        'function' : config_flims,
                        'args' : {'operation' : "database_engine", 'database_engine' : "MSSQLServer2019"},
                        'sub_command' :{
                        }
                    },
                    '2' : {
                        '?' : "MySQL",
                        'has_function' : True,
                        'function' : config_flims,
                        'args' : {'operation' : "database_engine", 'database_engine' : "MySQL"},
                        'sub_command' :{
                        }
                    },
                    'B' : {
                        '?' : "back to previous menu",
                        'has_function' : True,
                        'function' : print,
                        'args' : ("\n"),
                        'sub_command' :{
                        }
                    }                
                }
            },
            '2' : {
                '?' : "Database Connection Settings",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "database_connection_settings"},
                'sub_command' :{
                }
            },
            '3' : {
                '?' : "FLIMS System Server Config",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "flims_system_server_configurations"},
                'sub_command' :{
                }
            },
            '4' : {
                '?' : "Set Client Name",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "client_name"},
                'sub_command' :{
                }
            },
            '5' : {
                '?' : "Set LabContact Manager",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "lab_contact_manager"},
                'sub_command' :{
                }
            },
            '6' : {
                '?' : "Print FLIMS Configurations",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "get_flims_configurations"},
                'sub_command' :{
                }
            },
            'B' : {
                '?' : "back to previous menu",
                'has_function' : True,
                'function' : print,
                'args' : ("\n"),
                'sub_command' :{
                }
            }
        }
    },
    '2' : {
        '?' : "Import Lab Departments",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_lab_departments"},
        'sub_command' :{
        }
    },
    '3' : {
        '?' : "Import Analysis Categories",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_categories"},
        'sub_command' :{
        }
    },
    '4' : {
        '?' : "Import Analysis Services",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_services"},
        'sub_command' :{
        }
    },
    '5' : {
        '?' : "Import Patients",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_patients"},
        'sub_command' :{
        }
    },
    'E' : {
        '?' : "Exit FLIMS Importer.",
        'has_function' : True,
        'function' : print,
        'args' : ("Bye..."),
        'sub_command' :{
        }                        
    },
}

def run_app(commands_list):
    print("Before starting import process, please consider the following required steps:\n")
    print("1- Create a client from FLIMS interface. You should use the same client name to add patients under that client.\n")
    print("2- Create a Lab Contact from FLIMS interface. You should use the same lab contact name before importing lab departments.\n\n")
    for command_key in commands_list.keys():
        print (command_key, ": ", commands_list[command_key]['?'])
    print ("\n\n")
    command = input('Enter choice: ')
    while command != 'E' and command != 'B':
        while command not in commands_list.keys():
            command = input('Wrong choice, enter again: ')
            pass
        if commands_list[command]['has_function']:
            if len(commands_list[command]['args']) == 0:
                print (commands_list[command]['args'])
                commands_list[command]['function']()
            else:
                commands_list[command]['function'](**commands_list[command]['args'])
        else:
            run_app(commands_list[command]['sub_command'])
        for command_key in commands_list.keys():
            print (command_key, ": ", commands_list[command_key]['?'])
        print ("\n\n")
        command = input('Enter Choice: ')

run_app(commands_list)
