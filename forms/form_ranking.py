import pygame as pg
import modulos.variables as var
import modulos.auxiliar as aux
import forms.form_base as base
from utn_fra.pygame_widgets import Label, Button
  
def init_form_ranking(dict_form_data, jugador=None):
    form = base.create_base_form(dict_form_data)
    screen = dict_form_data['screen']

    fondo = pg.image.load(dict_form_data.get('background_path', var.RUTA_FONDO_RANKING))
    fondo = pg.transform.scale(fondo, dict_form_data.get('screen_dimentions', var.DIMENSION_PANTALLA))
    
    form['surface'] = fondo
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

    def update(eventos):
        for evento in eventos:
            if evento.type == pg.QUIT:
                pg.event.post(pg.event.Event(pg.QUIT))
            elif evento.type == pg.KEYDOWN and evento.key == pg.K_ESCAPE:
                base.set_active('form_menu')

    def draw():
        screen.blit(form['surface'], (0, 0))
        ranking = aux.cargar_ranking()
        y = 200
        for i, (nombre, puntaje) in enumerate(ranking[:10]):
            texto = f"{i + 1}. {nombre} - {puntaje} pts"
            aux.mostrar_texto(screen, texto, 45, var.COLOR_AMARILLO, 450, y)
            y += 35

        if jugador:
            aux.mostrar_texto(screen, f"Jugador: {jugador.get('nombre', 'Desconocido')}", 45, var.COLOR_AMARILLO, 20, 20)

        for widget in form['widgets_list']:
            widget.draw()

    form['custom_update'] = update
    form['custom_draw'] = draw

    return form
