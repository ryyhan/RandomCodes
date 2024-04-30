from opcua import Client
import time

client = None  # Initialize the OPC UA client variable

server_name = "opc.tcp://10.194.176.232:4840"
node_id = "ns=6;s=Cum_PartCount"

def connectToOPCUA(server_name, node_id) -> None:
    """
    Connects to the OPC UA server.

    Parameters:
        server_name (str): The OPC UA server URL.
        node_id (str): The Node ID of the variable to be monitored.
    """
    global client  # Use the global client variable
    try:
        # Create an OPC UA client and connect to the specified server
        client = Client(server_name)
        client.connect()
        print("Connected to OPC UA server.")

    except Exception as e:
        print(f"Error connecting to OPC UA server: {e}")

def fetchDataFromServer(node_id) -> None:
    """
    Fetches data from the OPC UA server at regular intervals.

    Parameters:
        node_id (str): The Node ID of the variable to be monitored.
    """
    while True:
        try:
            if client is not None:
                # Get the node corresponding to the specified Node ID
                var_node = client.get_node(node_id)

                # Read the current value of the variable
                value = var_node.get_value()
                print(value)

            time.sleep(1)  # Wait for 1 second before fetching data again

        except Exception as e:
            print(f"Error fetching data from OPC UA server: {e}")

def main():
    """
    Main function to connect to the OPC UA server and start fetching data.
    """
    connectToOPCUA(server_name, node_id)
    fetchDataFromServer(node_id)

if __name__ == "__main__":
    main()
