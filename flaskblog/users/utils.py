import os
import secrets
from PIL import Image
from flask import url_for
from flask import current_app
from flask_mail import Message
from flaskblog import mail


# save photo function
def save_photo(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics/' , picture_fn)
    
    resized_image = Image.open(form_picture)
    resized_image.thumbnail((200,200))

    resized_image.save(picture_path)

    return picture_fn

user = User()
def send_reset_email(user):
    
    token = User.get_reset_token(user)
    msg = Message('Password Reset', sender='techvalley2015@gmail.com', recipients=[user.email])
    msg.body = f''' Click Here to reset your password
        {url_for('users.reset_token', token = token, _external = True)}

        if you did not, ignore
    '''

