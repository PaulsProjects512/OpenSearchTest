import pycurl
import certifi
from io import BytesIO
import json

# Use dictionaries with the DOI or similar as the key.
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
        themes.append(dict(item))

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
        publications.append(dict(item))

def extractPublications():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/articles.json?page=' + str(pageNumber)

        json = readURL(url)
        getPublications(json)

        pageNumber = pageNumber + 1

        if json == "[]": # or json.find('404') > -1:
            # Terminate the page reader on an empty reply.
            keepTrying = False

# Read the institution information.
def getInstitutions(jsonData):
    data = json.loads(jsonData)
    for item in data:
        institutionNames.append(dict(item))

def extractInstitutions():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/affiliations.json?page=' + str(pageNumber)

        json = readURL(url)
        getInstitutions(json)

        pageNumber = pageNumber + 1

        if json == "[]":  # or json.find('404') > -1:
            # Terminate the page reader on an empty reply.
            keepTrying = False

# Read all the authors names from the json data amd store them.
def getAuthors(jsonData):
    data = json.loads(jsonData)
    for item in data:
        authorsName.append(dict(item))

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

        if json == "[]": # or json.find('404') > -1:
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

        if json == "[]" or pageNumber > 10: # or json.find('404') > -1:
            # Terminate the page reader on an empty reply.
            keepTrying = False

def getDataObjects(jsonData):
    data = json.loads(jsonData)
    for item in data:
        dataObjects.append(dict(item))

# data object list reading.
def extractAuthorsFromWebservice():
    pageNumber = 1
    keepTrying = True
    while keepTrying:
        url = 'http://cdi.ukcatalysishub.org/authors.json?page=' + str(pageNumber)

        json = readURL(url)
        getAuthors(json)
        pageNumber = pageNumber + 1

        if json == "[]": # or json.find('404') > -1:
            # Terminate the page reader on an empty reply.
            keepTrying = False
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
