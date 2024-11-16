# import psycopg2

# # Function to read the database credentials from a text file
# def read_db_credentials(filename='DatabasePassword.txt'):
#     credentials = {}
#     with open(filename, 'r') as file:
#         for line in file:
#             key, value = line.strip().split('=')
#             credentials[key] = value
#     return credentials

# # Function to establish a connection to the PostgreSQL database
# def get_db_connection():
#     credentials = read_db_credentials()
    
#     # Create and return the connection object
#     conn = psycopg2.connect(
#         dbname=credentials['database'],
#         user=credentials['user'],
#         password=credentials['password'],
#         host=credentials['host'],
#         port=credentials['port']
#     )
    
#     return conn

import psycopg2

# Directly hardcoding the database credentials
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='quefoodhall',
            user='developuser',
            password=']&l381[czY:F@sV*',
            host='34.123.21.31',
            port=5432
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        raise
