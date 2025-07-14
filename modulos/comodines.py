import modulos.variables as var
import pygame as pg
import forms.form_base as base
from utn_fra.pygame_widgets import Label

def activar_heal(estado):
    if not estado.get('heal_usado', False):
        estado['stats_jugador'] = estado['stats_iniciales_jugador'].copy()
        estado['heal_usado'] = True
        print("[INFO] HEAL activado: stats del jugador restaurados.")

def activar_shield(estado):
    if not estado.get('shield_usado', False):
        estado['shield_activo'] = True
        estado['shield_usado'] = True
        print("[INFO] SHIELD activado: la próxima derrota será invertida.")

def verificar_escudo(estado, perdedor):
    if perdedor == 'player' and estado.get('shield_activo', False):
        print("[INFO] SHIELD activado: el daño fue redirigido al enemigo.")
        estado['shield_activo'] = False
        return 'enemy'
    return perdedor

def usar_comodin(form_comodin):
    form_jugar = base.forms_dict.get('form_jugar')
    if not form_jugar:
        print("[ERROR] form_jugar no encontrado en forms_dict")
        return

    estado_jugar = form_jugar['estado']

    outro = pg.mixer.Sound(var.RUTA_SONIDO_COMODIN_OUTRO)
    outro.play()

    if form_comodin['name'] == 'form_comodin_heal':
        activar_heal(estado_jugar)
        if 'btn_heal' in form_jugar and form_jugar['btn_heal'] in form_jugar['widgets_list']:
            form_jugar['widgets_list'].remove(form_jugar['btn_heal'])

        if 'lbl_heal_active' not in form_jugar:
            screen = estado_jugar['screen']
            form_jugar['lbl_heal_active'] = Label(
                x = 1200,
                y = 197,
                text = "HEAL",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form_jugar['widgets_list'].append(form_jugar['lbl_heal_active'])

    elif form_comodin['name'] == 'form_comodin_shield':
        activar_shield(estado_jugar)
        if 'btn_shield' in form_jugar and form_jugar['btn_shield'] in form_jugar['widgets_list']:
            form_jugar['widgets_list'].remove(form_jugar['btn_shield'])

        if 'lbl_shield_active' not in form_jugar:
            screen = estado_jugar['screen']
            form_jugar['lbl_shield_active'] = Label(
                x = 1200,
                y = 272,
                text = "SHIELD",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form_jugar['widgets_list'].append(form_jugar['lbl_shield_active'])

    base.set_active('form_jugar')

def actualizar_estado_comodines(form):
    estado = form['estado']
    screen = estado['screen']

    if estado.get('heal_usado', False):
        if 'btn_heal' in form and form['btn_heal'] in form['widgets_list']:
            form['widgets_list'].remove(form['btn_heal'])
        if 'lbl_heal_active' not in form:
            form['lbl_heal_active'] = Label(
                x = 1200,
                y = 177,
                text = "HEAL",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form['widgets_list'].append(form['lbl_heal_active'])

    if estado.get('shield_usado', False):
        if 'btn_shield' in form and form['btn_shield'] in form['widgets_list']:
            form['widgets_list'].remove(form['btn_shield'])
        if 'lbl_shield_active' not in form:
            form['lbl_shield_active'] = Label(
                x = 1200,
                y = 227,
                text = "SHIELD",
                screen = screen,
                font_path = var.FUENTE_DBZ,
                font_size = 40,
                color = var.COLOR_AMARILLO,
            )
            form['widgets_list'].append(form['lbl_shield_active'])






