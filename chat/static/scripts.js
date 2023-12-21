$(document).ready(function() {
    function scrollToBottom() {
        $('#chat-messages').animate({ scrollTop: $('#chat-messages').prop('scrollHeight') }, 300);
    }

    function showMessage(message, isUser) {
        const sender = isUser ? 'Tú' : 'Chatbot';
        const cssClass = isUser ? 'message-user' : 'message-bot';
        const currentTime = new Date().toLocaleTimeString(); // Obtener la hora actual
        const messageDiv = `<div class="${cssClass}"><p>${message}</p><span class="message-time">${currentTime}</span></div>`;
        $("#chat-messages").append(messageDiv);
        scrollToBottom();
    }

    // Intercepta el envío del formulario
    $("#chat-form").submit(function(event) {
        event.preventDefault();
        const userMessage = $("#message-input").val();
        showMessage(userMessage, true);

        // Aquí puedes realizar la llamada a la API con fetch o AJAX si lo necesitas
        // Ejemplo de llamada fetch a una API
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
            showMessage(data.response, false);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        $("#message-input").val("");
    });

    scrollToBottom();
    $("#message-input").focus();
});
