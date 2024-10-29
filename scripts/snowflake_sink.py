import os
import sys
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Setting the path to import the constants module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import helper.constants as CNT

class SnowflakeConnector:
    """
    A class to manage Snowflake connections and operations.
    """

    def __init__(self):
        """
        Initializes the SnowflakeConnector instance. Sets the connection and cursor to None.
        """
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Connects to the Snowflake database using credentials from the CNTants module.
        Prints a success message upon connection or an error message if the connection fails.
        """
        try:
            print("Attempting to connect to Snowflake...")
            self.connection = snowflake.connector.connect(
                user=CNT.SF_USER,
                password=CNT.SF_PASSWORD,
                account=CNT.SF_ACCOUNT
            )
            self.cursor = self.connection.cursor()
            print("Successfully connected to Snowflake.")
        except Exception as e:
            print(f"Error connecting to Snowflake: {e}")
            raise

    def execute_query(self, query):
        """
        Executes the provided SQL query using the Snowflake cursor.
        
        :param query: The SQL query to be executed.
        :return: The results of the query as a list of tuples.
        :raises Exception: If the query execution fails or the cursor is not available.
        """
        if not self.cursor:
            raise Exception("Not connected to Snowflake.")
        try:
            print(f"Executing query: {query}")
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            print(f"Query executed successfully. Result: {result}")
            return result
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    def setup_env(self, dw_name, db_name, schema_name):
        """
        Creates the data warehouse, database, and schema if they do not exist.
        
        :param dw_name: Name of the data warehouse to be created.
        :param db_name: Name of the database to be created.
        :param schema_name: Name of the schema to be created.
        """
        print(f"Setting up environment: Data Warehouse '{dw_name}', Database '{db_name}', Schema '{schema_name}'")
        dw_query = f"CREATE WAREHOUSE IF NOT EXISTS {dw_name}"
        db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"
        schema_query = f"""CREATE SCHEMA IF NOT EXISTS {db_name}.{schema_name}"""
        
        self.execute_query(dw_query)
        self.execute_query(db_query)
        self.execute_query(schema_query)

        print(f"Environment setup complete: Data Warehouse: {dw_name}, Database: {db_name}, Schema: {schema_name}")

    def create_table(self, dw_name, db_name, schema_name, table_name, table_schema):
        """
        Creates a table in the specified data warehouse, database, and schema.
        
        :param dw_name: Name of the data warehouse to be used.
        :param db_name: Name of the database to be used.
        :param schema_name: Name of the schema to be used.
        :param table_name: Name of the table to be created.
        :param table_schema: The schema of the table to be created.
        """
        print(f"Creating table '{table_name}' in {dw_name}.{db_name}.{schema_name}")
        self.use_env(dw_name, db_name, schema_name)
        table_query = f"CREATE OR REPLACE TABLE {table_name}{table_schema}"

        self.execute_query(table_query)
        print(f"Table '{table_name}' created successfully.")

    def use_env(self, dw_name, db_name, schema_name):
        """
        Switches the environment to use the specified warehouse, database, and schema.
        
        :param dw_name: Name of the data warehouse to switch to.
        :param db_name: Name of the database to switch to.
        :param schema_name: Name of the schema to switch to.
        """
        print(f"Switching to environment: Data Warehouse '{dw_name}', Database '{db_name}', Schema '{schema_name}'")
        self.execute_query(f"USE WAREHOUSE {dw_name}")
        self.execute_query(f"USE DATABASE {db_name}")
        self.execute_query(f"USE SCHEMA {schema_name}")
        print("Environment switched successfully.")

    def get_connection(self):
        """
        Returns the Snowflake connection object.
        
        :return: The Snowflake connection object.
        """
        if self.connection is None:
            raise Exception("Connection not established.")
        return self.connection

    def close(self):
        """
        Closes the Snowflake connection and cursor. Prints a message indicating that the connection is closed.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Snowflake connection closed.")

class SnowFlakeSink:
    def __init__(self):
        self.sf_connection = SnowflakeConnector()
        print("Connecting to Snowflake...")
        self.sf_connection.connect()
        print(f"Using environment with Warehouse: {CNT.SF_WAREHOUSE}, Database: {CNT.SF_DATABASE}, Schema: {CNT.SF_SCHEMA}")
        self.sf_connection.use_env(CNT.SF_WAREHOUSE, CNT.SF_DATABASE, CNT.SF_SCHEMA)

    def get_data(self, path):
        """
        Reads data from the specified path and returns it as a DataFrame.
        :param path: The path to the data file (CSV)
        :return: DataFrame containing the data read from the file
        """
        try:
            print(f"Reading data from {path}...")
            data_df = pd.read_csv(path)
            data_df['incident_id'] = pd.to_numeric(data_df['incident_id'], errors='coerce')  
            data_df['date'] = pd.to_datetime(data_df['date'], errors='coerce').dt.date
            data_df['state'] = data_df['state'].astype(str)  
            data_df['city_or_county'] = data_df['city_or_county'].astype(str)  
            data_df['address'] = data_df['address'].astype(str)  
            data_df['n_killed'] = pd.to_numeric(data_df['n_killed'], errors='coerce')  
            data_df['n_injured'] = pd.to_numeric(data_df['n_injured'], errors='coerce')  
            data_df['congressional_district'] = pd.to_numeric(data_df['congressional_district'], errors='coerce')  
            data_df['incident_characteristics'] = data_df['incident_characteristics'].astype(str)  
            data_df['latitude'] = pd.to_numeric(data_df['latitude'], errors='coerce')  
            data_df['longitude'] = pd.to_numeric(data_df['longitude'], errors='coerce')  
            data_df['n_guns_involved'] = pd.to_numeric(data_df['n_guns_involved'], errors='coerce')  
            data_df['notes'] = data_df['notes'].astype(str)  
            data_df['year'] = pd.to_numeric(data_df['year'], errors='coerce')  
            data_df['month'] = pd.to_numeric(data_df['month'], errors='coerce')  
            data_df['day_of_week'] = pd.to_numeric(data_df['day_of_week'], errors='coerce')  

            # Convert frequency columns
            freq_columns = [
                'gun_stolen_not_stolen_freq', 'gun_stolen_stolen_freq', 
                'gun_stolen_unknown_freq', 'gun_type_ak_freq', 
                'gun_type_auto_freq', 'gun_type_gauge_freq', 
                'gun_type_handgun_freq', 'gun_type_lr_freq', 
                'gun_type_mag_freq', 'gun_type_mm_freq', 
                'gun_type_rem_ar_freq', 'gun_type_rifle_freq', 
                'gun_type_shotgun_freq', 'gun_type_spl_freq', 
                'gun_type_spr_freq', 'gun_type_sw_freq', 
                'gun_type_unknown_freq', 'gun_type_win_freq', 
                'participant_age_group_adult_18plus_freq', 
                'participant_age_group_child_0_11_freq', 
                'participant_age_group_teen_12_17_freq', 
                'participant_gender_female_freq', 
                'participant_gender_male_freq', 
                'participant_status_arrested_freq', 
                'participant_status_injured_freq', 
                'participant_status_killed_freq', 
                'participant_status_unharmed_freq', 
                'participant_type_subject_suspect_freq', 
                'participant_type_victim_freq'
            ]

            for col in freq_columns:
                data_df[col] = pd.to_numeric(data_df[col], errors='coerce')
            data_df.columns = [col.upper() for col in data_df.columns]
            print(f"Data read successfully. Shape: {data_df.shape}")
            return data_df
        except Exception as e:
            print(f"An error occurred while reading data from {path}: {e}")
            return None

    def write_table(self, path, table):
        """
        Reads data from the specified path and writes it to the specified Snowflake table.
        :param path: The path to the data file.
        :param table: The target Snowflake table where data will be written.
        """
        try:
            print(f"Reading and writing data at: {path} to table: {table}")
            data_df = self.get_data(path)

            if data_df is not None:
                print(f"Writing data to {table}...")
                success, nchunks, nrows, _ = write_pandas(self.sf_connection.get_connection(), data_df, table.upper())

                if success:
                    print(f"Data written successfully to {table}. Number of chunks: {nchunks}, Number of rows: {nrows}")
                else:
                    print(f"Failed to write data to {table}.")
            else:
                print(f"No data to write for the table {table}.")
        
        except Exception as e:
            print(f"An error occurred while writing to the table {table}: {e}")

if __name__ == "__main__":
    print("Starting the SnowFlake Sink Process:")
    print("Starting the SnowFlake Process:")
    sf = SnowflakeConnector()

    try:
        print("Connecting to Snowflake...")
        sf.connect()
        
        if len(sys.argv) > 1:
            print(f"Setting up environment with Warehouse: {CNT.SF_WAREHOUSE}, "
                  f"Database: {CNT.SF_DATABASE}, Schema: {CNT.SF_SCHEMA}...")
            sf.setup_env(dw_name=CNT.SF_WAREHOUSE,
                         db_name=CNT.SF_DATABASE,
                         schema_name=CNT.SF_SCHEMA)

            print(f"Creating table '{CNT.SF_TABLE_NAME}'...")
            sf.create_table(dw_name=CNT.SF_WAREHOUSE,
                            db_name=CNT.SF_DATABASE,
                            schema_name=CNT.SF_SCHEMA,
                            table_name=CNT.SF_TABLE_NAME,
                            table_schema=CNT.SF_TABLE_SCHEMA)
            print(f"Table '{CNT.SF_TABLE_NAME}' created successfully.")
        else:
            print("No arguments passed. Implementing sink process...")
            sf_sink = SnowFlakeSink()
            sf_sink.write_table(CNT.CLEANED_DATA_PATH, CNT.SF_TABLE_NAME)
            sf_sink.sf_connection.close()
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        print("Closing Snowflake connection...")
        sf.close()
        print("Connection closed.")