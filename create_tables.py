import os
import psycopg2
from dotenv import load_dotenv

def create_tables():
    """Connect to the PostgreSQL database and create the tables."""
    load_dotenv()

    conn = None
    try:
        # Get the database connection URL from the environment variables
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("DATABASE_URL environment variable not set. Please check your .env file.")

        # Connect to the database
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()

        # Open and read the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), 'database_setup.sql')
        with open(sql_file_path, 'r') as f:
            # Execute the SQL commands
            cur.execute(f.read())

        # Commit the changes
        conn.commit()
        print("Tables created successfully!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    create_tables()
