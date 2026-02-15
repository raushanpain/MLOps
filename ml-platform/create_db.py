import pymysql

# Database connection details
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "raushan@07"
DB_NAME = "ml_platform"

try:
    # Connect to MySQL Server (no database selected)
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    with connection.cursor() as cursor:
        # Create database execution
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' checked/created successfully.")
        
    connection.close()

except Exception as e:
    print(f"Error creating database: {e}")
