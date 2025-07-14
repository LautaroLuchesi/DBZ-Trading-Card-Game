import forms.form_base as base
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import Label, Button
import pygame as pg

def init_form_victoria(dict_form_data: dict, score_obtenido: int) -> dict:

    """
    Inicializa el formulario de victoria al ganar una partida.

    Args:
        dict_form_data (dict): Datos necesarios para inicializar el formulario.
        score_obtenido (int): Puntaje alcanzado por el jugador.

    Return:
        dict: Formulario con todos los elementos visuales y lógicos configurados.
    """

    form = base.create_base_form(dict_form_data)

    form['estado'] = {
        'input_nombre': '',
        'score': score_obtenido,
        'confirmado': False
        }
    
    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 35,
        text = var.TITULO,
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 60,
        color = var.COLOR_ROJO
        )
    form['lbl_victoria'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 160,
        text = "Victory",
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 70,
        color = var.COLOR_CIAN
        )
    form['lbl_score'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 260,
        text = f"Score: {score_obtenido}",
        screen = form['screen'],
        font_path = var.FUENTE_ALAGARD,
        font_size = 40,
        color = var.COLOR_AMARILLO
        )
    form['lbl_nombre'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 315,
        text = "Write your name:",
        screen = form['screen'],
        font_path = var.FUENTE_ALAGARD,
        font_size = 30,
        color = var.COLOR_ROJO
        )
    form['lbl_input'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 375,
        text = "",
        screen = form['screen'],
        font_path = var.FUENTE_ALAGARD,
        font_size = 35,
        color = var.COLOR_BLANCO
        )

    def confirmar_nombre(_=None) -> None:
        """
        Guarda el nombre ingresado y redirige al formulario de ranking.

        Args:
            _ (opcional): Argumento dummy si se llama desde un botón.

        Return:
            None
        """        
        nombre = form['estado']['input_nombre'].strip()
        if nombre:
            aux.guardar_puntaje(nombre, form['estado']['score'])
            base.set_active("form_ranking")

    form['btn_confirmar'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 460,
        text = "CONFIRM NAME",
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 35,
        color = var.COLOR_ROJO,
        on_click = confirmar_nombre
        )

    form['widgets_list'] = [
        form['lbl_titulo'],
        form['lbl_victoria'],
        form['lbl_score'],
        form['lbl_nombre'],
        form['lbl_input'],
        form['btn_confirmar']
        ]

    return form

def update(form: dict, eventos: list[pg.event.Event]) -> None:
    """
    Actualiza los elementos visuales del formulario y gestiona la lógica de ingreso de nombre.

    Args:
        form (dict): Formulario de victoria.
        eventos (list): Lista de eventos de Pygame.

    Return:
        None
    """
    base.update(form)
    aux.logica_enter_name(form, eventos)
def draw(form: dict) -> None:
    """
    Dibuja todos los elementos del formulario de victoria y una línea decorativa debajo del input.

    Args:
        form (dict): Formulario actual.

    Return:
        None
    """
    base.draw(form)
    pg.draw.line(form['screen'], var.COLOR_BLANCO, (400, 440), (880, 440), 2)

