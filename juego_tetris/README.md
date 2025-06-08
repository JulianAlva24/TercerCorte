# 🧩 Tetris – Versión Gamer Retro

Este es un juego completo de Tetris desarrollado en Python usando Pygame. Incluye velocidad progresiva, rotación de piezas, puntaje, niveles, caída rápida, pausa y reinicio.

---

## 📁 Estructura del proyecto

```
juego_tetris/
├── assets/
│   ├── images/
│   └── sounds/
├── venv/
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## ▶️ Requisitos

- Python 3.8 o superior
- Pygame (`pip install pygame`)

---

## ⚙️ Instalación y ejecución

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# .\venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py
```

---

## 🎮 Controles

- `A / ←`: Mover a la izquierda
- `D / →`: Mover a la derecha
- `S / ↓`: Caída suave (suma 1 punto)
- `W / ↑`: Rotar la pieza
- `Espacio`: Caída instantánea (hard drop, suma 2 puntos por celda)
- `P`: Pausar o continuar el juego
- `R`: Reiniciar juego
- `ESC`: Salir

---

## 🧠 Partes más importantes del código

### `class Piece`
Define cada pieza del Tetris:
- Almacena forma, color, rotación, posición `(x, y)`
- Métodos: `get_cells()`, `rotate()`, `get_rotated_shape()`

### `class TetrisGame` – Explicación detallada de métodos clave

#### `is_valid_position(piece, x=None, y=None, rotation=None)`
Verifica si una pieza puede colocarse en una posición específica del tablero. Revisa:
- Que las coordenadas estén dentro del grid.
- Que no haya colisión con otras piezas ya colocadas.

#### `place_piece()`
Fija la pieza actual en el tablero.
- Toma todas las celdas de la pieza y las pinta con su color en `self.grid`.
- Llama a `clear_lines()` para revisar si hay líneas completas.
- Crea una nueva pieza para continuar el juego.
- Si la nueva pieza no tiene espacio disponible, el juego termina.

#### `clear_lines()`
Elimina líneas completas del tablero:
- Recorre cada fila y verifica si está totalmente llena.
- Si es así, elimina la fila y agrega una nueva vacía en la parte superior.
- Calcula puntaje basado en cuántas líneas se eliminan a la vez:
  - 1 línea = 100 pts, 2 líneas = 300 pts, 3 líneas = 500 pts, 4 líneas = 800 pts.
- Aumenta el nivel cada 10 líneas y reduce la velocidad de caída (`fall_speed`).

#### `move_piece(dx, dy)`
Intenta mover la pieza actual horizontal o verticalmente:
- Si la nueva posición es válida (`is_valid_position`), actualiza las coordenadas `x` e `y`.

#### `rotate_piece()`
Rota la pieza actual si es posible:
- Calcula la nueva rotación.
- Si la rotación no genera colisión ni se sale del tablero, la aplica.

#### `hard_drop()`
Hace que la pieza caiga hasta el fondo instantáneamente:
- Suma 2 puntos por cada movimiento hacia abajo automático.
- Llama a `place_piece()` al llegar al fondo.

#### `draw_grid()`
Dibuja el tablero de juego:
- Pinta cada celda del `self.grid` y la pieza actual si aún no ha sido fijada.

#### `draw_ui()`
Dibuja la interfaz lateral:
- Muestra puntaje, nivel, líneas, y los controles del teclado.

#### `draw_next_piece()`
Dibuja la siguiente pieza que vendrá después de la actual:
- Se muestra como vista previa en la parte derecha de la pantalla.

#### `draw_game_over()`
Muestra una superposición oscura con el texto “GAME OVER” y el puntaje final.

#### `draw_pause()`
Muestra una superposición con el texto “PAUSADO” y cómo continuar.

#### `handle_events()`
Gestiona la interacción del jugador con el teclado:
- Movimiento, rotación, pausa, reinicio, y cierre del juego.

#### `update(dt)`
Controla el tiempo de caída de la pieza:
- Acumula tiempo (`fall_time`).
- Si se alcanza el tiempo de caída (`fall_speed`), intenta mover hacia abajo.
- Si no puede bajar más, fija la pieza.

#### `run()`
Bucle principal del juego:
- Ejecuta `handle_events()`, `update()`, y todos los métodos de dibujo.
- Refresca la pantalla con `pygame.display.flip()`.

---


### Piezas
Las piezas están definidas en formato de cadena (`PIECES`), incluyendo I, O, T, S, Z, J y L en múltiples rotaciones.

---

## 🕹️ Descripción del funcionamiento

1. Se genera una nueva pieza al iniciar el juego.
2. La pieza cae automáticamente, pero el jugador puede moverla o rotarla.
3. Cuando una pieza toca fondo o cae sobre otra, se fija en el tablero.
4. Si se completa una línea horizontal, se elimina y se suma puntaje.
5. El juego termina cuando una nueva pieza no puede colocarse en la parte superior.
6. El nivel y la velocidad aumentan cada 10 líneas eliminadas.
7. Se puede pausar y reiniciar el juego en cualquier momento.
