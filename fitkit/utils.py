import smtplib, ssl
import secrets
import math, random
import os
from flask import current_app, redirect, session
from functools import wraps # for using decorators

from PIL import Image

from fitkit.config import Config


MAIL_USERNAME=Config.MAIL_USERNAME
MAIL_PASSWORD=Config.MAIL_PASSWORD

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userid") is None:
            return redirect("/product/login")
        return f(*args, **kwargs)
    return decorated_function


''' for sending email using smtp '''
def send_Email(message, receiver_email=MAIL_USERNAME):

    port = 465
    smtp_server = "smtp.gmail.com"

    sender_email = MAIL_USERNAME
    password = MAIL_PASSWORD


    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as smtp:
        smtp.ehlo()


        smtp.login(sender_email, password)
        print(smtp.sendmail(sender_email, receiver_email, message))

    return


""" for the generation otp """
def generateOTP(receiver_email=MAIL_USERNAME) :


    print(receiver_email)
    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]


    message = f"""\
                Subject: Fitkit | Otp

                Your One Time Password(OTP) is:

                {OTP}"""

    send_Email(message, receiver_email)

    return OTP

def upload_img(form_image):

    random_hex = secrets.token_hex(8)

    # my_bucket = get_bucket()

    i = 0
    for file in form_image:
        _, f_ext = os.path.splitext(file.filename)

        print(f_ext, _, file.mode)

        # # convert webp to jpeg
        # if f_ext.lower() == '.webp':
        #         file = file.convert('RGB')


        # # convert png to jpeg
        # if f_ext.lower() == '.png':
        #     if file.mode == 'RGBA':
        #         file = file.convert('RGB')


        # # convert jpg to jpeg
        # if f_ext.lower() == '.jpg':
        #     f_ext = '.jpeg'


        image_name = f"{random_hex}_{str(i)}.jpeg"
        print(image_name)
        print('file and filemode', file.mode, file.filename)
        picture_path = os.path.join(current_app.blueprints['product'].root_path, 'static/images', image_name)
        file.save(picture_path)

        if i == 0:
            # Create a thumbnail for the product image
            thumbnail_image_name = random_hex + '_thumbnail' + '.jpeg'
            thumbnail_path = os.path.join(current_app.blueprints['product'].root_path, 'static/images', thumbnail_image_name)

            output_size = (500, 500)

            print(file)
            img = Image.open(file)

            # print(i.mode, i)

            # convert webp to jpeg
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            img.thumbnail(output_size)

            img.save(thumbnail_path)

        i += 1

    return random_hex




# def remove_img(productId):

#     print(productId)
#     my_bucket = get_bucket()

#     img_index = ['a', 'b', 'c', 'd']
#     for i in img_index:
#         filename = str(productId) + i + '.jpg'
#         print(filename)
#         try:
#             my_bucket.Object('images/' + filename).delete()
#         except:
#             print('object not found')
