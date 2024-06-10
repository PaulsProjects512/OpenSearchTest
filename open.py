import pycurl
import certifi
from io import BytesIO
import json
from opensearchpy import OpenSearch

# Use dictionaries with the DOI or similar as the key.
authorsName = []
institutionNames = []
publications = []
themes = []
dataObjects = []

def readAuthorsFromOpenSearch():
    host = 'localhost'
    port = 9200
    auth = ('admin',
            'admin')  # For testing only. Don't store credentials in code.a_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Optional client certificates if you don't want to use HTTP basic authentication.
    client_cert_path = '/full/path/to/client.pem'
    client_key_path = '/full/path/to/client-key.pem'
    ca_certs_path = '/full/path/to/root-ca.pem'  # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        # ca_certs = ca_certs_path
    )

    authors_index_name = 'authors_index'

    query = {
        'size': 50,
        'query': {
            'match_all': {},
        }
    }

    # READ from the opensearch database
    allAuthors = client.search(body=query, index=authors_index_name)
    #print("Search all authors at UK Cat = ", allAuthors)
    with open('./authors.json', 'w') as f:
        f.write(json.dumps(allAuthors, indent=4))

def writeAuthorsToOpenSearch():
    host = 'localhost'
    port = 9200
    auth = ('admin',
            'admin')  # For testing only. Don't store credentials in code.a_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Optional client certificates if you don't want to use HTTP basic authentication.
    client_cert_path = '/full/path/to/client.pem'
    client_key_path = '/full/path/to/client-key.pem'
    ca_certs_path = '/full/path/to/root-ca.pem'  # Provide a CA bundle if you use intermediate CAs with your root CA.

    # Create the client with SSL/TLS enabled, but hostname verification disabled.
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        # client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl=True,
        verify_certs=False,
        ssl_assert_hostname=False,
        ssl_show_warn=False,
        # ca_certs = ca_certs_path
    )

    authors_index_name = 'authors_index'

    # Delete the existing authors index if there is one.
    delRes = client.indices.delete(authors_index_name)
    print("del exisiting = ", delRes)

    print('Number of authors = ', len(authorsName))
    # write each author as a document to the index
    count = 1
    for author in authorsName:
        client.index(index=authors_index_name,
                     body=author,
                     id=str(count))
        count = count + 1

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

        if json == "[]":   # or json.find('404') > -1:
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
#writeAuthorsToOpenSearch()
readAuthorsFromOpenSearch()

extractInstitutions()
print("number of institutaions = ", len(institutionNames))

extractPublications()
print("number of publications = ", len(publications))

extractDataObjects()
print("number of data objects = ", len(dataObjects))
