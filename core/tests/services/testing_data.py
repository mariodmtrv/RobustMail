from core.mail.message import Message


def bad_message_wrong_address():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.add_recipient('other.userdomain.com', 'Regular Recipient')
    m.subject = "Very important"
    m.text = "Another spam message"
    return m


def good_message():
    m = Message()
    m.set_sender('user@domain.com', 'Regular Sender')
    m.add_recipient('mario.dimitrov@ymail.com', 'Regular Recipient')
    m.subject = "Very important"
    m.text = "Another spam message"
    return m
