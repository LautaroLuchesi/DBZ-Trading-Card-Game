import pygame as pg
import modulos.variables as var
import modulos.auxiliar as aux
import forms.form_base as base
from utn_fra.pygame_widgets import Label, Button
  
def init_form_ranking(dict_form_data: dict) -> dict:
    """
    Inicializa el formulario de ranking que muestra los mejores puntajes.

    Args:
        dict_form_data (dict): Diccionario con información para construir el formulario.
            - 'screen': pantalla de Pygame donde se dibuja.
            - 'background_path': ruta de la imagen de fondo.
            - 'screen_dimentions': tamaño de pantalla.

    Returns:
        dict: Diccionario con todos los elementos del formulario configurado.
    """
    form = base.create_base_form(dict_form_data)
    screen = dict_form_data['screen']

    surface = pg.image.load(dict_form_data.get('background_path', var.RUTA_FONDO_RANKING))
    surface = pg.transform.scale(surface, dict_form_data.get('screen_dimentions', var.DIMENSION_PANTALLA))
    
    form['surface'] = surface
    form['screen'] = screen
    
    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 85,
        text = var.TITULO,
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_AMARILLO
        )
    form['lbl_subtitulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 125,
        text = "RANKING",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 30,
        color=var.COLOR_AMARILLO
        )
    form['btn_back_menu'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 617,
        text = 'BACK TO MENU',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: base.set_active('form_menu')
        )
    form['widgets_list'] = [
        form['lbl_titulo'],
        form['lbl_subtitulo'],
        form['btn_back_menu']
    ]


    return form
def update(form: dict) -> None:
    """
    Actualiza los elementos del formulario de ranking (botones, etiquetas, etc.).

    Args:
        form (dict): Formulario de ranking.

    Returns:
        None
    """
    base.update(form)

def draw(form: dict) -> None:
    """
    Dibuja el fondo, el ranking y los widgets en pantalla.

    Args:
        form (dict): Formulario de ranking.

    Returns:
        None
    """
    aux.dibujar_ranking(form)

