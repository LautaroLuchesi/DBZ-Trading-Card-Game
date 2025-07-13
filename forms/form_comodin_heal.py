import modulos.variables as var
import forms.form_base as base
import modulos.comodines as comodin
from utn_fra.pygame_widgets import Button

def init_form_comodin_heal(dict_form_data):
    form = base.create_base_form(dict_form_data)
    screen = dict_form_data['screen']
    
    form['btn_usar_heal'] = Button(
        x = 350,
        y = 600,
        text = 'HEAL',
        screen = screen,
        font_path = var.FUENTE_DBZ,
        font_size = 46,
        color = var.COLOR_AMARILLO,
        on_click = lambda _: comodin.usar_comodin(form)
    )
    form['btn_volver'] = Button(
        x = 900,
        y = 600,
        text = 'EXIT',
        screen = screen, 
        font_path = var.FUENTE_DBZ,
        font_size = 46,
        color = var.COLOR_NARANJA,
        on_click = lambda _: base.set_active('form_jugar')
    )
    form['widgets_list'] = [form['btn_usar_heal'], form['btn_volver']]
    return form
