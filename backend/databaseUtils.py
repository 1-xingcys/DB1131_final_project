import psycopg2
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL")

# Connect to the database
def connect_to_database():
    for i in range(5):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            return conn
        except psycopg2.OperationalError:
            print("Database not ready, retrying in 3 seconds...")
            time.sleep(3)
    raise Exception("Database connection failed after retries")
  
# Execute an arbitrary query
def execute_query(query, data):
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        cur.execute(query, data)
        conn.commit()
        print("Query executed successfully")
    except Exception as e:
        conn.rollback()
        print(f"Failed to execute query with data{data}: {e}")
    finally:
        cur.close()
        conn.close()

# Execute a SELECT query
def execute_select_query(query, data=None):
    conn = connect_to_database()
    cur = conn.cursor()
    try:
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)
        results = cur.fetchall()
        return results
    except Exception as e:
        print(f"Failed to execute select query: {e}")
        return []
    finally:
        cur.close()
        conn.close()