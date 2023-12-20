    // URL de la API que deseas observar
    const apiUrl = '/notify';

    // Obtenemos el parrafo que va a servir como identificador
    let mensaje = document.getElementById("status");
    let caja = document.getElementById("box");
    let audio = document.getElementById("audio");
    const boton = document.getElementById("boton");

    // Mensajes a mostrar 
    let mensaje_clientes = "Cliente Afuera!!!";
    let mensaje_no_clientes = "No hay clientes";

    // Variable para controlar el estado del audio
    let audioActivo = false;

    // Función para activar/desactivar el audio
    function toggleAudio(activar) {
        if (activar) {
            audio.play();
            audio.loop = true;
        } else {
            audio.pause();
            audio.loop = false;
        }
    }

    // Reproducimos el sonido hasta que presione el boton
    boton.addEventListener("click", function (event) {
        event.preventDefault();
        if (audioActivo) {
            toggleAudio(false);
            audioActivo = false;
        }
        window.location.href = "/notify/0";
    });

    // Función para realizar la solicitud a la API y verificar cambios
    async function checkForChanges() {
        try {
            const response = await fetch(apiUrl);
            if (response.status === 200) {
                // Obtenemos el json de la API
                const data = await response.json();
                if (data.status != false) {
                    mensaje.innerHTML = mensaje_clientes;
                    caja.style.backgroundColor = "#94351b";
                    if (!audioActivo) {
                        toggleAudio(true);
                        audioActivo = true;
                    }
                } else {
                    mensaje.innerHTML = mensaje_no_clientes;
                    caja.style.backgroundColor = "#80dbff";
                    if (audioActivo) {
                        toggleAudio(false);
                        audioActivo = false;
                    }
                }
            } else {
                alert("Error al obtener datos de la API");
            }
        } catch (error) {
            alert('Error en la solicitud a la API', error);
        }
    }

    // Realizar la verificación cada cierto tiempo (por ejemplo, cada 1 segundo)
    setInterval(checkForChanges, 1000);