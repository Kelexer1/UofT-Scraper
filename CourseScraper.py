import json
from time import sleep, time
import math
import os

from CourseSearch import scrapePageableCourses
from FormatCourse import formatCourseData
from MiscSearch import scrapeReferenceData

# =========================
# CONFIG DATA
# =========================

OUTPUT_DIRECTORY = './output/'              # The path to the output folder

COURSES_FILE_NAME = 'courses.json'          # The file name to write the course data to
DIVISIONAL_FILE_NAME = 'divisional.json'    # The file name to write the divisional data to
REFERENCE_FILE_NAME = 'reference.json'      # The file name to write the reference data to
MISC_FILE_NAME = 'misc.json'                # The file name to write the miscellaneous data to

REQUEST_DELAY = 0.3                         # The time between API requests, setting it too low may cause rate limiting
MAX_PAGES = -1                              # The number of pages of courses to scrape. Set to -1 for no limit (all courses)

# =========================

class CourseScraper:
    """ A class to scrape course data and other reference data to a set of JSON files

    Usage:
    >>> CourseScraper.scrape()
    """

    def scrape() -> None:
        """ A method to scrape course data. Note that this method is not immediate,
        and can take 5+ minutes depending on how low your <REQUEST_DELAY> is
        """
        REFERENCE_DATA = scrapeReferenceData()

        DIVISIONS = [division['value'] for division in REFERENCE_DATA['divisions']]
        SESSIONS = list(set([subsession['value'] for sessionGroup in REFERENCE_DATA['currentSessions'].values() for subsession in sessionGroup['subsessions']]))

        PAGE_SIZE = 20

        page = 1
        scraping = True

        test = scrapePageableCourses(SESSIONS, DIVISIONS, 1, 1)

        TOTAL_COURSES = test[1]
        TOTAL_PAGES = math.ceil(TOTAL_COURSES / PAGE_SIZE)

        outputData = {}
        for session in SESSIONS:
            outputData[session] = []

        outputDivisionalLegends = {}
        outputDivisionalEnrolmentIndicators = {}

        startTime = time()
        while scraping:
            scrapeChunk = scrapePageableCourses(SESSIONS, DIVISIONS, page, PAGE_SIZE)

            # Divisional Legends
            for division in scrapeChunk[2]:
                if division not in outputDivisionalLegends:
                    outputDivisionalLegends[division] = scrapeChunk[2][division]

            # Divisional Enrolment Indicators
            for division in scrapeChunk[3]:
                if division not in outputDivisionalEnrolmentIndicators:
                    outputDivisionalEnrolmentIndicators[division] = scrapeChunk[3][division]

            # Course Data
            for course in scrapeChunk[0]:
                sessions = '-'.join(course['sessions'])
                outputData[sessions].append(formatCourseData(course))

            if len(scrapeChunk[0]) < PAGE_SIZE or (page >= MAX_PAGES > 0):
                scraping = False
            else:
                pages_left = TOTAL_PAGES - page
                est_time_remaining = pages_left * REQUEST_DELAY

                if os.name == 'nt':
                    os.system('cls')
                else:
                    os.system('clear')

                print(f"Scraping {page * PAGE_SIZE} / {TOTAL_COURSES} courses:\n{scrapeChunk[0][0]['code']} => {scrapeChunk[0][-1]['code']}\nEstimated time remaining: {round(est_time_remaining / 60 * 1.33, 2)} minutes")

                page += 1
                sleep(REQUEST_DELAY)

        print(f'Finished scraping in {(time() - startTime) / 60} minutes')

        print('Writing results to output files...')

        # Course Data
        with open(OUTPUT_DIRECTORY + COURSES_FILE_NAME, 'w') as output:
            json.dump(outputData, output, indent=4)

        # Divisional Data
        with open(OUTPUT_DIRECTORY + DIVISIONAL_FILE_NAME, 'w') as output:
            json.dump({
                'divisionalLegends': outputDivisionalLegends,
                'divisionalEnrolmentIndicators': outputDivisionalEnrolmentIndicators
            }, output, indent=4)

        # Reference Data
        with open(OUTPUT_DIRECTORY + REFERENCE_FILE_NAME, 'w') as output:
            json.dump(REFERENCE_DATA, output, indent=4)

        # Misc Data
        with open(OUTPUT_DIRECTORY + MISC_FILE_NAME, 'w') as output:
            json.dump({
                'totalCourses': TOTAL_COURSES
            }, output, indent=4)

        print('Finished writing to output files')