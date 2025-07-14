import pygame as pg
import forms.form_base as base
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.cartas as cart
import forms.form_base as base
import modulos.comodines as comodines
from utn_fra.pygame_widgets import Label, TextPoster, Button

def init_form_jugar(dict_form_data: dict) -> dict:
    """
    Inicializa el formulario de juego configurando el estado inicial, etiquetas, botones y demás elementos gráficos.

    Esta función prepara el entorno de juego con los mazos del jugador y enemigo,
    calcula estadísticas, carga imágenes y sonidos, y define las acciones de los botones
    para manejar la mecánica principal del juego.

    Args:
        dict_form_data (dict): Diccionario con los datos necesarios para crear el formulario,
                               incluyendo la pantalla, configuración de mazos y otros parámetros.

    Returns:
        dict: Diccionario que representa el formulario de juego configurado con sus widgets y estado.
    """
    screen = dict_form_data['screen']
    form = base.create_base_form(dict_form_data)

    mazo_j = cart.generar_mazo_desde_config(dict_form_data.get('mazo_jugador'))
    mazo_e = cart.generar_mazo_desde_config(dict_form_data.get('mazo_enemigo'))
    stats_j = cart.calcular_stats_totales(mazo_j)
    stats_e = cart.calcular_stats_totales(mazo_e)

    form['estado'] = {
        'screen': screen,
        'fondo': pg.transform.scale(pg.image.load(var.RUTA_FONDO_JUEGO), var.DIMENSION_PANTALLA),
        'tamanio_carta': var.TAMANIO_CARTA,
        'mensaje': '',
        'cartas_jugador': [],
        'cartas_enemigo': [],
        'reversos': cart.cargar_reversos(),
        'mazo_jugador': mazo_j,
        'mazo_enemigo':mazo_e,
        'stats_jugador': stats_j,
        'stats_enemigo': stats_e,
        'stats_iniciales_jugador': stats_j.copy(),
        'heal_usado': False, 
        'shield_usado': False, 
        'shield_activo': False,
        'time': 100,
        'clock': pg.time.Clock(),
        'ultimo_tick': pg.time.get_ticks(),
        'pausado': False,
        'acumulador_ms': 0,          
        'score': 0, 
        }
    form['lbl_stats_j'] = Label(
        x = 187,
        y = 560,
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 18,
        color = var.COLOR_AMARILLO
        )
    form['lbl_stats_j_hp'] = Label(
        x = 177,
        y = 525,
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 36,
        color = var.COLOR_AMARILLO
        )
    form['lbl_stats_e_hp'] = Label(
        x = 177,
        y = 200,
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 36,
        color=var.COLOR_AMARILLO
        )
    form['lbl_stats_e'] = Label(
        x = 187,
        y = 235,
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 18,
        color=var.COLOR_AMARILLO
        )
    form['txp_resultado'] = TextPoster(
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 21,
        color = var.COLOR_AMARILLO,
        background_dimentions = (400, 50),
        background_coords = (415, 8),
        )
    form['txp_time'] = TextPoster(
        text = "Time: 100",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 20,
        color = var.COLOR_ROJO,
        background_dimentions = (150, 40),
        background_coords = (20, 0),
        )
    form['txp_score'] = TextPoster(
        text = "Score: 0",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 20,
        color = var.COLOR_NARANJA,
        background_dimentions = (150, 40),
        background_coords = (20, 50),
        )
    form['btn_siguiente'] = Button(
        x = 1200,
        y = 386,
        text = "NEXT",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = cart.al_hacer_click, on_click_param = {'estado': form['estado']}
        )
    form['btn_pausa'] = Button(
        x = 950,
        y = 30,
        text = "PAUSE",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: aux.pausar_y_cambiar(form)
        )
    form['btn_heal'] = Button(
        x = 1200,
        y = 580,
        text = 'HEAL',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_AMARILLO,
        on_click=lambda _: base.set_active('form_comodin_heal') 
        )
    form['btn_shield'] = Button(
        x = 1200,
        y = 630,
        text = 'SHIELD',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_AMARILLO,
        on_click = lambda _: base.set_active('form_comodin_shield')
        )
    form['widgets_list'] =[
        form['lbl_stats_j_hp'], form['lbl_stats_j'], form['lbl_stats_e_hp'], form['lbl_stats_e'], form['txp_resultado'], form['btn_siguiente'], 
        form['btn_pausa'], form['btn_heal'], form['btn_shield'],form['txp_time'],form['txp_score']
        ]
    return form

def update(form_data: dict, form_manager: dict) -> None:
    """
    Actualiza el estado del formulario de juego, ejecutando la lógica principal y actualizando comodines y widgets.

    Args:
        form_data (dict): Diccionario que contiene los datos y estado actual del formulario de juego.
        form_manager (dict): Gestor de formularios que controla la navegación y estados entre formularios.

    Returns:
        None
    """
    form_data['estado']['pausado'] = False
    cart.logica_form_jugar(form_data, form_manager)
    comodines.actualizar_estado_comodines(form_data)
    base.update(form_data)


def draw(form: dict) -> None:
    """
    Dibuja en pantalla las cartas y elementos gráficos del formulario de juego.

    Args:
        form (dict): Diccionario que contiene los datos y widgets del formulario actual.

    Returns:
        None
    """
    cart.dibujar_cartas(form)