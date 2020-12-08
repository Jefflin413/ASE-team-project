""" 
Python standard libraries
"""
import os
import sqlite3
import time
import uuid
import json
from datetime import datetime, timedelta
import random

# Third party libraries
import boto3
from botocore.config import Config
from flask import Flask, redirect, request, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
# Web Socket for chatroom
from flask_socketio import SocketIO, join_room, leave_room
#from sklearn.linear_model import LinearRegression

# Internal imports
from utils.db import init_db_command
from utils.user import User
import json
import utils.db as db

# AWS Client
boto3_config = Config(
    region_name='us-east-1'
)
AWS_client = boto3.client('cloudformation', config=boto3_config)
# AWS_client = boto3.client('cloudformation')

# Google Login Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*")

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.unauthorized_handler
def unauthorized():
    """unauthorized handler"""
    return "You must be logged in to access this content.", 403

# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
Google_client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login helper to retrieve a user from our db"""
    return User.get(user_id)


@app.route("/")
def index():
    """landing endpoint"""
    current_streaming_list = db.get_streaming()
    if current_user.is_authenticated:
        return render_template("index.html", current_user_name=current_user.name, streams = current_streaming_list)
    else:
        return render_template("index.html", streams = current_streaming_list)


@app.route("/login")
def login():
    """login with google account"""
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = Google_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    """callback function of login endpoint"""
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = Google_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    Google_client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = Google_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    # print("ASDASDASDADA", picture, file=sys.stderr)
    # user = User(
    #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    # )
    user = User.get(unique_id)
    # Doesn't exist? Add to database
    if not user:
        User.create(unique_id, users_name, users_email, picture, 'Personal')
        return render_template("newuser.html", userid=unique_id, fullname=users_name,
                               email=users_email, profile_pic=picture)

    # user = User.create(unique_id, users_name, users_email, picture, usertype)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    """endpoint for setting up a new user"""
    if request.method == 'POST':
        uid = request.form.get('uid')
        name = request.form.get('fullname')
        email = request.form.get('email')
        profile_pic = request.form.get('profile_pic')
        usertype = request.form.get('usertype')
        db.update_user(uid, name, email, profile_pic, usertype)
        
        user = User.get(uid)
        login_user(user)
        return redirect(url_for("index"))
    else:
        return render_template("newuser.html")

@app.route("/testLogin", methods=['GET'])
def login_t():
    """endpoint for setting up an assigned new user"""
    # print("HIHI login")
    if User.get("cc2742") is None:
        User.create("cc2742", "Alice", "cc2742@columbia.edu", "qq.jpg", "personal")
    user = User(id_="cc2742", name="Alice", email="cc2742@columbia.edu", profile_pic="qq.jpg", usertype="personal")
    login_user(user)
    # print("Bye login")
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    """logout endpoint"""
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    """get google provider cfg"""
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# Login ends

@app.route("/test")
@login_required
def test():
        return "asdasdasd"

@app.route("/profile")
@login_required
def profile():
    """profile endpoint"""
    return render_template("profile.html",
                            current_user_name=current_user.name,
                            current_user_email=current_user.email,
                            current_user_profile_pic=current_user.profile_pic,
                            current_user_usertype=current_user.usertype,
                            audience_comment=json.dumps(db.get_audience_comment(current_user.id)),
                            watch_history=json.dumps(db.get_watch_history(current_user.id)))

@app.route("/editprofile")
@login_required
def editprofile():
    """editprofile endpoint"""
    return render_template("editprofile.html", userid=current_user.id,
                            fullname=current_user.name,
                            email=current_user.email,
                            profile_pic=current_user.profile_pic,
                            usertype=current_user.usertype)

@app.route("/stream", methods=['GET', 'POST'])
@login_required
def stream():
    """stream endpoint"""
    if request.method == 'POST' and 'stream_category' in request.form:
        # build pipeline request
        
        StackName = 'liveStreaming' + current_user.id
        try:
            # if the streaming pipeline already exists
            AWS_client.describe_stacks(StackName=StackName)
            return render_template("stream.html", current_user_name=current_user.name)

        except (ValueError, Exception):
            # if there's no pipeline for this streamer
            try:
                AWS_client.create_stack(
                    StackName=StackName,
                    TemplateBody=open('live-streaming-on-aws-with-mediastore.template', 'r').read(),
                    # If you don't have a template file in the folder then comment the line above and use the line below 
                    # TemplateURL='https://s3.amazonaws.com/solutions-reference/live-streaming-on-aws-with-mediastore/latest/live-streaming-on-aws-with-mediastore.template',
                    Parameters=[
                        {
                            'ParameterKey': 'InputType',
                            'ParameterValue': 'RTMP_PUSH',
                        },
                        {
                            'ParameterKey': 'InputCIDR',
                            'ParameterValue': '0.0.0.0/0',
                        }
                    ],
                    TimeoutInMinutes=10,
                    Capabilities=[
                        'CAPABILITY_IAM',
                    ],
                )
                stream_category = request.form.get('stream_category')
                db.create_stream(current_user.id, current_user.name, stream_category)
                return render_template("stream.html", current_user_name=current_user.name)
            except (ValueError, Exception):
                return "Fail to start creating streaming pipeline, try it again later" 
    elif request.method == 'POST':
        # delete pipeline request
        StackName = 'liveStreaming' + current_user.id
        AWS_client.delete_stack(StackName=StackName)
        db.delete_stream(current_user.id)
        return render_template("stream.html", current_user_name=current_user.name)

    else:
        # just access to the endpoint
        return render_template("stream.html", current_user_name=current_user.name)

@app.route("/stream/describe_stack")
@login_required
def stream_describe_stack():
    # Let the stream page can dynamically show the status of the AWS CloudFormation stack.
    StackName = 'liveStreaming' + current_user.id
    try:
        # if the streaming pipeline already exists
        stack_detail = AWS_client.describe_stacks(StackName=StackName)

        if stack_detail['Stacks'][0]['StackStatus'] == 'DELETE_IN_PROGRESS':
            Context = "Deleting Your Streaming Pipeline, if you want to build another one, please wait until this deletion complete"
            OBS_URL = ""
            Stream_Key = ""
        elif stack_detail['Stacks'][0]['StackStatus'] != 'CREATE_COMPLETE':
            Context = "Your Streaming Pipeline is under construction..."
            OBS_URL = ""
            Stream_Key = ""
        else:
            Context = "Your Streaming Pipeline is ready, using the information shown below in OBS and start your streaming"
            OBS_URL = stack_detail['Stacks'][0]['Outputs'][2]['OutputValue'][
                  :-7] # endpoint for live-streamer to input in OBS
            Stream_Key = "stream"

    except (ValueError, Exception):
        Context = "You haven't started the construction of your streaming pipeline, choose a category and click \"Build Pipeline\" to start"
        OBS_URL = ""
        Stream_Key = ""
    current_watching = db.get_current_watching(current_user.id)
    return render_template('stream_describe_stack.html', Context=Context, OBS_URL=OBS_URL, Stream_Key=Stream_Key, current_watching=current_watching)

@app.route("/stream/show_video_player")
@login_required
def stream_show_video_player():
    # Show a video player on the stream page.
    # If the pipeline is completed, the m3u8 URL will be embedded into the player
    # Otherwise, the URL will be empty
    StackName = 'liveStreaming' + current_user.id
    try:
        # if the streaming pipeline already exists
        stack_detail = AWS_client.describe_stacks(StackName=StackName)
        if stack_detail['Stacks'][0]['StackStatus'] != 'CREATE_COMPLETE':
            return render_template('stream_show_video_player.html', m3u8_URL="", current_user_name=current_user.name, room_name=current_user.id)
        else:
            m3u8_URL=stack_detail['Stacks'][0]['Outputs'][4]['OutputValue']
            db.update_stream(current_user.id, m3u8_URL)
            return render_template('stream_show_video_player.html', m3u8_URL=m3u8_URL, current_user_name=current_user.name, room_name=current_user.id)
    except (ValueError, Exception):
        return render_template('stream_show_video_player.html', m3u8_URL="", current_user_name=current_user.name, room_name=current_user.id)

@app.route("/view/<id_>")
def view_id(id_):
    UUID = str(uuid.uuid1())
    m3u8_URL = db.get_streaming_m3u8(id_)
    db.update_current_watching(id_, increase=True)
    advertise_list = db.get_advertise(streamer=id_)
    advertise = ""
    if advertise_list:
        advertise = random.choice(advertise_list)

    if m3u8_URL:
        m3u8_URL = m3u8_URL[0]
    if current_user.is_authenticated:
        db.insert_watch_history(current_user.id, id_, UUID)
        return render_template('view_id.html', m3u8_URL=m3u8_URL, current_user_name=current_user.name, room_name=id_, UUID=UUID, advertise=advertise)
    else:
        db.insert_watch_history('nonuser', id_, UUID)
        return render_template('view_id.html', m3u8_URL=m3u8_URL, room_name=id_, UUID=UUID, advertise=advertise)

@app.route("/company/<type_>", methods=['GET', 'POST'])
@login_required
def company(type_):
    print(current_user.usertype)
    if current_user.usertype != 'Company':
        return "You are not a company.", 403
    
    if type_ == 'category':
        if request.method == 'GET':
            category_all, cat_list = db.get_analytics_category_all()
            print(category_all, cat_list)
            chart = []
            for cat in category_all:
                potential = 31*cat['value']
                chart.append([cat['x'], str(potential)+'/mon', '$'+f'{potential/7:.2f}'])
            
            return render_template('company.html', chart = chart, cat_list = cat_list, typee = type_, data_all=category_all, current_user_name=current_user.name)
        else:
            selected = request.form['category']
            category_time, cat_list = db.get_analytics_category(selected)
            category_all, cat_list = db.get_analytics_category_all()
            print(category_time, cat_list)
            chart = []
            for cat in category_all:
                potential = 31*cat['value']
                chart.append([cat['x'], str(potential)+'/mon', '$'+f'{potential/7:.2f}'])
            
            return render_template('company2.html', chart = chart, selected = selected, cat_list = cat_list, typee = type_, data_all=category_time, current_user_name=current_user.name)
    else:
        if request.method == 'GET':
            user_all, cat_list = db.get_analytics_user_all()
            print(user_all, cat_list)
            chart = []
            for cat in user_all:
                potential = 31*cat['value']
                chart.append([cat['x'], str(potential)+'/mon', '$'+f'{potential/7:.2f}'])
                
            return render_template('company.html', chart = chart, cat_list = cat_list, typee = type_, data_all=user_all, current_user_name=current_user.name)
        else:
            selected = request.form['category']
            user_time, cat_list = db.get_analytics_user(selected)
            user_all, cat_list = db.get_analytics_user_all()
            print(user_time, cat_list)
            chart = []
            for cat in user_all:
                potential = 31*cat['value']
                chart.append([cat['x'], str(potential)+'/mon', '$'+f'{potential/7:.2f}'])
            
            return render_template('company2.html', chart = chart, selected = selected, cat_list = cat_list, typee = type_, data_all=user_time, current_user_name=current_user.name)

@app.route("/payment", methods=['GET', 'POST'])
@login_required
def payment():
    print(request.form)
    purchase = request.form.to_dict()
    purchase = [[k, purchase[k]] for k in purchase if purchase[k]]
    
    return render_template('payment.html', purchase = purchase, current_user_name=current_user.name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/thanks", methods=['GET', 'POST'])
@login_required
def thanks():
    data = request.form.to_dict()
    print(data)
    file = request.files['image']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect("/company/category")
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
    for k in data:
        if k != 'creditcard' and k != 'image':
            if type(data[k]) != int:
                data[k] = 1
            valid_until = datetime.now() + timedelta(days=30*data[k])
            valid_until = valid_until.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            db.insert_advertise(k, k, valid_until, '\\'+file_path)
        
    return render_template('thanks.html', current_user_name=current_user.name)



# socketio, it is for the chating function on the view page

@socketio.on('send_message')
def handle_send_message_event(data):
    db.insert_audience_comment(watcher=data['username'], streamer=data['room'], message=data['message'])
    app.logger.info("{} has sent message to the room {}: {}".format(data['username'],
                                                                    data['room'],
                                                                    data['message']))
    socketio.emit('receive_message', data, room=data['room'])


@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])


@socketio.on('leave_room')
def handle_leave_room_event(data):
    if data['username']:
        app.logger.info("{} has left the room {}".format(data['username'], data['room']))
        leave_room(data['room'])
        db.update_current_watching(data['room'], increase=False)
        db.update_watch_history(data['UUID'])
        socketio.emit('leave_room_announcement', data, room=data['room'])
    else:
        db.update_current_watching(data['room'], increase=False)
        db.update_watch_history(data['UUID'])

   
if __name__ == "__main__":
    #app.run(ssl_context="adhoc", debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, keyfile='localhost.key', certfile='localhost.crt', debug=True)
