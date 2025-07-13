import sys
import modulos.variables as var
import forms.form_base as base
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import Button, Label

def init_form_menu(dict_form_data: dict, form_manager):
    form = base.create_base_form(dict_form_data)

    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 140,
        text = var.TITULO,
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 70,
        color = var.COLOR_ROJO
        )
    form['btn_jugar'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 25,
        text = 'PLAY',
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda datos: (
            base.play_click_sound(),
            aux.reiniciar_form_jugar(datos['form_manager'], form['screen'])),
        on_click_param = {'form_manager': form_manager}
        )
    form['btn_ranking'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 90,
        text = 'RANKING',
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: (base.play_click_sound(), base.set_active('form_ranking'))
        )
    form['btn_opciones'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 155,
        text = 'OPCIONS',
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: (base.play_click_sound(), base.set_active('form_opciones'))
        )
    form['btn_salir'] = Button(
        x=var.DIMENSION_PANTALLA[0] // 2,
        y = var.DIMENSION_PANTALLA[1] // 2 + 220,
        text = 'EXIT',
        screen = form['screen'],
        font_path = var.FUENTE_DBZ,
        font_size = 40,
        color = var.COLOR_NARANJA,
        on_click = lambda _: sys.exit()
        )
    form['widgets_list'] = [
        form['lbl_titulo'],
        form['btn_jugar'],
        form['btn_ranking'],
        form['btn_opciones'],
        form['btn_salir']
        ]
    
    return form

def update(form_data: dict):
    base.update(form_data)

def draw(form_data: dict):
    base.draw(form_data) 

        





