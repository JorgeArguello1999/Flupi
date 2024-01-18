// Variable global para almacenar las fotos
let globalPhotos = [];

// Función para obtener las fotos y almacenarlas en la variable global
function getPhotos(apiUrl) {
    return fetch(`${apiUrl}/photos/`)
        .then(response => response.json())
        .then(data => {
            globalPhotos = data;  // Almacenar las fotos en la variable global
        })
        .catch(error => {
            console.error('Error fetching photos:', error);
        });
}

function init(apiUrl){
    $(document).ready(function() {
        // Elementos del chat
        const chatOpenBtn = $('#chat-open-btn');
        const chatPopup = $('#chat-popup');
        const chatMessages = $('#chat-messages');
        const chatForm = $('#chat-form');
        const messageInput = $('#message-input');

        // Cargamos las fotos 
        getPhotos(apiUrl);
        console.log(globalPhotos);

        // Mostrar el cuadro de diálogo emergente al hacer clic en el botón de apertura
        chatOpenBtn.click(function() {
            const chatPopupVisible = chatPopup.is(":visible");
            if (!chatPopupVisible) {
                chatPopup.css("bottom", chatOpenBtn.outerHeight() + parseInt(chatOpenBtn.css("bottom")) + "px");
            }
                chatPopup.toggle();
                scrollToBottom();
        });
 

        // Función para desplazarse hacia abajo en el contenedor de mensajes
        function scrollToBottom() {
            chatMessages.animate({ scrollTop: chatMessages.prop('scrollHeight') }, 300);
        }

        // Función para mostrar un mensaje en el chat
        function showMessage(message, isUser, image, time) {
            const sender = isUser ? 'Tú' : 'Chatbot';
            const cssClass = isUser ? 'message-user' : 'message-bot';

            // Eliminar el mensaje anterior del usuario si existe
            chatMessages.find('.message-user:contains("' + message + '")').remove();

            const messageDiv = `
                <div class="${cssClass}">
                <img src="data:image/png;base64,${image}" class="img_profile" />
                <p>${message}</p>
                <span class="message-time">${time}</span>
                </div>`;
            chatMessages.append(messageDiv);
            scrollToBottom();
        }

        // Lista de preguntas realizadas por el usuario
        let list = [];

        // Intercepta el envío del formulario
        chatForm.submit(function (event) {
            event.preventDefault();
            const userMessage = messageInput.val();
            const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            // Limitar la longitud del contexto y crear un resumen
            const contexto = `Con base a estas interacciones: ${list.slice(-5).join(';')} > Responde únicamente la pregunta actual: ${userMessage}`;

            // Guardamos las preguntas en la lista para generar un contexto
            list.push(userMessage);

            // Mostrar mensaje del usuario originalmente enviado con la imagen
            showMessage(userMessage, true, globalPhotos.photo_user, currentTime);

            // Mostrar mensaje de escritura del bot con la imagen
            showMessage("Escribiendo...", false, globalPhotos.photo_role, currentTime);

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
                    chatMessages.find('.message-bot:contains("Escribiendo...")').remove();

                    // Mostrar mensaje de respuesta de la API con la foto y la pregunta
                    showMessage(data.response, false, globalPhotos.photo_role, currentTime);

                    // Actualizar el mensaje del usuario con la información de la API
                    chatMessages.find('.message-user:contains("' + userMessage + '")').html(`
                        <img src="data:image/png;base64,${globalPhotos.photo_user}" class="img_profile" />
                        <p>${userMessage}</p>
                        <span class="message-time">${currentTime}</span>
                    `);

                    scrollToBottom();
                })
                .catch(error => {
                    // Eliminar el mensaje de escritura del bot en caso de error
                    chatMessages.find('.message-bot:contains("Escribiendo...")').remove();

                    console.error('Error:', error);
                });

            messageInput.val("");
        });
    });
}