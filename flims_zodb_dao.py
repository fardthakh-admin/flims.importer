import requests
import json

def login(session, flims_configurations):
    url = generate_url(flims_configurations) + "/@@API/senaite/v1/users/login"
    data = {"__ac_name": "admin", "__ac_password": "admin"}
    session.post(url, data).text

def login_by_form(flims_configurations):
    import mechanize
    url = generate_url(flims_configurations) + "/login_form"
    br = mechanize.Browser()
    br._factory.is_html = True
    br.set_handle_robots(False) # ignore robots
    br.open(url)
    br.select_form(id="login_form")
    br["__ac_name"] = "admin"
    br["__ac_password"] = "admin"
    br.submit()
    return br

def insert_lab_department(labDepartmentsList, flims_configurations):
    session=requests.Session()
    login(session, flims_configurations)
    url = generate_url(flims_configurations) +  "/@@API/senaite/v1/create"
    headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
    for labDepartmentEntity in labDepartmentsList:
        response = session.post(url,data=json.dumps(labDepartmentEntity.as_dictionary()),headers=headers)

def insert_analysis_category(analysisCategoriesList, flims_configurations):
    session=requests.Session()
    login(session, flims_configurations)
    url = generate_url(flims_configurations) + "/@@API/senaite/v1/create"
    headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
    for analysisCategoryEntity in analysisCategoriesList:
        response = session.post(url,data=json.dumps(analysisCategoryEntity.as_dictionary()),headers=headers)

def insert_analysis_services(analysisServicesList, flims_configurations):
    session=requests.Session()
    login(session, flims_configurations)
    # put the ip address or dns of your apic-em controller in this url
    url = generate_url(flims_configurations) +  "/@@API/senaite/v1/create"
    headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
    for analysisServiceEntity in analysisServicesList:
        url2 = generate_url(flims_configurations) +  "/@@API/senaite/v1/analysiscategory?title="
        response2 = session.get(url2+analysisServiceEntity.Category.title,headers=headers)
        if len(response2.json()["items"]) != 0:
            analysisServiceEntity.Category = response2.json()["items"][0]["uid"]
            response = session.post(url,data=json.dumps(analysisServiceEntity.as_dictionary()),headers=headers)

def insert_patients(patientsList, flims_configurations):
    session=requests.Session()
    login(session, flims_configurations)
    headers = {'User-Agent': 'Mozilla/5.0', "content-type": "application/json"}
    url2 = generate_url(flims_configurations) +  "/@@API/senaite/v1/client?title="
    response2 = session.get(url2+flims_configurations["client_name"],headers=headers)

    import mechanize
    br = login_by_form(flims_configurations)
    url = generate_url(flims_configurations) + "/patients/portal_factory/Patient/patient.2020-01-25.3571674204/edit?_authenticator=02cf2f763067db8f09ace52c3b13e725b4fcb0b4"

    for patientEntity in patientsList:
        br.open(url)
        br.select_form(id="patient-base-edit")
        br.find_control("PrimaryReferrer_uid").readonly = False
        br["PrimaryReferrer"] = flims_configurations["client_name"]
        br["PrimaryReferrer_uid"] = response2.json()["items"][0]["uid"]
        br["ClientPatientID"] = str(patientEntity.clientPatientID)
        br["Salutation"] = patientEntity.salutation
        br["Firstname"] = patientEntity.firstname
        br["Middleinitial"] = patientEntity.middleinitial
        br["Middlename"] = patientEntity.middlename
        br["Surname"] = patientEntity.surname
        #br["ConsentSMS"] = patientEntity.consentSMS
        #br["Gender"] = patientEntity.gender
        br.find_control("Gender").get(patientEntity.gender).selected = True
        br["BirthDate"] = patientEntity.birthDate
        br.find_control("AgeSplitted_year").readonly = False
        br["AgeSplitted_year"] = str(patientEntity.age_splitted_year)
        br.find_control("AgeSplitted_month").readonly = False
        br["AgeSplitted_month"] = str(patientEntity.age_splitted_month)
        br.find_control("AgeSplitted_day").readonly = False
        br["AgeSplitted_day"] = str(patientEntity.age_splitted_day)
        #br["CountryState.country"] = patientEntity.countryState_country
        #br.find_control("CountryState.country").get(patientEntity.countryState_country).selected = True
        br["EmailAddress"] = patientEntity.emailAddress
        br["HomePhone"] = patientEntity.homePhone
        br["MobilePhone"] = patientEntity.mobilePhone
        br["CivilStatus"] = patientEntity.civilStatus
        res = br.submit()

def generate_url(flims_configurations):
    return "http://" + flims_configurations["flims_system_ip"] + ":" + flims_configurations["flims_system_port"] + "/" + flims_configurations["flims_system_path"]
