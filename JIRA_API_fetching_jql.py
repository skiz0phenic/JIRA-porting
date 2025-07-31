
def JIRA_API_extracting(result):
    try:
        jira_test_application_name=result['fields']['customfield_16927']
    except:
        jira_test_application_name="No_app_name"
    #print(jira_test_application_name)
    try:
        jira_test_component=result['fields']['components'][0]['name']
    except:
        jira_test_component="No_component"
    #print(jira_test_component)

    try:
        jira_test_subcomponent=result['fields']['customfield_10212'][0]
    except:
        jira_test_subcomponent="No_subcomponent"
    #print(jira_test_subcomponent)
    try:
        jira_test_description=result["fields"]["description"]
    except:
        jira_test_description="No_description"
    #print(jira_test_description)
    try:
        jira_test_setup=result['fields']['customfield_19800']
    except:
        jira_test_setup="No_test_setup"
    #print(jira_test_setup)
    try:
        jira_timeout=result['fields']['customfield_16928']
    except:
        jira_timeout="No_timeout"

    return [jira_test_application_name,jira_test_component,jira_test_subcomponent,jira_test_description,jira_test_setup,jira_timeout]
