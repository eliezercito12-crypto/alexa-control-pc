from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def inicio():
    return "Servidor Alexa funcionando", 200


@app.route("/", methods=["POST"])
def alexa():

    datos = request.get_json(force=True)

    print("========== PETICION DE ALEXA ==========")
    print(datos)
    print("=======================================")

    request_data = datos.get("request", {})
    request_type = request_data.get("type")

    if request_type == "LaunchRequest":
        texto = "Hola. Control PC está conectado."

    elif request_type == "IntentRequest":

        intent_name = request_data.get("intent", {}).get("name")

        if intent_name == "AbrirNotasIntent":
            texto = "Recibí la orden de abrir el bloc de notas."

        else:
            texto = "No conozco ese comando."

    elif request_type == "SessionEndedRequest":
        return "", 200

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

    print("RESPUESTA:")
    print(respuesta)

    return jsonify(respuesta), 200


if __name__ == "__main__":
    import os

    puerto = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=puerto
    )
    app.run(
        host="0.0.0.0",
        port=puerto
    )
