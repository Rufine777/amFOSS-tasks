import mysql.connector
from mysql.connector import Error

class MySQLConnector:
    def __init__(self, host='localhost', user='root', password='Ajul@2007', database='moviesdb'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Establish connection to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return True
            else:
                return False
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False

    def disconnect(self):
        """Close the database connection."""
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def is_connected(self):
        """Check if the database connection is active."""
        return self.connection is not None and self.connection.is_connected()

    def execute_query(self, query, params=None):
        """
        Execute a SQL query with optional parameters.
        
        Args:
            query (str): The SQL query to be executed.
            params (tuple or list): Optional parameters for the query.
        
        Returns:
            list: Fetched results as list of tuples or None if error occurs.
        """
        if not self.is_connected():
            print("Database not connected.")
            return None
        
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Query execution error: {e}")
            return None
        finally:
            cursor.close()

    def batch_insert(self, insert_query, data_list, batch_size=1000):
        """
        Perform efficient batch insertion using executemany().
        
        Args:
            insert_query (str): SQL insert statement with placeholders.
            data_list (list of tuples): Data rows to insert.
            batch_size (int): Number of rows to insert per batch.
        """
        if not self.is_connected():
            print("Database not connected.")
            return
        
        cursor = self.connection.cursor()
        try:
            for i in range(0, len(data_list), batch_size):
                batch = data_list[i:i+batch_size]
                cursor.executemany(insert_query, batch)
                self.connection.commit()
            print(f"Inserted {len(data_list)} rows successfully.")
        except Error as e:
            print(f"Batch insert error: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def fetch_movies(self, columns=None, search_column=None, search_value=None):
        """
        Fetch movie records from the database, optionally filtering and selecting columns.
        
        Args:
            columns (list): List of columns to retrieve.
            search_column (str): Column to apply filter on.
            search_value (str): Value to filter with LIKE.
        
        Returns:
            list: Query results or None if error.
        """
        if not self.is_connected():
            print("Database not connected.")
            return None
        
        cursor = self.connection.cursor()
        try:
            cols = ", ".join(columns) if columns else "*"
            sql = f"SELECT {cols} FROM movies"
            params = ()
            
            if search_column and search_value:
                sql += f" WHERE {search_column} LIKE %s"
                params = (f"%{search_value}%",)
            
            cursor.execute(sql, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Fetch movies error: {e}")
            return None
        finally:
            cursor.close()
