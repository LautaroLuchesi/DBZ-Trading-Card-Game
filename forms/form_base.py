import pygame as pg
import modulos.variables as var
import os

forms_dict = {}

def create_base_form(dict_form_data: dict) -> dict:
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

pg.mixer.init()

click_sound = pg.mixer.Sound(var.RUTA_SONIDO_CLICK)

def play_click_sound():
    click_sound.play()

def play_music(form_dict: dict):
    pg.mixer.music.load(form_dict.get('music_path'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops = -1, fade_ms = 400)

def stop_music():
    pg.mixer.music.stop()

def set_active(name: str):
    for form in forms_dict.values():
        form['active'] = False

    if name in forms_dict:
        form = forms_dict[name]
        form['active'] = True
        print(f"[INFO] Formulario activo: {name}")

        stop_music()

        music_path = form.get('music_path')
        if music_path and os.path.exists(music_path):
            play_music(form)
            print(f"[INFO] Reproduciendo música: {music_path}")
        else:
            print(f"[WARN] No se encontró música para: {name} o ruta inválida")

        if name in ["form_comodin_heal", "form_comodin_shield"]:
            sonido_intro = pg.mixer.Sound(var.RUTA_SONIDO_COMODIN_INTRO)
            sonido_intro.play()

    else:
        print(f"[ERROR] Formulario '{name}' no encontrado en forms_dict.")

def update_widgets(form_data: dict):
    widgets = form_data.get('widgets_list', [])
    for i in range(len(widgets)):
        widgets[i].update()

def draw_widgets(form_data: dict):
    widgets = form_data.get('widgets_list', [])
    for i in range(len(widgets)):
        widgets[i].draw()

def draw(form_data: dict):
    print(f"Dibujando fondo de: {form_data['name']}")
    form_data['screen'].blit(form_data['background'], form_data['rect'])
    draw_widgets(form_data)

def update(form_data: dict):
    update_widgets(form_data)



