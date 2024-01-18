$(document).ready(function() {

    function scrollToBottom() {
        $('#chat-messages').animate({ scrollTop: $('#chat-messages').prop('scrollHeight') }, 300);
    }

    function showMessage(message, isUser, image, time) {
        const sender = isUser ? 'Tú' : 'Chatbot';
        const cssClass = isUser ? 'message-user' : 'message-bot';
        const messageDiv = `
            <div class="${cssClass}">
                <img src="data:image/png;base64,${image}" class="img_profile" />
                <p>${message}</p>
                <span class="message-time">${time}</span>
            </div>`;
        $("#chat-messages").append(messageDiv);
        scrollToBottom();
    }
    var apiUrl = window.location.origin;
    apiUrl = apiUrl+'/chatbot/';
    console.log(apiUrl);

    // Lista de preguntas realizadas por el usuario
    let list = [];

    // Intercepta el envío del formulario
    $("#chat-form").submit(function(event) {
        event.preventDefault();
        const userMessage = $("#message-input").val();
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); 

        // Limitar la longitud del contexto y crear un resumen
        const contexto = `Con base a estas interacciones: ${list.slice(-5).join(';')} > Responde unicamente la pregunta actual: ${userMessage}`;

        // Guardamos las preguntas en la lista para generar un contexto
        list.push(userMessage);

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "ask": contexto 
            })
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta de la API
            showMessage(userMessage, true, data.photo_user, currentTime); // Mostrar la foto del usuario después de su mensaje
            showMessage(data.response, false, data.photo_role, currentTime); // Mostrar la respuesta del chatbot después del mensaje del usuario
        })
        .catch(error => {
            console.error('Error:', error);
        });

        $("#message-input").val("");
    });

    scrollToBottom();
    $("#message-input").focus();
});
