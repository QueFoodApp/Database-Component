import psycopg2

# Function to read the database credentials from a text file
def read_db_credentials(filename='DatabasePassword.txt'):
    credentials = {}
    with open(filename, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            credentials[key] = value
    return credentials

# Function to establish a connection to the PostgreSQL database
def get_db_connection():
    credentials = read_db_credentials()
    
    # Create and return the connection object
    conn = psycopg2.connect(
        dbname=credentials['database'],
        user=credentials['user'],
        password=credentials['password'],
        host=credentials['host'],
        port=credentials['port']
    )
    
    return conn
