'''
FINAL PARAMS FORMAT

default core list: core_os or core (if core_os is not present)
bootmode_string
config_file_string
tifs_image_list
sbl_image_list
appimage_list
constraint_dict
{
message
log_port
}
uart I/O_dict
{
expected_string_in_uart_logs
uart_input
verify_string_in_uart_logs
timeout
newline
}
'''
"""
we populate this final params dictionary using the JIRA test setup metadata
we divide the test setup into 2 parts where our data is present: PLATFORM parameters and common parameters
First we try to populate the final params dictionary from PLATFORM parameters and takes all variables that are present in PLATFORM parameters
Then we try to populate the final params dictionary from common parameters and takes all variables that are not present in PLATFORM parameters
"""

def test_setup_JSON_parser(json_extracted_test_setup,PLATFORM):
    """
    Parse the JSON test setup and extract the necessary parameters.

    Args:
        json_extracted_test_setup (dict): The JSON test setup.
        jira_timeout (int): The JIRA timeout.
        PLATFORM (str): The platform.

    Returns:
        dict: The final parameters extracted from the JSON test setup.
    """
    #we extract the common parameters into a dictionary called common_params
    common_params=json_extracted_test_setup["common_params"]
    #we extract all PLATFORM specific parameters into a dictionary called PLATFORM_params
    PLATFORM_params={}
    if(PLATFORM in json_extracted_test_setup.keys()):
        PLATFORM_params=json_extracted_test_setup[PLATFORM]
    
    #we initialize the final_params dictionary that we are trying to populate
    final_params={
        "core_list":None,#list of cares applicable for input Platform
        "boot_mode":None,#string to specify the bootmode
        "config_file":None,#string to specify the default config file
        "tifs_image_list":None,#list of tifs images
        "sbl_image_list":None,#list of sbl images
        "app_image_list":None,#list of app images
        "uart_list_of_dict":None,#its a list of dictionary containing uart I/O specific parameters
        "constraint_dict":None,#its a dictionary containing constraints to chcek at the end
    }

#TRYING TO POPULATE THE FINAL PARAMS FROM PLATFORM SPECIFIC PARAMETERS
    #fill up final_params from PLATFORM_params only if PLATFORM specific paramseters is present in the metadata
    if(PLATFORM in json_extracted_test_setup.keys()):
        #extracting core_list
        #searching for core_os if not present then search for core
        if("core_os" in PLATFORM_params.keys()):
            final_params["core_list"]=PLATFORM_params["core_os"]
        elif("core" in PLATFORM_params.keys()):
            final_params["core_list"]=PLATFORM_params["core"]
        else:
            final_params["core_list"]=None
        #extracting boot_mode
        #some JIRA testcases give bootmode as "boot_mode"and some as "bootmode" so we are checking for both keys and taking the one thats present
        if("boot_mode" in PLATFORM_params.keys()):
            final_params["boot_mode"]=PLATFORM_params["boot_mode"]
        elif("bootmode" in PLATFORM_params.keys()):
            final_params["boot_mode"]=PLATFORM_params["bootmode"]
        else:
            final_params["boot_mode"]=None
        #extracting default cfg file
        if("default_cfg_file" in PLATFORM_params.keys()):
            final_params["config_file"]=PLATFORM_params["default_cfg_file"]
        else:
            final_params["config_file"]=None
        #extracting tifs_image_list
        if("tifs_image" in PLATFORM_params.keys()):
            final_params["tifs_image_list"]=[]
            i=1
            #keys might be of the form image1, image2 etc or image_1, image_2 etc for different projects
            #seaching for keys of the form image1, image2 etc
            key="image"+str(i)
            while(key in PLATFORM_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(PLATFORM_params["tifs_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            #searching for keys of the form image_1, image_2 etc
            key="image_"+str(i)
            while(key in PLATFORM_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(PLATFORM_params["tifs_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)
        else:
            final_params["tifs_image_list"]=None        
        #extracting sbl_image_list
        if("sbl_image" in PLATFORM_params.keys()):
            final_params["sbl_image_list"]=[]
            i=1
            #keys might be of the form image1, image2 etc or image_1, image_2 etc for different projects
            #seaching for keys of the form image1, image2 etc
            key="image"+str(i)
            while(key in PLATFORM_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(PLATFORM_params["sbl_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            #searching for keys of the form image_1, image_2 etc
            key="image_"+str(i)
            while(key in PLATFORM_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(PLATFORM_params["sbl_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)
        else:
            final_params["sbl_image_list"]=None
        #extracting appimage_list
        if("app_image" in PLATFORM_params.keys()):
            final_params["app_image_list"]=[]
            i=1
            #keys might be of the form image1, image2 etc or image_1, image_2 etc for different projects
            #seaching for keys of the form image1, image2 etc
            key="image"+str(i)
            while(key in PLATFORM_params["app_image"].keys()):
                final_params["app_image_list"].append(PLATFORM_params["app_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            #searching for keys of the form image_1, image_2 etc
            key="image_"+str(i)
            while(key in PLATFORM_params["app_image"].keys()):
                final_params["app_image_list"].append(PLATFORM_params["app_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)
        else:
            final_params["app_image_list"]=None
        #extracting uart_list_of_dict
        if("uart_input" in PLATFORM_params.keys()):
            final_params["uart_list_of_dict"]=[]
            current_dict={}
            #some JIRA testcases give uart_input from 0 and some from 1 so handling if 0 is present different case
            if("uart_input_0"in PLATFORM_params["uart_input"].keys()):
                """
                expected_string_in_uart_logs<-constraint
                uart_input<-command
                verify_string_in_uart_logs<-message
                timeout<-timeout
                newline<-send_command_with_newline
                """
                current_dict["expected_string_in_uart_logs"]=PLATFORM_params["uart_input"]["uart_input_0"]["constraint"]
                current_dict["uart_input"]=PLATFORM_params["uart_input"]["uart_input_0"]["command"]
                current_dict["verify_string_in_uart_logs"]=PLATFORM_params["uart_input"]["uart_input_0"]["message"]
                current_dict["timeout"]=PLATFORM_params["uart_input"]["uart_input_0"]["timeout"]
                current_dict["newline"]=0
                if("send_command_with_newline" in PLATFORM_params["uart_input"]["uart_input_0"].keys()):
                    current_dict["newline"]=PLATFORM_params["uart_input"]["uart_input_0"]["send_command_with_newline"]
                final_params["uart_list_of_dict"].append(current_dict)
                current_dict={}
            i=1
            #seaching for keys of the form uart_input_1, uart_input_2 etc
            key="uart_input_"+str(i)
            while(key in PLATFORM_params["uart_input"].keys()):
                """
                expected_string_in_uart_logs<-constraint
                uart_input<-command
                verify_string_in_uart_logs<-message
                timeout<-timeout
                newline<-send_command_with_newline
                """
                current_dict["expected_string_in_uart_logs"]=PLATFORM_params["uart_input"][key]["constraint"]
                current_dict["uart_input"]=PLATFORM_params["uart_input"][key]["command"]
                current_dict["verify_string_in_uart_logs"]=PLATFORM_params["uart_input"][key]["message"]
                current_dict["timeout"]=PLATFORM_params["uart_input"][key]["timeout"]
                current_dict["newline"]=0
                if("send_command_with_newline" in PLATFORM_params["uart_input"][key].keys()):
                    current_dict["newline"]=PLATFORM_params["uart_input"][key]["send_command_with_newline"]
                final_params["uart_list_of_dict"].append(current_dict)
                current_dict={}
                i+=1
                #seaching for keys of the form uart_input_1, uart_input_2 etc
                key="uart_input_"+str(i)
                #in some JIRA test cases there are human errors where they skip one index number for uart_input so checking is i+2 is present or not 
                if(key not in PLATFORM_params["uart_input"].keys()):
                    i+=1
                    key="uart_input_"+str(i)
        else:
            pass
        #extracting constraint_list
        if("constraint" in PLATFORM_params.keys()):
            final_params["constraint_dict"]=[]
            i=1
            #seaching for keys of the form constraint_1, constraint_2 etc
            key="constraint_"+str(i)
            while(key in PLATFORM_params["constraint"].keys()):
                final_params["constraint_dict"].append(PLATFORM_params["constraint"][key])
                i+=1
                key="constraint_"+str(i)
        else:
            final_params["constraint_dict"]=None

#FILL UP THE FINAL PARAMS FROM COMMON PARAMETERS ONLY IF NOT PRESENT IN PLATFORM SPECIFIC PARAMETERS i.e ITS NONE
#THE LOGIC FOR EXTRACTION IS EXACTLY SAME AS FOR PLATFORM SPECIFIC PARAMETERS
    #extracting core_list if not already present
    if(final_params["core_list"] is None):
        if("core_os" in common_params.keys()):
            final_params["core_list"]=common_params["core_os"]
        elif("core" in common_params.keys()):
            final_params["core_list"]=common_params["core"]
        else:
            final_params["core_list"]=None
    #extracting boot_mode if not already present
    if(final_params["boot_mode"] is None):
        if("boot_mode" in common_params.keys()):
            final_params["boot_mode"]=common_params["boot_mode"]
        elif("bootmode" in common_params.keys()):
            final_params["boot_mode"]=common_params["bootmode"]
        else:
            final_params["boot_mode"]="uart"
    #extracting config_file if not already present
    if(final_params["config_file"] is None):
        if("default_cfg_file" in common_params.keys()):
            final_params["config_file"]=common_params["default_cfg_file"]
        else:
            final_params["config_file"]=None
    #extracting tifs_image_list if not already present
    if(final_params["tifs_image_list"] is None):
        if("tifs_image" in common_params.keys()):
            final_params["tifs_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(common_params["tifs_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            key="image_"+str(i)
            while(key in common_params["tifs_image"].keys()):
                final_params["tifs_image_list"].append(common_params["tifs_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)    
        else:
            final_params["tifs_image_list"]=None
    #extracting sbl_image_list if not already present
    if(final_params["sbl_image_list"] is None):
        if("sbl_image" in common_params.keys()):
            final_params["sbl_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(common_params["sbl_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            key="image_"+str(i)
            while(key in common_params["sbl_image"].keys()):
                final_params["sbl_image_list"].append(common_params["sbl_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)
        else:
            final_params["sbl_image_list"]=None
    #extracting appimage_list if not already present
    if(final_params["app_image_list"] is None):
        if("app_image" in common_params.keys()):
            final_params["app_image_list"]=[]
            i=1
            key="image"+str(i)
            while(key in common_params["app_image"].keys()):
                final_params["app_image_list"].append(common_params["app_image"][key]["image_path"])
                i+=1
                key="image"+str(i)
            key="image_"+str(i)
            while(key in common_params["app_image"].keys()):
                final_params["app_image_list"].append(common_params["app_image"][key]["image_path"])
                i+=1
                key="image_"+str(i)
        else:
            final_params["app_image_list"]=None
    #extracting uart_list_of_dict if not already present
    if(final_params["uart_list_of_dict"] is None):
        if("uart_input" in common_params.keys()):
            final_params["uart_list_of_dict"]=[]
            current_dict={}
            i=1
            key="uart_input_"+str(i)
            while(key in common_params["uart_input"].keys()):
                current_dict["expected_string_in_uart_logs"]=common_params["uart_input"][key]["constraint"]
                current_dict["uart_input"]=common_params["uart_input"][key]["command"]
                current_dict["verify_string_in_uart_logs"]=common_params["uart_input"][key]["message"]
                current_dict["timeout"]=common_params["uart_input"][key]["timeout"]
                current_dict["newline"]=0
                if("send_command_with_newline" in common_params["uart_input"][key].keys()):
                    current_dict["newline"]=common_params["uart_input"][key]["send_command_with_newline"]
                final_params["uart_list_of_dict"].append(current_dict)
                current_dict={}
                i+=1
                key="uart_input_"+str(i)
                if(key not in common_params["uart_input"].keys()):
                    i+=1
                    key="uart_input_"+str(i)
        else:
            pass
    #extracting constraint_list if not already present
    if(final_params["constraint_dict"] is None):
        if("constraint" in common_params.keys()):
            final_params["constraint_dict"]=[]
            i=1
            key="constraint_"+str(i)
            while(key in common_params["constraint"].keys()):
                final_params["constraint_dict"].append(common_params["constraint"][key])
                i+=1
                key="constraint_"+str(i)
        else:
            pass
    return final_params  



