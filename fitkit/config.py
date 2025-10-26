import os
import tempfile

from dotenv import load_dotenv
load_dotenv()

class Config:
    print("Loading Config...")

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')



    S3_BUCKET = os.environ.get('S3_BUCKET')
    S3_KEY = os.environ.get('S3_KEY')
    S3_SECRET = os.environ.get('S3_SECRET')


    RAZORPAY_KEY=os.environ.get('RAZORPAY_KEY')
    RAZORPAY_SEC_ID=os.environ.get('RAZORPAY_SEC_ID')

    SECRET_KEY=os.environ.get('SECRET_KEY')


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
    # SQLALCHEMY_DATABASE_URI='sqlite:///mydatabase.db' ## for working with sqlite in the flask app



    DB_NAME = os.environ.get("DB_NAME")
    USER_NAME = os.environ.get("USER_NAME")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    print(DB_NAME, HOST

    try:
        SQLALCHEMY_DATABASE_URI='mysql+pymysql://USERNAME:PASSWORD@HOST/DB_NAME'
        SQLALCHEMY_TRACK_MODIFICATIONS=False # Optional, to suppress a warning
    except Exception as e:
        print("Error in DB connection string:", e)


