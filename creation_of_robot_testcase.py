
import os
tab_spaces = 4  # Define the number of spaces for indentation and between fields
def legacy_creation_of_each_testcase_string(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description, uart_list_of_dict):
    """
    Generate a testcase string for a legacy testcase.

    Args:
        core_name (str): The name of the core.
        JIRA_ID (str): The JIRA ID of the testcase.
        jira_component (str): The JIRA component.
        jira_subcomponent (str): The JIRA subcomponent.
        PLATFORM (str): The platform.
        jira_application_name (str): The name of the JIRA application.
        jira_test_description (str): The description of the testcase.
        uart_list_of_dict (List[Dict[str, Union[str, int]]]): The list of UART input and output dictionaries.

    Returns:
        str: The generated testcase string.
    """
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

def JSON_creation_of_each_testcase_string(core_name, JIRA_ID, jira_timeout,jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description,bootmode,default_cfg_file,tifs_image_list,sbl_image_list,appimage_list, uart_list_of_dict,constraint_dict):
    """
    Creates a string representation of a test case using the provided parameters.

    Args:
        core_name (str): The name of the core.
        JIRA_ID (str): The JIRA ID of the test case.
        jira_timeout (int): The timeout value for the test case.
        jira_component (str): The JIRA component.
        jira_subcomponent (str): The JIRA subcomponent.
        PLATFORM (str): The platform.
        jira_application_name (str): The name of the JIRA application.
        jira_test_description (str): The description of the test case.
        bootmode (str): The boot mode.
        default_cfg_file (str, optional): The default configuration file.
        tifs_image_list (List[str], optional): The list of TIFS images.
        sbl_image_list (List[str], optional): The list of SBL images.
        appimage_list (List[str], optional): The list of app images.
        uart_list_of_dict (List[Dict[str, Union[str, int]]], optional): The list of UART input and output dictionaries.
        constraint_dict (List[Dict[str, str]], optional): The list of constraint dictionaries.

    Returns:
        str: The string representation of the test case.
    """
    testcase_string = "\n"
    # adding JIRA_ID in line 1
    testcase_string +=JIRA_ID + "\n"
    # adding tags in line 2
    testcase_string += " " * tab_spaces + "[Tags]" + " " * tab_spaces + jira_component + " " * tab_spaces + jira_subcomponent + " " * tab_spaces + PLATFORM + " " * tab_spaces + jira_application_name + " " * tab_spaces + JIRA_ID + "\n"
    # adding description in line 3
    testcase_string += " " * tab_spaces + "[Documentation]" + " " * tab_spaces + jira_test_description + "\n"
    # adding boot setup in line 4
    testcase_string += " " * tab_spaces + "[Setup]" + " " * tab_spaces + "UART FLASH TESTCASE ENVIRONMENT SETUP" +" " * tab_spaces+bootmode+"\n"
    # adding default config file or list of binary pahs depending on whats preset in the testcase in line 5
    if(default_cfg_file is not None):
        testcase_string+=" " * tab_spaces + "DEFAULT_CONFIG_FILE_AND_FLASH_BINARIES" + " " * tab_spaces + default_cfg_file+"\n"
    else:
        testcase_string += " " * tab_spaces + "CREATE_CONFIG_FILE_AND_FLASH_BINARIES" + " " * tab_spaces + "${DEVICE_CONFIG}" + " " * tab_spaces + core_name + " " * tab_spaces + jira_application_name
        if(tifs_image_list is not None):
            for tifs_image in tifs_image_list:
                testcase_string+=" " * tab_spaces+"@{\""+tifs_image+"\"}"
        if(sbl_image_list is not None):
            for sbl_image in sbl_image_list:
                testcase_string+=" " * tab_spaces+"@{\""+sbl_image+"\"}"
        if(appimage_list is not None):
            for appimage in appimage_list:
                testcase_string+=" " * tab_spaces+"@{\""+appimage+"\"}"
        testcase_string += "\n"
    # adding uart I/O 
    if( uart_list_of_dict is not None):
        length = len(uart_list_of_dict)
        uart_number = 0
        while(uart_number < length):
            current_dict = uart_list_of_dict[uart_number]
            #checking for a string to appear at the UART port
            testcase_string += " " * tab_spaces + "DUT.EXPECT STRING AT UART PORT" + " " * tab_spaces + current_dict["expected_string_in_uart_logs"] + " " * tab_spaces + str(int(current_dict["timeout"])) + "\n"
            if(current_dict["uart_input"] != ""):
                if(current_dict["newline"]=="0"):
                    #give a UART input with or without newline depending on the "newline" value
                    testcase_string += " " * tab_spaces + "DUT.INPUT STRING AT UART PORT" + " " * tab_spaces + current_dict["uart_input"] + "\n"
                else:
                    testcase_string += " " * tab_spaces + "DUT.INPUT STRING WITH NEWLINE AT UART PORT" + " " * tab_spaces + current_dict["uart_input"] + "\n"
            #checking the output of the UART port after providing the input
            if(current_dict["verify_string_in_uart_logs"] is not None):
                testcase_string += " " * tab_spaces + "DUT.EXPECT STRING AT UART PORT" + " " * tab_spaces + current_dict["verify_string_in_uart_logs"] + " " * tab_spaces + str(int(current_dict["timeout"])) + "\n"
            uart_number += 1
    #adding constraint checks
    if (constraint_dict is not None):
        length = len(constraint_dict)
        constraint_number = 0
        while(constraint_number < length):
            current_dict = constraint_dict[constraint_number]
            testcase_string += " " * tab_spaces + "DUT.EXPECT STRING AT UART PORT" + " " * tab_spaces + current_dict["message"] + " " * tab_spaces + str(int(jira_timeout)) + "\n"
            constraint_number += 1
    # adding teardown in line last
    testcase_string += " " * tab_spaces + "[Teardown]" + " " * tab_spaces + "UART FLASH TESTCASE TEARDOWN"+"\n"
    #print(testcase_string)
    return testcase_string

def creating_robot_file_for_new_core(folder_structure,file_name,PARENT_FOLDER):
    """
    Creates a new robot file in the specified folder structure.

    Parameters:
        folder_structure (str): The path to the folder structure where the file will be created.
        file_name (str): The name of the file to be created.
        PARENT_FOLDER (str): The name of the parent folder.

    Returns:
        None
    """
    #seting up the initial string for file creation
    initial_string="***Settings***\n"
    initial_string+="Resource"+" "*tab_spaces+PARENT_FOLDER+".resource\n\n"
    initial_string+="***Test Cases***"

    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "w") as file:
        file.write(initial_string)



def appending_at_end_to_robot_file(folder_structure,file_name, current_testcase_string):
    """
    Appends the given `current_testcase_string` to the end of the file located at `file_location`.

    Parameters:
        folder_structure (str): The path to the directory where the file is located.
        file_name (str): The name of the file.
        current_testcase_string (str): The string to append to the end of the file.

    Returns:
        None
    """
    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "a") as file:
        file.write(current_testcase_string)

def replace_at_the_middle_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME):
    """
    Replaces a portion of a robot file with a new test case.

    Args:
        jira_ID (str): The JIRA ID of the test case.
        folder_structure (str): The path to the folder structure where the file is located.
        file_name (str): The name of the file.
        current_testcase_string (str): The string to replace the old test case with.
        PROJECT_NAME (str): The name of the project.

    Returns:
        None
    """
    file_location=os.path.join(folder_structure,file_name)
    with open(file_location, "r") as file:
        robot_file_string = file.read()
    index_start=robot_file_string.find(jira_ID)
    index_end=robot_file_string.find(PROJECT_NAME,robot_file_string.find(PROJECT_NAME,index_start+len(PROJECT_NAME))+len(PROJECT_NAME))
    if(index_end==-1):
        index_end=len(robot_file_string)
    robot_file_string=robot_file_string[:index_start-1]+current_testcase_string+robot_file_string[index_end-1:]
    with open(file_location, "w") as file:
        file.write(robot_file_string)

def appending_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME):
    file_location=os.path.join(folder_structure,file_name)
    """
    Appends the given `current_testcase_string` to the end of the file located at `file_location`.

    Parameters:
        jira_ID (str): The JIRA ID of the test case.
        folder_structure (str): The path to the folder structure where the file is located.
        file_name (str): The name of the file.
        current_testcase_string (str): The string to append to the end of the file.
        PROJECT_NAME (str): The name of the project.

    Returns:
        None
    """
    with open(file_location, "r") as file:
        robot_file_string = file.read()
    index_start=robot_file_string.find(jira_ID)
    if(index_start!=-1):
        print("replace")
        replace_at_the_middle_to_robot_file(jira_ID,folder_structure,file_name, current_testcase_string,PROJECT_NAME)
    else:
        print("end")
        appending_at_end_to_robot_file(folder_structure,file_name, current_testcase_string)


def legacy_creation_of_robot_testcase_main(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_application_name, jira_test_description, uart_list_of_dict):
    """
    Creates a robot test case and appends it to an existing file or creates a new file.

    Args:
        core_name (str): The name of the core.
        JIRA_ID (str): The JIRA ID of the test case.
        jira_component (str): The JIRA component.
        jira_subcomponent (str): The JIRA subcomponent.
        PLATFORM (str): The platform.
        PARENT_FOLDER (str): The name of the parent folder.
        PROJECT_NAME (str): The name of the project.
        jira_application_name (str): The name of the JIRA application.
        jira_test_description (str): The description of the test case.
        uart_list_of_dict (List[Dict[str, Union[str, int]]]): The list of UART input and output dictionaries.

    Returns:
        None
    """
    folder_structure = os.path.join(".", PROJECT_NAME,PARENT_FOLDER, PLATFORM)
    current_testcase_string=legacy_creation_of_each_testcase_string(core_name, JIRA_ID, jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description, uart_list_of_dict)
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

def JSON_creation_of_robot_testcase_main(core_name, JIRA_ID,jira_timeout, jira_component, jira_subcomponent, PLATFORM,PARENT_FOLDER,PROJECT_NAME, jira_application_name, jira_test_description, bootmode, default_cfg_file,tifs_image_list,sbl_image_list,appimage_list,uart_list_of_dict,constraint_dict):
    """
    Creates a robot test case and appends it to an existing file or creates a new file.

    Args:
        core_name (str): The name of the core.
        JIRA_ID (str): The JIRA ID of the test case.
        jira_timeout (int): The timeout value for the test case.
        jira_component (str): The JIRA component.
        jira_subcomponent (str): The JIRA subcomponent.
        PLATFORM (str): The platform.
        PARENT_FOLDER (str): The name of the parent folder.
        PROJECT_NAME (str): The name of the project.
        jira_application_name (str): The name of the JIRA application.
        jira_test_description (str): The description of the test case.
        bootmode (str): The boot mode.
        default_cfg_file (str, optional): The default configuration file.
        tifs_image_list (List[str], optional): The list of TIFS images.
        sbl_image_list (List[str], optional): The list of SBL images.
        appimage_list (List[str], optional): The list of app images.
        uart_list_of_dict (List[Dict[str, Union[str, int]]], optional): The list of UART input and output dictionaries.
        constraint_dict (List[Dict[str, str]], optional): The list of constraint dictionaries.

    Returns:
        None
    """
    folder_structure = os.path.join(".", PROJECT_NAME,PARENT_FOLDER, PLATFORM)
    current_testcase_string=JSON_creation_of_each_testcase_string(core_name, JIRA_ID, jira_timeout,jira_component, jira_subcomponent, PLATFORM, jira_application_name, jira_test_description,bootmode,default_cfg_file,tifs_image_list,sbl_image_list,appimage_list, uart_list_of_dict,constraint_dict)
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
