import pycurl
import certifi
from io import BytesIO
import json

authorsName = []
institutionNames = []
publications = []
themes = []
dataObjects = []

# Read the webpage as json.
def readURL(url):
    try:
        c = pycurl.Curl()
        buffer = BytesIO()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.CAINFO, certifi.where())
        c.perform()
        c.close()

        body = buffer.getvalue()
        text = body.decode('iso-8859-1')

        return text

    except:
        return "Error reading: " + url

# Read the theme information.
def getTheme(jsonData):
    data = json.loads(jsonData)
    for item in data:
        name = str(item["name"]) + ", " + str(item["url"])
        themes.append(name)

def extractThemes(printout=False):
    url = 'http://cdi.ukcatalysishub.org/themes.json'

    json = readURL(url)
    getTheme(json)

    if printout:
        print("Number of themes = ", len(themes))

# Read the publication information.
def getPublications(jsonData):
    data = json.loads(jsonData)
    for item in data:
        name = str(item["title"]) + ", " + str(item["link"]) + ", " + str(item["doi"]) + ", " + str(item["pub_print_year"])
        publications.append(name)

def extractPublications():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/articles.json?page=' + str(pageNumber)

        json = readURL(url)
        getPublications(json)

        pageNumber = pageNumber + 1

        if json == "[]":
            # Terminate the page reader on an empty reply.
            keepTrying = False

# Read the institution information.
def getInstitutions(jsonData):
    data = json.loads(jsonData)
    for item in data:
        name = item["institution"]
        institutionNames.append(name)

def extractInstitutions():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/affiliations.json?page=' + str(pageNumber)

        json = readURL(url)
        getInstitutions(json)

        pageNumber = pageNumber + 1

        if json == "[]":
            # Terminate the page reader on an empty reply.
            keepTrying = False

# Read all the authors names from the json data amd store them.
def getAuthors(jsonData):
    data = json.loads(jsonData)
    for item in data:
        fullName = item["given_name"] + ", " + item["last_name"] + ", " + item["orcid"]
        authorsName.append(fullName)

'''
Py curl method of read Catalysis UK publications database.
'''
def extractAuthorsFromWebservice():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/authors.json?page=' + str(pageNumber)

        json = readURL(url)
        getAuthors(json)

        pageNumber = pageNumber + 1

        if json == "[]":
            # Terminate the page reader on an empty reply.
            keepTrying = False

def extractDataObjects():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/datasets.json?page=' + str(pageNumber)

        json = readURL(url)
        getDataObjects(json)

        pageNumber = pageNumber + 1

        if json == "[]" or pageNumber > 10:
            # Terminate the page reader on an empty reply.
            keepTrying = False

def getDataObjects(jsonData):
    data = json.loads(jsonData)
    for item in data:
        d1 = item["dataset_description"]
        d2 = item["dataset_doi"]
        d3 = item["dataset_location"]
        dataObjectName = str(item["dataset_description"]) + ", " + str(item["dataset_doi"]) + ", " + item["dataset_location"]
        dataObjects.append(dataObjectName)

# data object list reading.
def extractAuthorsFromWebservice():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/authors.json?page=' + str(pageNumber)

        json = readURL(url)
        getAuthors(json)

        pageNumber = pageNumber + 1

        if json == "[]":
            # Terminate the page reader on an empty reply.
            keepTrying = False

#============================================================
# Run the loading process.
print("started to load the .....")

extractThemes(True)

extractAuthorsFromWebservice()
print("number of authors = ", len(authorsName))

extractInstitutions()
print("number of institutaions = ", len(institutionNames))

extractPublications()
print("number of publications = ", len(publications))

extractDataObjects()
print("number of data objects = ", len(dataObjects))

