from opensearchpy import OpenSearch, RequestsHttpConnection
import logging

# --- Configuration ---
host = ''  # Your OpenSearch instance's Public IPv4 address
port =            # OpenSearch HTTP port
username = ''    # Default admin user
password = '' # <--- IMPORTANT: Replace with your actual password!

# --- Set up logging (optional, but good for debugging) ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_opensearch():
    """Establishes connection to OpenSearch."""
    try:
        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=(username, password),
            use_ssl=False,
            verify_certs=False,            # Set to True in production with proper CA certs
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            connection_class=RequestsHttpConnection
        )
        # Verify connection
        if not client.ping():
            raise Exception("Could not connect to OpenSearch. Ping failed.")
        logger.info("Successfully connected to OpenSearch.")
        return client
    except Exception as e:
        logger.error(f"Error connecting to OpenSearch: {e}")
        logger.error(f"Please ensure OpenSearch is running and accessible at {host}:{port} with correct credentials.")
        logger.error("Also check your EC2 Security Group for inbound rules on port 9200.")
        return None

def list_all_indices(client):
    """Lists all indices in OpenSearch."""
    try:
        # Using _cat/indices for a simple list of names
        # You can also use client.indices.get_alias("*") or client.indices.get_mapping("*")
        indices_raw = client.cat.indices(format='json')
        
        index_names = []
        for index_info in indices_raw:
            index_names.append(index_info['index'])
        
        index_names.sort() # Sort alphabetically for easier viewing
        
        if not index_names:
            logger.info("No indices found in OpenSearch.")
            return []

        logger.info("Current indices in OpenSearch:")
        for i, name in enumerate(index_names):
            print(f"{i + 1}. {name}")
        return index_names
    except Exception as e:
        logger.error(f"Error listing indices: {e}")
        return None

def delete_selected_index(client, index_name):
    """Deletes a specified index."""
    try:
        logger.warning(f"Attempting to delete index: {index_name}")
        response = client.indices.delete(index=index_name)
        if response.get('acknowledged', False):
            logger.info(f"Index '{index_name}' deleted successfully.")
            return True
        else:
            logger.error(f"Failed to delete index '{index_name}'. Response: {response}")
            return False
    except Exception as e:
        logger.error(f"An error occurred while deleting index '{index_name}': {e}")
        return False

# --- Main execution ---
if __name__ == "__main__":
    opensearch_client = connect_to_opensearch()

    if opensearch_client:
        while True:
            print("\n------------------------------------")
            indices = list_all_indices(opensearch_client)
            if not indices:
                print("No indices to delete. Exiting.")
                break

            try:
                selection = input("\nEnter the number of the index to delete (or 'q' to quit): ").strip().lower()
                if selection == 'q':
                    print("Exiting without deleting any index.")
                    break

                selected_index_number = int(selection)
                if 1 <= selected_index_number <= len(indices):
                    index_to_delete = indices[selected_index_number - 1]
                    
                    print(f"\n--- WARNING: You are about to DELETE the index '{index_to_delete}'. ---")
                    confirmation = input(f"Type 'yes' to confirm deletion of '{index_to_delete}': ").strip()

                    if confirmation == 'yes':
                        delete_selected_index(opensearch_client, index_to_delete)
                    else:
                        print("Deletion cancelled.")
                else:
                    print("Invalid selection. Please enter a number from the list.")

            except ValueError:
                print("Invalid input. Please enter a number or 'q'.")
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}")

    print("\nScript finished.")
