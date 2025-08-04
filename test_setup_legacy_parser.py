#for certain testcases the deafult core list is given of the form <core: ....>
def extract_default_core_list(legacy_setup_string):
    """
    Extracts the default core list from a legacy setup string.

    Parameters:
        legacy_setup_string (str): The string containing the legacy setup.

    Returns:
        list or None: A list of strings representing the default core list, or None if no default core list is found.
    """
    index_start=legacy_setup_string.find("<core:")
    if(index_start!=-1):
        index_start=legacy_setup_string.find(":",index_start)
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start)
        return legacy_setup_string[index_start:index_end].split(",")
    else:
        return None

def extract_default_coreos_list(legacy_setup_string):
    """
    Extracts the default core_os list from a legacy setup string.

    Parameters:
        legacy_setup_string (str): The string containing the legacy setup.

    Returns:
        list or None: A list of strings representing the default core_os list, or None if no default core_os list is found.
    """
    index_start=legacy_setup_string.find("<core_os:")
    if(index_start!=-1):
        index_start=legacy_setup_string.find(":",index_start)
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start)
        return legacy_setup_string[index_start:index_end].split(",")
    else:
        return None

def extract_custom_cores(index_start,legacy_setup_string,search_string):
    """
    Extracts a list of custom cores from a legacy setup string.

    Parameters:
        index_start (int): The starting index of the search.
        legacy_setup_string (str): The string containing the legacy setup.
        search_string (str): The string to search for.

    Returns:
        list: A list of strings representing the custom cores.
    """
    length_of_search_string=len(search_string)
    index_end=legacy_setup_string.find(">",index_start)
    return legacy_setup_string[index_start+length_of_search_string:index_end].split(",")

def extract_hw_assets(legacy_setup_string):
    """
    Extracts the hardware assets from a legacy setup string.

    Parameters:
        legacy_setup_string (str): The string containing the legacy setup.

    Returns:
        str: The extracted hardware assets.
    """
    print(len("""hw_assets:dut1=[""<platform>\"\""""))
    index_start=legacy_setup_string.find("""hw_assets:dut1=[""<platform>\"\"""")
    if(index_start!=-1):
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start+30)
        index_end-=1
    return legacy_setup_string[index_start+30:index_end]

def extract_project_id(element):
    """
    Extracts the project ID from a given element.

    Parameters:
        element (str): The element from which to extract the project ID.

    Returns:
        str: The extracted project ID.
    """
    index_start=element.find("projectid=")
    index_start+=10
    index_end=element.find(";",index_start)
    return element[index_start+1:index_end]


#default timeout is coded to 1st element in commands add logic to change it to jira_timeout if no timeout is present
def extract_commands(command_string):
    """
    Extracts commands from a command string.

    Args:
        command_string (str): The command string.

    Returns:
        list: A list of dictionaries containing UART input and expected string and timeout.
    """
    #remove command: from the command_string
    command_string=command_string[9:]
    #splitting command_string wrt , old list because timeout field is not present for each expected output
    old_command_list=command_string.split(",")
    print("OLD")
    print(old_command_list)
    print("\n")
    #the first timeout is assigned as the default timeout
    default_timeout=old_command_list[0][5:]
    print(default_timeout)

    #creating new_command_list adding default timeout value if no timeout is present for each expected output
    command_list=[]
    for element in old_command_list:
        #current element is expected output
        if(element.find("exp:")!=-1):
            #timeout is not  present
            if(command_list[-1].find("tout")==-1):
                #add default timeout value
                command_list.append("tout:"+default_timeout)
                command_list.append(element)
            else:
                #timeout is already present
                command_list.append(element)
        else:
            command_list.append(element)
    print("NEW")
    print(command_list)
    print("\n")

    uart_list=[]#list of dictionaries with uart input and expected string and timeout 
    current_dict={}#dictionary with uart input and expected string and timeout
    #creating individual dictionaries with uart input and expected string and timeout and then appending it to the list
    i=0
    while(i<len(command_list)):
        element=command_list[i]
        #if current element is expected output
        if(element.find("exp:")!=-1):
            #add expected output to current dictionary
            current_dict["expected_string_in_uart_logs"]=element[4:]
            #if this is the last element then add it to the dictionary and add the current dictionary to the list
            if(i==len(command_list)-1):
                current_dict["uart_input"]=None
                uart_list.append(current_dict)
                current_dict={}
                break
            #Not last element cases
            #if next element is timeout add None as UART input to the list and add the current dictionary to the list
            if(command_list[i+1].find("tout:")!=-1):
                current_dict["uart_input"]=None
                uart_list.append(current_dict)
                current_dict={}
            #if next element is uart input add it to the current dictionary and add the current dictionary to the list 
            else:
                current_dict["uart_input"]=command_list[i+1]
                i+=1
                uart_list.append(current_dict)
                current_dict={}
        #if current element is timeout add timeout to the current dictionary
        elif(element.find("tout:")!=-1):
            current_dict["timeout"]=element[5:]
        #if current element is uart input, this case will not come as we are append the uart input in previous case and doing i+=1
        else:
            pass
        #increment the while loop
        i+=1
    print(uart_list)
    return uart_list

def extract_constraints(constraints_string,jira_timeout):
    """
    Extracts constraints from a constraints string.

    Args:
        constraints_string (str): The constraints string.
        jira_timeout (int): The JIRA timeout.

    Returns:
        list: A list containing a dictionary with the extracted constraints.
    """
    constraints_string=constraints_string[12:]
    current_dict={}
    current_dict["timeout"]=jira_timeout
    current_dict["expected_string_in_uart_logs"]=constraints_string
    current_dict["uart_input"]=None
    return [current_dict]

def extract_params_dut(params_dut_string,jira_timeout):
    """
    Extracts parameters from a params_dut string.

    Args:
        params_dut_string (str): The params_dut string.
        jira_timeout (int): The JIRA timeout.

    Returns:
        list: A list containing the project_id and uart_list_of_dict.
    """
    params_dut_list=params_dut_string.split(";")
    uart_list_of_dict=None
    #spliting params_dut wrt ; and check for each element 
    for element in params_dut_list:
        if(element.find("projectid")!=-1):
            project_id=extract_project_id(element)
        elif(element.find("commands")!=-1):
            uart_list_of_dict=extract_commands(element)
        elif(element.find("constraints")!=-1):
            uart_list_of_dict=extract_constraints(element,jira_timeout)
    return [project_id,uart_list_of_dict]

def extract_scripts(scripts_string):
    """
    Extracts a substring from the input string.

    Args:
        scripts_string (str): The input string.

    Returns:
        str: The extracted substring.
    """
    index_start=scripts_string.find("<scripts:")
    index_end=scripts_string.find(">",index_start)
    return scripts_string[index_start+9:index_end]

def test_setup_legacy_parser(legacy_setup_string,jira_timeout,exact_platform_name):
    """
	Parses the legacy test setup string and extracts the necessary parameters.

	Args:
		legacy_setup_string (str): The string containing the legacy test setup.
		jira_timeout (int): The JIRA timeout.
		exact_platform_name (str): The exact platform name.

	Returns:
	    list: A list containing the core list, UART list of dictionaries, project ID, hardware assets, and scripts.
    """

    #parsing the cores from legacy_setup_string and creating the  core : list of plstform dictionary
    #extracting core_os:
    default_coreos_list=extract_default_coreos_list(legacy_setup_string)
    #extracting core:
    default_core_list=extract_default_core_list(legacy_setup_string)

    #if both are present we take core_os: as default
    if(default_coreos_list is not None):
        default_list=default_coreos_list
    else:
        default_list=default_core_list
    #extracting core_platform_name
    search_string="<core_"+exact_platform_name+":"
    index_start=legacy_setup_string.find(search_string)
    core_list=[]
    if(index_start!=-1):
        core_list=extract_custom_cores(index_start,legacy_setup_string,search_string)
    else:
        core_list=default_list
    #parsing hw_assets
    hw_assets="None"
    if(legacy_setup_string.find("<hw_assets:")!=-1):
        hw_assets=extract_hw_assets(legacy_setup_string)
    #end of parsing hw_assets
    uart_list_of_dict=None
    project_id=None
    #parsing params_dut
    index_start=legacy_setup_string.find("<params_dut:")
    if(index_start!=-1 ):
        index_end=legacy_setup_string.find(">",index_start)
        return_pair=extract_params_dut(legacy_setup_string[index_start+12:index_end],jira_timeout)
        uart_list_of_dict=return_pair[1]
        project_id=return_pair[0]
    #end of parsing params_dut
    if(uart_list_of_dict is None):
        current_dict={}
        current_dict["timeout"]=jira_timeout
        current_dict["expected_string_in_uart_logs"]="\"All Test have Passed\""
        current_dict["uart_input"]=None
        uart_list_of_dict=[current_dict]
    #parsing scripts
    scripts="None"
    if(legacy_setup_string.find("<scripts:")!=-1):
        scripts=extract_scripts(legacy_setup_string)
        #print(scripts)
    return [core_list,uart_list_of_dict,project_id,hw_assets,scripts]
    

#test_setup_legacy_parser(legacy_setup_string,120,"am275x-hsse")