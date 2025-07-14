import pygame as pg
import modulos.variables as var
import os

forms_dict = {}
pg.mixer.init()

def create_base_form(dict_form_data: dict) -> dict:
    """
    Crea un formulario base a partir de los datos proporcionados.

    Este formulario incluye propiedades como nombre, pantalla, coordenadas, fondo,
    número de nivel, música y una lista vacía de widgets. También lo registra en el
    diccionario global `forms_dict`.

    Args:
        dict_form_data (dict): Diccionario con los datos necesarios para inicializar
                               el formulario (pantalla, fondo, música, coordenadas, etc.).

    Returns:
        dict: Diccionario que representa el formulario base inicializado.
    """
    form = {}
    form['name'] = dict_form_data.get('name')
    form['screen'] = dict_form_data.get('screen')
    form['active'] = dict_form_data.get('active')
    form['x_coord'] = dict_form_data.get('coords')[0]
    form['y_coord'] = dict_form_data.get('coords')[1]
    form['level_number'] = dict_form_data.get('level_num')
    form['music_path'] = dict_form_data.get('music_path')
    form['background'] = pg.image.load(dict_form_data.get('background_path')).convert()
    form['background'] = pg.transform.scale(form['background'], dict_form_data.get('screen_dimentions'))
    form['rect'] = form['background'].get_rect()
    form['rect'].x = form['x_coord']
    form['rect'].y = form['y_coord']
    form['widgets_list'] = []

    forms_dict[form['name']] = form 

    return form

click_sound = pg.mixer.Sound(var.RUTA_SONIDO_CLICK)

def play_click_sound() -> None:
    """
    Reproduce un sonido de clic, normalmente utilizado al presionar un botón.

    Returns:
        None
    """
    click_sound.play()

def play_music(form_dict: dict) -> None:
    """
    Reproduce la música asociada al formulario indicado.

    Args:
        form_dict (dict): Diccionario que representa el formulario, debe contener el path de la música.

    Returns:
        None
    """
    pg.mixer.music.load(form_dict.get('music_path'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops=-1, fade_ms=400)

def stop_music() -> None:
    """
    Detiene la música que esté sonando actualmente.

    Returns:
        None
    """
    pg.mixer.music.stop()

def set_active(name: str) -> None:
    """
    Establece como activo el formulario con el nombre indicado.

    Desactiva todos los formularios, detiene la música actual,
    reproduce la música del nuevo formulario (si tiene) y,
    en caso de formularios de comodines, reproduce un sonido adicional.

    Args:
        name (str): Nombre del formulario que se quiere activar.

    Returns:
        None
    """
    for form in forms_dict.values():
        form['active'] = False

    if name in forms_dict:
        form = forms_dict[name]
        form['active'] = True

        stop_music()

        music_path = form.get('music_path')
        if music_path and os.path.exists(music_path):
            play_music(form)

        if name in ["form_comodin_heal", "form_comodin_shield"]:
            sonido_intro = pg.mixer.Sound(var.RUTA_SONIDO_COMODIN_INTRO)
            sonido_intro.play()

def update_widgets(form_data: dict) -> None:
    """
    Actualiza todos los widgets del formulario actual.

    Args:
        form_data (dict): Diccionario que representa el formulario actual.

    Returns:
        None
    """
    widgets = form_data.get('widgets_list', [])
    for i in range(len(widgets)):
        widgets[i].update()

def draw_widgets(form_data: dict) -> None:
    """
    Dibuja todos los widgets del formulario actual en la pantalla.

    Args:
        form_data (dict): Diccionario que representa el formulario actual.

    Returns:
        None
    """
    widgets = form_data.get('widgets_list', [])
    for i in range(len(widgets)):
        widgets[i].draw()

def draw(form_data: dict) -> None:
    """
    Dibuja el fondo y los widgets del formulario actual en pantalla.

    Args:
        form_data (dict): Diccionario que representa el formulario actual.

    Returns:
        None
    """
    form_data['screen'].blit(form_data['background'], form_data['rect'])
    draw_widgets(form_data)

def update(form_data: dict) -> None:
    """
    Actualiza todos los widgets del formulario actual.

    Args:
        form_data (dict): Diccionario que representa el formulario actual.

    Returns:
        None
    """
    update_widgets(form_data)




