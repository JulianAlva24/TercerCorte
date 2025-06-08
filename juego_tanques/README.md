# 🛡️ Juego de Tanques en Laberinto

Este es un juego clásico de tanques para 2 jugadores en un laberinto, implementado en Python con Pygame. Cada jugador controla un tanque, puede moverse, girar, disparar balas, y debe evitar los muros y eliminar al oponente.

---

## 📁 Estructura del proyecto

```
juego_tanques_real/
├── assets/
│   ├── images/     # Aquí puedes agregar sprites de los tanques, balas, fondo, muros
│   └── sounds/     # Aquí puedes agregar sonidos como disparo o explosión
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

**Jugador 1 (Tanque Azul):**
- `W` / `S`: Avanzar / Retroceder
- `A` / `D`: Girar
- `Espacio`: Disparar

**Jugador 2 (Tanque Rojo):**
- `↑ ↓ ← →`: Mover y girar
- `Enter`: Disparar

**Otros:**
- `R`: Reiniciar juego después de perder
- `ESC`: Cerrar ventana

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
