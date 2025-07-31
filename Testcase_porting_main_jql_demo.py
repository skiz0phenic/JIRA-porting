import os
from JIRA_API_fetching_jql import JIRA_API_extracting
from creation_of_robot_testcase_jql import creation_of_robot_testcase_main
from test_setup_legacy_parser_jql import test_setup_legacy_parser
from JQL_API_fetching_jql import fetch_testcases_using_jql

PROJECT_NAME=""
PARENT_FOLDER=""
PLATFORM=""


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

    response_list=test_setup_legacy_parser(jira_test_setup,jira_timeout,PLATFORM)
    core_list=response_list[0]
    uart_list_of_dict=response_list[1]
    project_id=response_list[2]
    hw_assets=response_list[3]
    scripts=response_list[4]

    #print(uart_list_of_dict)
    '''
    print(core_list)
    pretty_print(uart_list_of_dict)
    print(project_id)
    print(hw_assets)
    print(scripts)
    '''
    for core_name in core_list:
        creation_of_robot_testcase_main(core_name, ID, jira_test_component, jira_test_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_test_application_name, jira_test_description, uart_list_of_dict)



def main():
    
    global PROJECT_NAME
    global PARENT_FOLDER
    global PLATFORM
    
    PROJECT_NAME = "SITSW"
    PARENT_FOLDER = "am654x"
    PLATFORM = "am654x-idk-hsse"
    make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM)
    all_issue_list=fetch_testcases_using_jql("""issuekey in  ("SITSW-1250","SITSW-1307","SITSW-4735")""", "XrClUfvKjXPW2xjvGMnQ54MPhRr2rFua3Su3yL")
    for issue in all_issue_list:
        main_for_each_ID(issue)

    
    PROJECT_NAME = "MCUSDK"
    PARENT_FOLDER = "am243x"
    PLATFORM = "am243x-lp"
    make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM)
    all_issue_list=fetch_testcases_using_jql("""issuekey in  ("MCUSDK-1001","MCUSDK-4195","MCUSDK-239")""", "XrClUfvKjXPW2xjvGMnQ54MPhRr2rFua3Su3yL")
    for issue in all_issue_list:
        main_for_each_ID(issue)
    

    PROJECT_NAME = "PDK"
    PARENT_FOLDER = "j784s4"
    PLATFORM = "j784s4-hsevm"
    make_necessary_folders(PROJECT_NAME,PARENT_FOLDER,PLATFORM)
    all_issue_list=fetch_testcases_using_jql("""issuekey in  ("PDK-5024","PDK-14456")""", "XrClUfvKjXPW2xjvGMnQ54MPhRr2rFua3Su3yL")
    for issue in all_issue_list:
        main_for_each_ID(issue)

    

if __name__ == "__main__":
    main()
