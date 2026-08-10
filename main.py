from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def inicio():
    return {
        "mensaje": "Servidor de Cebollins funcionando"
    }


@app.get("/ranking")
def ranking():
    return {
        "ranking": [
            {
                "usuario": "Jugador1",
                "puntos": 1500
            },
            {
                "usuario": "Jugador2",
                "puntos": 1200
            }
        ]
    }


mensajes_chat = []


@app.post("/chat/enviar")
def enviar_mensaje(data: dict):

    usuario = data.get("usuario", "").strip()
    mensaje = data.get("mensaje", "").strip()

    if not usuario or not mensaje:
        return {
            "ok": False,
            "mensaje": "Datos incompletos"
        }

    if len(mensaje) > 150:
        return {
            "ok": False,
            "mensaje": "Mensaje demasiado largo"
        }

    mensajes_chat.append({
        "usuario": usuario,
        "mensaje": mensaje
    })

    if len(mensajes_chat) > 50:
        mensajes_chat.pop(0)

    return {
        "ok": True
    }


@app.get("/chat/mensajes")
def obtener_mensajes():

    return {
        "ok": True,
        "mensajes": mensajes_chat
    }