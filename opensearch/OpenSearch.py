# This is an opensearch test
from opensearchpy import OpenSearch

host = 'localhost'
port = 9200
#auth = ('admin', 'Abcdefgh1')
auth = ('admin', 'admin')

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = True,
    http_auth = auth,
    verify_certs = False,
    ssl_show_warn = False
)

index_name = 'python-test-index'
index_body = {
  'settings': {
    'index': {
      'number_of_shards': 1,
      'number_of_replicas': 0
    }
  },
  'mappings': {
    'properties': {
        'title': {
            'type': 'text'
        },
        'description': {
            'type': 'text'
        },
        'timestamp': {
            'type': 'date'
        }
    }
  }
}

print("0000000")

response = client.indices.create(index=index_name, body=index_body)

if client.exists:
    print("client.exists")
else:
    print("client.exists NOT")

print("111")
print(response)
print("222")
