import requests
def fetch_testcases_using_jira_api(jira_filter, bearer_token):
    """Fetch testcases using Jira API with Bearer token authentication

    Args:
        jira_filter (string): JQL
        bearer_token (string): Bearer token for authentication

    Returns:
        dict: test case data
    """
    # base url
    jqsl_api_base_url = "https://jira.itg.ti.com/rest/api/2/search/"
    request_type = "GET"
    
    # Set up headers with Bearer token
    headers = {
        "Accept": "application/json", 
        "Content-Type": "application/json",
        "Authorization": f"Bearer {bearer_token}"
    }

    # Define the maximum number of results per request
    max_results = 1000

    # Initialize the startAt parameter
    start_at = 0

    # Create an empty list to store all issues
    all_testcases = []

    while True:
        jira_query = {
            "jql": jira_filter,
            "startAt": start_at,
            "maxResults": max_results,
        }
        response = requests.request(
            request_type,
            url=jqsl_api_base_url,
            headers=headers,
            params=jira_query
        )

        # Convert the http response to json
        test_case_data = response.json()

        # Add the issues from this response to the list of all issues
        all_testcases.extend(test_case_data["issues"])
        
        # Check if there are more issues to fetch
        total = test_case_data["total"]
        if start_at + max_results >= total:
            break
        
        # Update the startAt parameter for the next request
        start_at += max_results

    print( all_testcases)

fetch_testcases_using_jira_api("""issuekey = \"MCUSDK-1001\"""", "XrClUfvKjXPW2xjvGMnQ54MPhRr2rFua3Su3yL")