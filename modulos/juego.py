import pygame as pg
import modulos.variables as var
import modulos.auxiliar as aux
import modulos.cartas as cart
import forms.form_manager as form_manager
import random as rd


def ejecutar_juego():
    """
    Inicializa y ejecuta el bucle principal del juego de cartas.

    Esta función configura la ventana de Pygame, carga la configuración de los mazos desde un JSON,
    divide las cartas entre el jugador y el enemigo, genera los mazos y calcula los stats iniciales.
    Luego, crea los formularios necesarios y entra en el bucle principal del juego, donde se manejan
    los eventos, se actualiza la lógica y se renderiza la interfaz.

    El juego continúa ejecutándose hasta que el usuario cierre la ventana.

    Returns:
        None
    """
    pg.init()
    pantalla = pg.display.set_mode(var.DIMENSION_PANTALLA)
    pg.display.set_caption(var.TITULO)

    cantidades = cart.cargar_json("./archivos/config.json") 

    items = list(cantidades.items())
    rd.shuffle(items)
    
    jugador_config = {}
    enemigo_config = {}

    for i, (mazo, cantidad) in enumerate(items):
        if i % 2 == 0:
            jugador_config[mazo] = cantidad
        else:
            enemigo_config[mazo] = cantidad

    mazo_jugador = cart.generar_mazo_desde_config(jugador_config)
    mazo_enemigo = cart.generar_mazo_desde_config(enemigo_config)

    stats_jugador = cart.calcular_stats_totales(mazo_jugador)
    stats_enemigo = cart.calcular_stats_totales(mazo_enemigo)
    
    datos_juego = {
        "mazo_jugador": jugador_config,
        "mazo_enemigo": enemigo_config,
        "cartas_jugador": [],
        "cartas_enemigo": [],
        "stats_jugador": stats_jugador,
        "stats_enemigo": stats_enemigo,
        "mensaje": ""
        }
    
    manager = form_manager.create_form_manager(pantalla, datos_juego)

    reloj = pg.time.Clock()
    corriendo = True

    while corriendo:
        eventos = pg.event.get()
        for evento in eventos:
            if evento.type == pg.QUIT:
                corriendo = False

        pantalla.fill(var.COLOR_NEGRO)

        form_manager.update(manager, eventos)
        form_manager.draw(manager)

        pg.display.flip()
        reloj.tick(var.FPS)

    pg.quit()