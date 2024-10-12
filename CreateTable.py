import pandas as pd
from DatabaseConnection import get_db_connection

# Create tables based on excel sheets 
def create_tables(conn):
    
    with conn.cursor() as cursor:
        # Define SQL statements for each sheet (table)
        create_table_queries = {
            'Restaurant_Table': '''
            CREATE TABLE IF NOT EXISTS Restaurant_Table(
                Restaurant_ID INT PRIMARY KEY,
                Restaurant_Name VARCHAR(500) NOT NULL,
                Ratings DECIMAL(3, 2) CHECK (Ratings >= 1.0 AND Ratings <= 5.0),
                Restaurant_Type VARCHAR(500),
                Pricing_Levels VARCHAR(5) CHECK (Pricing_Levels IN ('$','$$','$$$', '$$$$'))
            );''',
            
            'Address_Table': '''
            CREATE TABLE IF NOT EXISTS Address_Table(
                Restaurant_ID INT PRIMARY KEY,
                State VARCHAR(20) NOT NULL,
                City VARCHAR(100) NOT NULL, 
                Street_Address VARCHAR(500) NOT NULL, 
                Postal_Code INT NOT NULL, 
                Latitude DOUBLE PRECISION NOT NULL,
                Longtitude DOUBLE PRECISION NOT NULL,
                FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant_Table(Restaurant_ID)
            );''',
            
            'Manager_Account_Table': '''
            CREATE TABLE IF NOT EXISTS Manager_Account_Table(
                Restaurant_ID INT PRIMARY KEY,
                Manager_ID INT NOT NULL, 
                Restaurant_Name VARCHAR(500) NOT NULL,
                Manager_Account_Name VARCHAR(500) NOT NULL, 
                Manager_Account_Password VARCHAR(500) NOT NULL
            );''',
            
            'Menu_Table': '''
            CREATE TABLE IF NOT EXISTS Menu_Table(
                Restaurant_ID INT NOT NULL, 
                Menu_ID INT NOT NULL,
                Category VARCHAR(500) NOT NULL,
                Food_Name VARCHAR(500) NOT NULL,
                Food_Description VARCHAR(10000) NOT NULL,
                Food_Price DOUBLE PRECISION NOT NULL,
                PRIMARY KEY (Restaurant_ID, Menu_ID, Food_Name, Food_Description, Food_Price),
                FOREIGN KEY (Restaurant_ID) REFERENCES Restaurant_Table(Restaurant_ID)
            );''',
        }

        # Execute the create table queries
        for query in create_table_queries.values():
            cursor.execute(query)
            print(f"Executed query: {query}")
        
        # Commit the changes to the database
        conn.commit()

def insert_data_from_excel(conn, sheet_name):
    # Load the data from the specified Excel sheet
    excel_file_path = 'TheQueAppDatabase.xlsx'  # Specify the path to the Excel file
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name)  # Read the content of the Excel file 

    # Define SQL insert statements for each table
    insert_queries = {
        'Restaurant_Table': '''
        INSERT INTO Restaurant_Table (Restaurant_ID, Restaurant_Name, Ratings, Restaurant_Type, Pricing_Levels)
        VALUES (%s, %s, %s, %s, %s);
        ''',
        
        'Address_Table': '''
        INSERT INTO Address_Table (Restaurant_ID, State, City, Street_Address, Postal_Code, Latitude, Longtitude)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        ''',
        
        'Manager_Account_Table': '''
        INSERT INTO Manager_Account_Table (Restaurant_ID, Manager_ID, Restaurant_Name, Manager_Account_Name, Manager_Account_Password)
        VALUES (%s, %s, %s, %s, %s);
        ''',
        
        'Menu_Table': '''
        INSERT INTO Menu_Table (Restaurant_ID, Menu_ID, Category, Food_Name, Food_Description, Food_Price)
        VALUES (%s, %s, %s, %s, %s, %s);
        ''',
    }

    # Insert the data into the PostgreSQL table
    with conn.cursor() as cursor:
        batch_size = 100  # Define the batch size for commits
        row_count = 0      # Initialize row counter

        for index, row in df.iterrows():
            # Use the sheet name to get the corresponding insert query
            if sheet_name in insert_queries:
                if sheet_name == 'Restaurant_Table':
                    cursor.execute(insert_queries[sheet_name], (
                        row['Restaurant_ID'],
                        row['Restaurant_Name'],
                        row['Ratings'],
                        row['Restaurant_Type'],
                        row['Pricing_Levels']
                    ))
                elif sheet_name == 'Menu_Table':
                    cursor.execute(insert_queries[sheet_name], (
                        row['Restaurant_ID'],
                        row['Menu_ID'],
                        row['Category'],
                        row['Food_Name'],
                        row['Food_Description'],
                        row['Food_Price']
                    ))
                elif sheet_name == 'Address_Table':
                    cursor.execute(insert_queries[sheet_name], (
                        row['Restaurant_ID'],
                        row['State'],
                        row['City'],
                        row['Street_Address'],
                        row['Postal_Code'],
                        row['Latitude'], 
                        row['Longtitude']
                    ))
                if sheet_name == 'Manager_Account_Table':
                    cursor.execute(insert_queries[sheet_name], (
                        row['Restaurant_ID'],
                        row['Manager_ID'],
                        row['Restaurant_Name'],
                        row['Manager_Account_Name'],
                        row['Manager_Account_Password']
                    ))
            
            row_count += 1
            
            # Commit every 1000 rows and print progress
            if row_count % batch_size == 0:
                conn.commit()  # Commit the current batch
                print(f"Committed {row_count} rows from sheet: {sheet_name}")

        # Commit remaining rows after the loop
        if row_count % batch_size != 0:
            conn.commit()
            print(f"Committed the last batch of {row_count % batch_size} rows from sheet: {sheet_name}")

def main():
    conn = get_db_connection()  # Get the database connection
    create_tables(conn)  # Create tables 
    
    # Load the Excel file and get the sheet names
    excel_file_path = 'TheQueAppDatabase.xlsx'  # Specify the path to the Excel file
    sheet_names = pd.ExcelFile(excel_file_path).sheet_names  # Get the sheet names

    # Loop through sheet names and insert data for matching table names
    for sheet_name in sheet_names:
        print(f"Inserting data from sheet: {sheet_name}")
        insert_data_from_excel(conn, sheet_name)  # Insert data from the matched sheet

    conn.close()  # Close the connection

if __name__ == '__main__':
    main()
