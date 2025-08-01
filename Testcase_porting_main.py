import os
import json
from JIRA_API_extracting import JIRA_API_extracting
from legacy_creation_of_robot_testcase import legacy_creation_of_robot_testcase_main
from test_setup_legacy_parser import test_setup_legacy_parser
from JQL_API_fetching import fetch_testcases_using_jql
from test_setup_JSON_parser import test_setup_JSON_parser

PROJECT_NAME = "SITSW"
PARENT_FOLDER = "am654x"
PLATFORM = "am654x-idk-hsse"
JQL_string="""issuekey in  ("SITSW-1250","SITSW-1307","SITSW-4735","MCAL-2684")"""
#JQL_string="""issuekey in  ("SITSW-1758")"""


def make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM):
    project_folder_path=os.path.join(".",PROJECT_NAME)
    if(os.path.exists(project_folder_path)):
        pass
    else:
        os.mkdir(project_folder_path)
    parent_folder_path=os.path.join(".",PROJECT_NAME,PARENT_FOLDER)
    platform_folder_path=os.path.join(parent_folder_path,PLATFORM)
    if(os.path.exists(parent_folder_path)):
        if(os.path.exists(platform_folder_path)):
            pass
        else:
            os.mkdir(platform_folder_path)
    else:
        os.mkdir(parent_folder_path)
        os.mkdir(platform_folder_path)

def main_for_each_ID(issue):
    ID=issue['key']
    response_list=JIRA_API_extracting(issue)
    jira_test_application_name=response_list[0]
    jira_test_component=response_list[1]
    jira_test_subcomponent=response_list[2]
    jira_test_description=response_list[3]
    jira_test_setup=response_list[4]
    jira_timeout=response_list[5]

    json_flag=True
    json_extracted_test_setup=None
    try:
        jira_test_setup_json_check = jira_test_setup.replace("\n", "").replace("\r", "").strip()
        json_extracted_test_setup = json.loads(jira_test_setup_json_check)  
        #print(json_extracted_test_setup)
    except json.JSONDecodeError :
        json_flag=False

    if(not json_flag):
        response_list=test_setup_legacy_parser(jira_test_setup,jira_timeout,PLATFORM)
        core_list=response_list[0]
        uart_list_of_dict=response_list[1]
        project_id=response_list[2]
        hw_assets=response_list[3]
        scripts=response_list[4]
        for core_name in core_list:
            legacy_creation_of_robot_testcase_main(core_name, ID, jira_test_component, jira_test_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_test_application_name, jira_test_description, uart_list_of_dict)
    else:
        response_list=test_setup_JSON_parser(json_extracted_test_setup,jira_timeout,PLATFORM)
        print(json.dumps(response_list, indent = 4))

def main():
    make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM)
    failed_testcase_ID_list=[]
    all_issue_list=fetch_testcases_using_jql(JQL_string, "XrClUfvKjXPW2xjvGMnQ54MPhRr2rFua3Su3yL")
    for issue in all_issue_list:
        try:
            main_for_each_ID(issue)
        except Exception as e:
            print(e)
            failed_testcase_ID_list.append(issue['key'])
    
    print("failed_testcase_ID_list: ",failed_testcase_ID_list)
    

if __name__ == "__main__":
    main()
