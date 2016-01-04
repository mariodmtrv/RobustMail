from flask import Flask
import json
from core.mail.email_validator import EmailValidator
import logging
from core.services.message_service import send_message, add_together, message_service
from flask import request
from core.mail.message import Message

app = Flask(__name__)


@app.route('/api/send-mail')
def send_mail():
    data = request.get_json()
    message = Message()
    send_message.apply_assync(message_service, message)


@app.route('/add')
def add():
    result = add_together.delay(14, 25)
    return result.wait()


@app.route('/hello')
def hello():
    return "Hello RobustMail"


class EmailValidatorResponse():
    def __init__(self, is_successful=False, message=''):
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
