import requests
import json

def scrapePageableCourses(sessions: list[str], divisions: list[str], page, pageSize):
    """ Return a JSON representation of the pageable courses
    """
    url = "https://api.easi.utoronto.ca/ttb/getPageableCourses"

    payload = {
        "courseCodeAndTitleProps": {
            "courseCode": '',
            "courseTitle": '',
            "courseSectionCode": ''
        },
        "departmentProps": [],
        "campuses": [],
        "sessions": sessions,
        "requirementProps": [],
        "instructor": "",
        "courseLevels": [],
        "deliveryModes": [],
        "dayPreferences": [],
        "timePreferences": [],
        "divisions": divisions,
        "creditWeights": [],
        "availableSpace": False,
        "waitListable": False,
        "page": page,
        "pageSize": pageSize,
        "direction": "asc"
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    if response.ok:
        result = response.json()
        return (result['payload']['pageableCourse']['courses'], result['payload']['pageableCourse']['total'], result['payload']['divisionalLegends'], result['payload']['divisionalEnrolmentIndicators'])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None