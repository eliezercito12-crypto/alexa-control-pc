from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():
    return "Servidor Alexa funcionando"


@app.route("/", methods=["POST"])
def alexa():
    datos = request.get_json(silent=True) or {}

    print("Petición recibida de Alexa:")
    print(datos)

    request_data = datos.get("request", {})
    tipo = request_data.get("type")

    if tipo == "LaunchRequest":
        texto = "Hola. Control PC está conectado."

    elif tipo == "IntentRequest":
        intent = request_data.get("intent", {}).get("name")

        if intent == "AbrirNotasIntent":
            texto = "Recibí la orden de abrir el bloc de notas."

            # Aquí posteriormente enviaremos la orden a tu PC.

        else:
            texto = "No conozco ese comando todavía."

    else:
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

    return jsonify(respuesta)


if __name__ == "__main__":
    import os

    puerto = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=puerto
    )
