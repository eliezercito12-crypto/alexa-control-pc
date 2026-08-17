from flask import Flask, request, jsonify
import os

app = Flask(__name__)

ultimo_comando = "Ninguno todavía"


@app.route("/", methods=["GET"])
def inicio():
    return f"""
    <html>
        <head>
            <title>Alexa Control PC</title>
        </head>
        <body>
            <h1>Servidor Alexa funcionando</h1>
            <h2>Último comando recibido:</h2>
            <p>{ultimo_comando}</p>
        </body>
    </html>
    """, 200


@app.route("/", methods=["POST"])
def alexa():
    global ultimo_comando

    datos = request.get_json(silent=True)

    print("========== ALEXA ==========")
    print("Petición recibida:", datos)

    if not datos:
        print("ERROR: No llegó JSON")

        respuesta = {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "No recibí los datos correctamente."
                },
                "shouldEndSession": True
            }
        }

        return jsonify(respuesta), 200

    tipo = datos.get("request", {}).get("type")

    print("Tipo:", tipo)

    if tipo == "LaunchRequest":
        ultimo_comando = "LaunchRequest recibido"
        texto = "Hola. Control PC está conectado."

    elif tipo == "IntentRequest":

        intent = datos.get("request", {}).get("intent", {})
        nombre_intent = intent.get("name")

        print("Intent:", nombre_intent)

        ultimo_comando = f"Intent recibido: {nombre_intent}"

        if nombre_intent == "AbrirNotasIntent":
            texto = "Recibí la orden de abrir el bloc de notas."
        else:
            texto = f"Recibí el comando {nombre_intent}."

    elif tipo == "SessionEndedRequest":

        ultimo_comando = "Sesión terminada"
        return "", 200

    else:

        ultimo_comando = f"Tipo recibido: {tipo}"
        texto = "Solicitud recibida."

    respuesta = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": texto
            },
            "shouldEndSession": True
        }
    }

    print("Respuesta enviada:", respuesta)
    print("==========================")

    return jsonify(respuesta), 200


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=puerto)
