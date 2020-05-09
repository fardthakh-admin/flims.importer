import itertools
from flims_importer_services import LabDepartmentService, SampleTypeService, AnalysisCategoryService, AnalysisServiceService, AnalysisSpecificationService, PatientService

#import flims_zodb_dao as FLIMS_DAO
#from dao import PulledDAO
#from flims_entities import AnalysisCategoryEntity, LabDepartmentEntity

database_engines = {
    "1" : "MSSQLServer2019",
    "2" : "MySQL"
}
importer_configurations = {
    "database_configurations" : {
        "database_engine" : "MSSQLServer2019",
        "database_host_url" : "localhost",
        "database_port" : "1433",
        "database_username" : "sa",
        "database_password" : "sa",
        "database_name" : "IntegratedLAB",
        "database_schema" : "dao"
    },
    "flims_configurations" : {
        "lab_contact_manager" : "Ayman Abu Awwad",
        "client_name" : "GenoLab",
        "server_ip" : "localhost",
        "server_port" : "8080",
        "server_path" : "flims",
        "flims_account_username" : "admin",
        "flims_account_password" : "admin"
    }
}

def config_flims(operation, **kwargs):

    def set_database_engine(**kwargs):
        for key, value in kwargs.items():
            if (key == "database_engine"):
                flims_configurations["database_engine"] = value

    def setDatabaseSettings():
        print ("Database Connection Settings:")
        for database_engine in database_engines.keys():
            print (database_engine, ": ", database_engines[command_key]['?'])
        print ("\n\n")
        database_engine_input = input('Database: ')
        while database_engines[database_engine] == None:
            print ("Wrong choice, enter again: ")
            database_engine_input = input('Enter choice: ')
        importer_configurations["database_configurations"]["database_engine"] = database_engine_input
        importer_configurations["database_configurations"]["database_host_url"] = input('Host(URL): ')
        importer_configurations["database_configurations"]["database_port"] = input('Port: ')
        importer_configurations["database_configurations"]["database_username"] = input('Username: ')
        importer_configurations["database_configurations"]["database_password"] = input('Password: ')
        importer_configurations["database_configurations"]["database_name"] = input('Database name: ')
        importer_configurations["database_configurations"]["database_schema"] = input('Database schema name: ')

    def setFlimsServerConfigurations():
        print ("FLIMS System Server Config:")
        importer_configurations["flims_configurations"]["server_ip"] = input('Server IP: ')
        importer_configurations["flims_configurations"]["server_port"] = input('Server Port: ')
        importer_configurations["flims_configurations"]["server_path"] = input('FLIMS web path: ')

    def setFlimsUserAccount():
        print ("FLIMS User Credentials:")
        importer_configurations["flims_configurations"]["flims_account_username"] = input('Username: ')
        importer_configurations["flims_configurations"]["flims_account_password"] = input('Password: ')

    def setClientName():
        importer_configurations["flims_configurations"]["client_name"] = input('Enter Client Name: ')

    def setLabContactManager():
        importer_configurations["flims_configurations"]["lab_contact_manager"] = input('Enter LabContact Manager Full Name: ')

    def printConfigurations():
        print("========Importer Configurations=========")
        print("========================================")
        def printConfig(config):
            for k, v in config.items():
                if type(v) is dict:
                    print("====",k.replace("_"," ").title(),"====")
                    print(*list(itertools.repeat("=", len(k) + 10)), sep = "")
                    printConfig(v)
                else:
                    print(k, ":", v, "\n")
        printConfig(importer_configurations)
        print("========================================")

    # map the inputs to the function blocks
    config_type = {
        'database_engine' : set_database_engine,
        'database_connection_settings' : setDatabaseSettings,
        'flims_server_configurations' : setFlimsServerConfigurations,
        'flims_user_credentials' : setFlimsUserAccount,
        'lab_contact_manager' : setLabContactManager,
        'client_name' : setClientName,
        'get_flims_configurations' : printConfigurations
    }[operation](**kwargs)        

def flims_services(operation, **kwargs):

    def importLabDepartments():
        print ("Importing Lab Departments Started...\n")
        labDepartmentService = LabDepartmentService(importer_configurations)
        labDepartmentService.importLabDepartments()
        print ("Importing Lab Departments Finished...\n")

    def importSampleTypes():
        print ("Importing Sample Types Started...\n")
        sampleTypeService = SampleTypeService(importer_configurations)
        sampleTypeService.importSampleTypes()
        print ("Importing Sample Types Finished...\n")

    def importAnalysisCategories():
        print ("Importing Analysis Categories Started...\n")
        analysisCategoryService = AnalysisCategoryService(importer_configurations)
        analysisCategoryService.importAnalysisCategories()
        print ("Importing Analysis Categories Finished...\n")

    def importAnalysisServices():
        print ("Importing Analysis Services Started...\n")
        analysisServiceService = AnalysisServiceService(importer_configurations)
        analysisServiceService.importAnalysisServices()
        print ("Importing Analysis Services Finished...\n")

    def importAnalysisSpecifications():
        print ("Importing Analysis Specifications Started...\n")
        analysisSpecificationService = AnalysisSpecificationService(importer_configurations)
        analysisSpecificationService.importAnalysisSpecifications()
        print ("Importing Analysis Specifications Finished...\n")

    def importPatients():
        print ("Importing Patients Started...\n")
        patientService = PatientService(importer_configurations)
        patientService.importPatients()
        print ("Importing Patients Finished...\n")

    def importAnalysisRequests():
        print ("Importing Analysis Requests Started...\n")
        analysisRequestService = AnalysisRequestService(importer_configurations)
        analysisRequestService.importAnalysisRequests()
        print ("Importing Analysis Requests Finished...\n")

    # map the inputs to the function blocks
    services = {
        'import_lab_departments' : importLabDepartments,
        'import_sample_types' : importSampleTypes,
        'import_analysis_categories' : importAnalysisCategories,
        'import_analysis_services' : importAnalysisServices,
        'import_analysis_specifications' : importAnalysisSpecifications,
        'import_patients' : importPatients,
        'import_analysis_requests' : importAnalysisRequests
    }[operation]()

commands_list = {
    '1' : {
        '?' : "FLIMS Importer Configurations",
        'has_function' : False,
        'function' : None,
        'args' : None,
        'sub_command' :{
            '1' : {
                '?' : "Database Connection Settings",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "database_connection_settings"},
                'sub_command' :{
                }
            },
            '2' : {
                '?' : "FLIMS System Server Config",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "flims_system_server_configurations"},
                'sub_command' :{
                }
            },
            '3' : {
                '?' : "Set Client Name",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "client_name"},
                'sub_command' :{
                }
            },
            '4' : {
                '?' : "Set LabContact Manager",
                'has_function' : True,
                'function' : config_flims,
                'args' : {'operation' : "lab_contact_manager"},
                'sub_command' :{
                }
            },
            '5' : {
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
        '?' : "Import Sample Types",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_sample_types"},
        'sub_command' :{
        }
    },
    '4' : {
        '?' : "Import Analysis Specifications",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_specifications"},
        'sub_command' :{
        }
    },
    '5' : {
        '?' : "Import Analysis Categories",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_categories"},
        'sub_command' :{
        }
    },
    '6' : {
        '?' : "Import Analysis Services",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_services"},
        'sub_command' :{
        }
    },
    '7' : {
        '?' : "Import Patients",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_patients"},
        'sub_command' :{
        }
    },
    '8' : {
        '?' : "Import Analysis Requests",
        'has_function' : True,
        'function' : flims_services,
        'args' : {'operation' : "import_analysis_requests"},
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
