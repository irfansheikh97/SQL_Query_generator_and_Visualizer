import psycopg2
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define connection strings (replace placeholders)
postgres_url = 'postgresql://postgres:root@localhost/netflix_data'
sqlite_url = 'sqlite:///C:/Users/welcome/Desktop/Sql_Query_Generator/netflix_data.db'

# Create SQLAlchemy engines
postgres_engine = create_engine(postgres_url)
sqlite_engine = create_engine(sqlite_url)

# Create declarative base for table models (optional, for complex data manipulation)
Base = declarative_base()


# Function to execute raw SQL statements (modify for your specific needs)
def execute_query(engine, query):
    with engine.connect() as conn:
        conn.execute(query)


# Connect to databases and create session makers
PostgresSession = sessionmaker(bind=postgres_engine)
SQLiteSession = sessionmaker(bind=sqlite_engine)

# Define your list of tables to convert
tables = ['netflix', 'netflix_cast', 'netflix_country', 'netflix_directors',
          'netflix_genre']  # Replace with actual table names


def get_table_definitions(conn):
    """Fetches column definitions for all tables in the connected database."""
    cursor = conn.cursor()
    cursor.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public';
  """)
    return cursor.fetchall()


def create_table_statement(table_definitions, table_name):
    """Constructs a CREATE TABLE statement based on table definitions."""
    columns = []
    for row in table_definitions:
        if row[0] == table_name:  # Filter for the specific table
            column_def = f"{row[1]} {row[2]}"  # Combine column name and data type
            columns.append(column_def)
    return text(f"""CREATE TABLE IF NOT EXISTS {table_name} ({','.join(columns)});""")


# Usage
# Connect to PostgreSQL database (replace with your connection details)
conn = psycopg2.connect(dbname='netflix_data', user='postgres', password='root', host='localhost')

# Fetch table definitions
table_definitions = get_table_definitions(conn)

# Create tables in SQLite based on PostgreSQL definitions
for table in tables:
    create_table_stmt = create_table_statement(table_definitions, table)
    execute_query(sqlite_engine, create_table_stmt)

# Copy data from PostgreSQL to SQLite
PostgresSessionLocal = PostgresSession()
SQLiteSessionLocal = SQLiteSession()

postgres_metadata = MetaData()
postgres_metadata.reflect(bind=postgres_engine)

sqlite_metadata = MetaData()
sqlite_metadata.reflect(bind=sqlite_engine)

try:
    for table_name in tables:
        postgres_table = Table(table_name, postgres_metadata, autoload_with=postgres_engine)
        sqlite_table = Table(table_name, sqlite_metadata, autoload_with=sqlite_engine)

        # Fetch data from PostgreSQL
        postgres_data = PostgresSessionLocal.query(postgres_table).all()

        # Insert data into SQLite
        for row in postgres_data:
            insert_stmt = sqlite_table.insert().values(**row._asdict())
            SQLiteSessionLocal.execute(insert_stmt)

        SQLiteSessionLocal.commit()
finally:
    PostgresSessionLocal.close()
    SQLiteSessionLocal.close()

conn.close()  # Close PostgreSQL connection

print("Conversion complete!")
