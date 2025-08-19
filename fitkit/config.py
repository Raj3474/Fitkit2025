import os
import tempfile

class Config:

    ADMIN_EMAIL = '' # os.environ.get("ADMIN_EMAIL")
    ADMIN_EMAIL_PASS = '' # os.environ.get("ADMIN_EMAIL_PASS")

    ADMIN_LOGIN_ID = '' # os.environ.get("ADMIN_LOGIN_ID")
    ADMIN_LOGIN_PASS= '' #os.environ.get("ADMIN_LOGIN_PASS")

    RPAY_KEY = '' # os.environ.get("RPAY_KEY")
    RPAY_SECRET = '' # os.environ.get("RPAY_SECRET")

    S3_BUCKET = '' # os.environ.get("S3_BUCKET")
    S3_KEY = '' # os.environ.get("S3_KEY")
    S3_SECRET = '' #os.environ.get("S3_SECRET")


    SECRET_KEY = 'd8f3efea434853075f253b7e7fad1210'
    # Ensure templates are auto-reloaded
    TEMPLATES_AUTO_RELOAD = True

    # Configure session to use filesystem (instead of signed cookies)
    SESSION_FILE_DIR = tempfile.mkdtemp()
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"

    '''
    setting up our database connection.
    '''
    
    # this is for testing, use os.environ.get('SQLALCHEMY_DATABASE_URI) in prod
    SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db' ## for working with sqlite in the flask app
    
    # DBNAME = os.environ.get("DBNAME")
    # USER = os.environ.get("USER")
    # PASSWORD = os.environ.get("PASSWORD")
    # HOST = os.environ.get("HOST")

    # db_connection = psycopg2.connect(
    #     dbname=DBNAME,
    #     user=USER,
    #     password=PASSWORD,
    #     host=HOST,
    #     port=5432
    # )