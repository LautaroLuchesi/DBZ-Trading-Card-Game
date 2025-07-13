import pygame as pg
import forms.form_base as base
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.cartas as cart
import forms.form_base as base
import modulos.comodines as comodines
from utn_fra.pygame_widgets import Label, TextPoster, Button

def init_form_jugar(dict_form_data: dict):
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
    
    sonido_next = pg.mixer.Sound(var.RUTA_SONIDO_NEXT)

    def al_hacer_click(params):
        sonido_next.play()
        estado = params['estado']
        if estado['mazo_jugador'] and estado['mazo_enemigo']:
            cart.revelar_siguiente_cartas(estado)
            carta_j = estado['cartas_jugador'][-1]
            carta_e = estado['cartas_enemigo'][-1]

            stats_j, stats_e, perdedor = cart.resolver_mano(
                carta_j, carta_e, estado['stats_jugador'], 
                estado['stats_enemigo'], estado
                )

            estado['stats_jugador'] = stats_j
            estado['stats_enemigo'] = stats_e
            
            if perdedor == 'enemy':
                daño_hp = int(carta_e['hp'] * (1 + carta_e['bonus'] / 100))
                daño_atk = int(carta_e['atk'] * (1 + carta_e['bonus'] / 100))
                daño_def = int(carta_e['def'] * (1 + carta_e['bonus'] / 100))
                score = (daño_hp + daño_atk + daño_def) // 10
                estado['score'] += score
                print(f"[INFO] Ganaste {score} puntos. Total: {estado['score']}")

            if perdedor:
                estado['mensaje'] = f"The loser of the round was: {perdedor.upper()}"
            else:
                "none"

    form['btn_siguiente'] = Button(
        x = 1200,
        y = 386,
        text = "NEXT",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = al_hacer_click, on_click_param = {'estado': form['estado']}
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

def update(form_data: dict, form_manager: dict):
    cart.logica_form_jugar(form_data, form_manager)
    comodines.actualizar_estado_comodines(form_data) # hacemos lo específico
    base.update(form_data) # delegamos la parte común    # hacemos lo específico

def draw(form):
    screnn = form['estado']['screen']
    screnn.blit(form['estado']['fondo'], (0, 0))

    # Reversos
    if form['estado']['mazo_jugador']:
        reverso_j = cart.obtener_reverso_según_expansion(form['estado']['mazo_jugador'][0]['expansion'], form['estado']['reversos'])
        screnn.blit(reverso_j, (400, 430))

    if form['estado']['mazo_enemigo']:
        reverso_e = cart.obtener_reverso_según_expansion(form['estado']['mazo_enemigo'][0]['expansion'], form['estado']['reversos'])
        screnn.blit(reverso_e, (400, 99))

    # Cartas actuales
    if form['estado']['cartas_jugador']:
        carta = form['estado']['cartas_jugador'][-1]
        img = cart.cargar_imagen_carta(carta['ruta'], * form['estado']['tamanio_carta'])
        screnn.blit(img, (633, 430))

    if form['estado']['cartas_enemigo']:
        carta = form['estado']['cartas_enemigo'][-1]
        img = cart.cargar_imagen_carta(carta['ruta'], * form['estado']['tamanio_carta'])
        screnn.blit(img, (633, 99))

    for widget in form['widgets_list']:
        widget.draw()