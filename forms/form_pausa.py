import modulos.auxiliar as aux
import forms.form_base as base
import modulos.variables as var
from utn_fra.pygame_widgets import Label, Button

def init_form_pausa(dict_form_data: dict, form_jugar: dict) -> dict:
    """
    Inicializa el formulario de pausa, mostrando opciones para continuar o volver al menú.

    Args:
        dict_form_data (dict): Diccionario con datos de configuración del formulario.
            - 'screen': superficie donde se dibuja.
        form_jugar (dict): Formulario del juego, al cual se vuelve al reanudar.

    Returns:
        dict: Formulario de pausa con sus widgets configurados.
    """
    
    form = base.create_base_form(dict_form_data)
    screen = dict_form_data['screen']

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 100,
        text = var.TITULO,
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 60,
        color = var.COLOR_ROJO
        )
    form['lbl_pausa'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 180,
        text = 'PAUSE',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 70,
        color = var.COLOR_ROJO
        )
    form['btn_volver'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 350,
        text = "BACK TO GAME",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: aux.volver_al_juego(form_jugar)
        )
    form['btn_menu'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 440,
        text = "BACK TO MENU",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: base.set_active("form_menu")
        )
    form['widgets_list'] = [
        form['lbl_titulo'],
        form['lbl_pausa'],
        form['btn_volver'],
        form['btn_menu']
    ]

    return form

def update(form_data: dict) -> None:
    """
    Actualiza los elementos del formulario de pausa (botones, etiquetas).

    Args:
        form_data (dict): Diccionario del formulario de pausa.

    Returns:
        None
    """
    base.update(form_data)

def draw(form_data: dict) -> None:
    """
    Dibuja el fondo y los elementos del formulario de pausa en pantalla.

    Args:
        form_data (dict): Diccionario del formulario de pausa.

    Returns:
        None
    """
    base.draw(form_data)

