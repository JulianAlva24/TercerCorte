# Juegos Clásicos en Python con Docker

Este repositorio contiene la implementación de tres juegos clásicos desarrollados con Python y Pygame, personalizados con estilo propio y ejecutables a través de contenedores Docker.

---

## 🧪 Cómo ejecutar los juegos

1. Asegúrate de tener Docker instalado
2. Ejecuta:

```bash
docker start juego_<nombre_del_juego>_local
```

Reemplaza `<nombre_del_juego>` por:
- `juego_naves`
- `juego_tanques`
- `juego_tetris`

---

## 📂 Estructura del Repositorio

```
TercerCorte/
│
├── juegos/
    ├── juego_naves/
    │   ├── assets/
    │   │   ├── images/
    │   │   └── sounds/
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   └── README.md
    ├── juego_tanques/
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   └── README.md│   
    ├── juego_tetris/
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   └── README.md
    ├── Imagenes/
    └── README.md (este archivo)
 
```

---

# 🚀 Space Shooter – Juego de Naves Espaciales

Este es un juego clásico de naves espaciales desarrollado en Python usando Pygame. El jugador controla una nave, dispara a enemigos que bajan por la pantalla, y debe evitar ser destruido. El juego utiliza imágenes y sonidos externos almacenados en la carpeta `assets/`.



**🎨 Personalización:**  
- Gráficos estilizados
- Part sonidos y HUD con detalles visuales
- Fondos personalizados

**🎮 Controles:**
- `←` / `→`: mover nave
- `Espacio`: disparar
- `ESC`: salir

---

## 🧠 Partes más importantes del código

### `class Game`
Controla todo el juego: lógica principal, dibujado en pantalla, control de niveles, colisiones y generación de enemigos.

- `spawn_enemy()`: Genera enemigos aleatoriamente.
- `check_collisions()`: Detecta impactos entre balas y enemigos o jugador.
- `run()`: Bucle principal que actualiza y dibuja todo el juego.

### `class Player`
Representa la nave espacial del jugador.

- `update()`: Controla el movimiento con teclas y el disparo.
- `draw()`: Dibuja la nave y su barra de vida.
- Dispara balas hacia arriba, almacenadas en `self.bullets`.

### `class Enemy`
Define los enemigos que bajan por la pantalla.

- Tiene 3 tipos, cada uno con imagen, velocidad y vida diferentes.
- `update()`: Mueve al enemigo verticalmente.
- `draw()`: Dibuja su sprite y barra de vida.

### `class Bullet`
Controla los proyectiles del jugador.

- `update()`: Mueve la bala.
- `draw()`: La dibuja con imagen externa (`bullet.png`).

---

## 🕹️ Descripción del Funcionamiento del Juego

El juego "Space Shooter" es una recreación moderna de los clásicos juegos arcade de disparos espaciales. A continuación se describe su funcionamiento general:

### 🎮 Objetivo del juego
El jugador controla una nave espacial ubicada en la parte inferior de la pantalla. El objetivo es **sobrevivir y obtener la mayor cantidad de puntos posibles** al destruir enemigos que descienden desde la parte superior.

### 🔄 Mecánica general

1. **Inicio del juego**:  
   Se inicializa una ventana con fondo estrellado y la nave del jugador en el centro inferior de la pantalla.

2. **Movimiento del jugador**:  
   Se controla con las flechas del teclado, sin salirse de los límites de la pantalla.

3. **Disparo**:  
   Presionando ESPACIO, se dispara hacia arriba. Cada disparo emite un sonido (`laser.wav`).

4. **Aparición de enemigos**:  
   Se generan aleatoriamente desde la parte superior. Hay 3 tipos con diferentes tamaños y vida.

5. **Colisiones**:  
   - Balas impactan enemigos → pierden vida → se suman puntos.
   - Enemigos impactan al jugador → se pierde salud.
   - Si la salud del jugador llega a 0, el juego termina.

6. **Dificultad progresiva**:  
   Aumenta la velocidad de generación de enemigos conforme sube el puntaje.

7. **Fin del juego**:  
   Al perder toda la vida, se muestra el puntaje final y se permite reiniciar o salir.
---
# Imagen
![imagen](https://github.com/user-attachments/assets/d6081dbf-f1c8-455e-9d5b-c884af2ef7f8)

---

# 🛡️ Juego de Tanques en Laberinto

Este es un juego clásico de tanques para 2 jugadores en un laberinto, implementado en Python con Pygame. Cada jugador controla un tanque, puede moverse, girar, disparar balas, y debe evitar los muros y eliminar al oponente.


**🎨 Personalización:**  
- Gráficos estilizados
- HUD con detalles visuales
- Fondos personalizados

**🎮 Controles:**
*Jugador 1 (Tanque Azul):*
- `W` / `S`: Avanzar / Retroceder
- `A` / `D`: Girar
- `Espacio`: Disparar

*Jugador 2 (Tanque Rojo):*
- `↑ ↓ ← →`: Mover y girar
- `Enter`: Disparar
---

## 🧠 Partes más importantes del código

### `class Wall`
Define cada muro en el laberinto con su posición y tamaño. Se dibuja como un bloque gris.

### `class Tank`
Representa a cada tanque:
- Tiene posición, color, rotación, velocidad, salud y balas.
- Métodos:
  - `move(walls)`: Se mueve en la dirección según teclas y evita muros.
  - `shoot()`: Lanza una bala en la dirección del cañón.
  - `update_bullets(walls, other_tank)`: Actualiza posición de balas y detecta colisiones con muros y el otro tanque.
  - `draw()`: Dibuja el tanque rotado, cañón, salud y balas.

### `MAP_LAYOUT`
Matriz de texto que define la posición de muros (`1`) y caminos libres (`0`). Cada línea es una fila del laberinto.

### `Bucle principal`
- Escucha eventos de teclado y mouse.
- Llama a los métodos `move`, `shoot`, `update_bullets`, `draw` de cada tanque.
- Dibuja todo: fondo, muros, tanques, balas.
- Detecta si un tanque llega a 0 de salud y muestra el mensaje de victoria.

---

## 🕹️ Descripción del funcionamiento

1. **Inicio del juego**: Se genera el mapa y los tanques aparecen en esquinas opuestas.
2. **Movimiento**: Cada tanque puede avanzar, retroceder y girar.
3. **Disparo**: Al disparar, se lanza una bala que se detiene con muros o al impactar al oponente.
4. **Colisión**: Si una bala impacta al enemigo, se reduce su salud.
5. **Ganador**: El primer tanque en destruir al otro gana. Se muestra en pantalla y se puede reiniciar presionando `R`.

---
# Imagen
![imagen](https://github.com/user-attachments/assets/3ca2b9c2-39ac-4d4a-8721-0e93bfe33dab)

---

# 🧩 Tetris – Versión Gamer Retro

Este es un juego completo de Tetris desarrollado en Python usando Pygame. Incluye velocidad progresiva, rotación de piezas, puntaje, niveles, caída rápida, pausa y reinicio.

**🎨 Personalización:**  
- Gráficos estilizados
- HUD con detalles visuales
- Fondos personalizados

**🎮 Controles:**
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

---
# Imagen
![imagen](https://github.com/user-attachments/assets/9cbad09e-2f00-4569-a0bf-80866b5e925f)

---

# 🐳 Repositorios en DockerHub

- 🛰️ [SpaceMax Defender](https://hub.docker.com/r/julianse27/juego_naves)
- 🛡️ [Tank Clash](https://hub.docker.com/r/julianse27/juego_tanques)
- 🧱 [RetroBlocks](https://hub.docker.com/r/julianse27/juego_tetris)

---

# ✅ Estado del Proyecto

| Elemento        | Estado  |
|------------------|---------|
| Código funcional | ✅       |
| Dockerfile       | ✅       |
| README detallado | ✅       |
| Imágenes subidas | ✅       |
| Probado en Docker| ✅       |

---

🔧 Desarrollado con ❤️  por **Julian**
