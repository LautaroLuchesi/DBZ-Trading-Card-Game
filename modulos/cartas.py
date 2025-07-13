import os
import json
import pygame as pg
import random as rd
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.comodines as comodines

def cargar_config_mazo():
    ruta_config = './archivos/config.json'
    if os.path.exists(ruta_config):
        with open(ruta_config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    else:
        return {}

def generar_mazo_desde_config(config, cartas_usadas=None):
    if cartas_usadas is None:
        cartas_usadas = set()

    mazo = []

    for carpeta in config:
        cantidad = config[carpeta]
        ruta_carpeta = f'./assets/img/mazos/{carpeta}'

        if not os.path.exists(ruta_carpeta):
            print(f"[!] Carpeta no encontrada: {ruta_carpeta}")
            continue

        # Recolectar las cartas válidas
        todas = []
        for nombre_archivo in os.listdir(ruta_carpeta):
            if nombre_archivo.endswith('.png') and nombre_archivo != "reverse.png" and "_HP_" in nombre_archivo:
                todas.append(nombre_archivo)

        disponibles = []
        for nombre in todas:
            if nombre not in cartas_usadas:
                disponibles.append(nombre)

        if not disponibles:
            continue

        # Elegir al azar hasta "cantidad"
        seleccionadas = []
        cantidad_seleccion = min(cantidad, len(disponibles))
        while len(seleccionadas) < cantidad_seleccion:
            eleccion = rd.choice(disponibles)
            disponibles.remove(eleccion)
            seleccionadas.append(eleccion)

        # Agregar al mazo
        for nombre in seleccionadas:
            ruta = os.path.join(ruta_carpeta, nombre)
            stats = obtener_stats_desde_nombre(nombre)  # función propia
            carta = {
                "nombre": nombre,
                "ruta": ruta,
                "expansion": carpeta
            }
            carta.update(stats)
            mazo.append(carta)
            cartas_usadas.add(nombre)

    rd.shuffle(mazo)
    return mazo


def cargar_cartas(ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    
def cargar_configuracion(ruta_config):
    with open(ruta_config, "r", encoding="utf-8") as f:
        return json.load(f)
    
def cargar_imagen_carta(ruta, ancho, alto):
    ancho = var.TAMANIO_CARTA[0]
    alto = var.TAMANIO_CARTA[1]
    if os.path.exists(ruta):
        imagen = pg.image.load(ruta)
    else:
        imagen = pg.image.load('./assets/img/cartas/carta_default.png')
    return pg.transform.scale(imagen, (ancho, alto))

def obtener_stats_desde_nombre(nombre_archivo):
    nombre_sin_ext = nombre_archivo.replace('.png', '')
    partes = nombre_sin_ext.split('_')

    if len(partes) != 8:
        return {'hp': 0, 'atk': 0, 'def': 0, 'bonus': 0}

    hp_str = partes[2]
    atk_str = partes[4]
    def_str = partes[6]
    bonus_str = partes[7]

    if hp_str.isdigit() and atk_str.isdigit() and def_str.isdigit() and bonus_str.isdigit():
        hp = int(hp_str)
        atk = int(atk_str)
        defensa = int(def_str)
        bonus = int(bonus_str)
        print(f"[OK] Stats: HP={hp}, ATK={atk}, DEF={defensa}, BONUS={bonus}")
        return {'hp': hp, 'atk': atk, 'def': defensa, 'bonus': bonus}
    else:
        print(f"[ERROR] Alguno de los valores no es numérico: hp='{hp_str}', atk='{atk_str}', def='{def_str}', bonus='{bonus_str}'")
        return {'hp': 0, 'atk': 0, 'def': 0, 'bonus': 0}

def cargar_reversos():
    rutas = {
        "black_deck_expansion_1": "./assets/img/mazos/black_deck_expansion_1/reverse.png",
        "blue_deck_expansion_1": "./assets/img/mazos/blue_deck_expansion_1/reverse.png",
        "blue_deck_expansion_2": "./assets/img/mazos/blue_deck_expansion_2/reverse.png",
        "blue_deck_expansion_3": "./assets/img/mazos/blue_deck_expansion_3/reverse.png",
        "golden_deck_expansion_1": "./assets/img/mazos/golden_deck_expansion_1/reverse.png",
        "green_deck_expansion_1": "./assets/img/mazos/green_deck_expansion_1/reverse.png",
        "green_deck_expansion_2": "./assets/img/mazos/green_deck_expansion_2/reverse.png",
        "green_deck_expansion_3": "./assets/img/mazos/green_deck_expansion_3/reverse.png",
        "platinum_deck_expansion_1": "./assets/img/mazos/platinum_deck_expansion_1/reverse.png",
        "purple_deck_expansion_1": "./assets/img/mazos/purple_deck_expansion_1/reverse.png",
        "purple_deck_expansion_2": "./assets/img/mazos/purple_deck_expansion_2/reverse.png",
        "red_deck_expansion_1": "./assets/img/mazos/red_deck_expansion_1/reverse.png",
        "red_deck_expansion_2": "./assets/img/mazos/red_deck_expansion_2/reverse.png",
        "red_deck_expansion_3": "./assets/img/mazos/red_deck_expansion_3/reverse.png",
        "silver_deck_expansion_1": "./assets/img/mazos/silver_deck_expansion_1/reverse.png",
        "silver_deck_expansion_2": "./assets/img/mazos/silver_deck_expansion_2/reverse.png",
        "silver_deck_expansion_3": "./assets/img/mazos/silver_deck_expansion_3/reverse.png",
    }
    reversos = {}
    for clave, ruta in rutas.items():
        if os.path.exists(ruta):
            img = pg.image.load(ruta)
            reversos[clave] = pg.transform.scale(img, var.TAMANIO_CARTA)
    return reversos 

def obtener_reverso_según_expansion(expansion, reversos):
    return reversos.get(expansion, reversos.get("default"))

def revelar_siguiente_cartas(estado):
    if estado["mazo_jugador"]:
        carta_j = estado["mazo_jugador"].pop(0)
        estado["cartas_jugador"].append(carta_j)
        if len(estado["cartas_jugador"]) > 1:
            estado["cartas_jugador"].pop(0)

    if estado["mazo_enemigo"]:
        carta_e = estado["mazo_enemigo"].pop(0)
        estado["cartas_enemigo"].append(carta_e)
        if len(estado["cartas_enemigo"]) > 1:
            estado["cartas_enemigo"].pop(0)

def calcular_stats_totales(mazo):
    aplicar_bonus = lambda valor, bonus: int(valor * (1 + bonus / 100))
    total_hp = total_atk = total_def = 0

    for carta in mazo:
        total_hp += aplicar_bonus(carta['hp'], carta['bonus'])
        total_atk += aplicar_bonus(carta['atk'], carta['bonus'])
        total_def += aplicar_bonus(carta['def'], carta['bonus'])

    return {'hp': total_hp, 'atk': total_atk, 'def': total_def}

def es_golpe_critico(probabilidad = 0.25) -> tuple[bool, int]:
    """Determina si se aplica un golpe crítico. Devuelve (es_critico, multiplicador)."""
    critico = rd.random() < probabilidad
    if critico:
        pg.mixer.Sound(var.RUTA_SONIDO_CRITICO).play()
        print("[CRÍTICO] ¡Golpe crítico aplicado!")
        return True, 10
    return False, 1

def resolver_mano(carta_j, carta_e, stats_jugador, stats_enemigo, estado=None): 
    atk_j = int(carta_j['atk'] * (1 + carta_j['bonus'] / 100))
    atk_e = int(carta_e['atk'] * (1 + carta_e['bonus'] / 100))

    if atk_j < atk_e:
        perdedor = 'player'
        carta_perdedora = carta_j
    elif atk_e < atk_j:
        perdedor = 'enemy'
        carta_perdedora = carta_e
    else:
        return stats_jugador, stats_enemigo, None
    
    critico, multiplicador = es_golpe_critico()

    if estado is not None:
        perdedor = comodines.verificar_escudo(estado, perdedor)

    hp_desc = int(carta_perdedora['hp'] * (1 + carta_perdedora['bonus'] / 100)) * multiplicador
    atk_desc = int(carta_perdedora['atk'] * (1 + carta_perdedora['bonus'] / 100)) * multiplicador
    def_desc = int(carta_perdedora['def'] * (1 + carta_perdedora['bonus'] / 100)) * multiplicador

    if perdedor == 'player':
        stats_jugador['hp'] = max(stats_jugador['hp'] - hp_desc, 0)
        stats_jugador['atk'] = max(stats_jugador['atk'] - atk_desc, 0)
        stats_jugador['def'] = max(stats_jugador['def'] - def_desc, 0)
    else:
        stats_enemigo['hp'] = max(stats_enemigo['hp'] - hp_desc, 0)
        stats_enemigo['atk'] = max(stats_enemigo['atk'] - atk_desc, 0)
        stats_enemigo['def'] = max(stats_enemigo['def'] - def_desc, 0)

    if critico:
        print(f"[CRÍTICO] ¡Golpe crítico aplicado! Daño x5 al {perdedor.upper()}")
    return stats_jugador, stats_enemigo, perdedor

def logica_form_jugar(form: dict, form_manager: dict):
    estado = form['estado']
    if estado.get('pausado', False):
        return

    ms_transcurridos = estado['clock'].tick(60)
    estado['acumulador_ms'] += ms_transcurridos

    if estado['acumulador_ms'] >= 1000:
        estado['acumulador_ms'] -= 1000
        if estado['time'] > 0:
            estado['time'] -= 1
            print(f"[INFO] Tiempo restante: {estado['time']}")

    # Actualizar stats
    form['lbl_stats_j_hp'].update_text(f"HP: {estado['stats_jugador']['hp']}", var.COLOR_AMARILLO)
    form['lbl_stats_j'].update_text(
        f"ATK: {estado['stats_jugador']['atk']} DEF: {estado['stats_jugador']['def']}", var.COLOR_AMARILLO)
    form['lbl_stats_e_hp'].update_text(f"HP: {estado['stats_enemigo']['hp']}", var.COLOR_AMARILLO)
    form['lbl_stats_e'].update_text(
        f"ATK: {estado['stats_enemigo']['atk']} DEF: {estado['stats_enemigo']['def']}", var.COLOR_AMARILLO)

    form['txp_resultado'].update_text(estado['mensaje'])
    form['txp_time'].update_text(f"TIME: {estado['time']}")
    form['txp_score'].update_text(f"SCORE: {estado['score']}")

    # Lógica de juego general
    comodines.actualizar_estado_comodines(form)
    aux.verificar_fin_de_juego(form, form_manager)




