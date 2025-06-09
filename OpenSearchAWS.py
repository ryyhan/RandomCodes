from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
import logging

# --- Configuration ---
host = ''  # Your OpenSearch instance's Public IPv4 address
port =            # OpenSearch HTTP port
username = ''    # Default admin user
password = '' # <--- IMPORTANT: Replace with the actual password you set!

# For basic authentication, uncomment the following line and comment out AWSV4SignerAuth if using AWS IAM roles
# auth = (username, password)

# --- Set up logging (optional, but good for debugging) ---
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# --- Connect to OpenSearch ---
try:
    # Create the client with SSL/TLS configuration
    # If using self-signed certificates or for local testing, you might need verify_certs=False, but it's not recommended for production.
    # For production, you'd configure trusted CAs.
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_auth=(username, password), # Use basic auth
        use_ssl=False,                  # OpenSearch often uses SSL/TLS by default
        verify_certs=False,            # Set to True in production with proper CA certs
        ssl_assert_hostname=False,     # Set to True in production with proper hostname verification
        ssl_show_warn=False,           # Suppress SSL warnings (for verify_certs=False)
        connection_class=RequestsHttpConnection
    )

    # --- 1. Check Cluster Health ---
    print("--- Cluster Health ---")
    health_response = client.cluster.health(wait_for_status='yellow', timeout=None)
    print(f"Cluster Health: {health_response['status']}")
    print(health_response)

    # --- 2. Index a Sample Document ---
    print("\n--- Indexing Document ---")
    index_name = 'my-sample-data'
    document = {
        'title': 'The Quick Brown Fox',
        'author': 'John Doe',
        'content': 'The quick brown fox jumps over the lazy dog.',
        'timestamp': '2025-06-09T10:00:00Z'
    }
    document_id = '1'

    # Check if index exists, create if not
    if not client.indices.exists(index=index_name):
        print(f"Creating index: {index_name}")
        client.indices.create(index=index_name, body={
            'settings': {
                'index.number_of_shards': 1,
                'index.number_of_replicas': 0
            }
        })
        print("Index created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

    response = client.index(
        index=index_name,
        body=document,
        id=document_id,
        refresh=True # Makes the document searchable immediately
    )
    print(f"Document indexed: {response}")

    # --- 3. Perform a Search ---
    print("\n--- Searching Document ---")
    search_body = {
        'query': {
            'match': {
                'content': 'fox'
            }
        }
    }
    search_response = client.search(
        index=index_name,
        body=search_body
    )
    print(f"Search results ({search_response['hits']['total']['value']} hits):")
    for hit in search_response['hits']['hits']:
        print(f"  ID: {hit['_id']}, Source: {hit['_source']['title']}")

except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please ensure:")
    print(f"1. OpenSearch is running and accessible at {host}:{port}.")
    print("2. Your EC2 Security Group allows inbound traffic on port 9200 from your IP.")
    print("3. The 'OPENSEARCH_INITIAL_ADMIN_PASSWORD' used for the container matches 'password' in this script.")
    print("4. For production, properly configure SSL certificate verification.")
