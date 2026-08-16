from fastapi import FastAPI
import secrets

app = FastAPI()

usuarios = {}
sesiones = {}
mensajes_chat = []

@app.get("/")
def inicio():
    return {
        "ok": True,
        "mensaje": "Servidor de Cebollins funcionando"
    }

@app.post("/registro")
def registro(data: dict):

    usuario = str(data.get("usuario", "")).strip()
    password = str(data.get("password", ""))

    if not usuario:
        return {
            "ok": False,
            "mensaje": "Ingresá un usuario"
        }

    if not password:
        return {
            "ok": False,
            "mensaje": "Ingresá una contraseña"
        }

    if len(usuario) < 3:
        return {
            "ok": False,
            "mensaje": "El usuario debe tener al menos 3 caracteres"
        }

    if len(password) < 4:
        return {
            "ok": False,
            "mensaje": "La contraseña debe tener al menos 4 caracteres"
        }

    if len(usuario) > 30:
        return {
            "ok": False,
            "mensaje": "El usuario es demasiado largo"
        }

    if usuario in usuarios:
        return {
            "ok": False,
            "mensaje": "El usuario ya existe"
        }

    usuarios[usuario] = {
        "usuario": usuario,
        "password": password,
        "monedas": 100,
        "trofeos": 0
    }

    return {
        "ok": True,
        "mensaje": "Cuenta creada"
    }

@app.post("/login")
def login(data: dict):

    usuario = str(data.get("usuario", "")).strip()
    password = str(data.get("password", ""))

    if not usuario:
        return {
            "ok": False,
            "mensaje": "Ingresá un usuario"
        }

    if not password:
        return {
            "ok": False,
            "mensaje": "Ingresá una contraseña"
        }

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "El usuario no existe"
        }

    if usuarios[usuario]["password"] != password:
        return {
            "ok": False,
            "mensaje": "Contraseña incorrecta"
        }

    token = secrets.token_hex(32)

    sesiones[token] = usuario

    return {
        "ok": True,
        "usuario": usuario,
        "token": token
    }