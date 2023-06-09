import mysql.connector
import os

# Set the path to the SSL certificate
current_dir = os.path.dirname(os.path.abspath(__file__))
ca_cert_path = os.path.join(current_dir, "-.cert")

# Connect to the MySQL database
db = mysql.connector.connect(
    host="-",
    user="-",
    password="-",
    database="-",
    ssl_ca=ca_cert_path,
    ssl_verify_cert=True,
    ssl_cipher="AES128-SHA",
)

# Connect to the login database
logindb = mysql.connector.connect(
    host="-",
    user="-",
    password="-",
    database="-",
    ssl_ca=ca_cert_path,
    ssl_verify_cert=True,
    ssl_cipher="AES128-SHA",
)

# Check if the connection to the login database was successful
if logindb.is_connected():
    print("Successfully connected to MySQL database")
else:
    print("Failed to connect to MySQL database")
if db.is_connected():
        print("Successfully connected to MySQL database")
else:
        print("Failed to connect to MySQL database")
