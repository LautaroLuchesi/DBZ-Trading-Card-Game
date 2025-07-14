import pygame as pg
import os
import modulos.variables as var
import forms.form_base as base
import modulos.cartas as cart
import csv
import forms.form_jugar as jugar

def mostrar_texto(surface: pg.Surface, texto: str, font_size: int, color, x: int, y: int) -> None:
    '''
    Muestra texto en pantalla usando una fuente predeterminada.

    Args:
        surface (pg.Surface): Superficie donde se mostrará el texto.
        texto (str): Cadena de texto a mostrar.
        font_size (int): Tamaño de la fuente.
        color: Color del texto (puede ser una tupla RGB o pg.Color).
        x (int): Posición horizontal.
        y (int): Posición vertical.

    Return:
        None
    '''
    font = pg.font.SysFont(None, font_size)
    texto_render = font.render(texto, True, color)
    surface.blit(texto_render, (x, y))

def cargar_ranking() -> list[tuple[str, int]]:
    '''
    Carga y ordena el ranking desde un archivo CSV.

    Return:
        list[tuple[str, int]]: Lista de tuplas con nombre y puntaje ordenados de mayor a menor.
    '''
    ranking = []
    if os.path.exists(var.RUTA_RANKING_CSV):
        with open(var.RUTA_RANKING_CSV, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for fila in reader:
                if len(fila) == 2:
                    nombre = fila[0].strip()
                    puntaje_str = fila[1].strip()
                    if puntaje_str.isdigit():
                        puntaje = int(puntaje_str)
                        ranking.append((nombre, puntaje))

        # Ordenamiento por Selección (mayor a menor)
        n = len(ranking)
        for i in range(n - 1):
            max_idx = i
            for j in range(i + 1, n):
                if ranking[j][1] > ranking[max_idx][1]:
                    max_idx = j
            ranking[i], ranking[max_idx] = ranking[max_idx], ranking[i]

    return ranking[:10]

def guardar_ranking(jugador_dict: dict) -> None:
    '''
    Guarda el nombre y puntaje del jugador en el archivo de ranking.

    Args:
        jugador_dict (dict): Contiene 'nombre' y 'puntaje_actual'.

    Return:
        None
    '''
    with open(var.RUTA_RANKING_CSV, 'a', encoding='utf-8') as file:
        data = f'{jugador_dict.get("nombre")},{jugador_dict.get("puntaje_actual")}\n'
        file.write(data)

def crear_cuadro(dimensiones: tuple, coordenadas: tuple, color: tuple) -> dict:
    '''
    Crea un cuadro coloreado como superficie con rectángulo.

    Args:
        dimensiones (tuple): (ancho, alto) del cuadro.
        coordenadas (tuple): Posición (x, y) de la esquina superior izquierda.
        color (tuple): Color en formato RGB.

    Return:
        dict: Contiene 'superficie' y 'rectangulo'.
    '''
    cuadro = {}
    cuadro['superficie'] = pg.Surface(dimensiones)
    cuadro['rectangulo'] = cuadro['superficie'].get_rect()
    cuadro['rectangulo'].topleft = coordenadas
    cuadro['superficie'].fill(pg.Color(color))
    return cuadro

def pausar_y_cambiar(form: dict) -> None:
    '''
    Pausa el juego y cambia al formulario de pausa.

    Args:
        form (dict): Formulario de juego activo.

    Return:
        None
    '''
    form['estado']['pausado'] = True
    base.set_active("form_pausa")

def volver_al_juego(form_jugar: dict) -> None:
    '''
    Reanuda el juego desde la pausa.

    Args:
        form_jugar (dict): Formulario del juego.

    Return:
        None
    '''
    estado = form_jugar['estado']
    estado['pausado'] = False
    estado['clock'].tick(60)
    base.set_active("form_jugar")

def ruta_fin_juego(estado: dict, form_manager: dict) -> None:
    '''
    Determina si se ganó o perdió la partida y redirige al form correspondiente.

    Args:
        estado (dict): Estado actual del juego.
        form_manager (dict): Contenedor de formularios.

    Return:
        None
    '''
    score = estado['score']
    if estado['stats_jugador']['hp'] > estado['stats_enemigo']['hp']:
        for f in form_manager['form_list']:
            if f['name'] == 'form_victoria':
                f['estado']['score'] = score
                return base.set_active("form_victoria")
    else:
        for f in form_manager['form_list']:
            if f['name'] == 'form_derrota':
                f['estado']['score'] = score
                return base.set_active("form_derrota")

def verificar_fin_de_juego(form: dict, form_manager: dict) -> None:
    '''
    Verifica si el juego debe finalizar por tiempo, vida o cartas agotadas.

    Args:
        form (dict): Formulario actual del juego.
        form_manager (dict): Contenedor de formularios.

    Return:
        None
    '''
    estado = form['estado']

    if estado['time'] <= 0 or not estado['mazo_jugador'] or not estado['mazo_enemigo']:
        ruta_fin_juego(estado, form_manager)
        return

    if estado['stats_jugador']['hp'] <= 0 or estado['stats_enemigo']['hp'] <= 0:
        ruta_fin_juego(estado, form_manager)
        return

def guardar_puntaje(nombre: str, puntaje: int, ruta: str = "archivos/ranking.csv") -> None:
    '''
    Guarda un puntaje en el archivo de ranking.

    Args:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje alcanzado.
        ruta (str): Ruta al archivo CSV.

    Return:
        None
    '''
    if nombre.strip() == "":
        return

    with open(ruta, "a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([nombre.strip(), puntaje])

def reiniciar_form_jugar(form_manager: dict, pantalla: pg.Surface) -> None:
    '''
    Reinicia el formulario del juego, reestableciendo cartas y estado.

    Args:
        form_manager (dict): Contenedor de formularios.
        pantalla (pg.Surface): Superficie principal del juego.

    Return:
        None
    '''
    configs = cart.cargar_json("archivos/config.json")
    mazo_j = configs
    mazo_e = configs

    nuevo_form_jugar = jugar.init_form_jugar({
        "screen": pantalla,
        "screen_dimentions": var.DIMENSION_PANTALLA,
        "name": "form_jugar",
        "active": True,
        "background_path": var.RUTA_FONDO_JUEGO,
        "music_path": var.RUTA_MUSICA_JUGAR,
        "coords": (0, 0),
        "mazo_jugador": mazo_j,
        "mazo_enemigo": mazo_e,
        "level_num": None
    })

    for i, form in enumerate(form_manager['form_list']):
        if form['name'] == "form_jugar":
            form_manager['form_list'][i] = nuevo_form_jugar
        else:
            form_manager['form_list'][i]['active'] = False

    if nuevo_form_jugar.get("music_path"):
        base.stop_music()
        base.play_music(nuevo_form_jugar)

def logica_enter_name(form: dict, eventos: list[pg.event.Event]) -> None:
    '''
    Procesa los eventos para escribir un nombre en pantalla.

    Args:
        form (dict): Formulario con campos de entrada.
        eventos (list): Lista de eventos capturados por pygame.

    Return:
        None
    '''
    estado = form['estado']

    for evento in eventos:
        if evento.type == pg.KEYDOWN:
            if evento.key == pg.K_BACKSPACE:
                estado['input_nombre'] = estado['input_nombre'][:-1]
            else:
                if len(estado['input_nombre']) < 12 and evento.unicode.isprintable():
                    estado['input_nombre'] += evento.unicode

    form['lbl_input'].update_text(estado['input_nombre'], var.COLOR_ROJO)
    form['lbl_score'].update_text(f"Score: {estado['score']}", var.COLOR_BLANCO)


def dibujar_ranking(form: dict) -> None:
    '''
    Dibuja el fondo, los puntajes del ranking y los widgets del formulario.

    Args:
        form (dict): Formulario del ranking.

    Return:
        None
    '''
    screen = form['screen']
    screen.blit(form['surface'], (0, 0))

    ranking = cargar_ranking()
    y = 200
    for i, (nombre, puntaje) in enumerate(ranking[:10]):
        texto = f"{i + 1}. {nombre} - {puntaje} pts"
        mostrar_texto(screen, texto, 45, var.COLOR_AMARILLO, 450, y)
        y += 35

    for widget in form['widgets_list']:
        widget.draw()
