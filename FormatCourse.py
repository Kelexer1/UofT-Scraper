import re

def formatCourseData(course):
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
    code = field.get('code', '').strip()
    name = field.get('name', '').strip()

    if code and code != '*' and name:
        return (textIfNotAll or f"the {name}") + (suffix or '')
    return ''

if __name__ == '__main__':
    testData = {
        "id": "67fcf9bede40c67f1da33b94",
        "name": "Introduction to Academic Studies",
        "ucName": None,
        "code": "ABP100Y1",
        "sectionCode": "Y",
        "campus": "St. George",
        "sessions": [
            "20259",
            "20261"
        ],
        "sections": [
            {
                "name": "LEC0101",
                "type": "Lecture",
                "teachMethod": "LEC",
                "sectionNumber": "0101",
                "meetingTimes": [
                    {
                        "start": {
                            "day": 2,
                            "millisofday": 36000000
                        },
                        "end": {
                            "day": 2,
                            "millisofday": 46800000
                        },
                        "building": {
                            "buildingCode": "WW",
                            "buildingRoomNumber": "",
                            "buildingRoomSuffix": "",
                            "buildingUrl": "https://map.utoronto.ca/?id=1809#!m/494547",
                            "buildingName": None
                        },
                        "sessionCode": "20259",
                        "repetition": "WEEKLY",
                        "repetitionTime": "ONCE_A_WEEK"
                    },
                    {
                        "start": {
                            "day": 2,
                            "millisofday": 36000000
                        },
                        "end": {
                            "day": 2,
                            "millisofday": 46800000
                        },
                        "building": {
                            "buildingCode": "WW",
                            "buildingRoomNumber": "",
                            "buildingRoomSuffix": "",
                            "buildingUrl": "https://map.utoronto.ca/?id=1809#!m/494547",
                            "buildingName": None
                        },
                        "sessionCode": "20261",
                        "repetition": "WEEKLY",
                        "repetitionTime": "ONCE_A_WEEK"
                    }
                ],
                "firstMeeting": None,
                "instructors": [],
                "currentEnrolment": 18,
                "maxEnrolment": 30,
                "subTitle": "",
                "cancelInd": "N",
                "waitlistInd": "N",
                "deliveryModes": [
                    {
                        "session": "20259",
                        "mode": "INPER"
                    },
                    {
                        "session": "20261",
                        "mode": "INPER"
                    }
                ],
                "currentWaitlist": 0,
                "enrolmentInd": "E",
                "tbaInd": "N",
                "openLimitInd": "N",
                "notes": [
                    {
                        "name": "Section Note",
                        "type": "SECTION",
                        "content": ""
                    }
                ],
                "enrolmentControls": [
                    {
                        "yearOfStudy": "*",
                        "post": {
                            "code": "AS   NDEGB",
                            "name": "Academic Bridging Program"
                        },
                        "subject": {
                            "code": "*",
                            "name": "All"
                        },
                        "subjectPost": {
                            "code": "",
                            "name": ""
                        },
                        "typeOfProgram": {
                            "code": "*",
                            "name": "All"
                        },
                        "designation": {
                            "code": "*",
                            "name": "All"
                        },
                        "primaryOrg": {
                            "code": "*",
                            "name": "All"
                        },
                        "associatedOrg": {
                            "code": "*",
                            "name": "All"
                        },
                        "secondOrg": {
                            "code": "*",
                            "name": "All"
                        },
                        "adminOrg": {
                            "code": "*",
                            "name": "All"
                        },
                        "collaborativeOrgGroupCode": "*",
                        "quantity": 30,
                        "sequence": 1
                    }
                ],
                "linkedMeetingSections": None
            }
        ],
        "duration": None,
        "cmCourseInfo": {
            "description": "This interdisciplinary, skills-focused course parallels the other component courses of the full-time Academic Bridging Program, supplementing those courses and helping students integrate their entire Academic Bridging experience, while providing intensive, workshop-style training in the fundamental skills needed for success in further university studies in the Humanities and Social Sciences. The course will also provide academic advising and planning, to help students understand and navigate university culture. Open only to Academic Bridging Program students. Not eligible for CR/NCR option.",
            "title": "Introduction to Academic Studies",
            "levelOfInstruction": "undergraduate",
            "prerequisitesText": "",
            "corequisitesText": "",
            "exclusionsText": "",
            "recommendedPreparation": "",
            "note": None,
            "division": "Arts and Science, Faculty of",
            "breadthRequirements": [
                "Creative and Cultural Representations (1)",
                "Society and its Institutions (3)"
            ],
            "distributionRequirements": [
                "Humanities"
            ],
            "publicationSections": [
                "Academic Bridging Program"
            ],
            "cmPublicationSections": [
                {
                    "section": "Academic Bridging Program",
                    "subSections": None
                }
            ]
        },
        "created": "2025-07-29@01:38:48.021",
        "modified": None,
        "lastSaved": 0,
        "primaryTeachMethod": "LEC",
        "faculty": {
            "code": "ARTSC",
            "name": "Faculty of Arts and Science"
        },
        "coSec": {
            "code": "",
            "name": None
        },
        "department": {
            "code": "WDW",
            "name": "Woodsworth College"
        },
        "title": None,
        "maxCredit": 0.0,
        "minCredit": 0.0,
        "breadths": [
            {
                "org": {
                    "code": "ARTSC",
                    "name": "Faculty of Arts and Science"
                },
                "breadthTypes": [
                    {
                        "kind": "BREADTH",
                        "type": "Creative Cultural",
                        "description": "BR=1 Creative and Cultural Representation",
                        "code": "BR=1"
                    }
                ]
            }
        ],
        "notes": [
            {
                "name": "Course Note",
                "type": "COURSE",
                "content": "<p><strong>Timetable Instructions</strong></p><p>This course is available only to students in the Academic Bridging Program.&nbsp; For more information, please contact academic.bridging@utoronto.ca or 416-978-4444.</p>"
            }
        ],
        "cancelInd": "N",
        "subscriptionTtb": False,
        "subscriptionOpenData": False,
        "tb1Active": False,
        "tb2Active": False,
        "primaryFull": False,
        "fullyOnline": False,
        "primaryWaitlistable": False
    }

    print(formatCourseData(testData))