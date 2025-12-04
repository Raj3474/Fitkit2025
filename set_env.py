import os
from dotenv import load_dotenv
<<<<<<< HEAD


load_dotenv()


# email related env variables
os.environ['EMAIL_USERNAME']='' # your email here
os.environ['EMAIL_PASSWORD']='' # your         

=======
load_dotenv()
# email related env variables
os.environ['EMAIL_USERNAME']='' # your email here
os.environ['EMAIL_PASSWORD']='' # your         
>>>>>>> d1146cc754c361c1bca5ced9d4beb43dcef2470f
# S3 bucket related env variables
S3_BUCKET = ''
S3_KEY = ''
S3_SECRET = ''
<<<<<<< HEAD


# razorpay related env variables
os.environ['RAZORPAY_KEY']='rzp_test_VjLgQwIciQveWC'
os.environ['RAZORPAY_SEC_ID']='DhDWNz9Q1Ta0YOeR3rmRlqoC'


# secret key related env variables
os.environ['SECRET_KEY']='test'
print("Secret Key:", os.environ['SECRET_KEY'])

=======
# razorpay related env variables
os.environ['RAZORPAY_KEY']='rzp_test_VjLgQwIciQveWC'
os.environ['RAZORPAY_SEC_ID']='DhDWNz9Q1Ta0YOeR3rmRlqoC'
# secret key related env variables
os.environ['SECRET_KEY']='test'
print("Secret Key:", os.environ['SECRET_KEY'])
>>>>>>> d1146cc754c361c1bca5ced9d4beb43dcef2470f
# database related env variables
os.environ['DB_HOST']='Rajcs50x.mysql.pythonanywhere-services.com'
os.environ['DB_USERNAME']='Rajcs50x'
os.environ['DB_PASSWORD']='Myfitkitdbpassword'
<<<<<<< HEAD
os.environ['DB_NAME']='Rajcs50x$fitkitDB'

=======
os.environ['DB_NAME']='Rajcs50x$fitkitDB'
>>>>>>> d1146cc754c361c1bca5ced9d4beb43dcef2470f
