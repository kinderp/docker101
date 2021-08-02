import os
PASSWORD_FILE = '/run/secrets/db-password'
DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = open(PASSWORD_FILE, 'r').read()
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")


