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

function init(apiUrl){
    $(document).ready(function() {
        // Elementos del chat
        const chatOpenBtn = $('#chat-open-btn');
        const chatPopup = $('#chat-popup');
        const chatMessages = $('#chat-messages');
        const chatForm = $('#chat-form');
        const messageInput = $('#message-input');

        // Cargamos las fotos 
        let photosUrl = apiUrl + 'photos/';
        console.log("url:", photosUrl);
        getPhotos(photosUrl);

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

        function showMessage(message, isUser, image, time) {
            const sender = isUser ? 'Tú' : 'Chatbot';
            const cssClass = isUser ? 'message-user' : 'message-bot';

            const messageDiv = `
                <div class="${cssClass}">
                <img src="data:image/png;base64,${image}" class="img_profile" />
                <p>${message}</p>
                <span class="message-time">${time}</span>
                </div>`;
            chatMessages.append(messageDiv);
            scrollToBottom();
        }

        // Intercepta el envío del formulario
        chatForm.submit(function (event) {
            event.preventDefault();
            const userMessage = messageInput.val();
            const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

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
                    "ask": userMessage 
                })
            })
                .then(response => response.json())
                .then(data => {
                    // Eliminar el mensaje de escritura del bot
                    chatMessages.find('.message-bot:contains("Escribiendo...")').remove();

                    // Mostrar mensaje de respuesta de la API con la foto y la pregunta
                    let response = data.response;
                    response = response.toString();
                    console.log(response);
                    showMessage(response, false, globalPhotos.photo_role, currentTime);

                    // Actualizar el mensaje del usuario con la información de la API
                    chatMessages.find(`.${cssClass}-user-message`).html(`
                        <img src="data:image/png;base64,${globalPhotos.photo_user}" class="img_profile" />
                        <p>${userMessage}</p>
                        <span class="message-time">${currentTime}</span>
                    `);
                    showMessage(userMessage, true, globalPhotos.photo_user, currentTime);
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