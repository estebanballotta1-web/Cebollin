import pygame
import random
import math
import sys
import json

reloj_cursor = 0
mostrar_cursor = True
rango = "Usuario"
respuesta = 0

pygame.init()
#icono = pygame.image.load("assetscartas/icono.png").convert_alpha()
#pygame.display.set_icon(icono)

# =========================================================
# CONFIGURACIÓN
# =========================================================

ANCHO = 1280
ALTO = 720

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cebollins")

reloj = pygame.time.Clock()

FPS = 60

# =========================================================
# COLORES
# =========================================================

NEGRO = (15, 12, 20)
NEGRO2 = (25, 18, 30)

BLANCO = (245, 245, 245)
GRIS = (150, 150, 160)

VERDE = (0, 255, 0)
VERDE2 = (28, 120, 70)

DORADO = (220, 170, 55)
DORADO_CLARO = (255, 210, 100)

ROJO = (255, 0, 0)
ROJO_OSCURO = (100, 25, 30)

AZUL = (50, 100, 180)

# =========================================================
# FUENTES
# =========================================================

fuente_titulo = pygame.font.Font(None, 80)
fuente_grande = pygame.font.Font(None, 60)
fuente = pygame.font.Font(None, 40)
fuente_chica = pygame.font.Font(None, 28)
fuente_mini = pygame.font.Font(None, 22)

# =========================================================
# ESTADOS
# =========================================================

estado = "menu"

admin_usuario = ""
admin_contraseña = ""

activo_admin_usuario = True
mensaje_admin = ""

ADMIN_USUARIO = "Paton"
ADMIN_CONTRASEÑA = "marieletchegaray"

# =========================================================
# MONEDAS
# =========================================================

monedas = 100
apuesta = 5
trofeos = 0

# =========================================================
# PARTIDA
# =========================================================

victorias = 0

carta_ganadora = None
cartas_reveladas = False
carta_elegida = None

mensaje = ""
tiempo_mensaje = 0

# =========================================================
# ANIMACIÓN
# =========================================================

tiempo = 0
imagenes_cartas = [
    pygame.image.load("assetscartas/p.png").convert_alpha(),
    pygame.image.load("assetscartas/speed.png").convert_alpha(),
    pygame.image.load("assetscartas/cuagulo.png").convert_alpha(),
    pygame.image.load("assetscartas/foca.png").convert_alpha(),
    pygame.image.load("assetscartas/ve.png").convert_alpha(),
    pygame.image.load("assetscartas/jesus.png").convert_alpha(),
    pygame.image.load("assetscartas/v.png").convert_alpha()
]

ANCHO_CARTA = 115
ALTO_CARTA = 165

cartas = [
    pygame.Rect(50 + i * 130, 250, ANCHO_CARTA, ALTO_CARTA)
    for i in range(7)
]

imagen_ganadora = pygame.image.load("assetscartas/g.png").convert_alpha()
imagen_ganador = pygame.image.load("assetscartas/g.png").convert_alpha()

cartas_texturas = []
carta_elegida = None
cartas_reveladas = False

# =========================================================
# BURBUJAS
# =========================================================

burbujas = []

for i in range(35):

    burbujas.append({
        "x": random.randint(0, ANCHO),
        "y": random.randint(0, ALTO),
        "radio": random.randint(8, 35),
        "velocidad": random.uniform(0.2, 0.8),
        "fase": random.uniform(0, math.pi * 2)
    })

# =========================================================
# BOTONES
# =========================================================



def cargar_datos():
    try:
        with open("cebolling.json","r") as archivo:
            return json.load(archivo)
    except:
        return {
            "monedas": 0,
            "trofeos": 0,
        }
       
datos = cargar_datos()

monedas = datos["monedas"]
trofeos = datos["trofeos"]
        
def guardar_datos(monedas, trofeos):
    datos_c = {
        "monedas": monedas,
        "trofeos": trofeos
    }

    with open("cebolling.json","w") as archivo:
        json.dump(datos_c,archivo)

def boton(texto, x, y, ancho, alto):

    rect = pygame.Rect(x, y, ancho, alto)

    mouse = pygame.mouse.get_pos()

    encima = rect.collidepoint(mouse)

    if encima:
        color = DORADO_CLARO
        texto_color = NEGRO
    else:
        color = DORADO
        texto_color = NEGRO

    pygame.draw.rect(
        pantalla,
        color,
        rect,
        border_radius=12
    )

    pygame.draw.rect(
        pantalla,
        (120, 80, 25),
        rect,
        3,
        border_radius=12
    )

    texto_render = fuente.render(texto, True, texto_color)

    pantalla.blit(
        texto_render,
        (
            x + (ancho - texto_render.get_width()) // 2,
            y + (alto - texto_render.get_height()) // 2
        )
    )

    return rect

# =========================================================
# FONDO ANIMADO
# =========================================================

def dibujar_fondo():

    pantalla.fill(NEGRO)

    # Degradado aproximado mediante franjas
    for y in range(0, ALTO, 20):

        factor = y / ALTO

        color = (
            int(15 + factor * 10),
            int(12 + factor * 8),
            int(20 + factor * 15)
        )

        pygame.draw.rect(
            pantalla,
            color,
            (0, y, ANCHO, 20)
        )

    # Burbujas

    for burbuja in burbujas:

        burbuja["y"] -= burbuja["velocidad"]

        burbuja["x"] += math.sin(
            tiempo * 0.02 + burbuja["fase"]
        ) * 0.25

        if burbuja["y"] < -burbuja["radio"]:

            burbuja["y"] = ALTO + burbuja["radio"]

            burbuja["x"] = random.randint(
                0,
                ANCHO
            )

        pygame.draw.circle(
            pantalla,
            (45, 35, 55),
            (
                int(burbuja["x"]),
                int(burbuja["y"])
            ),
            burbuja["radio"]
        )

        pygame.draw.circle(
            pantalla,
            (75, 60, 85),
            (
                int(burbuja["x"]),
                int(burbuja["y"])
            ),
            burbuja["radio"],
            2
        )

# =========================================================
# MONEDAS
# =========================================================

def dibujar_monedas():
    global monedas, trofeos

    ancho = 250
    alto = 60

    x = ANCHO - ancho - 20
    y = 20

    trofeo_img=pygame.image.load("assetscartas/trofeos.png").convert_alpha()
    trofeo_img=pygame.transform.scale(trofeo_img,(35,35))

    pygame.draw.rect(pantalla, (30, 25, 35), (x, y, ancho, alto), border_radius=15)
    pygame.draw.rect(pantalla, DORADO, (x, y, ancho, alto), 2, border_radius=15)

    # Monedas
    pygame.draw.circle(pantalla, DORADO, (x + 30, y + 30), 14)
    texto_monedas = fuente.render(str(monedas), True, BLANCO)
    pantalla.blit(texto_monedas, (x + 50, y + 17))

    # Trofeos
    pantalla.blit(trofeo_img, (x + 125, y + 15))
    texto_trofeos = fuente.render(str(trofeos), True, BLANCO)
    pantalla.blit(texto_trofeos, (x + 165, y + 17))
# =========================================================
# CRUPIER
# =========================================================

def dibujar_crupier2():

    if not hasattr(dibujar_crupier,"frames"):

        dibujar_crupier.frames = []

        for i in range(9):

            imagen = pygame.image.load(
                f"assetscartas/frame_{i:02}.png"
            ).convert_alpha()

            # TODOS los frames exactamente 350x350
            imagen = pygame.transform.scale(
                imagen,
                (350,350)
            )

            dibujar_crupier.frames.append(imagen)

        dibujar_crupier.frame = 0
        dibujar_crupier.tiempo = 0

    dibujar_crupier.tiempo += 1

    if dibujar_crupier.tiempo >= 20:

        dibujar_crupier.tiempo = 0

        dibujar_crupier.frame += 1

        if dibujar_crupier.frame >= 9:
            dibujar_crupier.frame = 0

    imagen = dibujar_crupier.frames[dibujar_crupier.frame]

    x = ANCHO // 2 - 175
    y = 180

    pantalla.blit(imagen,(x,y))

def dibujar_crupier():

    if not hasattr(dibujar_crupier,"imagen"):

        dibujar_crupier.imagen = pygame.image.load(
            "assetscartas/cebolla.png"
        ).convert_alpha()

        dibujar_crupier.imagen = pygame.transform.scale(
            dibujar_crupier.imagen,
            (350,350)
        )

    imagen = dibujar_crupier.imagen

    x = ANCHO // 2 - imagen.get_width() // 2
    y = 180

    pantalla.blit(imagen,(x,y))

# =========================================================
# CARTAS
# =========================================================
baraja = list(range(52))
cartas = random.sample(baraja, 7)
carta_ganadora = random.choice(cartas)
cartas_valores = random.sample(baraja, 7)
carta_ganadora = random.choice(cartas_valores)

def obtener_rect_cartas():

    cartas = []

    ancho = 115
    alto = 165
    separacion = 18

    total = (
        ancho * 7 +
        separacion * 6
    )

    inicio_x = (
        ANCHO - total
    ) // 2

    y = 500

    for i in range(7):

        x = inicio_x + i * (
            ancho + separacion
        )

        cartas.append(
            pygame.Rect(
                x,
                y,
                ancho,
                alto
            )
        )

    return cartas


def dibujar_carta(rect, imagen, revelada):

    pygame.draw.rect(
        pantalla,
        (10, 8, 12),
        (rect.x + 5, rect.y + 7, rect.width, rect.height),
        border_radius=10
    )

    if revelada:

        if imagen == imagen_ganador:
            color = DORADO_CLARO
        else:
            color = (180, 180, 185)

        pygame.draw.rect(
            pantalla,
            color,
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            pantalla,
            NEGRO,
            rect,
            3,
            border_radius=10
        )

        mascara = imagen.get_bounding_rect()

        if mascara.width > 0 and mascara.height > 0:
            imagen = imagen.subsurface(mascara).copy()

        margen = 2

        ancho_max = rect.width - margen * 2
        alto_max = rect.height - margen * 2

        escala = min(
            ancho_max / imagen.get_width(),
            alto_max / imagen.get_height()
        )

        nuevo_ancho = max(
            1,
            int(imagen.get_width() * escala)
        )

        nuevo_alto = max(
            1,
            int(imagen.get_height() * escala)
        )

        imagen = pygame.transform.smoothscale(
            imagen,
            (nuevo_ancho, nuevo_alto)
        )

        pantalla.blit(
            imagen,
            (
                rect.centerx - imagen.get_width() // 2,
                rect.centery - imagen.get_height() // 2
            )
        )

    else:

        pygame.draw.rect(
            pantalla,
            (45, 55, 85),
            rect,
            border_radius=10
        )

        pygame.draw.rect(
            pantalla,
            DORADO,
            rect,
            3,
            border_radius=10
        )

        pygame.draw.rect(
            pantalla,
            (65, 75, 110),
            (
                rect.x + 10,
                rect.y + 10,
                rect.width - 20,
                rect.height - 20
            ),
            2,
            border_radius=7
        )

        render = fuente_grande.render(
            "?",
            True,
            BLANCO
        )

        pantalla.blit(
            render,
            (
                rect.centerx - render.get_width() // 2,
                rect.centery - render.get_height() // 2
            )
        )
    
###########################################################
def dibujar_admin_login():
    global reloj_cursor, mostrar_cursor

    reloj_cursor += 1

    if reloj_cursor >= 30:

        mostrar_cursor = not mostrar_cursor
        reloj_cursor = 0

    pantalla.fill(NEGRO)

    titulo = fuente_titulo.render("ADMIN CHECK",True,DORADO_CLARO)

    pantalla.blit(titulo,(ANCHO // 2 - titulo.get_width() // 2,100))

    pantalla.blit(fuente.render("Usuario:", True, BLANCO),(400, 210))

    pantalla.blit(fuente.render("Contraseña:", True, BLANCO),(400, 350))

    caja_usuario = pygame.Rect(
        400,
        250,
        480,
        60
    )

    caja_contra = pygame.Rect(
        400,
        390,
        480,
        60
    )

    color_usuario = DORADO_CLARO if activo_admin_usuario else BLANCO
    color_contra = BLANCO if activo_admin_usuario else DORADO_CLARO

    pygame.draw.rect(
        pantalla,
        color_usuario,
        caja_usuario,
        3,
        border_radius=8
    )

    pygame.draw.rect(
        pantalla,
        color_contra,
        caja_contra,
        3,
        border_radius=8
    )

    pantalla.blit(
        fuente.render(
            admin_usuario,
            True,
            BLANCO
        ),
        (420, 263)
    )

    pantalla.blit(
        fuente.render(
            "*" * len(admin_contraseña),
            True,
            BLANCO
        ),
        (420, 403)
    )

    if mensaje_admin:

        pantalla.blit(
            fuente_chica.render(
                mensaje_admin,
                True,
                ROJO
            ),
            (
                400,
                475
            )
        )

    # CURSOR DE ESCRITURA

    if mostrar_cursor:

        if activo_admin_usuario:

            x = 420 + fuente.render(admin_usuario,True,BLANCO).get_width()

            pygame.draw.line(pantalla,BLANCO,(x, 263),(x, 300),3)

        else:

            x = 420 + fuente.render("*" * len(admin_contraseña),True,BLANCO).get_width()

            pygame.draw.line(pantalla,BLANCO,(x, 403),(x, 440),3)

    boton_ingresar = boton(
        "INGRESAR",
        400,
        530,
        220,
        60
    )

    boton_volver = boton(
        "VOLVER",
        660,
        530,
        220,
        60
    )

    return (
        caja_usuario,
        caja_contra,
        boton_ingresar,
        boton_volver
    )


###########################################################


# =========================================================
# NUEVA RONDA
# =========================================================

def nueva_ronda():

    global carta_elegida
    global cartas_reveladas
    global mensaje
    global cartas_texturas

    cartas_texturas = []

    # 6 cartas normales aleatorias
    for i in range(7):

        cartas_texturas.append(
            random.choice(imagenes_cartas)
        )

    # g.png se coloca en una posición aleatoria
    posicion_ganadora = random.randint(0, 6)

    cartas_texturas[posicion_ganadora] = imagen_ganador

    carta_elegida = None
    cartas_reveladas = False
    mensaje = ""
    
# =========================================================
# INICIAR JUEGO
# =========================================================

def iniciar_juego():

    global estado
    global victorias

    victorias = 0

    nueva_ronda()

    estado = "juego"

# =========================================================
# PANTALLA MENU
# =========================================================
titulo_y = -100

def dibujar_menu():
    global rango, titulo_y

    dibujar_fondo()

    # Título

    #titulo = fuente_titulo.render("no que que poner",True,DORADO_CLARO)
    #pantalla.blit(titulo,(ANCHO // 2 -titulo.get_width() // 2,100))
    
    titulo = fuente_titulo.render("Encuentra a Cebollin",True,DORADO_CLARO)

    titulo_y += (100 - titulo_y) * 0.10

    titulo_y_animado = titulo_y + math.sin(tiempo * 0.04) * 3

    pantalla.blit(titulo,(ANCHO // 2 - titulo.get_width() // 2,titulo_y_animado))

    subtitulo = fuente.render(
        "Made By PG. Versión 1",
        True,
        GRIS
    )
    
    if activo_admin_usuario:
        rango_int2 = fuente.render(rango, True, VERDE)      
    else:
        rango = "Administrador"
        rango_int2 = fuente.render(rango, True, ROJO)

    rango_int = fuente.render("Accediste como: ", True, BLANCO)
    
    pantalla.blit(rango_int, (10, 10))
    pantalla.blit(rango_int2, (235, 11))
    pantalla.blit(subtitulo,(ANCHO // 2 - subtitulo.get_width() // 2,180))

    # Botones

    boton_jugar = boton(
        "JUGAR",
        ANCHO // 2 - 150,
        280,
        300,
        70
    )

    boton_opciones = boton(
        "OPCIONES",
        ANCHO // 2 - 150,
        375,
        300,
        70
    )

    boton_salir = boton(
        "SALIR",
        ANCHO // 2 - 150,
        470,
        300,
        70
    )

    # Monedas

    dibujar_monedas()
    
    boton_admin = boton("SOY ADMIN",20,50,170,50)

    return (
        boton_jugar,
        boton_opciones,
        boton_salir,
        boton_admin
    )

# =========================================================
# PANTALLA OPCIONES
# =========================================================

def dibujar_opciones():

    dibujar_fondo()

    titulo = fuente_titulo.render(
        "OPCIONES",
        True,
        DORADO_CLARO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 -
            titulo.get_width() // 2,
            100
        )
    )

    mantenimiento = fuente_grande.render(
        "EN MANTENIMIENTO",
        True,
        ROJO
    )

    pantalla.blit(
        mantenimiento,
        (
            ANCHO // 2 -
            mantenimiento.get_width() // 2,
            280
        )
    )

    texto = fuente.render(
        "Esta sección estará disponible próximamente.",
        True,
        GRIS
    )

    pantalla.blit(
        texto,
        (
            ANCHO // 2 -
            texto.get_width() // 2,
            350
        )
    )

    boton_volver = boton(
        "VOLVER",
        ANCHO // 2 - 150,
        470,
        300,
        70
    )

    return boton_volver

# =========================================================
# PANTALLA JUEGO
# =========================================================

def dibujar_juego():

    # Mesa
    pantalla.fill(
        (12, 35, 28)
    )

    # Borde superior
    pygame.draw.rect(
        pantalla,
        (20, 70, 45),
        (
            0,
            0,
            ANCHO,
            ALTO
        ),
        20
    )

    # Línea decorativa
    pygame.draw.line(
        pantalla,
        DORADO,
        (0, 470),
        (ANCHO, 470),
        3
    )

    # Crupier
    dibujar_crupier()

    # Monedas
    dibujar_monedas()

    # Contador
    texto_victorias = fuente.render(
        f"VICTORIAS: {victorias}/3",
        True,
        DORADO_CLARO
    )

    pantalla.blit(
        texto_victorias,
        (
            25,
            25
        )
    )

    # Apuesta
    texto_apuesta = fuente_chica.render(
        f"Apuesta: {apuesta} monedas",
        True,
        BLANCO
    )

    pantalla.blit(
        texto_apuesta,
        (
            25,
            65
        )
    )

    # Mensaje
    if mensaje:

        mensaje_render = fuente.render(
            mensaje,
            True,
            DORADO_CLARO
        )

        pantalla.blit(
            mensaje_render,
            (
                ANCHO // 2 -
                mensaje_render.get_width() // 2,
                440
            )
        )

    # Cartas
    cartas = obtener_rect_cartas()

    for i, rect in enumerate(cartas):

        revelada = (
            cartas_reveladas
            and
            i == carta_elegida
        )

        dibujar_carta(
            rect,
            cartas_texturas[i],
            revelada
        )

    return cartas
# =========================================================
# PANTALLA DERROTA
# =========================================================

def dibujar_derrota():

    dibujar_fondo()

    titulo = fuente_titulo.render(
        "PERDISTE",
        True,
        ROJO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 -
            titulo.get_width() // 2,
            150
        )
    )

    texto = fuente.render(
        "No has encontrado a cebollin.",
        True,
        BLANCO
    )

    pantalla.blit(
        texto,
        (
            ANCHO // 2 -
            texto.get_width() // 2,
            260
        )
    )

    boton_reintentar = boton(
        "INTENTAR DE NUEVO",
        ANCHO // 2 - 180,
        370,
        360,
        70
    )

    boton_menu = boton(
        "MENU",
        ANCHO // 2 - 180,
        460,
        360,
        70
    )

    return boton_reintentar, boton_menu

# =========================================================
# PANTALLA VICTORIA
# =========================================================

def dibujar_victoria():
    global monedas, trofeos

    dibujar_fondo()

    titulo = fuente_titulo.render(
        "¡GANASTE!",
        True,
        DORADO_CLARO
    )

    pantalla.blit(
        titulo,
        (
            ANCHO // 2 -
            titulo.get_width() // 2,
            120
        )
    )

    texto = fuente_grande.render(
        "7 VICTORIAS",
        True,
        DORADO
    )

    pantalla.blit(
        texto,
        (
            ANCHO // 2 -
            texto.get_width() // 2,
            230
        )
    )

    texto2 = fuente.render(
        "El crupier no puede creerlo...",
        True,
        BLANCO
    )

    pantalla.blit(
        texto2,
        (
            ANCHO // 2 -
            texto2.get_width() // 2,
            310
        )
    )

    boton_jugar = boton(
        "JUGAR DE NUEVO",
        ANCHO // 2 - 180,
        420,
        360,
        70
    )

    boton_menu = boton(
        "MENU",
        ANCHO // 2 - 180,
        510,
        360,
        70
    )

    return boton_jugar, boton_menu

# =========================================================
# BUCLE PRINCIPAL
# =========================================================

ejecutando = True

while ejecutando:

    reloj.tick(FPS)

    tiempo += 1

    # =================================================
    # PROCESAR EVENTOS
    # =================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            ejecutando = False

        # =================================================
        # MENU
        # =================================================

        if estado == "menu":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                botones = dibujar_menu()

                boton_jugar = botones[0]
                boton_opciones = botones[1]
                boton_salir = botones[2]
                boton_admin = botones[3]

                if boton_jugar.collidepoint(evento.pos):

                    iniciar_juego()

                elif boton_opciones.collidepoint(evento.pos):

                    estado = "opciones"

                elif boton_salir.collidepoint(evento.pos):

                    ejecutando = False

                elif boton_admin.collidepoint(evento.pos):

                    estado = "admin_login"

        # =================================================
        # OPCIONES
        # =================================================

        elif estado == "opciones":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                boton_volver = dibujar_opciones()

                if boton_volver.collidepoint(evento.pos):

                    estado = "menu"

        # =================================================
        # JUEGO
        # =================================================

        elif estado == "juego":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                cartas = obtener_rect_cartas()

                if not cartas_reveladas:

                    for i, rect in enumerate(cartas):

                        if rect.collidepoint(evento.pos):

                            carta_elegida = i
                            cartas_reveladas = True

                            if cartas_texturas[i] == imagen_ganador:

                                monedas += apuesta
                                victorias += 1

                                guardar_datos(monedas, trofeos)

                                mensaje = "¡ACERTASTE!"

                                if victorias >= 3:

                                    trofeos += 1
                                    victorias = 0

                                    guardar_datos(monedas, trofeos)

                            else:

                                monedas -= apuesta

                                guardar_datos(monedas, trofeos)

                                mensaje = "¡FALLASTE!"

                            break

                else:

                    if cartas_texturas[carta_elegida] == imagen_ganador:

                        nueva_ronda()

                    else:

                        estado = "derrota"                      
        # =================================================
        # LOGIN ADMIN
        # =================================================

        elif estado == "admin_login":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                caja_usuario = pygame.Rect(400,250,480,60)

                caja_contra = pygame.Rect(400,390,480,60)

                if caja_usuario.collidepoint(evento.pos):

                    activo_admin_usuario = True

                    pygame.key.start_text_input()

                elif caja_contra.collidepoint(evento.pos):

                    activo_admin_usuario = False

                    pygame.key.start_text_input()

                else:

                    botones = dibujar_admin_login()

                    boton_ingresar = botones[2]
                    boton_volver = botones[3]

                    if boton_ingresar.collidepoint(evento.pos):

                        if (
                            admin_usuario == ADMIN_USUARIO
                            and
                            admin_contraseña == ADMIN_CONTRASEÑA
                        ):

                            pygame.key.stop_text_input()

                            soy_admin = True

                            estado = "menu"
                            monedas = 9999
                            mensaje_admin = ""

                        else:

                            mensaje_admin = "Error 401"

                    elif boton_volver.collidepoint(evento.pos):

                        pygame.key.stop_text_input()

                        admin_usuario = ""
                        admin_contraseña = ""
                        mensaje_admin = ""
                        activo_admin_usuario = True

                        estado = "menu"

            elif evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_BACKSPACE:

                    if activo_admin_usuario:

                        admin_usuario = admin_usuario[:-1]

                    else:

                        admin_contraseña = admin_contraseña[:-1]

                elif evento.key == pygame.K_TAB:

                    activo_admin_usuario = not activo_admin_usuario

            elif evento.type == pygame.TEXTINPUT:

                if activo_admin_usuario:

                    admin_usuario += evento.text

                else:

                    admin_contraseña += evento.text

                mensaje_admin = ""

        # =================================================
        # DERROTA
        # =================================================

        elif estado == "derrota":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                botones = dibujar_derrota()

                boton_reintentar = botones[0]
                boton_menu = botones[1]

                if boton_reintentar.collidepoint(evento.pos):

                    iniciar_juego()

                elif boton_menu.collidepoint(evento.pos):

                    estado = "menu"

        # =================================================
        # VICTORIA
        # =================================================

        elif estado == "victoria":

            if evento.type == pygame.MOUSEBUTTONDOWN:

                botones = dibujar_victoria()

                boton_jugar = botones[0]
                boton_menu = botones[1]

                if boton_jugar.collidepoint(evento.pos):

                    iniciar_juego()

                elif boton_menu.collidepoint(evento.pos):

                    estado = "menu"

    # =====================================================
    # DIBUJAR ESTADO ACTUAL
    # =====================================================

    if monedas > 9999: 
        monedas = 9999
    if monedas < 0:
        monedas = 0
    if trofeos > 9999:
            trofeos = 9999
        
    if estado == "menu":
            
        dibujar_menu()

    elif estado == "opciones":

        dibujar_opciones()

    elif estado == "juego":

        dibujar_juego()

    elif estado == "admin_login":
            
        dibujar_admin_login()

    elif estado == "derrota":

        dibujar_derrota()

    elif estado == "victoria":

        dibujar_victoria()

    pygame.display.flip()

pygame.quit()
sys.exit()