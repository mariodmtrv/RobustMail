/**
 * Created by mariodimitrov
 */

function address_server_validation(source, address) {
    this.message = {
        "email": address
    }
    $.ajax({
        type: "POST",
        url: "/api/validate-email",
        data: JSON.stringify(this.message),
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    }).complete(function (data) {
    if (data.responseJSON["correct"] == false){
        display_response(ResponseType.FAILURE, source + "  " + data.responseJSON.message);
     }
    });
}
function send_simple_message() {
 this.senderEmail = $("#sender-email").val();
 this.senderName = $("#sender-name").val();

    this.message = {
        "sender": {"email":  this.senderEmail, "name": this.senderName}, "recipients": [{"email": "", "name": ""}],
        "text": "",
        "subject": ""
    }

    $.ajax({
        type: "POST",
        url: "api/send-mail",
        data: this.message,
        contentType: "application/json; charset=utf-8",
        dataType: "json"
    }).complete(function (data) {

        // success
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
        this.email = $("#sender-email").val();
            address_server_validation("Sender email", this.email);
            console.log(this.email);
        })
        $("#recipient-email").focusout(function () {
           this.email = $("#recipient-email").val();
            address_server_validation("Recipient email",this.email);
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