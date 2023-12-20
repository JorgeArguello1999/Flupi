        // Cuando se hace clic en el botón "Abrir"
        document.getElementById('openBtn').addEventListener('click', function(event) {
            const selectedFile = document.getElementById('filename').value;
            fetch(`/configs/context/${selectedFile}`)  // Modificar la URL aquí
            .then(response => response.json())
            .then(data => {
                document.getElementById('content').value = data.content;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        document.getElementById('editForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const filename = document.getElementById('filename').value;
            const content = document.getElementById('content').value;
            
            fetch(`/configs/context/${filename}`, {  // Modificar la URL aquí
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content: content })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
        
        // Obtener el contenido del archivo seleccionado al cargar la página
        window.addEventListener('DOMContentLoaded', function() {
            const filename = document.getElementById('filename').value;
            fetch(`/configs/context/${filename}`)  // Modificar la URL aquí
            .then(response => response.json())
            .then(data => {
                document.getElementById('content').value = data.content;
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
 