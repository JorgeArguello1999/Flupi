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

        // Mostrar mensaje del usuario originalmente enviado
        showMessage(userMessage, true, null, currentTime);

        // Mostrar mensaje de escritura del bot
        showMessage("Escribiendo...", false, null, currentTime);

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
            // Eliminar el mensaje de escritura del bot
            $('#chat-messages').find('.message-bot:contains("Escribiendo...")').remove();

            // Mostrar mensaje de respuesta de la API con la foto y la pregunta
            showMessage(data.response, false, data.photo_role, currentTime);

            // Actualizar el mensaje del usuario con la información de la API
            $('#chat-messages').find('.message-user:contains("' + userMessage + '")').html(`
                <img src="data:image/png;base64,${data.photo_user}" class="img_profile" />
                <p>${userMessage}</p>
                <span class="message-time">${currentTime}</span>
            `);

            scrollToBottom();
        })
        .catch(error => {
            // Eliminar el mensaje de escritura del bot en caso de error
            $('#chat-messages').find('.message-bot:contains("Escribiendo...")').remove();

            console.error('Error:', error);
        });

        $("#message-input").val("");
    });

    scrollToBottom();
    $("#message-input").focus();
});
