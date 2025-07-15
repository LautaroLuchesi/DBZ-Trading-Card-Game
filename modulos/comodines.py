import modulos.variables as var
import pygame as pg
import forms.form_base as base
from utn_fra.pygame_widgets import Label

def activar_heal(estado: dict):
    """
    Aplica el efecto del comodín HEAL al jugador.

    Esta función:
    - Restaura los stats del jugador a los valores iniciales.
    - Marca que el comodín HEAL ya fue utilizado para evitar usos múltiples.

    Args:
        estado (dict): Diccionario con el estado actual del juego.

    Returns:
        None
    """
    if not estado.get('heal_usado', False):
        estado['stats_jugador'] = estado['stats_iniciales_jugador'].copy()
        estado['heal_usado'] = True

def activar_shield(estado: dict):
    """
    Activa el comodín SHIELD para el jugador.

    Marca el escudo como activo y el comodín como usado. El escudo protegerá al jugador
    una vez, redirigiendo el daño de una derrota al enemigo.

    Args:
        estado (dict): Diccionario que contiene el estado actual del juego, incluyendo
                       si el escudo ya fue usado y si está activo.

    Returns:
        None
    """
    if not estado.get('shield_usado', False):
        estado['shield_activo'] = True
        estado['shield_usado'] = True

def verificar_escudo(estado: dict, perdedor: str):
    """
    Verifica si el escudo está activo y, si el perdedor de la ronda es el jugador,
    invierte el resultado para que el enemigo pierda en su lugar.

    Args:
        estado (dict): Estado actual del juego.
        perdedor (str): Nombre del perdedor de la ronda ('player' o 'enemy').

    Returns:
        str: El nuevo perdedor, considerando si el escudo estaba activo o no.
    """
    if perdedor == 'player' and estado.get('shield_activo', False):
        estado['shield_activo'] = False
        return 'enemy'
    return perdedor

def usar_comodin(form_comodin: dict) -> None:
    """
    Aplica el efecto del comodín seleccionado (heal o shield) al formulario de juego principal.

    Esta función:
    - Obtiene el formulario de juego activo.
    - Reproduce el sonido de activación del comodín.
    - Según el comodín seleccionado, activa el efecto correspondiente (heal o shield).
    - Actualiza el formulario de juego eliminando el botón del comodín usado y mostrando una etiqueta
      que indica que el comodín está activo.
    - Cambia la pantalla activa al formulario principal de juego.

    Args:
        form_comodin (dict): El formulario del comodín desde donde se invoca la función.
                             Puede ser 'form_comodin_heal' o 'form_comodin_shield'.

    Returns:
        None
    """
    form_jugar = base.forms_dict.get('form_jugar')
    if not form_jugar:
        return

    estado_jugar = form_jugar['estado']

    outro = pg.mixer.Sound(var.RUTA_SONIDO_COMODIN_OUTRO)
    outro.play()

    if form_comodin['name'] == 'form_comodin_heal':
        activar_heal(estado_jugar)
        if 'btn_heal' in form_jugar and form_jugar['btn_heal'] in form_jugar['widgets_list']:
            form_jugar['widgets_list'].remove(form_jugar['btn_heal'])

        if 'lbl_heal_active' not in form_jugar:
            screen = estado_jugar['screen']
            form_jugar['lbl_heal_active'] = Label(
                x = 1200,
                y = 207,
                text = "HEAL",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form_jugar['widgets_list'].append(form_jugar['lbl_heal_active'])

    elif form_comodin['name'] == 'form_comodin_shield':
        activar_shield(estado_jugar)
        if 'btn_shield' in form_jugar and form_jugar['btn_shield'] in form_jugar['widgets_list']:
            form_jugar['widgets_list'].remove(form_jugar['btn_shield'])

        if 'lbl_shield_active' not in form_jugar:
            screen = estado_jugar['screen']
            form_jugar['lbl_shield_active'] = Label(
                x = 1200,
                y = 262,
                text = "SHIELD",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form_jugar['widgets_list'].append(form_jugar['lbl_shield_active'])

    base.set_active('form_jugar')

def actualizar_estado_comodines(form: dict):
    """
    Actualiza el estado visual de los comodines en el formulario de juego principal.

    Esta función verifica si los comodines 'heal' o 'shield' ya fueron usados y:
    - Elimina los botones correspondientes si aún están visibles.
    - Añade etiquetas (labels) que indican que el comodín está activo en el juego.

    Args:
        form (dict): Formulario principal del juego que contiene el estado y widgets.

    Returns:
        None
    """
    estado = form['estado']
    screen = estado['screen']

    if estado.get('heal_usado', False):
        if 'btn_heal' in form and form['btn_heal'] in form['widgets_list']:
            form['widgets_list'].remove(form['btn_heal'])
        if 'lbl_heal_active' not in form:
            form['lbl_heal_active'] = Label(
                x = 1200,
                y = 177,
                text = "HEAL",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form['widgets_list'].append(form['lbl_heal_active'])

    if estado.get('shield_usado', False):
        if 'btn_shield' in form and form['btn_shield'] in form['widgets_list']:
            form['widgets_list'].remove(form['btn_shield'])
        if 'lbl_shield_active' not in form:
            form['lbl_shield_active'] = Label(
                x = 1200,
                y = 227,
                text = "SHIELD",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form['widgets_list'].append(form['lbl_shield_active'])





