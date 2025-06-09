# 🤖 Proyecto: Análisis de Emociones con PEPPER

Este repositorio documenta el desarrollo de un sistema de análisis emocional aplicado al robot humanoide **PEPPER**. El proyecto combina el análisis facial mediante visión artificial y el análisis vocal usando la API integrada `AEmotionRecognition`.

---

## 📌 Objetivo General

Implementar un sistema multimodal de reconocimiento emocional que permita identificar emociones humanas básicas en tiempo real a través de la voz del usuario y un modelo visual entrenado con imágenes externas.

---

## 🧭 Pasos realizados

A continuación, se describen los pasos seguidos para el desarrollo completo del proyecto:

---

### 🔹 Paso 1: Definición del enfoque y modalidades de análisis

- Se establecieron dos vías principales de reconocimiento:
  - **Análisis facial**: usando imágenes obtenidas desde Google y etiquetadas manualmente.
  - **Análisis de voz**: utilizando la API `AEmotionRecognition` de PEPPER.
- Se determinó trabajar con las emociones: **alegría**, **tristeza**, **enojo** y **sorpresa**.

---

### 🔹 Paso 2: Recolección de imágenes para el análisis facial

- Se buscaron imágenes representativas de cada emoción en Google.
- Se seleccionaron 10 imágenes por emoción, totalizando 40.
- Se aseguraron criterios como frontalidad del rostro y expresividad clara.

---

### 🔹 Paso 3: Construcción del dataset en Roboflow

- Se creó un nuevo proyecto en [Roboflow](https://roboflow.com/).
- Se subieron las imágenes y se clasificaron manualmente según su emoción.
- El dataset fue dividido 80/20 en subconjuntos de entrenamiento y validación.
- Se exportó el dataset en formato **YOLOv8** para su posterior uso.

---

### 🔹 Paso 4: Corrección del script de captura de imágenes (opcional)

Aunque PEPPER no fue usado para capturar las imágenes del dataset, se probó un script que permite capturar una foto y mostrarla en su tablet:

```python
# -*- coding: utf-8 -*-
import qi

session = qi.Session()
session.connect("tcp://198.18.0.1:9559")

photo_service = session.service("ALPhotoCapture")
photo_service.setResolution(2)
photo_service.setPictureFormat("jpg")
photo_service.takePictures(1, "/home/nao/recordings/camera/", "imagen_prueba")

tablet_service = session.service("ALTabletService")
tablet_service.showImage("http://198.18.0.1/recordings/camera/imagen_prueba_0.jpg")
