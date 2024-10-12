import psycopg2

try:
    connection = psycopg2.connect(
        host="34.123.21.31",       
        database="quefoodhall", 
        user="developuser",         
        password="]&l381[czY:F@sV*", 
        port = "5432"
    )
    print("Database connection successful!")
    
except Exception as error:
    print(f"Error while connecting to the database: {error}")
    
