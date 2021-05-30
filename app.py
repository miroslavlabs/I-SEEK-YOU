import logging
from datetime import datetime

import pytz
from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal, fields, inputs, HTTPException, abort
from flask_sqlalchemy import SQLAlchemy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api = Api(app)
db = SQLAlchemy(app)


class UserNotLoggedInError(HTTPException):
    pass


class UserResource(Resource):
    fields = {
        'id': fields.Integer,
        'username': fields.String,
        'joined_at': fields.DateTime(dt_format='iso8601')
    }

    def get(self):
        users = User.query.all()
        return marshal(users, self.fields, envelope='users')

    def post(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()

        return marshal(user, self.fields, envelope='user')


class MessageResource(Resource):
    post_message_parser = reqparse.RequestParser()
    post_message_parser.add_argument('username', type=str, required=True)
    post_message_parser.add_argument('message', type=str, required=True)

    get_messages_parser = reqparse.RequestParser()
    get_messages_parser.add_argument('username', type=str, required=False)
    get_messages_parser.add_argument('start_time', type=inputs.datetime_from_iso8601, required=False)

    fields = {
        'username': fields.String(attribute='user.username'),
        'message': fields.String,
        'timestamp': fields.DateTime(dt_format='iso8601')
    }

    def get(self):
        data = self.get_messages_parser.parse_args()
        username = data['username']
        start_time = data['start_time']

        messages = Message.query

        if username is not None:
            messages = messages.filter(User.username == username)

        if start_time is not None:
            messages = messages.filter(Message.timestamp >= start_time)

        return marshal(messages.all(), self.fields, envelope='messages')

    def post(self):
        data = self.post_message_parser.parse_args()
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if user is None:
            return abort(401, message='Log in first!')

        message = Message(message=data['message'])
        message.user_id = user.id
        db.session.add(message)
        db.session.commit()
        return marshal(message, self.fields, envelope='message')


class BillingCostResource(Resource):
    get_messages_parser = reqparse.RequestParser()
    get_messages_parser.add_argument('username', type=str, required=True)

    fields = {
        'username': fields.String,
        'total_cost': fields.Float,
    }

    def get(self):
        data = self.get_messages_parser.parse_args()
        username = data['username']

        user = User.query.filter_by(username=username).first()
        if user is None:
            return abort(401, message='User not found!')

        total_cost = sum(message.cost() for message in user.messages)

        return marshal({'username': username, 'total_cost': total_cost}, self.fields, envelope='cost')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.utc))
    messages = db.relationship('Message', backref='user', lazy=True)

    def __repr__(self):
        return "<User username: {}, joined_at: {}>".format(self.username, self.joined_at)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow().replace(tzinfo=pytz.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def cost(self):
        spaces_count = self.message.count(' ')
        return spaces_count * 10 + len(self.message) - spaces_count


@app.route('/')
def index():
    return 'Hello programmers!'


api.add_resource(
    MessageResource,
    '/api/v1/messages'
)
api.add_resource(
    UserResource,
    '/api/v1/users',
    '/api/v1/users/<string:username>',
)
api.add_resource(
    BillingCostResource,
    '/api/v1/billing-cost'
)

if __name__ == '__main__':
    app.run()

db.create_all()
db.session.commit()
