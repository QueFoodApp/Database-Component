from DatabaseConnection import get_db_connection

# SQL statement to fetch data without the manager condition
fetch_data_query = '''
SELECT * FROM order_table
WHERE restaurant_id IN (
    SELECT restaurant_id 
    FROM manager_account_table
);
'''

# Function to fetch data from the database
def read_table_info():
    # Get the database connection
    conn = get_db_connection()

    try:
        # Create a cursor to execute the query
        with conn.cursor() as cur:
            # Execute the query
            cur.execute(fetch_data_query)
            # Fetch all rows from the result
            rows = cur.fetchall()
            print("Data fetched successfully!")
            
            # Optionally print or process the fetched rows
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No data found.")
            
            return rows  # Return the rows for further processing, if needed
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

# Run the function to read table information
if __name__ == "__main__":
    read_table_info()
