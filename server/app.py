from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
# POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method == 'GET':
        response_body = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        status_code = 200
        
    elif request.method == 'POST':
        
        new_message = Message(
            body = request.get_json().get('body'),
            username = request.get_json().get('username')
        )
        
        db.session.add(new_message)
        db.session.commit()
        
        response_body = new_message.to_dict()
        status_code = 201
        
    return make_response(response_body, status_code)

# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
# DELETE /messages/<int:id>: deletes the message from the database.
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    body = Message.query.filter(Message.id == id).first()
    
    if request.method == 'PATCH':
        for attr in request.get_json():
            setattr(body, attr, request.get_json().get(attr))
        db.session.commit()
        response_body = body.to_dict()
        status_code = 200
        
    elif request.method == 'DELETE':
        db.session.delete(body)
        db.session.commit()
        response_body = {'message': 'The record has been successfully deleted'}
        status_code = 200
        
    return make_response(response_body, status_code)

if __name__ == '__main__':
    app.run(port=5555)
