from fastmcp import FastMCP
import requests
import os

# Create a server instance
mcp = FastMCP(
    name="MyAssistantServer", 
              instructions="You are a helpful assistant that can help with tasks related to HiBob. You can use the tools provided to you to get information and perform actions. when using search tools, you need to use the filters to get the employee you are looking for. if you are not sure about the employee, you can use the search tools always use metadata to get the fields"              
              )

def _hibob_api_call(endpoint: str, body: dict = None, method: str = "POST") -> dict:
    """Helper to call the HiBob API with proper headers, supporting GET and POST."""
    url = f"https://api.hibob.com/v1/{endpoint}"
    hibob_token = os.environ.get("HIBOB_API_TOKEN", "")
    headers = {
        'authorization': f'Basic {hibob_token}',
        'content-type': 'application/json',
        'X-Requested-With': 'hibob-public-mcp'
    }
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, json=body, headers=headers)
    elif method == "PUT":
        response = requests.put(url, json=body, headers=headers)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    response.raise_for_status()
    
    # Check if the response has content before trying to parse it as JSON
    if response.text and response.text.strip():
        try:
            return response.json()
        except ValueError:
            # Return a dictionary with the text content if it can't be parsed as JSON
            return {"text": response.text, "status_code": response.status_code}
    else:
        # Return a success message with status code for empty responses
        return {"message": "Success", "status_code": response.status_code}

@mcp.tool()
def hibob_people_search(fields: list = None, filters: list = None, showInactive: bool = False) -> dict:
    """
    Search for employees in HiBob using advanced filters.

    To get available field paths for fields always use the hibob_get_employee_fields tool before using this tool.
    important to search just the relevant fields you need! otherwise the responce can be very large and slow.


    Parameters:
        fields (list, optional): List of field paths to return for each employee. Use hibob_get_employee_fields to discover available fields.
        filters (list, optional): filter by ID or email. Options - 
        Example filter usage:
        filters = [
            {
                "fieldPath": "root.id",
                "operator": "equals",
                "values": ["EMPLOYEE_ID"]
            }
        ] 
        OR
        filters = [
            {
                "fieldPath": "root.email",
                "operator": "equals",
                "values": ["bla@example.com"]
            }
        ]

        to find employee by name you need to fetch with empty filters and then filter by name by yourself.

        showInactive = true
            to the filters to get all employees including inactive ones - use this to show new hires, or terminated employees, or employees on leave statues
         
        Example:
        hibob_people_search(
        fields=["root.id", "root.firstName", "root.surname", "root.email"],
        filters=[{"fieldPath": "root.id", "operator": "equals", "values": ["EMPLOYEE_ID"]}]
        showInactive=true)


    """
    body = {}
    if fields:
        body["fields"] = fields
    if filters:
        body["filters"] = filters
    if showInactive:
        body["showInactive"] = showInactive
    return _hibob_api_call("people/search", body)

@mcp.tool()
def hibob_get_employee_fields() -> dict:
    """
    Get metadata about all employee fields from HiBob.
    Use this tool to discover available field paths for use in filters in hibob_people_search.
    """
    return _hibob_api_call("company/people/fields", method="GET")

@mcp.tool()
def hibob_update_employee(employeeId: str, fields: dict) -> dict:
    """
    Update specific fields in an employee's record in HiBob.
    Only employee fields are supported; table updates are not allowed via this endpoint.
    Parameters:
        employeeId (string, mandatory): List of field paths to return for each employee. Use hibob_get_employee_fields to discover available fields.
        fields (dict, mandatory): object with field to value for update. example: {"root.firstName": "NewName"}
    Example usage:
        hibob_update_employee("EMPLOYEE_ID", {"root.firstName": "NewName"})
    To get available field for filters and fields, use the hibob_get_employee_fields tool.
    See: https://apidocs.hibob.com/reference/put_people-identifier
    """
    endpoint = f"people/{employeeId}"
    return _hibob_api_call(endpoint, body=fields, method="PUT")

@mcp.tool()
def hibob_get_timeoff_policy_types() -> dict:
    """
    Get a list of all timeoff policy type names from HiBob.
    See: https://apidocs.hibob.com/reference/get_timeoff-policy-types
    """
    return _hibob_api_call("timeoff/policy-types", method="GET")

@mcp.tool()
def hibob_submit_timeoff_request(employee_id: str, request_details: dict) -> dict:
    """
    Submit a new time off request for an employee in HiBob.
    
    Parameters:
        employee_id (str): The HiBob employee ID.
        request_details (dict): The request body as required by the API. See the API docs for required fields for each request type.
            Common parameters for a Holiday request include:
                - policyType (str): The time off type, e.g., "Holiday"
                - requestRangeType: Value must be 'days'. mandatory. (automatically added)
                - startDatePortion: Value must be 'all_day'. mandatory.
                - endDatePortion: Value must be 'all_day'. mandatory.
                - startDate (str): Start date in YYYY-MM-DD format
                - endDate (str): End date in YYYY-MM-DD format
                - reason (str, optional): Reason for the request
                - comment (str, optional): Additional comments
                - halfDay (bool, optional): If the request is for a half day
                - policyType (str, optional): Policy type name
                - reasonCode (str, optional): Reason code if required by policy

            Example:
                hibob_submit_timeoff_request(
                    "EMPLOYEE_ID",
                    {
                        "policyType": "Holiday",
                        "startDate": "2024-07-01",
                        "endDate": "2024-07-05",
                        "startDatePortion": 'all_day',
                        "endDatePortion": 'all_day',
                        "reason": "Vacation",
                        "comment": "Family trip",
                        "halfDay": False
                    }
                )
    
    See: https://apidocs.hibob.com/reference/post_timeoff-employees-id-requests
    """
    # Always ensure requestRangeType is set to "days"
    request_details["requestRangeType"] = "days"
    
    endpoint = f"timeoff/employees/{employee_id}/requests"
    return _hibob_api_call(endpoint, body=request_details, method="POST")

@mcp.tool()
def hibob_create_employee(fields: dict) -> dict:
    """
    Create a new employee record in HiBob.

    Parameters:
        fields (dict): Dictionary of employee fields to set. Only fields listed in the Fields Metadata API are allowed.
        check that you have site and startDate which are manadatory
        use the jsonPath to set the fields. example: "firstName" should be in the first level of the json.
        personal.honorific should be in the personal level of the json, like  
        { "personal": { "honorific": "Mr." } }

    Example usage:
        hibob_create_employee({
            "root.firstName": "Jane",
            "root.surname": "Doe",
            "root.email": "jane.doe@example.com"
        })

    Example fields param for the api call - 
            {
            "work": {
                "site": "US",
                "startDate": "2025-05-03"
            },
            "firstName": "shuki",
            "surname": "buki",
            "email": "shuki@fake.com"
            }
    
    See: https://apidocs.hibob.com/reference/post_people
    """
    return _hibob_api_call("people", body=fields, method="POST")

@mcp.tool()
def hibob_get_employee_tasks(employee_id: str) -> dict:
    """
    Get all tasks for a specific employee in HiBob.

    Parameters:
        employee_id (str): The HiBob employee ID.

    Example usage:
        hibob_get_employee_tasks("EMPLOYEE_ID")

    See: https://apidocs.hibob.com/reference/get_tasks-people-id
    """
    endpoint = f"tasks/people/{employee_id}"
    return _hibob_api_call(endpoint, method="GET")

@mcp.tool()
def hibob_get_timeoff_balance(employee_id: str) -> dict:
    """
    Get the timeoff balance for a given employee.

    Parameters:
        employee_id (str): The HiBob employee ID.

    Example usage:
        hibob_get_timeoff_balance("EMPLOYEE_ID")

    See: https://api.hibob.com/v1/timeoff/employees/{id}/balance
    API Docs: https://apidocs.hibob.com/reference/get_timeoff-employees-id-balance
    """
    endpoint = f"timeoff/employees/{employee_id}/balance"
    return _hibob_api_call(endpoint, method="GET")

@mcp.tool()
def hibob_upload_avatar(employee_id: str, image_url: str) -> dict:
    """
    Upload an employee's avatar by providing a URL to the image.

    Parameters:
        employee_id (str): The HiBob employee ID.
        image_url (str): URL of the image to upload as the employee's avatar.

    Example usage:
        hibob_upload_avatar("EMPLOYEE_ID", "https://example.com/profile-photo.jpg")

    See: https://apidocs.hibob.com/reference/put_avatars-employeeid
    """
    endpoint = f"avatars/{employee_id}"
    body = {"url": image_url}
    result = _hibob_api_call(endpoint, body=body, method="PUT")
    
    # If the result contains a status_code, check if it's a success code
    if isinstance(result, dict) and "status_code" in result:
        if 200 <= result["status_code"] < 300:
            return {"status": "success", "message": f"Avatar uploaded successfully for employee {employee_id}"}
    
    return result

if __name__ == "__main__":
    mcp.run(transport="stdio")
