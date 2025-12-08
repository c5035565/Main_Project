import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# Create a database configuration dictionary
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB')
} 
