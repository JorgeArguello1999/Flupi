$(document).ready(function() {
    function getProfileImage(isUser, imageData) {
        if (isUser) {
            return `<img src="${convertBase64ToImage(imageData)}" alt="user_profile" class="img_profile">`;
        } else {
            return `<img src="${convertBase64ToImage(imageData)}" alt="chatbot_profile" class="img_profile">`;
        }
    }

    function convertBase64ToImage(base64String) {
        return `data:image/jpeg;base64,${base64String}`;
    }

    function showApiResponse(responseData) {
        const response = responseData.response;
        const role = responseData.role;
        const photoUser = responseData.photo_user; // Imagen base64 del usuario
        const photoRole = responseData.photo_role; // Imagen base64 del chatbot
        const timeAnswer = responseData.time_answer; // Hora de la respuesta

        let photo = "";

        if(role === "assistant") {
            photo = photoRole;
        } else if(role === "user") {
            photo = photoUser;
        }

        const cssClass = role === "assistant" ? 'message-bot' : 'message-user';
        
        const messageDiv = `<div class="${cssClass}">${getProfileImage(role === "assistant", photo)}<p>${response}</p><span class="message-time">${timeAnswer}</span></div>`;
        $("#chat-messages").prepend(messageDiv);

        $("#chat-container").scrollTop(0);
    }

    function showMessage(message, isUser, photoUser) {
        const sender = isUser ? 'Tú' : 'Chatbot';
        const cssClass = isUser ? 'message-user' : 'message-bot';
        const profileImg = getProfileImage(isUser, photoUser);
        const currentTime = new Date().toLocaleTimeString(); // Obtener la hora actual
        const messageDiv = `<div class="${cssClass}">${profileImg}<p>${message}</p><span class="message-time">${currentTime}</span></div>`;
        $("#chat-messages").prepend(messageDiv);

        $("#chat-container").scrollTop(0);
    }

    $("#chat-form").submit(function(event) {
        event.preventDefault();
        const userMessage = $("#message-input").val();
        showMessage(userMessage, true, 'user');

        $.ajax({
            type: "POST",
            url: "/api/",
            data: JSON.stringify({ 
                "ask": userMessage, 
                "user": "Bot",
                "device": "computer"
            }),
            contentType: "application/json",
            dataType: "json",
            success: function(data) {
                showApiResponse(data);
            }
        });

        $("#message-input").val("");
    });

    $("#message-input").focus();

    $(".command").on("click", function(event) {
        const selectedCommand = $(this).text();
        $("#message-input").val(selectedCommand);
    });
});