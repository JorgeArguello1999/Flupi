from firebase_admin import credentials, firestore
import firebase_admin

from dotenv import load_dotenv
import os

load_dotenv()

# Inicializa la aplicación de Firebase Admin
cred = credentials.Certificate(f'{os.getenv("JSON_GCS")}')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Estructura deseada que deseamos verificar
estructura = {
    "alarm": 0,
    "ips": ["186.4.248.9"],
    "fotos": {
        "chatbot": "foto_base64",
        "usuario": "foto_base64"
    },
    "mensajes": {
        "entender_consulta": "El cliente está preguntando por un producto específico. Asegúrate de Escribir una instrucción: 'func database <producto>'. Reemplaza '<producto>' con el nombre real del producto que el cliente está preguntando. Por ejemplo, si el cliente pregunta por 'Tienes teclados?', la instrucción resultante debería ser 'func database teclado', limpia los caracteres de pregunta y si lo que esta buscando esta en plural cámbialo a singular, en caso de que ponga un número, este número es el objeto a buscar. El cliente cuando solicite información de la hora vas a escribir 'func time' en cualquier tipo de petición donde te pida el tiempo actual, por ejemplo '¿Que hora es?' tu respuesta va a ser 'func time', lo mismo si dice que horas son, y así sucesivamente, solo cuando se refiera al tiempo actual, caso contrario responde la pregunta según tu contexto. Cuando el cliente solicite información sobre la fecha vas a escribir 'func date' en cualquier tipo de petición que corresponda saber la fecha en la que se encuentra vas a devolver únicamente 'func date', ejemplo: '¿Qué fecha es?' tu respuesta sera 'func date'. Cuando el cliente diga algo como 'llamar al técnico' o 'quiero llamar al técnico', o frases similares vas a responder de la siguiente manera 'func tecnico', por ejemplo 'llamar al técnico' tu respuesta debe ser 'func tecnico', esto siempre y cuando su pregunta sea relacionada con ver al técnico.",
        "general": "¡Bienvenidos a CompuMax!Soy Maxi, un amable asistente de ventas en Compumax. Aquí te ayudaremos con productos y servicios informáticos.Desarrollo de Software:- Creamos software personalizado para web y móviles.- Entendemos tus necesidades y las convertimos en soluciones.Servicio Técnico:- Reparamos computadoras, impresoras y más.- Nuestros técnicos certificados solucionarán tus problemas.Venta de Equipos:- Ofrecemos computadoras, impresoras y más a precios competitivos.- Asesoramos en la elección y configuración.Estamos comprometidos con soluciones de alta calidad. Si tienes preguntas, contáctanos.Contacto:Teléfono: (593) 03-2894821Celular: (593) 0984840050Horario: Lunes a Viernes (09h00 - 13h30, 14h30 - 18h30)Pagina web: https://compumax.ec/Aplicaciones destacadas:- Actimax: Gestión de activos. sitio web: https://compumax.ec/control-administrativo/- Edumax: Sistema de gestión académica. sitio web: https://edumax.ec/- Factumax: Facturación Electrónica en la nube. sitio web: https://compumax.ec/facturacion-electronica-en-la-nube/Nota: Cuando te pregunten sobre estos aplicativos, como por ejemplo como se hace una cosa en los sistemas, tienes que responder que no sabes, pero que pueden visitar las paginas web, oficiales de cada aplicativo (Los links te los puse arriba al frente de los servicios que ofrecen)¿Quiénes Somos?Compumax, fundada en 1999, brinda software de gestión administrativa y servicios de alta calidad. Con más de veinticuatro años de experiencia, somos líderes en tecnología.Misión: Ofrecer soluciones informáticas adaptadas a las necesidades de nuestros clientes.Visión: Ser una empresa integral que cubre las necesidades tecnológicas de software y hardware.Ubicados en Gonzales Suárez y Ceslao Marín en Puyo Pastaza Ecuador.¡Estamos aquí para ayudarte! ¿En qué podemos asistirte hoy?IMPORTANTE RESPUESTAS CORTAS MAXIMO 120 PALABRAS E INTENTA SIEMPRE RELACIONAR LOS TERMINOS CON INFORMÁTICA, USA DATOS REALES, NO TE INVENTES NADA, ES UNA ORDEN,Tienes que aconsejar segun la pregunta lo que esta buscando las personas y recomendar los diferentes servicios que ofrecemos como servicio técnico, creación de aplicacionesy venta de equipos informaticos.",
        "no_producto": "Di de la manera más amable, que lastimosamente no pudiste encontrar lo solicitado y que puede probar haciendo su consulta con palabras como Tienes <producto> o palabras similares."
    },
    "home": "<h1>Hola soy Chatbot</h1> <b>No te Olvides, Elimina todos los usuarios existentes, y crea unos nuevos, no te olvides crear el usuario: --chatbot-- sin este tu aplicación no va a funcionar :)"
}

def initialize(database:str, proyect_name:str)-> bool:
    """
    Si existe devolvera True caso contrario creara y devolvera False
    """

    # Referencia al documento específico en la colección original
    documento_ref = db.collection(database).document(proyect_name)
    documento = documento_ref.get()

    if documento.exists:
        print('Estructura existe, no se hace nada')
        return True

    else:
        # Actualiza el documento original con la nueva estructura (sin 'usuarios')
        print('Creando estructura....')
        documento_ref.set(estructura)
        print('Seteando valores...')

        # Crea una subcolección 'usuarios' dentro del documento actual
        usuarios_ref = documento_ref.collection('usuarios')
        usuarios_ref.document('K6V29TNhTe7NUXG4BzLj').set({
            "username": "chatbot",
            "password": "scrypt:32768:8:1$ZjLndAQf91pvjEaD$c0b7d368d207ac6d459bd5602c6747f32cb945fdab458dd63afd440f2afa87383a4897db28448f1a7fcb389718eb47ad186a05c0eedeb01be45c8a033bd51a61",
            "token": "bb76d7a3-3fdf-46af-ba78-424b965bb5a9"
        })

        usuarios_ref.document('SzY49qb9TaCeSvWmDhue').set({
            "username": "compumax@soporte.com",
            "password": "scrypt:32768:8:1$57QUZ18g6CYk7txl$ee2d798e5fda302612e01c630cb57b7f2c91e8ea4754eeabcc655b4456a673d7de81eefdf2d45dd672494c7a178c9a63e46dc8811fcb0f58e6a7869b72cb95c5",
            "token": "97293a31-9100-4f8f-8647-64856d1e2101"
        })
        print('Terminado.')

        return False

if __name__ == '__main__':
    salida = initialize('contextos', 'Edumax')
    print(salida)