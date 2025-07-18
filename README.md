# 🃏 Juego de Cartas por Turnos - Dragon Ball Z (Pygame)

Este proyecto es un juego de cartas por turnos inspirado en el universo de Dragon Ball Z. Está desarrollado en Python utilizando la librería **Pygame**, con lógica de combate, interfaz gráfica, manejo de eventos, formularios y stats dinámicos.

## 🎮 ¿Cómo se juega?

- Cada jugador (usuario vs enemigo) tiene un mazo aleatorio con cartas de distintas expansiones.
- En cada turno, se revela una carta por jugador.
- Se comparan los valores de ataque para determinar un ganador de la ronda.
- Se aplican daños a los stats según la carta perdedora (con posibilidad de golpes críticos).
- Gana el jugador que reduce las estadísticas del enemigo a cero o el que tiene mas HP al finalizar el tiempo.

---

## 🧠 Funcionalidades destacadas

- Carga dinámica de cartas desde carpetas organizadas por expansión.
- Cálculo automático de stats con bonificaciones.
- Interfaz con formularios personalizados, botones y textos actualizados en tiempo real.
- Comodines (Heal y Shield) que permiten recuperar stats o evitar derrotas.
- Música, sonidos y reversos personalizados para cada mazo.
- Estructura modular con separación de lógica (`auxiliar.py`, `cartas.py`, `comodines.py`, etc).

---

## 🛠️ Tecnologías

- **Python 3**
- **Pygame**
- Manejo de archivos (`OS`, `CSV`, `JSON`)
- Programación estructurada y modular
- Principios básicos de TDA (listas, diccionarios, sets, tuplas)


---

## 🖼️ Capturas

#### 📋 Menú principal  
<img src="assets/img/capturas/cap_menu.png" alt="Menú principal" width="600"/>

---

#### ⚙️ Opciones 
<img src="assets/img/capturas/cap_opciones.png" alt="Combate en curso" width="600"/>

---

#### ⚔️ Combate en curso  
<img src="assets/img/capturas/cap_juego.png" alt="Comodín activado" width="600"/>

---

#### ⏸️ Pausa 
<img src="assets/img/capturas/cap_pausa.png" alt="Derrota" width="600"/>
---

#### 🏆 Pantalla de Victoria  
<img src="assets/img/capturas/cap_victoria.png" alt="Victoria" width="600"/>

---

#### 📊 Ranking 
<img src="assets/img/capturas/cap_ranking.png" alt="Derrota" width="600"/>

---

## 📌 Estado del proyecto:    
✅ Funcional y completo  
🎓 Desarrollado como parte de la materia Programación 1 - UTN  
🏆 Promocionado en julio 2025  

---

## 📬 Contacto  
Lautaro Luchesi  
📧 lautaroluchesi00@gmail.com  
🔗 GitHub: lautaroLuchesi  

---

## ▶️ Ejecución

Cloná el repositorio:
```bash
git clone https://github.com/lautaroLuchesi/DBZ-Trading-Card-Game.git
pip install pygame
python main.py

