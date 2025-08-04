import os
import json
from JIRA_API_extracting import JIRA_API_extracting
from creation_of_robot_testcase import legacy_creation_of_robot_testcase_main
from creation_of_robot_testcase import JSON_creation_of_robot_testcase_main
from test_setup_legacy_parser import test_setup_legacy_parser
from JQL_API_fetching import fetch_testcases_using_jql
from test_setup_JSON_parser import test_setup_JSON_parser

#This must be the same as in the JIRA ID beacuse the replace logic is based on finding this keyword
PROJECT_NAME = "SITSW"

PARENT_FOLDER = "am275x"

PLATFORM = "am275x-evm"
#JQL_string="""issuekey in  ("SITSW-1250","SITSW-1307","SITSW-4735","SITSW-1758")"""
#JQL_string="""issuekey in  ("MCUSDK-248","MCUSDK-13682","MCUSDK-249")"""
#JQL_string="""issuekey in  ("SITSW-6362")"""
JQL_string="""project = SITSW AND type = 'Test Case' AND component = 'MCU+SDK' AND Platform in (am275x-evm) AND 'Execution Type' = Automated AND issuetype = 'Test Case' AND 'Execution Type' = Automated"""

#This is to remove special characters from test description as special characters are not allowed in robot file
def remove_special_chars(text):
    """
    Remove special characters from the given text.

    Parameters:
        text (str): The text from which special characters need to be removed.

    Returns:
        str: The text with special characters removed.

    """
    return ''.join(char for char in text if char.isalnum() or char == ' ')

def make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM):
    """
    Creates necessary project, parent, and platform folders if they do not already exist.

    Parameters:
        PROJECT_NAME (str): The name of the project.
        PARENT_FOLDER (str): The name of the parent folder.
        PLATFORM (str): The name of the platform.

    Returns:
        None
    """
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
    """
    Extracts relevant information from a JIRA issue and creates robot test cases.

    Parameters:
        issue (dict): The JIRA issue containing information about a test case.

    Returns:
        None
    """
    ID=issue['key']
    response_list=JIRA_API_extracting(issue)
    jira_test_application_name=response_list[0]
    jira_test_component=response_list[1]
    jira_test_subcomponent=response_list[2]
    jira_test_description=response_list[3]
    jira_test_description=remove_special_chars(jira_test_description)
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
            core_name=core_name.strip()
            legacy_creation_of_robot_testcase_main(core_name, ID, jira_test_component, jira_test_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_test_application_name, jira_test_description, uart_list_of_dict)
    else:
        response_dict=test_setup_JSON_parser(json_extracted_test_setup,PLATFORM)
        print(json.dumps(response_dict, indent = 4))
        core_list=response_dict["core_list"]
        tifs_image_list=response_dict["tifs_image_list"]
        sbl_image_list=response_dict["sbl_image_list"]
        appimage_list=response_dict["app_image_list"]
        uart_list_of_dict=response_dict["uart_list_of_dict"]
        constraint_dict=response_dict["constraint_dict"]
        boot_mode=response_dict["boot_mode"]
        default_cfg_file=response_dict["config_file"]
        for core_name in core_list:
            JSON_creation_of_robot_testcase_main(core_name,ID,jira_timeout,jira_test_component,jira_test_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_test_application_name, jira_test_description,boot_mode,default_cfg_file, tifs_image_list,sbl_image_list,appimage_list, uart_list_of_dict,constraint_dict)


def main():
    """
    The main function of the program.

    This function creates necessary folders, fetches test cases using JQL, and then iterates over the fetched issues.
    For each issue, it calls the `main_for_each_ID` function. If an exception is raised, it prints the exception and
    appends the issue's key to the `failed_testcase_ID_list`. Finally, it prints the `failed_testcase_ID_list`.

    Parameters:
        None

    Returns:
        None
    """
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
