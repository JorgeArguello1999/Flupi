        // Función para actualizar la vista previa del archivo seleccionado actualmente
        function displayCurrentImagePreview(selectedImage) {
            fetch(`/configs/images/${selectedImage}`)
                .then(response => response.json())
                .then(data => {
                    if ('content' in data) {
                        document.getElementById('currentImagePreview').src = `data:image/jpeg;base64, ${data.content}`;
                    } else {
                        console.error('Image not found');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }

        document.getElementById('openBtn').addEventListener('click', function(event) {
            const selectedImage = document.getElementById('filename').value;
            displayCurrentImagePreview(selectedImage);
        });

        document.getElementById('editForm').addEventListener('submit', function(event) {
            event.preventDefault();
            const filename = document.getElementById('filename').value;
            const newImage = document.getElementById('newImage').files[0];

            const formData = new FormData();
            formData.append('new_image', newImage);

            fetch(`/configs/images/${filename}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                // Actualizar la vista previa del archivo actual y del nuevo archivo
                displayCurrentImagePreview(filename);
                document.getElementById('newImagePreview').src = URL.createObjectURL(newImage);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });

        document.getElementById('newImage').addEventListener('change', function(event) {
            const newImage = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function() {
                document.getElementById('newImagePreview').src = reader.result;
            };
            reader.readAsDataURL(newImage);
        });

        window.addEventListener('DOMContentLoaded', function() {
            const selectedImage = document.getElementById('filename').value;
            displayCurrentImagePreview(selectedImage);
        });
 