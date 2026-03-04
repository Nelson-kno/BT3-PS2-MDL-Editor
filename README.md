# BT3 PS2 MDL Editor (Python)

> **Aviso:** Este software es una herramienta de investigación independiente. **Dragon Ball Z: Budokai Tenkaichi 3** y todos sus recursos son propiedad de **Bandai Namco**, **Spike** y sus respectivos licenciantes. Este proyecto no busca infringir derechos de autor y se distribuye bajo la licencia **GPLv3** únicamente con fines de preservación y estudio técnico.

Este es un editor experimental desarrollado en Python para el análisis y visualización de archivos del juego. El proyecto permite gestionar modelos 3D, texturas y diversos parámetros internos del motor del juego.

## 🚀 Características
- **Visor de Modelos:** Soporte para archivos `.pmdl` y `.pmdf`.
- **Gestor de Texturas:** Extracción y conversión de archivos `.dbt` basados en el estándar BMP.
- **Edición de Parámetros:** Soporte para archivos de datos (`.dat`), animaciones (`.anm`) y cámaras (`.cma`).
- **Interfaz Gráfica:** Desarrollada con PySide2 y estilizada mediante CSS personalizado.

## 🛠️ Instalación y Uso

Este proyecto ha sido desarrollado y testeado bajo las siguientes especificaciones técnicas:

1. **Requisitos de Python:**
   - Versión utilizada: **Python 3.7.0**

2. **Instalación de dependencias:**
   Se recomienda instalar las versiones exactas para asegurar la compatibilidad del renderizado:
   ```bash
   pip install PySide2==5.15.2.1 PyOpenGL==3.1.7

## 📚 Referencias Técnicas
Este proyecto se basa en la investigación de formatos de archivos de PlayStation 2 y estándares de imagen:
* **Formato BMP:** Documentación técnica de la **Universidad de Valladolid (UVA)** sobre el manejo de bytes y cabeceras. [Ver guía original](https://www.ele.uva.es/~jesman/BigSeti/seti1/PRACTICAS/PE20012002/BMP_prac.txt)
* **Ingeniería Inversa:** Análisis propio de los archivos `.dbt` y `.pmdl` del motor de Spike.