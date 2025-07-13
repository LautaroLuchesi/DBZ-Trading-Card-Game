import pygame as pg
import modulos.variables as var
import forms.form_menu as menu
import forms.form_jugar as jugar
import forms.form_ranking as ranking
import forms.form_opciones as opciones
import forms.form_base as form_base
import forms.form_jugar as form_jugar
import forms.form_pausa as pausa
import forms.form_comodin_heal as heal
import forms.form_comodin_shield as shield
import forms.form_victoria as victoria
import forms.form_derrota as derrota

def create_form_manager(screen: pg.Surface, datos_juego: dict):
    form = {}
    form['main_screen'] = screen
    form['current_level'] = 1
    form['game_started'] = False
    form['player'] = None
    form['enemy'] = None
    form['jugador'] = datos_juego.get('jugador')

    # Inicializar el form_manager vacío
    form_manager = {
        'form_list': []
    }

    # Ahora sí podés pasarle form_manager al form_menu
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

    # Agregar todos los formularios al form_manager
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
        }, jugador=form.get('jugador')),
        opciones.init_form_opciones({
            "name": 'form_opciones',
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 1,
            "music_path": var.RUTA_MUSICA_OPCIONES,
            "background_path": var.RUTA_FONDO_OPCIONES,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }, jugador=form.get('jugador')),
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
        }, score_obtenido=0),
        derrota.init_form_derrota({
            "name": "form_derrota",
            "screen": screen,
            "active": False,
            "coords": (0, 0),
            "level_num": 3,
            "music_path": var.RUTA_MUSICA_DERROTA,
            "background_path": var.RUTA_FONDO_DERROTA,
            "screen_dimentions": var.DIMENSION_PANTALLA
        }, score_obtenido=0)
    ]

    return form_manager

def forms_update(form_manager: dict, lista_eventos: list):
    for form in form_manager['form_list']:
        if form.get('active'):
            nombre_form = form.get('name')
            if nombre_form == 'form_jugar':
                form_jugar.update(form, form_manager)
            elif nombre_form == 'form_victoria':
                victoria.update(form, lista_eventos)
            elif nombre_form == 'form_derrota':
                derrota.update(form, lista_eventos)
            elif nombre_form == 'form_ranking':
                form['custom_update'](lista_eventos)
            else:
                for widget in form.get('widgets_list', []):
                    if isinstance(widget, dict):
                        widget['update'](lista_eventos)
                    else:
                        widget.update()
            break 

def forms_draw(form_manager: dict):
    for form in form_manager['form_list']:
        if form.get('active'):
            nombre_form = form.get('name')
            if nombre_form == 'form_jugar':
                form_jugar.draw(form)
            elif nombre_form == 'form_ranking':
                form['custom_draw']()
            else:
                form_base.draw(form)
            break

def update(form_manager: dict, lista_eventos: list):
    for form in form_manager['form_list']:
        if form['active']:
            print(f"[DEBUG] ACTIVO: {form['name']}")  # 👈 Esto te muestra qué form está activo

    forms_update(form_manager, lista_eventos)  # 👈 Actualiza solo el form activo


def draw(form_manager: dict):
    forms_draw(form_manager)



    