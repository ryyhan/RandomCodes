import sqlite3
from influxdb_client_3 import InfluxDBClient3, Point

# Connect to SQLite database (creates if not exists)
conn = sqlite3.connect('sample.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

token = INFLUX_TOKEN
org = "AI Team"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

database="edgeData"

client = InfluxDBClient3(host=host, token=token, org=org)

# Create a table
cursor.execute("""CREATE TABLE IF NOT EXISTS sensor_data (
    number INTEGER,
    square INTEGER,
    cube INTEGER
)""")
conn.commit()

data = []
for number in range(10):
    data.append((number, number**2, number**3))
    cursor.executemany('''INSERT INTO sensor_data (number, square, cube) VALUES (?, ?, ?)''', data)
    
    cursor.execute("SELECT * FROM sensor_data")
    rows = cursor.fetchall()
    for row in rows:
    # Format data into InfluxDB point
        influx_point = Point("generateThenWrite") \
        .field("number", row[0]) \
        .field("square", row[1]) \
        .field("cuber", row[2]) 

        try:
            client.write(database=database, record=influx_point)
            delete_query = "DELETE FROM sensor_data WHERE number=?"  # Assuming an "id" column for unique identification
            cursor.execute(delete_query, (row[0],))  # Use the first column value (adjust if needed)
            conn.commit()

            print(f"Successfully wrote data to InfluxDB and deleted row from SQLite: {row}")

        except Exception as e:
            print(e)
        
        data.clear()


# Commit changes and close connection
conn.commit()
conn.close()

print("SQLite database created and values inserted successfully.")
