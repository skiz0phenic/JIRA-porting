
import os
tab_spaces = 4  # Define the number of spaces for indentation and between fields
def creation_of_each_testcase_string(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description, uart_list_of_dict):
    testcase_string = "\n"
    # adding JIRA_ID in line 1
    testcase_string +=JIRA_ID + "\n"
    # adding tags in line 2
    testcase_string += " " * tab_spaces + "[Tags]" + " " * tab_spaces + jira_component + " " * tab_spaces + jira_subcomponent + " " * tab_spaces + PLATFORM + " " * tab_spaces + jira_application_name + " " * tab_spaces + JIRA_ID + "\n"
    # adding description in line 3
    testcase_string += " " * tab_spaces + "[Documentation]" + " " * tab_spaces + jira_test_description + "\n"
    # adding setup in line 4
    testcase_string += " " * tab_spaces + "[Setup]" + " " * tab_spaces + "UART FLASH TESTCASE ENVIRONMENT SETUP" + "\n"
    # adding binary find and flash in line 5
    testcase_string += " " * tab_spaces + "FIND_AND_FLASH_BINARIES_THROUGH_UART" + " " * tab_spaces + "${DEVICE_CONFIG}" + " " * tab_spaces + core_name + " " * tab_spaces + jira_application_name + "\n"
    # adding uart input in line 6 and last but one
    length = len(uart_list_of_dict)
    uart_number = 0
    while(uart_number < length):
        current_dict = uart_list_of_dict[uart_number]
        testcase_string += " " * tab_spaces + "DUT.EXPECT STRING AT UART PORT" + " " * tab_spaces + current_dict["expected_string_in_uart_logs"] + " " * tab_spaces + str(int(current_dict["timeout"])) + "\n"
        if(current_dict["uart_input"] is not None):
            testcase_string += " " * tab_spaces + "DUT.INPUT STRING AT UART PORT" + " " * tab_spaces + current_dict["uart_input"] + "\n"
        uart_number += 1
    
    # adding teardown in line last
    testcase_string += " " * tab_spaces + "[Teardown]" + " " * tab_spaces + "UART FLASH TESTCASE TEARDOWN"+"\n"

    return testcase_string


def creating_robot_file_for_new_core(folder_structure,file_name,PARENT_FOLDER):
    initial_string="***Settings***\n"
    initial_string+="Resource"+" "*tab_spaces+PARENT_FOLDER+".resource\n\n"
    initial_string+="***Test Cases***"

    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "w") as file:
        file.write(initial_string)



def appending_at_end_to_robot_file(folder_structure,file_name, current_testcase_string):
    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "a") as file:
        file.write(current_testcase_string)

def replace_at_the_middle_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME):
    #from Testcase_porting_main import PROJECT_NAME
    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "r") as file:
        robot_file_string = file.read()
    index_start=robot_file_string.find(jira_ID)
    index_end=robot_file_string.find(PROJECT_NAME,robot_file_string.find(PROJECT_NAME,index_start+len(PROJECT_NAME))+len(PROJECT_NAME))
    if(index_end==-1):
        index_end=len(robot_file_string)
    robot_file_string=robot_file_string[:index_start-1]+current_testcase_string+robot_file_string[index_end-1:]
    #print(robot_file_string)
    with open(file_location, "w") as file:
        file.write(robot_file_string)

def appending_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME):
    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "r") as file:
        robot_file_string = file.read()
    index_start=robot_file_string.find(jira_ID)
    if(index_start!=-1):
        print("replace")
        replace_at_the_middle_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME)
    else:
        print("end")
        appending_at_end_to_robot_file(folder_structure,file_name, current_testcase_string)


def creation_of_robot_testcase_main(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_application_name, jira_test_description, uart_list_of_dict):
    folder_structure = os.path.join(".", PROJECT_NAME,PARENT_FOLDER, PLATFORM)
    current_testcase_string=creation_of_each_testcase_string(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description, uart_list_of_dict)
    file_name=core_name+".robot"
    file_location=os.path.join(folder_structure,file_name)
    print(file_location)
    if(os.path.exists(file_location)):
        print("append")
        appending_to_robot_file(JIRA_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME)
    else:
        print("create")
        creating_robot_file_for_new_core(folder_structure,file_name, PARENT_FOLDER)
        appending_at_end_to_robot_file(folder_structure,file_name,current_testcase_string)

'''
uart_list_of_dict=[{"uart_input":"\"\"","expected_string_in_uart_logs":"\"\"","timeout":5}]
creation_of_robot_testcase_main("core_name","SITSW-1250","RASHFORD___ljdl;kjasd;","jira_subcomponent","am275x-evm","jira_application_name","jira_test_description",uart_list_of_dict)


creation_of_robot_testcase_main("core_name","SITSW-1426","INIESTA___ljdl;kjasd;","jira_subcomponent","PLATFORM","jira_application_name","jira_test_description",uart_list_of_dict)
'''
