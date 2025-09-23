import re

def formatCourseData(course):
    """ Format the server JSON response for <course> to save space by deleting niche parameters and precomputing enrolment controls.
    Also modifies some parameters to be easier to work with (ex. days converted to seconds after midnight). 
    """

    del course['id']
    del course['ucName']
    del course['duration']
    del course['created']
    del course['modified']
    del course['lastSaved']
    del course['subscriptionTtb']
    del course['subscriptionOpenData']
    del course['tb1Active']
    del course['tb2Active']

    for section in course['sections']:
        del section['teachMethod']
        del section['firstMeeting']

        for meetingTime in section['meetingTimes']:
            meetingTime['day'] = meetingTime['start']['day']
            meetingTime['start'] = meetingTime['start']['millisofday'] / 1000
            meetingTime['end'] = meetingTime['end']['millisofday'] / 1000

            del meetingTime['building']['buildingRoomNumber']
            del meetingTime['building']['buildingRoomSuffix']
            del meetingTime['building']['buildingName']

        section['enrolmentControls'] = parseEnrolmentControls(section['enrolmentControls'])

    if course.get('cmCourseInfo'):
        course['cmCourseInfo']['prerequisitesText'] = re.sub(r"<.*?>", "", course['cmCourseInfo'].get('prerequisitesText') or "") or None
        course['cmCourseInfo']['corequisitesText'] = re.sub(r"<.*?>", "", course['cmCourseInfo'].get('corequisitesText') or "") or None
        course['cmCourseInfo']['exclusionsText'] = re.sub(r"<.*?>", "", course['cmCourseInfo'].get('exclusionsText') or "") or None
        course['cmCourseInfo']['recommendedPreparation'] = re.sub(r"<.*?>", "", course['cmCourseInfo'].get('recommendedPreparation') or "") or None

    return course

def parseEnrolmentControls(controls):
    """ Parses the list of enrolment controls into a list of the string representations. Taken from ttb.utoronto.ca source code
    and modified slightly
    """
    lines = []

    for control in controls:
        if control['post']['code'] != 'EXCEPTIONS':
            base = "All students" if control['quantity'] else 'No students'

            if control['yearOfStudy'] != '*':
                line = f'{base} in year of study {control['yearOfStudy']} '
            else:
                line = f'{base} '

            line += getDescription(control["primaryOrg"], f"in the {control['primaryOrg']['name']}")
            line += getDescription(control["associatedOrg"], f"in the {control['associatedOrg']['name']}")
            line += getDescription(control["secondOrg"], f"in the {control['secondOrg']['name']}")
            line += getDescription(control["adminOrg"], f"in the {control['adminOrg']['name']}")
            line += getDescription(control["post"], f"in the {control['post']['name']}")
            line += getDescription(control["subjectPost"], f"in the {control['subjectPost']['name']}")
            line += getDescription(control["subject"], f"in {control['subject']['name']}")
            line += getDescription(control["designation"], f"{control['designation']['name']}s")

            lines.append(line.strip())

    seen = set()
    uniqueLines = []

    for line in lines:
        if line not in seen:
            seen.add(line)
            uniqueLines.append(line)

    return uniqueLines

def getDescription(field, textIfNotAll, suffix = ' '):
    """ Return a description for an enrolment control. Helper method for parseEnrolmentControls
    """
    code = field.get('code', '').strip()
    name = field.get('name', '').strip()

    if code and code != '*' and name:
        return (textIfNotAll or f"the {name}") + (suffix or '')
    return ''