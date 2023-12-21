$(document).ready(function() {
    function scrollToBottom() {
        $('#chat-messages').animate({ scrollTop: $('#chat-messages').prop('scrollHeight') }, 300);
    }

    function showMessage(message, isUser, image) {
        const sender = isUser ? 'Tú' : 'Chatbot';
        const cssClass = isUser ? 'message-user' : 'message-bot';
        const currentTime = new Date().toLocaleTimeString(); // Obtener la hora actual del computador
        const messageDiv = `
            <div class="${cssClass}">
                <img src="data:image/png;base64,${image}" class="img_profile" />
                <p>${message}</p>
                <span class="message-time">${currentTime}</span>
            </div>`;
        $("#chat-messages").append(messageDiv);
        scrollToBottom();
    }

    // Intercepta el envío del formulario
    $("#chat-form").submit(function(event) {
        event.preventDefault();
        const userMessage = $("#message-input").val();

        fetch('/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "ask": userMessage,
                "user": "Bot",
                "device": "computer"
            })
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta de la API
            showMessage(data.response, false, data.photo_role); // Suponiendo que 'data.botImage' contiene la imagen en base64 del bot
            showMessage(userMessage, true, data.photo_user); // Suponiendo que 'data.userImage' contiene la imagen en base64 del usuario
        })
        .catch(error => {
            console.error('Error:', error);
        });

        $("#message-input").val("");
    });

    scrollToBottom();
    $("#message-input").focus();
});