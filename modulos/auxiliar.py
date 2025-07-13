import pygame as pg
import json
import os
import modulos.variables as var
import forms.form_base as base
import modulos.cartas as cart
import csv
import forms.form_jugar as jugar

def mostrar_texto(surface: pg.Surface, texto: str, font_size: int, color, x: int, y: int):
    """Muestra texto simple en pantalla usando una fuente estándar."""
    font = pg.font.SysFont(None, font_size)
    texto_render = font.render(texto, True, color)
    surface.blit(texto_render, (x, y))

def cargar_ranking():
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
        ranking.sort(key=lambda x: x[1], reverse=True)
    return ranking[:10]

def guardar_ranking(jugador_dict: dict):
    with open(var.RUTA_RANKING_CSV, 'a', encoding='utf-8') as file:
        data = f'{jugador_dict.get("nombre")},{jugador_dict.get("puntaje_actual")}\n'
        file.write(data)

def crear_cuadro(dimensiones: tuple, coordenadas: tuple, color: tuple) -> dict:
    cuadro = {}
    cuadro['superficie'] = pg.Surface(dimensiones)
    cuadro['rectangulo'] = cuadro['superficie'].get_rect()
    cuadro['rectangulo'].topleft = coordenadas
    cuadro['superficie'].fill(pg.Color(color))
    return cuadro

def pausar_y_cambiar(form):
    """
    Pausa el juego y cambia al formulario de pausa.
    """
    form['estado']['pausado'] = True
    base.set_active("form_pausa")


def volver_al_juego(form_jugar):
    """
    Reanuda el juego y vuelve al formulario de jugar.
    """
    form_jugar['estado']['pausado'] = False
    form_jugar['estado']['clock'].tick(60)  # Reinicia el contador de tiempo acumulado
    base.set_active("form_jugar")

def ruta_fin_juego(estado, form_manager):
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

def verificar_fin_de_juego(form, form_manager):
    estado = form['estado']

    if estado['time'] <= 0:
        estado['mensaje'] = "¡Se acabó el tiempo!"
        ruta_fin_juego(estado, form_manager)
        return

    if not estado['mazo_jugador'] or not estado['mazo_enemigo']:
        estado['mensaje'] = "¡Se acabaron las cartas!"
        ruta_fin_juego(estado, form_manager)
        return

    if estado['stats_jugador']['hp'] <= 0:
        estado['mensaje'] = "¡PERDISTE!"
        for f in form_manager['form_list']:
            if f['name'] == 'form_derrota':
                f['estado']['score'] = estado['score']
                return base.set_active("form_derrota")
    elif estado['stats_enemigo']['hp'] <= 0:
        estado['mensaje'] = "¡GANASTE!"
        for f in form_manager['form_list']:
            if f['name'] == 'form_victoria':
                f['estado']['score'] = estado['score']
                return base.set_active("form_victoria")

def guardar_puntaje(nombre: str, puntaje: int, ruta="archivos/ranking.csv"):
    """
    Guarda el nombre y puntaje en el archivo de ranking sin try.
    """
    if nombre.strip() == "":
        print("[ERROR] Nombre vacío. No se guardó el puntaje.")
        return

    with open(ruta, "a", newline="") as archivo:
        writer = csv.writer(archivo)
        writer.writerow([nombre.strip(), puntaje])
        print(f"[INFO] Puntaje guardado: {nombre.strip()} - {puntaje}")


def reiniciar_form_jugar(form_manager, pantalla):
    configs = cart.cargar_cartas("archivos/config.json")

    mazo_j = configs
    mazo_e = configs

    nuevo_form_jugar = jugar.init_form_jugar({
        "screen": pantalla,
        "screen_dimentions": var.DIMENSION_PANTALLA,
        "name": "form_jugar",
        "active": True,  # 🔴 MARCAR COMO ACTIVO
        "background_path": var.RUTA_FONDO_JUEGO,
        "music_path": var.RUTA_MUSICA_JUGAR,
        "coords": (0, 0),
        "mazo_jugador": mazo_j,
        "mazo_enemigo": mazo_e,
        "level_num": None  # o lo que uses en los demás formularios
    })

    # Reemplazamos en la lista de formularios
    for i, form in enumerate(form_manager['form_list']):
        if form['name'] == "form_jugar":
            form_manager['form_list'][i] = nuevo_form_jugar
        else:
            form_manager['form_list'][i]['active'] = False

    # También activamos la música directamente si existe la ruta
    if nuevo_form_jugar.get("music_path"):
        base.stop_music()
        base.play_music(nuevo_form_jugar)



