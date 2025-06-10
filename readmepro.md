# 🤖 Pepper + DeepSeek Chatbot (Bart Simpson)

Este proyecto conecta al robot **Pepper** con un **chatbot inteligente basado en DeepSeek** que simula la personalidad rebelde de **Bart Simpson**. El robot reconoce comandos por voz, los envía a un servidor en Python (Flask), y responde oralmente con respuestas creativas al estilo del personaje.

---

## 🎯 Funcionalidades

- 🤖 Reconocimiento de voz en español con Pepper.
- 🧠 Chatbot DeepSeek (modelo `deepseek-chat`) con personalidad de Bart Simpson.
- 🗣️ Respuesta hablada usando `ALAnimatedSpeech`.
- 🚫 Limpieza automática de texto (sin emojis, comandos TTS compatibles).
- 🐳 Servidor Python ejecutado en un contenedor Docker.

---

## 🧱 Arquitectura

```
[Pepper Robot] --(voz reconocida)--> cliente_pepper.py
     |
     └---> [Servidor Flask en PC] ---> DeepSeek API
                      |
                      └---> Respuesta de Bart (estilo travieso)
                                   |
                      <--- cliente recibe y reproduce con TTS
```

---

## ⚙️ Requisitos

### En el PC (Servidor Flask)

- Python 3.8+
- Docker y Docker Compose (opcional)
- Cuenta en [DeepSeek](https://deepseek.com/) con API Key

### En el Robot Pepper

- SDK de Aldebaran/Naoqi
- Python 2.7 (por compatibilidad con NAOqi)
- Conectividad por IP en la misma red que el PC

---

## 🛠️ Instalación y ejecución

### 1. Clonar este repositorio

```bash
git clone https://github.com/JulianAlva/TercerCorte.git
cd TercerCorte/Tarea_9
```

---

### 2. Configurar servidor Flask

#### `server.py`

El servidor escucha en el puerto 9559 y usa tu API Key de DeepSeek:

```bash
export DEEPSEEK_API_KEY="tu_clave_aqui"
```

#### Crear entorno con Docker

Archivo `Dockerfile`:

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY server.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 9559
CMD ["python", "server.py"]
```

Archivo `requirements.txt`:

```
flask
requests
```

#### Construcción y ejecución

```bash
docker build -t bart_server .
docker run -d -p 9559:9559 \
  -e DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY \
  --name chatbot_bart_container \
  bart_server
```

---

### 3. Ejecutar cliente en Pepper

Cargar y ejecutar el script `cliente_pepper.py` en Pepper (usando SSH o USB):

```bash
python cliente_pepper.py
```

El robot escuchará comandos como:

- `hola`
- `cuéntame un chiste`
- `qué puedes hacer`
- `cómo te llamas`
- `adiós`

---

## 🔐 Seguridad

Este proyecto usa variables de entorno para proteger la clave de API de DeepSeek. Nunca incluyas tu clave directamente en el código.

---

## 🧪 Ejemplo de interacción

```text
[AUDIO] Detectado: cuéntame un chiste
[DEBUG] Enviando payload: {"question": "cuéntame un chiste"}
[TTS] Respondiendo: Bart: ¡Ay caramba! ¿Por qué Lisa nunca juega conmigo? Porque siempre quiere estudiar. ¡Aburrido!
```

---

## 👨‍💻 Autor

- 🧠 Proyecto para curso de **Sistemas Digitales III**
- 📍 Universidad — Semestre 6 — Ingeniería Electrónica
