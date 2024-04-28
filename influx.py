from influxdb_client_3 import InfluxDBClient3, Point


def influx_connection():
    """
    Establishes a connection to InfluxDB using the provided credentials.

    Returns:
        InfluxDBClient3: A client object for interacting with InfluxDB.
    """
    try:
        # Set the InfluxDB access token
        token = INFLUX_TOKEN

        # Set the InfluxDB organization
        org = "VMC_Data_log"

        # Set the InfluxDB host URL
        host = "https://us-east-1-1.aws.cloud2.influxdata.com"

        # Create an InfluxDB client object
        client = InfluxDBClient3(host=host, token=token, org=org)

        return client

    except Exception as e:
        print(f"An error occurred while connecting to InfluxDB: {e}")
        return None
