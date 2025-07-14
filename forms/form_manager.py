import pygame as pg
import modulos.variables as var
import forms.form_menu as menu
import forms.form_jugar as jugar
import forms.form_ranking as ranking
import forms.form_opciones as opciones
import forms.form_base as base
import forms.form_pausa as pausa
import forms.form_comodin_heal as heal
import forms.form_comodin_shield as shield
import forms.form_victoria as victoria
import forms.form_derrota as derrota

def create_form_manager(screen: pg.Surface, datos_juego: dict) -> dict:
    """
    Crea y configura todos los formularios del juego, agrupándolos en un gestor de formularios.

    Inicializa formularios como el menú, juego, ranking, opciones, victoria, derrota y comodines.
    Cada formulario es creado con sus parámetros específicos y luego agregado al form manager.

    Args:
        screen (pg.Surface): Superficie principal donde se dibujan los formularios.
        datos_juego (dict): Diccionario con información del jugador y configuración de mazos.

    Returns:
        dict: Diccionario que actúa como gestor de formularios, con la lista de todos los formularios.
    """
    form = {}
    form['main_screen'] = screen
    form['current_level'] = 1
    form['game_started'] = False
    form['jugador'] = datos_juego.get('jugador')

    form_manager = {
        'form_list': []
    }
    form_menu = menu.init_form_menu({
        "name": 'form_menu',
        "screen": screen,
        "active": True,
        "coords": (0, 0),
        "level_num": 1,
        "music_path": var.RUTA_MUSICA_MENU,
        "background_path": var.RUTA_FONDO_MENU,
        "screen_dimentions": var.DIMENSION_PANTALLA
    }, form_manager)

    form_jugar = jugar.init_form_jugar({
        "name": 'form_jugar',
        "screen": screen,
        "active": False,
        "coords": (0, 0), 
        "level_num": 1,
        "music_path": var.RUTA_MUSICA_JUGAR,
        "background_path": var.RUTA_FONDO_JUEGO,
        "screen_dimentions": var.DIMENSION_PANTALLA,
        "mazo_jugador": datos_juego.get("mazo_jugador"),
        "mazo_enemigo": datos_juego.get("mazo_enemigo")
    })
    form_jugar['estado']['pausado'] = False

    form_pausa = pausa.init_form_pausa({
        "name": 'form_pausa',
        "screen": screen,
        "active": False,
        "coords": (0, 0),
        "level_num": 1,
        "music_path": var.RUTA_MUSICA_PAUSA,
        "background_path": var.RUTA_FONDO_PAUSA,
        "screen_dimentions": var.DIMENSION_PANTALLA
    }, form_jugar)

    form_manager['form_list'] = [
        form_menu,
        form_jugar,
        form_pausa,
        ranking.init_form_ranking({
            "name": 'form_ranking',
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 1,
            "music_path": var.RUTA_MUSICA_RANKING,
            "background_path": var.RUTA_FONDO_RANKING,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }),
        opciones.init_form_opciones({
            "name": 'form_opciones',
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 1,
            "music_path": var.RUTA_MUSICA_OPCIONES,
            "background_path": var.RUTA_FONDO_OPCIONES,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }),
        heal.init_form_comodin_heal({
            "name": 'form_comodin_heal',
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 2,
            "music_path": var.RUTA_MUSICA_COMODIN,
            "background_path": var.RUTA_FONDO_COMODIN,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }),
        shield.init_form_comodin_shield({
            "name": 'form_comodin_shield',
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 2,
            "music_path": var.RUTA_MUSICA_COMODIN,
            "background_path": var.RUTA_FONDO_COMODIN,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }),
        victoria.init_form_victoria({
            "name": "form_victoria",
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 3,
            "music_path": var.RUTA_MUSICA_VICTORIA,
            "background_path": var.RUTA_FONDO_VICTORIA,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }, score_obtenido = 0),
        derrota.init_form_derrota({
            "name": "form_derrota",
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 3,
            "music_path": var.RUTA_MUSICA_DERROTA,
            "background_path": var.RUTA_FONDO_DERROTA,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }, score_obtenido = 0)
    ]

    return form_manager

def forms_update(form_manager: dict, lista_eventos: list) -> None:
    """
    Actualiza el formulario actualmente activo en base a los eventos recibidos.

    Cada formulario tiene su propia lógica de actualización, y en algunos casos como `form_jugar`,
    `form_victoria` y `form_derrota`, se delega esa lógica a funciones especializadas.

    Args:
        form_manager (dict): Gestor de formularios con la lista de formularios del juego.
        lista_eventos (list): Lista de eventos de Pygame capturados en el bucle principal.

    Returns:
        None
    """
    for form in form_manager['form_list']:
        if form.get('active'):
            nombre_form = form.get('name')
            if nombre_form == 'form_jugar': 
                jugar.update(form, form_manager)
            elif nombre_form == 'form_victoria':
                victoria.update(form, lista_eventos)
            elif nombre_form == 'form_derrota':
                derrota.update(form, lista_eventos)
            else:
                for widget in form.get('widgets_list', []):
                    if isinstance(widget, dict):
                        widget['update'](lista_eventos)
                    else:
                        widget.update()
            break 

def forms_draw(form_manager: dict) -> None:
    """
    Dibuja en pantalla el formulario que esté activo actualmente.

    Algunos formularios como `form_jugar` y `form_ranking` usan funciones de dibujo específicas.
    Los demás usan la función de dibujo genérica de base.

    Args:
        form_manager (dict): Gestor de formularios con la lista de formularios del juego.

    Returns:
        None
    """
    for form in form_manager['form_list']:
        if form.get('active'):
            nombre_form = form.get('name')
            if nombre_form == 'form_jugar':
                jugar.draw(form)
            elif nombre_form == 'form_ranking':
                ranking.draw(form)
            else:
                base.draw(form)
            break

def update(form_manager: dict, lista_eventos: list) -> None:
    """
    Función externa simplificada para actualizar el formulario activo.

    Encapsula la llamada a `forms_update` para mantener el código limpio.

    Args:
        form_manager (dict): Gestor de formularios con la lista de formularios del juego.
        lista_eventos (list): Lista de eventos de Pygame capturados en el bucle principal.

    Returns:
        None
    """
    forms_update(form_manager, lista_eventos) 

def draw(form_manager: dict) -> None:
    """
    Función externa simplificada para dibujar el formulario activo.

    Encapsula la llamada a `forms_draw` para mantener el código limpio.

    Args:
        form_manager (dict): Gestor de formularios con la lista de formularios del juego.

    Returns:
        None
    """
    forms_draw(form_manager)



    