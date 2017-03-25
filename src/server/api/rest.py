from src.server import app, db
from src.server.models.message import Message
from src.server.models.user import User, talk_users_table
from flask import jsonify, request
from marshmallow import Schema, fields, ValidationError, pre_load



class MessageSchema(Schema):
    id = fields.Int(dump_only=True)
    message = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)

    def format_name(self, author):
        return "{}".format(author.message)


message_schema = MessageSchema()


@app.route("/messages/", methods=["POST"])
def new_message():
    json_data = request.get_json()
    print json_data
    if not json_data:
        return jsonify({'message': 'No input data provided'}), 400
    # # Validate and deserialize input
    data, errors = message_schema.load(json_data)
    if errors:
        return jsonify(errors), 422
    print data
    message = data['message']
    message = Message(message=message)
    db.session.add(message)
    db.session.commit()

    result = message_schema.dump(Message.query.get(message.id))
    return jsonify({"message": "Created new quote.",
                    "quote": result.data}
                   )
