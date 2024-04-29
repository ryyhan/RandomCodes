import sqlite3
from influxdb_client_3 import InfluxDBClient3, Point

sqlite_conn = sqlite3.connect('sample.db')
sqlite_cursor = sqlite_conn.cursor()

sqlite_cursor.execute("SELECT * FROM sample_table")
rows = sqlite_cursor.fetchall()

token = "fU3G-a0B8LZ_dfjSd4bMGkop2ZkuTpq8CCZCHGeZJNBMugflr1tTWqXwkQZjn3EnEb9PkIz8q47mpJwVb7C6IQ=="
org = "AI Team"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

database="edgeData"

client = InfluxDBClient3(host=host, token=token, org=org)


for row in rows:
    # Format data into InfluxDB point
    influx_point = Point("test_writing") \
        .field("id", row[0]) \
        .field("name", row[1]) \
        .field("value", row[2]) 

    try:
        client.write(database=database, record=influx_point)
    except Exception as e:
        print(e)
# # Close connections
# sqlite_cursor.close()
# sqlite_conn.close()
