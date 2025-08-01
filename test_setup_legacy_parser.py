
def pretty_print(data):
    for index, item in enumerate(data, start=1):
        print(f"Item {index}:")
        for key, value in item.items():
            print(f"  {key}: {value}")
        print()
legacy_setup_string="""<core:m4fss0-0_freertos,m4fss0-0_nortos,r5fss0-0_freertos,mcu-r5fss0-0_freertos,mcu-r5fss0-0_nortos,a53ss0-0_freertos,a53ss0-0_nortos,a53ss0-0_freertos-smp,wkup-r5fss0-0_freertos,c75ss0-0_freertos>
<core_am654x-idk:r5fss0-0_freertos>
<core_am654x-idk-hsse:r5fss0-0_freertos>
<core_am275x-evm:wkup-r5fss0-0_freertos,c75ss0-0_freertos,c75ss1-0_freertos,r5fss0-0_freertos,r5fss0-0_nortos,r5fss0-1_freertos,r5fss0-1_nortos,r5fss1-0_freertos,r5fss1-0_nortos,r5fss1-1_freertos,r5fss1-1_nortos>
<core_am275x-hsse:wkup-r5fss0-0_freertos,c75ss0-0_freertos,c75ss1-0_freertos,r5fss0-0_freertos,r5fss0-0_nortos,r5fss0-1_freertos,r5fss0-1_nortos,r5fss1-0_freertos,r5fss1-0_nortos,r5fss1-1_freertos,r5fss1-1_nortos><params_dut:projectid="hello_world";constraints="Hello\sWorld">"""

 



    
def extract_default_core_list(legacy_setup_string):
    index_start=legacy_setup_string.find("<core:")
    if(index_start!=-1):
        index_start=legacy_setup_string.find(":",index_start)
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start)
        return legacy_setup_string[index_start:index_end].split(",")
    else:
        return None

def extract_default_coreos_list(legacy_setup_string):
    index_start=legacy_setup_string.find("<core_os:")
    if(index_start!=-1):
        index_start=legacy_setup_string.find(":",index_start)
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start)
        return legacy_setup_string[index_start:index_end].split(",")
    else:
        return None

def extract_custom_cores(index_start,legacy_setup_string,search_string):
    length_of_search_string=len(search_string)
    index_end=legacy_setup_string.find(">",index_start)
    return legacy_setup_string[index_start+length_of_search_string:index_end].split(",")

def extract_hw_assets(legacy_setup_string):
    print(len("""hw_assets:dut1=[""<platform>\"\""""))
    index_start=legacy_setup_string.find("""hw_assets:dut1=[""<platform>\"\"""")
    if(index_start!=-1):
        index_start+=1
        index_end=legacy_setup_string.find(">",index_start+30)
        index_end-=1
    return legacy_setup_string[index_start+30:index_end]

def extract_project_id(element):
    index_start=element.find("projectid=")
    index_start+=10
    index_end=element.find(";",index_start)
    return element[index_start+1:index_end]


#default timeout is coded to 1st element in commands add logic to change it to jira_timeout if no timeout is present
def extract_commands(command_string):
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
                #print(current_dict)
                current_dict={}
                break
            #Not last element cases
            #if next element is timeout add None as UART input to the list and add the current dictionary to the list
            if(command_list[i+1].find("tout:")!=-1):
                current_dict["uart_input"]=None
                uart_list.append(current_dict)
                #print(current_dict)
                current_dict={}
            #if next element is uart input add it to the current dictionary and add the current dictionary to the list 
            else:
                current_dict["uart_input"]=command_list[i+1]
                i+=1
                uart_list.append(current_dict)
                #print(current_dict)
                current_dict={}
        #if current element is timeout add timeout to the current dictionary
        elif(element.find("tout:")!=-1):
            current_dict["timeout"]=element[5:]
        #if current element is uart input, this case will not come as we are append the uart input in previous case and doing i+=1
        else:
            pass
            #print(str(i)+"\n"+"unknown command")
        #increment the while loop
        i+=1
    print(uart_list)
    return uart_list

def extract_constraints(constraints_string,jira_timeout):
    constraints_string=constraints_string[12:]
    #print(constraints_string)
    current_dict={}
    current_dict["timeout"]=jira_timeout
    current_dict["expected_string_in_uart_logs"]=constraints_string
    current_dict["uart_input"]=None
    return [current_dict]

def extract_params_dut(params_dut_string,jira_timeout):
    #print("\n\n"+params_dut_string)
    params_dut_list=params_dut_string.split(";")
    uart_list_of_dict=None
    #spliting params_dut wrt ; and check for each element 
    for element in params_dut_list:
        if(element.find("projectid")!=-1):
            project_id=extract_project_id(element)
            #print(project_id)
        elif(element.find("commands")!=-1):
            uart_list_of_dict=extract_commands(element)
        elif(element.find("constraints")!=-1):
            uart_list_of_dict=extract_constraints(element,jira_timeout)
    return [project_id,uart_list_of_dict]

def extract_scripts(scripts_string):
    index_start=scripts_string.find("<scripts:")
    index_end=scripts_string.find(">",index_start)
    return scripts_string[index_start+9:index_end]

def test_setup_legacy_parser(legacy_setup_string,jira_timeout,exact_platform_name):

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
    #print("default core list is ",default_list)
    #extracting core_platform_name
    search_string="<core_"+exact_platform_name+":"
    index_start=legacy_setup_string.find(search_string)
    core_list=[]
    if(index_start!=-1):
        core_list=extract_custom_cores(index_start,legacy_setup_string,search_string)
    else:
        core_list=default_list
    
    #print("core list is ",core_list)
    #parsing hw_assets
    hw_assets="None"
    if(legacy_setup_string.find("<hw_assets:")!=-1):
        hw_assets=extract_hw_assets(legacy_setup_string)
        #print(hw_assets)
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
    #pretty_print(uart_list_of_dict)
    #print("project id is ",project_id)
    #parsing scripts
    scripts="None"
    if(legacy_setup_string.find("<scripts:")!=-1):
        scripts=extract_scripts(legacy_setup_string)
        #print(scripts)
    return [core_list,uart_list_of_dict,project_id,hw_assets,scripts]
    

#test_setup_legacy_parser(legacy_setup_string,120,"am275x-hsse")