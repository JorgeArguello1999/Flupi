function init(apiUrl){
    $(document).ready(function() {
        // Elementos del chat
        const chatOpenBtn = $('#chat-open-btn');
        const chatPopup = $('#chat-popup');
        const chatMessages = $('#chat-messages');
        const chatForm = $('#chat-form');
        const messageInput = $('#message-input');

        // Mostrar el cuadro de diálogo emergente al hacer clic en el botón de apertura
        chatOpenBtn.click(function() {
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
        chatForm.submit(function(event) {
            event.preventDefault();
            const userMessage = messageInput.val();
            const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

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
                // Manejar la respuesta de la API
                showMessage(userMessage, true, data.photo_user, currentTime); // Mostrar la foto del usuario después de su mensaje
                showMessage(data.response, false, data.photo_role, currentTime); // Mostrar la respuesta del chatbot después del mensaje del usuario
            })
            .catch(error => {
                console.error('Error:', error);
            });

            messageInput.val("");
        });
    });
}