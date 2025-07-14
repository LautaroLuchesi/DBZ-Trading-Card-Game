import forms.form_base as base
import modulos.variables as var
from utn_fra.pygame_widgets import Label, Button

def init_form_opciones(dict_form_data: dict) -> dict:
    """
    Inicializa el formulario de opciones con sus etiquetas y botones.

    Este formulario permite al usuario activar o desactivar la música, o volver al menú principal.

    Args:
        dict_form_data (dict): Diccionario con los datos necesarios para crear el formulario,
                               como pantalla, dimensiones, fondo, nombre, etc.

    Returns:
        dict: Diccionario que representa el formulario ya configurado.
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
    form['lbl_options'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 180,
        text = 'OPTIONS',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 70,
        color = var.COLOR_ROJO
        )
    form['btn_music_on'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 - 30,
        text = 'MUSIC ON',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click=lambda _: base.play_music(form)
        )
    form['btn_music_off'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 30,
        text = 'MUSIC OFF',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: base.stop_music() 
        )
    form['btn_back_menu'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 150,
        text = 'BACK TO MENU',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 50,
        color = var.COLOR_NARANJA,
        on_click = lambda _: base.set_active('form_menu')
        )
    form['widgets_list'] = [
        form['lbl_titulo'],
        form['lbl_options'],
        form['btn_music_on'],
        form['btn_music_off'],
        form['btn_back_menu']
        ]
    return form

def update(form_data: dict) -> None:
    """
    Actualiza todos los widgets del formulario de opciones.

    Args:
        form_data (dict): Diccionario del formulario actual.

    Returns:
        None
    """
    base.update(form_data)

def draw(form_data: dict) -> None:
    """
    Dibuja el fondo y todos los elementos del formulario de opciones en pantalla.

    Args:
        form_data (dict): Diccionario del formulario actual.

    Returns:
        None
    """
    base.draw(form_data)


