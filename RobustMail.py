from flask import Flask
import json
from core.mail.email_validator import EmailValidator
import logging
from core.services.message_service import send_message, add_together, message_service
from flask import request
from core.mail.message import Message

app = Flask(__name__)


class SendEmailResponse():
    def __init__(self, is_successful=False, message=""):
        self.__is_successful = is_successful
        self.__message = message

    def to_JSON(self):
        return json.dumps({"correct": self.__is_successful, "message": self.__message}, indent=4)


def gen_email_user(data):
    if data["email"] is not None:
        email = data["email"]
        name = ""
        if data["name"] is not None:
            name = data["name"]
        return (email, name)
    return None


@app.route('/api/send-mail', methods=['POST'])
def send_mail():
    data = request.get_json()
    message = Message()
    if "sender" in data and data["sender"] is not None:
        result = gen_email_user(data["sender"])
        if result is not None:
            message.set_sender(result[0], result[1])
    if "subject" in data and data["subject"] is not None:
        message.subject = data["subject"]
    if "text" in data and data["text"] is not None:
        message.text = data["text"]
    if "recipients" in data and data["recipients"] is not None and len(data["recipients"]) > 0:
        for recipient in data["recipients"]:
            result = gen_email_user(recipient)
            if result is not None:
                message.add_recipient(result[0], result[1])
    if 'cc' in data and data["cc"] is not None and len(data["cc"]) > 0:
        for recipient in data["cc"]:
            result = gen_email_user(recipient)
            if result is not None:
                message.add_cc(result[0], result[1])
    if "bcc" in data and data["bcc"] is not None and len(data["bcc"]) > 0:
        for recipient in data["bcc"]:
            result = gen_email_user(recipient)
            if result is not None:
                message.add_bcc(result[0], result[1])
    if "body" in data and data["body"] is not None:
        message.body = data["body"]
    is_valid = message.validate()
    if not is_valid:
        return SendEmailResponse(is_valid[0], is_valid[1]).to_JSON()
    result = send_message.delay(message_service, message)
    if result == True:
        return SendEmailResponse(True, "Successfully sent!").to_JSON()
    return SendEmailResponse(False, "Sending failed").to_JSON()


@app.route('/add')
def add():
    result = add_together.delay(14, 25)
    return result.wait()


@app.route('/hello')
def hello():
    return "Hello RobustMail"


class EmailValidatorResponse():
    def __init__(self, is_successful=False, message=""):
        self.__is_successful = is_successful
        self.__message = message

    def to_JSON(self):
        return json.dumps({"correct": self.__is_successful, "message": self.__message}, indent=4)


@app.route('/api/validate-email', methods=['POST'])
def validate_email():
    """

        :param email: string the address to be validates
        :return: response: EmailValidatorResponse JSON stringified success status and message
    """
    email = request.get_json()["email"].strip()
    if not EmailValidator.is_syntax_valid(email):
        response = EmailValidatorResponse(False, "Address syntax invalid")
    elif not EmailValidator.is_mx_valid(email):
        response = EmailValidatorResponse(False, "Address domain not found")
    else:
        response = EmailValidatorResponse(True, "Syntax and domain accepted")
        # address existence validation was excluded because of performance and reliability issues
    return response.to_JSON()


@app.route('/')
def root():
    return app.send_static_file('index.html')


if __name__ == '__main__':
    app.run(debug=True)
