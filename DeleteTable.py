from DatabaseConnection import get_db_connection

# SQL statement to delete the table
delete_table_query = '''
DROP TABLE IF EXISTS Testing;
'''

# Function to delete the table
def delete_table():
    # Get the database connection
    conn = get_db_connection()

    # Create a cursor to execute the query
    with conn.cursor() as cur:
        cur.execute(delete_table_query)
        print("Table 'Testing' deleted successfully!")

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

# Run the function to delete the table
if __name__ == "__main__":
    delete_table()
