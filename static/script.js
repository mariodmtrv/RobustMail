/**
 * Created by mariodimitrov
 */

function address_server_validation(source, address) {
    var message = {
        "email": address
    }
    $.ajax({
        type: "POST",
        url: "/api/validate-email",
        data: JSON.stringify(message),
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    }).complete(function (data) {
    if (data.responseJSON["correct"] == false){
        display_response(ResponseType.FAILURE, source + "  " + data.responseJSON.message);
     }
    });
}
function mock_message(){
 var message = {
        "sender": {"email":  "regular@domain.com", "name": "Regular spammer"}, "recipients": [{"email": "mario.dimitrov@ymail.com", "name": "Regular recipient"}],
        "text": "Another spam message",
        "subject": "Very important"
    }
     var result = JSON.stringify(message);
    return result;
}
function collect_data(){

 var senderEmail = $("#sender-email").val();
 var senderName = $("#sender-name").val();
 var recipientEmail = $("#recipient-email").val();
 var recipientName = $("#recipient-name").val();
 var text = $("#message-text").val();
 var subject = $("#subject").val();


    var message = {
        "sender": {"email":  senderEmail, "name": senderName}, "recipients": [{"email": recipientEmail, "name": recipientName}],
        "text": text,
        "subject": subject
    }
    var result = JSON.stringify(message);
    return result;
}
function send_simple_message() {
var message = mock_message();
    $.ajax({
        type: "POST",
        url: "/api/send-mail",
        data: message,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    }).complete(function (data) {
   if (data.responseJSON["correct"] == false){
        display_response(ResponseType.FAILURE, data.responseJSON.message);
     }
     else {
      display_response(ResponseType.SUCCESS, data.responseJSON.message);
     }
    });
}
ResponseType = {
    SUCCESS: 0,
    WARNING: 1,
    FAILURE: 2
}
$(document)
    .ready(
    function () {
        $("#sender-email").focusout(function () {
        var email = $("#sender-email").val();
            address_server_validation("Sender email", email);
            console.log(email);
        })
        $("#recipient-email").focusout(function () {
           var email = $("#recipient-email").val();
            address_server_validation("Recipient email",email);
        })
    });
function display_response(type, message) {
    /*alert alert-warning
     alert alert-danger
     alert alert-success
     */
    self.responseArea = $('#message');
    console.log("Test");
    if (type == ResponseType.SUCCESS) {
        self.responseArea.addClass("alert alert-success");
    }
    else if (type = ResponseType.WARNING) {
        self.responseArea.addClass("alert alert-warning");
    }
    else if(type == ResponseType.FAILURE){
        self.responseArea.addClass("alert alert-danger");
    }
    self.responseArea.html(message);
}