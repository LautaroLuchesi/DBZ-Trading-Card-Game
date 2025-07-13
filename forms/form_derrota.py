import forms.form_base as base
import modulos.variables as var
import modulos.auxiliar as aux
from utn_fra.pygame_widgets import Label, Button
import pygame as pg

def init_form_derrota(dict_form_data, score_obtenido):
    form = base.create_base_form(dict_form_data)
    screen = dict_form_data['screen'] 

    form['estado'] = {
        'input_nombre': '',
        'score': score_obtenido,
        }
    form['lbl_titulo'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 35,
        text = var.TITULO,
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 60,
        color = var.COLOR_ROJO
        )
    form['lbl_victoria'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 160,
        text = "Defeat",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 70,
        color = var.COLOR_ROJO
        )
    form['lbl_score'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 260,
        text = f"Score: {score_obtenido}",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 40,
        color = var.COLOR_AMARILLO
        )
    form['lbl_nombre'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 315,
        text = "Write your name:",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 30,
        color = var.COLOR_ROJO
        )
    form['lbl_input'] = Label(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 375,
        text = "",
        screen = screen,
        font_path = var.FUENTE_ALAGARD,
        font_size = 35,
        color = var.COLOR_BLANCO
        )

    def confirmar_nombre(_=None):
        nombre = form['estado']['input_nombre'].strip()
        if nombre:
            aux.guardar_puntaje(nombre, form['estado']['score'])
            base.set_active("form_menu")

    form['btn_confirmar'] = Button(
        x = var.DIMENSION_PANTALLA[0] // 2,
        y = 460,
        text = "CONFIRM NAME",
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 35,
        color = var.COLOR_ROJO,
        on_click = confirmar_nombre
        )

    form['widgets_list'] = [
        form['lbl_titulo'],
        form['lbl_victoria'],
        form['lbl_score'],
        form['lbl_nombre'],
        form['lbl_input'],
        form['btn_confirmar']
        ]

    return form

def update(form, eventos):
    base.update(form)
    estado = form['estado']

    for evento in eventos:
        if evento.type == pg.KEYDOWN:
            print(f"[DEBUG] KEYDOWN detectado: {evento.key}")
            if evento.key == pg.K_BACKSPACE:
                estado['input_nombre'] = estado['input_nombre'][:-1]
                print(f"Backspace presionado, texto ahora: '{estado['input_nombre']}'")
            elif evento.key == pg.K_RETURN:
                form['btn_confirmar'].on_click(None)
            else:
                if len(estado['input_nombre']) < 12 and evento.unicode.isprintable():
                    estado['input_nombre'] += evento.unicode
                    print(f"Tecla presionada: '{evento.unicode}', texto ahora: '{estado['input_nombre']}'")

    form['lbl_input'].update_text(estado['input_nombre'], var.COLOR_ROJO)
    form['lbl_score'].update_text(f"Score: {estado['score']}", var.COLOR_BLANCO)

 
def draw(form):
    base.draw(form)
    pg.draw.line(form['screen'], var.COLOR_BLANCO, (400, 440), (880, 440), 2)