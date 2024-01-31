// Variable global para almacenar las fotos
let globalPhotos = [];

// Función para obtener las fotos y almacenarlas en la variable global
function getPhotos(photosUrl) {
    return fetch(photosUrl)
        .then(response => response.json())
        .then(data => {
            globalPhotos = data;  // Almacenar las fotos en la variable global
        })
        .catch(error => {
            console.error('Error fetching photos:', error);
        });
}

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
    var originUrl= window.location.origin;
    let apiUrl = originUrl+'/chatbot/';
    let photosUrl = originUrl+'/widget/photos/';

    console.log(originUrl);
    console.log(apiUrl);
    console.log(photosUrl);

    // Cargamos las fotos
    getPhotos(photosUrl);

    // Intercepta el envío del formulario
    $("#chat-form").submit(function(event) {
        event.preventDefault();
        const userMessage = $("#message-input").val();
        const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }); 

        // Mostrar mensaje del usuario originalmente enviado
        showMessage(userMessage, true, globalPhotos.photo_user, currentTime);

        // Mostrar mensaje de escritura del bot
        showMessage("Escribiendo...", false, globalPhotos.photo_role, currentTime);

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "ask": userMessage 
            })
        })
        .then(response => response.json())
        .then(data => {
            // Eliminar el mensaje de escritura del bot
            $('#chat-messages').find('.message-bot:contains("Escribiendo...")').remove();

            // Mostrar mensaje de respuesta de la API con la foto y la pregunta
            let response = data.response;
            response = response.replace(/\n/g, "</br>");
            showMessage(response, false, globalPhotos.photo_role, currentTime);

            // Actualizar el mensaje del usuario con la información de la API
            $('#chat-messages').find('.message-user:contains("' + userMessage + '")').html(`
                <img src="data:image/png;base64,${globalPhotos.photo_user}" class="img_profile" />
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
