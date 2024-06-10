import opensearchpy.client.ingest
from opensearchpy import OpenSearch
import json

host = 'localhost'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.a_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
client_cert_path = '/full/path/to/client.pem'
client_key_path = '/full/path/to/client-key.pem'
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,  # enables gzip compression for request bodies
    http_auth = auth,
    #client_cert = client_cert_path,
    #client_key = client_key_path,
    use_ssl = True,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    #ca_certs = ca_certs_path
)

# ingest tests.
#autoReader = opensearchpy.client.ingest.IngestClient(client)
#pipe = autoReader.
#print("++++++ pipe = " ,pipe)

# Create an index with non-default settings.
index_name = 'test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 4
    }
  }
}

if client.exists:
    print("client OK")
else:
    print("client failed")

#response = client.indices.create(index=index_name, body=index_body)
#print('\nCreating index:')
#print(response)

# search query
index_name = 'test-index'
query = {'query': {
        'match_all': {},
    }
}

# READ from the opensearch database
res2 = client.search(body=query, index=index_name)
print("Search all = ", res2)

# CREATE A NEW INDEX
print('2 ===========================================')
index_body3 = {
  'name': 'fred',
  'doi': 'unique URL code'
}

res3 = client.index(index=index_name, body=index_body3)
print('3 ====================================')
print(res3)

# CREATE A NEW DOCUMENT IN THE NEW INDEX WITH A CUSTOM INDEX.
id = '4'
res4 = client.index(index=index_name, body=index_body3, id=id)
print('4 ====================================')
print(res4)

# Add a document to the index.
document = {
  'name': 'Superman',
  'doi': 'Flying',
}
id = '100'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
)

print('\nAdding document: ================================')
print(response)

# READ A DOCUMENT USING A SEARCH.
query = {
    'query': {
        'multi_match': {
            'query': 'fred',
            'fields': ['name']
        }
    }
}

print('5 ====================================')
res5 = client.search(index=index_name, body=query)
print(res5)

# search query
index_name = 'test-index'
query = {'query': {
        'match_all': {},
    }
}

# READ from the opensearch database
res2 = client.search(body=query, index=index_name)
# print("Search all = ", json.dumps(res2, indent=4))

'''
response = client.search(
    body = query,
    index = index_name
)
print('\nSearch results:')
print(response)

# Delete the document.
response = client.delete(
    index = index_name,
    id = id
)

print('\nDeleting document:')
print(response)

# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)
'''