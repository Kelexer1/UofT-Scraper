import requests

def scrapeReferenceData():
    """ Return a JSON representation of the reference data needed to browse courses.
    This includes:
    - Campuses
    - Departments / Faculties
    - Sessions
    """
    url = "https://api.easi.utoronto.ca/ttb/reference-data"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        responseJson = response.json()['payload']
        result = { 'currentSessions': {}, 'divisions': [], 'campuses': [] }

        #
        # Parse currentSessions
        #

        # First pass to define all session groups
        for session in responseJson['currentSessions']:
            if not session['value'][0].isdigit():
                result['currentSessions'][session['group']] = {
                    'label': session['label'],
                    'value': session['value'],
                    'subsessions': []
                }

        # Second pass to distribute all subsessions
        for session in responseJson['currentSessions']:
            if session['value'][0].isdigit():
                result['currentSessions'][session['group']]['subsessions'].append({
                    'label': session['label'],
                    'value': session['value']
                })

        #
        # Parse divisions
        #

        for division in responseJson['divisions']:
            result['divisions'].append({
                'label': division['label'],
                'value': division['value'],
            })

        #
        # Parse campuses
        #

        for campus in responseJson['campuses']:
            result['campuses'].append({
                'label': campus['label'],
                'value': campus['value']
            })

        return result