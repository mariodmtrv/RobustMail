/**
 * Created by mariodimitrov
 */
 /*
 Collects the data from the message sending form
 */
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
function mock_message(){
 var message = {
        "sender": {"email":  "regular@domain.com", "name": "Regular spammer"}, "recipients": [{"email": "mario.dimitrov@ymail.com", "name": "Regular recipient"}],
        "text": "Another spam message",
        "subject": "Message from javascript"
    }
     var result = JSON.stringify(message);
    return result;
}
/*
Sends a simple message request and displays the server response
*/
function send_simple_message() {
var message = collect_data();
    $.ajax({
        type: "POST",
        url: "/api/send-mail",
        data: message,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        async: true,
    }).complete(function (data) {
    if (data.responseJSON["correct"] == true){
      displayResponse(ResponseType.SUCCESS, data.responseJSON.message);
      /*Clears the recipient*/
      $("#recipient-email").html("");
       $("#recipient-name").html("");
     }
     else{
        displayResponse(ResponseType.FAILURE, data.responseJSON.message);
     }
    });
    }
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
        displayResponse(ResponseType.FAILURE, source + "  " + data.responseJSON.message);
     }
    });
}
function mock_message(){
 var message = {
        "sender": {"email":  "regular@domain.com", "name": "Regular spammer"}, "recipients": [{"email": "mario.dimitrov@ymail.com", "name": "Regular recipient"}],
        "text": "Another spam message",
        "subject": "Message from javascript"
    }
     var result = JSON.stringify(message);
    return result;
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
        })
          $("#sender-email").focusin(function () {
            clearResponseArea();
          });

        $("#recipient-email").focusout(function () {
           var email = $("#recipient-email").val();
            address_server_validation("Recipient email",email);
        });
         $("#recipient-email").focusin(function () {
            clearResponseArea();
          });
    });
/*
Displays the server response in a stylized message area
*/
function displayResponse(type, message) {
    clearResponseArea();
    var responseArea = $('#message');
    if (type == ResponseType.SUCCESS) {
        responseArea.addClass("alert alert-success");
    }
    else if (type = ResponseType.WARNING) {
        responseArea.addClass("alert alert-warning");
    }
    else if(type == ResponseType.FAILURE){
        responseArea.addClass("alert alert-danger");
    }
    responseArea.html(message);
}
function clearResponseArea(){
    var responseArea = $('#message');
       responseArea.removeClass(function() {
  return responseArea.attr( "class" );
    });
    responseArea.html("");
}