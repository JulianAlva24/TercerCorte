# 🚀 Space Shooter – Juego de Naves Espaciales

Este es un juego clásico de naves espaciales desarrollado en Python usando Pygame. El jugador controla una nave, dispara a enemigos que bajan por la pantalla, y debe evitar ser destruido. El juego utiliza imágenes y sonidos externos almacenados en la carpeta `assets/`.

---

## 📁 Estructura del proyecto

```
juego_naves/
├── assets/
│   ├── images/
│   └── sounds/
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

## ⚙️ Instalación y ejecución local

```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# .\venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py
```

---

## 🎮 Controles

- **Flechas**: Mover la nave
- **Espacio**: Disparar
- **ESC**: Salir

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

## 🐳 Docker (opcional)

```bash
docker build -t juego_naves .
xhost +local:root
docker run -it --rm \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    juego_naves
```
