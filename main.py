from fastapi import FastAPI
import secrets

app = FastAPI()

# =========================
# DATOS
# =========================

usuarios = {}
sesiones = {}
mensajes_chat = []


# =========================
# INICIO
# =========================

@app.get("/")
def inicio():
    return {
        "ok": True,
        "mensaje": "Servidor de Cebollins funcionando"
    }


# =========================
# REGISTRO
# =========================

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


# =========================
# LOGIN
# =========================

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


# =========================
# COMPROBAR SESIÓN
# =========================

@app.post("/comprobar_sesion")
def comprobar_sesion(data: dict):

    token = str(data.get("token", ""))

    if not token:
        return {
            "ok": False,
            "mensaje": "Token faltante"
        }

    if token not in sesiones:
        return {
            "ok": False,
            "mensaje": "Sesión inválida"
        }

    usuario = sesiones[token]

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }

    return {
        "ok": True,
        "usuario": usuario
    }


# =========================
# CERRAR SESIÓN
# =========================

@app.post("/cerrar_sesion")
def cerrar_sesion(data: dict):

    token = str(data.get("token", ""))

    if token in sesiones:
        del sesiones[token]

    return {
        "ok": True
    }


# =========================
# OBTENER USUARIO
# =========================

@app.get("/usuario/{usuario}")
def obtener_usuario(usuario: str):

    usuario = usuario.strip()

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }

    datos = usuarios[usuario]

    return {
        "ok": True,
        "usuario": datos["usuario"],
        "monedas": datos["monedas"],
        "trofeos": datos["trofeos"]
    }


# =========================
# ACTUALIZAR DATOS
# =========================

@app.post("/usuario/{usuario}/datos")
def actualizar_datos(usuario: str, data: dict):

    usuario = usuario.strip()

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }

    if "monedas" in data:
        try:
            monedas = int(data["monedas"])

            if monedas < 0:
                monedas = 0

            usuarios[usuario]["monedas"] = monedas

        except (ValueError, TypeError):
            return {
                "ok": False,
                "mensaje": "Monedas inválidas"
            }

    if "trofeos" in data:
        try:
            trofeos = int(data["trofeos"])

            if trofeos < 0:
                trofeos = 0

            usuarios[usuario]["trofeos"] = trofeos

        except (ValueError, TypeError):
            return {
                "ok": False,
                "mensaje": "Trofeos inválidos"
            }

    return {
        "ok": True,
        "usuario": usuario,
        "monedas": usuarios[usuario]["monedas"],
        "trofeos": usuarios[usuario]["trofeos"]
    }


# =========================
# ACTUALIZAR MONEDAS
# =========================

@app.post("/usuario/{usuario}/monedas")
def actualizar_monedas(usuario: str, data: dict):

    usuario = usuario.strip()

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }

    try:
        monedas = int(data.get("monedas"))

    except (ValueError, TypeError):
        return {
            "ok": False,
            "mensaje": "Monedas inválidas"
        }

    if monedas < 0:
        monedas = 0

    usuarios[usuario]["monedas"] = monedas

    return {
        "ok": True,
        "monedas": monedas
    }


# =========================
# ACTUALIZAR TROFEOS
# =========================

@app.post("/usuario/{usuario}/trofeos")
def actualizar_trofeos(usuario: str, data: dict):

    usuario = usuario.strip()

    if usuario not in usuarios:
        return {
            "ok": False,
            "mensaje": "Usuario no encontrado"
        }

    try:
        trofeos = int(data.get("trofeos"))

    except (ValueError, TypeError):
        return {
            "ok": False,
            "mensaje": "Trofeos inválidos"
        }

    if trofeos < 0:
        trofeos = 0

    usuarios[usuario]["trofeos"] = trofeos

    return {
        "ok": True,
        "trofeos": trofeos
    }


# =========================
# RANKING
# =========================

@app.get("/ranking")
def ranking():

    lista = []

    for datos in usuarios.values():

        lista.append({
            "usuario": datos["usuario"],
            "monedas": datos["monedas"],
            "trofeos": datos["trofeos"]
        })

    lista.sort(
        key=lambda jugador: jugador["trofeos"],
        reverse=True
    )

    return {
        "ok": True,
        "ranking": lista
    }


# =========================
# CHAT - ENVIAR
# =========================

@app.post("/chat/enviar")
def enviar_mensaje(data: dict):

    usuario = str(data.get("usuario", "")).strip()
    mensaje = str(data.get("mensaje", "")).strip()

    if not usuario:
        return {
            "ok": False,
            "mensaje": "Usuario faltante"
        }

    if not mensaje:
        return {
            "ok": False,
            "mensaje": "Mensaje vacío"
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


# =========================
# CHAT - OBTENER
# =========================

@app.get("/chat/mensajes")
def obtener_mensajes():

    return {
        "ok": True,
        "mensajes": mensajes_chat
    }