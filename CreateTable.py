from DatabaseConnection import get_db_connection

# SQL statement to create a table
create_table_query = '''
CREATE TABLE IF NOT EXISTS Testing (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

# Use the connection to execute the SQL statement
def create_table():
    # Get the database connection
    conn = get_db_connection()

    # Create a cursor to execute the query
    with conn.cursor() as cur:
        cur.execute(create_table_query)
        print("Table 'users' created successfully!")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Run the function to create the table
if __name__ == "__main__":
    create_table()
