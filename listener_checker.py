from word_list import lenguajes, links_int

class MessageCheck:
    key_word= None
    message_class = None

    @classmethod
    def chat(cls, message):
        cls.message_class = message
        contenido = message.content.lower()
        trigger_word = ['aprender','aprendiendo',]
        if any(word in contenido for word in trigger_word):
            # si alguna de las palabras en el mensaje es una palabra clave inicia la busqueda de la misma y su resultado.
            if any(word in contenido for word in lenguajes):
                contenido = contenido.split()
                for palabra in contenido:
                    if palabra in lenguajes:
                        cls.key_word = palabra
                        return cls.answer(cls.key_word)
            else:
                return

    @classmethod
    def answer(cls, data):
        match data:
            case 'python':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return (mensaje, links_int['python'])
            case 'java':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return mensaje
            case 'java script':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return mensaje
            case 'c':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return mensaje
            case 'c++':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return mensaje
            case 'c#':
                mensaje = f'Hola {cls.message_class.author.mention} si estas interesado en aprender **{data.upper()}** te recomiendo visitar los siguientes enlaces: '
                return mensaje
            case 'programar':
                mensaje = f"Hola {cls.message_class.author.mention} si estas interesado en iniciar en la programación lo principal es iniciar con las bases, te recomiendo buscar información sobre algoritmos, lógica de programación, pseudocodigos, y elegir un lenguaje puedes iniciar por algo sencillo, como html y css para tener una idea, y saltar a Java Script, u algún lenguaje como C/C++ o Python para empezar, adicionalmente te paso estos links donde puedes iniciar tu busqueda: "
                return (mensaje, links_int['programacion'])
            case _:
                return "None"
